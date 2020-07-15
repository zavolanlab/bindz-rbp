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
outdir = str(options.outfile)

rel_outfile = os.path.relpath(outdir)
rel_outfile_csv = os.path.join(
    os.path.dirname(rel_outfile),
    "combined_MotEvo_results.csv")

ii = -1
for dirr in dirrs:
    abs_path = os.path.join(dirr, filenameparam)

    filename = os.path.relpath(abs_path)

    i = 0
    j = 0
    file = open(filename, "r")
    for each in file:
        each_word = each.split(' ')
        if(i % 2 == 0):
            tabb['binding_position'] = tabb['binding_position'] + [each_word[0]]
            tabb['strand'] = tabb['strand'] + [each_word[1]]
            tabb['binding_posterior'] = tabb['binding_posterior'] + [each_word[2]]
            tabb['pwm_id'] = tabb['pwm_id'] + [each_word[3]]
            tabb['binding_region'] = tabb['binding_region'] + [each_word[4]]
        else:
            tabb['binding_sequence'] = tabb['binding_sequence'] + [each_word[0]]
            tabb['binding_energy'] = tabb['binding_energy'] + [each_word[1]]
            tabb['fasta_record'] = tabb['fasta_record'] + [each_word[2]]
        i = i + 1

df = pd.DataFrame({key: pd.Series(value) for key, value in tabb.items()})
df.to_csv(rel_outfile_csv, index=False)


with open(rel_outfile_csv, 'r') as csvin, open(rel_outfile, 'w') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter='\t')

    for row in csvin:
        tsvout.writerow(row) #printing row by row in tsv




