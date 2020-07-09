import os 
import pandas as pd 
import csv
 
tabb = dict()
tabb['strand'] = []
tabb['binding_position'] = []
tabb['binding_posterior'] = []
tabb['pwm_id'] = []
tabb['binding_region'] = []
tabb['binding_sequence'] = []
tabb['binding_energy'] = []
tabb['fast_record'] =[] 

print(snakemake.input)
files2 = snakemake.input
ii = -1
for file in files2:  
    print(file)
    ii = ii +1 

    filename = os.path.relpath(files2[ii])

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
df.to_csv('combine_MotEvo_results.csv', index=False)



with open('combine_MotEvo_results.csv','r') as csvin, open('combine_MotEvo_results.tsv', 'w') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter='\t')

    for row in csvin:
        tsvout.writerow(row)