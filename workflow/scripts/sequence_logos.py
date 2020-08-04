###############################################################################
#
#   Script to plot sequence logos for motifs
#
#   AUTHOR: Krish Agarwal
#   AFFILIATION: University_of_Basel
#   CONTACT: akrish136@gmail.com
#   CREATED: 02-08-2020
#   LICENSE: Apache_2.0
#
###############################################################################

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import logomaker
from argparse import ArgumentParser, RawTextHelpFormatter

##### Using argparse to get input from command line #####
parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)

parser.add_argument(
    "--input_files",
    nargs="+",
    dest="input_files",
    help="input files for sequence logos",
    required=True,
    metavar="FILE",
)

parser.add_argument(
    "--output_location",
    dest="output_location",
    help="location where the png logos will be saved",
    required=True,
    metavar="DIR",
)

try:
    options = parser.parse_args()
except Exception:
    parser.print_help()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

#### Storing commnad line arguments in variables ####
input_files = options.input_files
output_location = options.output_location

input_files = sorted(input_files)

for input_file in input_files:

    main_file = str(input_file)
    main_file_temp = (
        main_file + "_temp"
    )  # create a temporary file which will store only the required data

    filename = os.path.split(main_file)[-1]  # filename of the input file

    #### Calculate total number of lines in the file ####
    j = 0
    with open(main_file) as f:
        for line in f:
            j = j + 1

    #### Copy the contents of the file to temp except 1st, 2nd and last line ####
    i = 0
    with open(main_file) as f:
        with open(main_file_temp, "w") as f1:
            for line in f:
                if i != 0 and i != 1 and i != j - 1:
                    f1.write(line)
                i = i + 1

    crp_matrix_df = pd.read_csv(
        main_file_temp, delim_whitespace=True, index_col=0
    )  # read csv and convert to dataframe
    crp_matrix_df.head()

    os.remove(main_file_temp)  # delete the temporary file

    prob_mat = logomaker.transform_matrix(
        crp_matrix_df, from_type="probability", to_type="weight"
    )
    logo = logomaker.Logo(
        prob_mat,
        ## fade_probabilities=True, ## will fade the smaller probabilities
        stack_order="small_on_top",
    )

    final_png = os.path.join(output_location, filename)  # location for saving the file

    axes = plt.gca() # get current axes of the plots
    axes.set_ylim([0, 2]) # set the y-axis limits from 0 to 2

    #### Hide the top and the right axes of the plot ####
    axes.spines['right'].set_color('none') 
    axes.spines['top'].set_color('none')

    plt.savefig(final_png)  # final png saved
