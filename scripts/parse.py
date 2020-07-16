##############################################################################
#   AUTHOR: Krish Agarwal
#   AFFILIATION: University_of_Basel
#   CONTACT: akrish136@gmail.com
#   CREATED: 14-07-2020
#   LICENSE: Apache_2.0
##############################################################################

##### Importing necessary libraries #####
import os
import sys
import pandas as pd
import csv
from argparse import ArgumentParser, RawTextHelpFormatter

##### Using argparse to get input from command line #####
parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawTextHelpFormatter)

parser.add_argument(
    "--input_directories",
    nargs='+',
    dest="input_directories",
    help="input directory for the script to search",
    required=True,
    metavar="DIR",
)

parser.add_argument(
    "--filename",
    dest="filename",
    help="filename to be searched in input_directories",
    required=True,
    metavar="NAME",
)

parser.add_argument(
    "--outfile",
    dest="outfile",
    help="location and name of the tsv file",
    required=True,
    metavar="FILE",
)

try:
    options = parser.parse_args()
except Exception:
    parser.print_help()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

##### Initializing dictionaries and list #####
tabb = dict()
tabb['strand'] = []
tabb['binding_position'] = []
tabb['binding_posterior'] = []
tabb['pwm_id'] = []
tabb['binding_region'] = []
tabb['binding_sequence'] = []
tabb['binding_energy'] = []
tabb['fasta_record'] = []

##### Taking input from commandline #####
filenameparam = str(options.filename)
dirrs = options.input_directories
outdir = str(options.outfile)

##### Sorting the input directories so as to prevent different orders for same input #####
dirrs = sorted(dirrs)
 
rel_outfile = os.path.relpath(outdir)

##### Processing each directory one by one using a for loop #####
for dirr in dirrs: 
    abs_path = os.path.join(dirr, filenameparam) # absolute path of the input file

    filename = os.path.relpath(abs_path) # relative path of input file

    i = 0 # this variable will be used to check whether we are at the first line of the record or second

    file = open(filename, "r") # open the file in read mode

    for each in file: # processing the file line by line 

        each_word = each.split(' ') # splitting the line into individual words

        if(i % 2 == 0): # if i is even then we are at the first line 

            ##### Appending values #####
            tabb['binding_position'] = tabb['binding_position'] + [each_word[0]]  
            tabb['strand'] = tabb['strand'] + [each_word[1]]
            tabb['binding_posterior'] = tabb['binding_posterior'] + [each_word[2]]
            tabb['pwm_id'] = tabb['pwm_id'] + [each_word[3]]
            tabb['binding_region'] = tabb['binding_region'] + [each_word[4]]

        else: # if i is odd then we are at the second line 

            ##### Appending values #####
            tabb['binding_sequence'] = tabb['binding_sequence'] + [each_word[0]]
            tabb['binding_energy'] = tabb['binding_energy'] + [each_word[1]]
            tabb['fasta_record'] = tabb['fasta_record'] + [each_word[2]]

        i = i + 1 # increment the value of i after we are done processing each line 

list_items = ['pwm_id', 'binding_position', 'binding_sequence', 'binding_posterior', 'binding_energy'] # these will be the headers in the final tsv file

tempDict1 = {} # initializing empty dictionary that will contain data only of the headers mentioned in list_items

for item in list_items: 

    tempDict = {item : pd.Series(tabb[item])} # appending list of values for each key 
    tempDict1.update(tempDict) # concating dictionary

df = pd.DataFrame(tempDict1) # convert dictionary to dataframe

df.to_csv(rel_outfile, index=False, sep='\t', header=list_items) # creating a tsv file




