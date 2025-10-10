#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:17:40 2025

@author: inf-33-2025
"""


# Import libraries
import sys


# Save command line inputs to variables
try:
    script_name, fasta_file, blast_file, output_path = sys.argv[0:5]

# Exit the program and throw an error if more or fewer than 4 arguments are
# passed to the script.
except ValueError:
    sys.exit('\nError: please enter a fasta file, blast file, and output path '
             'after the script name\n')


# Create the empty lists IDs_fasta, headers_fasta, and seqs_fasta to store data
# from the file fasta_file passed to the program.
IDs_fasta = []
headers_fasta = []
seqs_fasta = []

# Open the fasta file using with to ensure that it is closed after completion.
with open(fasta_file, 'r') as fasta:
    
    # Read the lines of the fasta file into the list lines_fasta. Fasta file
    # headers are read as strings where data entries are separated by '\t'.
    lines_fasta = fasta.readlines()
    
    # Loop through the strings in the list lines_fasta, appending them to the
    # appropriate list.
    for l in lines_fasta:
        
        # Headers start with the charater '>'. Append the header to the list
        # headers_fasta, replacing the final '\n' with '\t', since more data
        # will be added to the header in the output.
        if l.startswith('>'):
            headers_fasta.append(l.replace('\n', '\t'))
            
            # Split the characters in string l into a list, appending the
            # characters of the first item follwing the leading '>' to the list
            # IDs_fasta.
            IDs_fasta.append(l.split()[0][1:])
            
        # If the string l does not start with '>' it is a sequence. Append the
        # string to the list seqs_fasta.
        else:
            seqs_fasta.append(l)


# Create the empty list data_blast. This list will store all the data from 
# blast_file in a list, where every line is a list nested within data_blast.
data_blast = []

# Open the blast file using with to ensure that it is closed after completion.
with open(blast_file, 'r') as blast:
    
    # Read the lines of the blast file into the list lines_blast. Each line of
    # the blast file is read as a string where data entries are separated by
    # '\t', making each line of the file blast_file one item in the list lines.
    lines_blast = blast.readlines()
    
    # Loop through the strings in the list lines_blast, making each string into
    # a list, splitting them by the delimiter '\t'.
    for i, l in enumerate(lines_blast):
        
        # The first line of the file blast_file is the header. Assign this line
        # to its own list blast_header.
        if i == 0:
            blast_header = l.split('\t')
        
        # For all other strings of data in lines, split them into lists and
        # append them to data_blast.
        else:
            data_blast.append(l.split('\t'))

# Save the indecies of the columns used for generation of the output file.
ID_blast_col = blast_header.index('#queryName')
desc_blast_col = blast_header.index('hitDescription')


# Create an empty dictionary to store protein IDs and their corresponding
# descriptions based on the contents of blast_file
custom_strings_dict = {}

# Loop through the nested lists inside the list data_blast.
for i, row in enumerate(data_blast):
    
    # Assign the protein ID and its description to variables ID_blast and
    # desc_blast and add them to the dictionary custom_strings_dict.
    # if 'null' not in data_blast[i][desc_blast_col]:
    ID_blast = data_blast[i][ID_blast_col]
    desc_blast = data_blast[i][desc_blast_col]
    custom_strings_dict[ID_blast] = (f'protein={desc_blast}\n')
        



#IDs_blast = list(blast['#queryName'])

# print(len(IDs_fasta), type(IDs_fasta))
# print(len(headers_fasta), type(headers_fasta))
# print(len(seqs_fasta), type(seqs_fasta))
# print(len(IDs_blast), type(IDs_blast))

# print(len(custom_strings_dict), type(custom_strings_dict))

#IDs_fasta_set = set(IDs_fasta)
#IDs_blast_set = set(IDs_blast)

# data length mismatch:
# len(ID_fasta_set) != len(ID_blast_set)

# protein ID mismatch (only possible if there is no data length mismatch
# len(IDs_fasta_set & IDs_blast_set) != len(ID_fasta_set)








# Create the blank list null_IDs_blast to store the protein IDs from blast_file
# whose entry in 'hitDescription' is null.
null_IDs_blast = []

# Loop through the keys of the dictionary custom_strings_dict.keys
for k in custom_strings_dict.keys():
    if 'null' in custom_strings_dict[k]:
        null_IDs_blast.append(k)




if (len(IDs_fasta) == len(headers_fasta) == len(seqs_fasta)
    == len(custom_strings_dict)) != 1:
    print('data length error')

IDs_fasta_set = set(IDs_fasta)
    


with open(output_path, 'w') as output:
    for i, header_fasta in enumerate(headers_fasta):
        if IDs_fasta[i] not in null_IDs_blast:
            output.write(header_fasta
                         + custom_strings_dict[IDs_fasta[i]])
            output.write(seqs_fasta[i])