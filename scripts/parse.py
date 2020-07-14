import os 
import sys
import pandas as pd 
import csv
from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)

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

print(len(sys.argv))    

tabb = dict()
tabb['strand'] = []
tabb['binding_position'] = []
tabb['binding_posterior'] = []
tabb['pwm_id'] = []
tabb['binding_region'] = []
tabb['binding_sequence'] = []
tabb['binding_energy'] = []
tabb['fast_record'] =[] 

# print(snakemake.input)
# print(snakemake.params)

filenameparam = str(options.filename)

dirrs = options.indir
print(dirrs)
outdir = str(options.outfile)
print(outdir)

rel_outfile = os.path.relpath(outdir)
print(rel_outfile)
rel_outfile_csv = os.path.join(os.path.dirname(rel_outfile), "combined_MotEvo_results.csv")

ii = -1
for dirr in dirrs:
    print(dirr)  
    abs_path = os.path.join(dirr, filenameparam) 
    print(abs_path)

    filename = os.path.relpath(abs_path)
    print(filename)

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
            tabb['fast_record'] = tabb['fast_record'] + [each_word[2]]
        i = i+1

    #print(tabb)
df = pd.DataFrame({ key:pd.Series(value) for key, value in tabb.items() })
df.to_csv(rel_outfile_csv, index=False)



with open(rel_outfile_csv,'r') as csvin, open(rel_outfile, 'w') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter='\t')

    for row in csvin:
        tsvout.writerow(row)