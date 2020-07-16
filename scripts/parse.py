##############################################################################
#   AUTHOR: Krish Agarwal
#   AFFILIATION: University_of_Basel
#   CONTACT: akrish136@gmail.com
#   CREATED: 14-07-2020
#   LICENSE: Apache_2.0
##############################################################################

import os
import sys
import pandas as pd
import csv
from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawTextHelpFormatter)

parser.add_argument(
    "--indir",
    nargs='+',
    dest="indir",
    help="input directory for the script to search",
    required=True,
    metavar="DIR",
)

parser.add_argument(
    "--filename",
    dest="filename",
    help="filename to be searched in indir",
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


tabb = dict()
tabb['strand'] = []
tabb['binding_position'] = []
tabb['binding_posterior'] = []
tabb['pwm_id'] = []
tabb['binding_region'] = []
tabb['binding_sequence'] = []
tabb['binding_energy'] = []
tabb['fasta_record'] = []


filenameparam = str(options.filename)

dirrs = options.indir
dirrs = sorted(dirrs) # sorting so that we dont have any random order
outdir = str(options.outfile)

rel_outfile = os.path.relpath(outdir)
rel_outfile_csv = os.path.join(
    os.path.dirname(rel_outfile),
    "combined_MotEvo_results.csv")

for dirr in dirrs:
    abs_path = os.path.join(dirr, filenameparam)

    filename = os.path.relpath(abs_path)

    i = 0 # this variable will check whether we are at the first line of the record or second
    file = open(filename, "r")
    for each in file:
        each_word = each.split(' ')
        if(i % 2 == 0): # first line 
            tabb['binding_position'] = tabb['binding_position'] + [each_word[0]] 
            tabb['strand'] = tabb['strand'] + [each_word[1]]
            tabb['binding_posterior'] = tabb['binding_posterior'] + [each_word[2]]
            tabb['pwm_id'] = tabb['pwm_id'] + [each_word[3]]
            tabb['binding_region'] = tabb['binding_region'] + [each_word[4]]
        else: # second line 
            tabb['binding_sequence'] = tabb['binding_sequence'] + [each_word[0]]
            tabb['binding_energy'] = tabb['binding_energy'] + [each_word[1]]
            tabb['fasta_record'] = tabb['fasta_record'] + [each_word[2]]
        i = i + 1

list_items = ['pwm_id', 'binding_position', 'binding_sequence', 'binding_posterior', 'binding_energy'] # these will be the headers in the final tsv file

tempDict1 = {} # initializing empty dictionaries
for item in list_items:
    tempDict = {item : pd.Series(tabb[item])} # appending list of values for each key 
    tempDict1.update(tempDict) # concating dictionary
df = pd.DataFrame(tempDict1)
df.to_csv(rel_outfile, index=False, sep='\t', header=list_items) # creating a tsv file




