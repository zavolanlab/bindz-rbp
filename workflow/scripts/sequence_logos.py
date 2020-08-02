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


try:
    options = parser.parse_args()
except Exception:
    parser.print_help()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)


input_files = options.input_files

sorted(input_files)

for input_file in input_files:

    main_file = str(input_file)
    main_file_temp = main_file + "_temp"

    j = 0
    with open(main_file) as f:
	    for line in f:
		    j = j+1

    i = 0	
    with open(main_file) as f:
        with open(main_file_temp, "w") as f1:
       	    for line in f:
                if(i != 0 and i != 1 and i != j-1):
                	f1.write(line)
                i = i+1

    crp_matrix_df = pd.read_csv(main_file_temp, delim_whitespace=True, index_col=0)
    crp_matrix_df.head()

    os.remove(main_file_temp)
    
    prob_mat = logomaker.transform_matrix(crp_matrix_df, from_type='counts', to_type='probability')
    logo = logomaker.Logo(prob_mat, 
               	## fade_probabilities=True, ## will fade the smaller probabilities
               	stack_order='small_on_top')

    final_png = main_file + ".png"
    plt.savefig(final_png)
