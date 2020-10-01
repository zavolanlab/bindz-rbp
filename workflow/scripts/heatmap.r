###############################################################################
#
#   R script to generate a heatmap
#
#   AUTHOR: Krish Agarwal
#   AFFILIATION: University_of_Basel
#   CONTACT: akrish136@gmail.com
#   CREATED: 23-07-2020
#   LICENSE: Apache_2.0
#
###############################################################################

# by default: suppress warnings
options(warn = -1)

# load libraries
library("optparse")
library(ggplot2)
library(ggtext)


# list the command-line arguments
option_list <- list(
  make_option(c("--input_tsv"),
    action = "store",
    dest = "input_tsv",
    type = "character",
    help = "location and name of the tsv file"
  ),
  make_option(c("--input_sequence"),
    action = "store",
    dest = "input_sequence",
    type = "character",
    help = "full input_sequence"
  ),
  make_option(c("--outfile"),
    action = "store",
    dest = "output_tsv",
    type = "character",
    help = "location and name of output heatmap"
  ),
  make_option(c("--sequence_logos_directory"),
    action = "store",
    dest = "sequence_logos_directory",
    type = "character",
    default=FALSE,
    help = "location of directory of sequence logos"
  )
)
# parse command-line arguments
opt_parser <- OptionParser(
  usage = "Usage: %prog [OPTIONS] --message [STRING]",
  option_list = option_list,
  add_help_option = FALSE,
  description = ""
)
opt <- parse_args(opt_parser)

# Storing command line arguments in variables
input_sequence <- opt$input_sequence 
input_tsv <- opt$input_tsv
output_tsv <- opt$output_tsv
sequence_logos_directory <- opt$sequence_logos_directory

input_sequence <- gsub("T", "U", input_sequence) # Replace all T with U in input sequence

# This will be the hidden column names for the graph
x_axis_numbers = 1:nchar(input_sequence)

file = file(input_tsv, "r")

y_axis_labels = c()

while (length(line <- readLines(file, n = 1)) > 0) # Read the file line by line
{
    words = strsplit(line, '\t')
    pwm_id = words[[1]][1]
    if(is.element(pwm_id, y_axis_labels) == FALSE && pwm_id != "pwm_id")
    {
      y_axis_labels <- c(y_axis_labels, pwm_id)
    } 
}
uniform_data = matrix(as.double("0.00"), length(y_axis_labels), length(x_axis_numbers))

close(file)

file = file(input_tsv, "r")

while (length(line <- readLines(file, n = 1)) > 0) 
{
    words = strsplit(line, '\t')
    pwm_id = words[[1]][1]
    bind_pos = words[[1]][2]
    bind_prob = words[[1]][4]
    if(bind_pos != 'binding_position')
    {
      bind_combined = strsplit(bind_pos, '-') # splitting to get the starting and the last position of binding
      bind_start = bind_combined[[1]][1]
      bind_end = bind_combined[[1]][2]

      for(i in as.integer(bind_start):as.integer(bind_end))
      {
        gg = grep(pwm_id, y_axis_labels)
        uniform_data[gg, i] <- as.double(bind_prob) ## adding the probability to each position
      }
    }
}
uniform_data[uniform_data == 0] <- NA

colnames(uniform_data) <- x_axis_numbers
rownames(uniform_data) <- y_axis_labels

# Converting matrix to data frame
dff <-data.frame(col = rep(colnames(uniform_data), each = nrow(uniform_data)), 
           row = rep(rownames(uniform_data), ncol(uniform_data)), 
           Binding_Probability = as.vector(uniform_data))

input_seq = strsplit(input_sequence,"") 

labels = c()

#### Add the sequence logo pngs to the dictionary ####
if(sequence_logos_directory != FALSE)
{
	for (label in y_axis_labels) 
	{
		labels[label] = paste("<b>", label, "<b><img src='", sequence_logos_directory, "/motif_", label, ".png'
    	width='100' height='18'>", sep = "")
	}	
}


if(sequence_logos_directory != FALSE)
{
	a <- ggplot(dff, aes(x = reorder(col, sort(as.numeric(col))), y = row, fill= Binding_Probability)) + 
  geom_tile(color = "gray") + 
  scale_x_discrete(breaks=1:nchar(input_sequence),labels=input_seq) + 
  scale_y_discrete(name = NULL, labels=labels) + 
  scale_fill_gradientn(colours=c("white","orange","red","dark red"), limits=c(0,1), na.value="white") + # Sets default NA colour and scale
  labs(x ="Sequence", y = "") + # Name of the x and y axis
  theme_classic()+
  theme(
    axis.text.y = element_markdown(color = "black", size = 11)
  )+
  coord_fixed(3)
  #coord_equal() #make the grid squares and independent of number of motifs analyzed
} else
{
    a <- ggplot(dff, aes(x = reorder(col, sort(as.numeric(col))), y = row, fill= Binding_Probability)) + 
  geom_tile(color = "gray") + 
  scale_x_discrete(breaks=1:nchar(input_sequence),labels=input_seq) + 
  scale_fill_gradientn(colours=c("white","orange","red","dark red"), limits=c(0,1), na.value="white") + # Sets default NA colour and scale
  labs(x ="Sequence", y = "") + # Name of the x and y axis
  theme_classic()+
  coord_fixed(3)
  #coord_equal() #make the grid squares and independent of number of motifs analyzed
}

ggsave(output_tsv, width=ceiling(nchar(input_sequence)/4)+10, height = ceiling(length(y_axis_labels))+10, limitsize = FALSE)
