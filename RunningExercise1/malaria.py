#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The program malaria.py is a command line tool that takes arguments in the
following format:
    
    Script name (malaria.py, unless renamed)
    FASTA file
    Tab-delimited BLAST data file
    File path to a text file where the program's output will be written
    
To run the program, type 'python' or 'python3' in your terminal, followed by
the 4 arguments above, in order.

Written by Oliver Todreas for RunningExerciseI in the course BINP16.
"""


# Import libraries.
import sys
import os

# Save command line inputs to variables.
try:
    script_name, fasta_file, blast_file, output_path = sys.argv[0:5]

# Exit the program and throw an error if more or fewer than 4 arguments are
# passed to the script.
except ValueError:
    sys.exit('\nError: too few or too many arguments passed.\n'
             'Please pass a FASTA file, a tab-delimited BLAST file, and '
             'output path after the script name.\n')

# Check that fasta_file is a FASTA file. '.txt' files are not accepted.
fasta_exts = ('.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn')
if not fasta_file.endswith(fasta_exts):
    sys.exit('\nError: a non-FASTA file has been passed to the program.\n')
        

# Check that output_path is a text file.
if not output_path.endswith(('.txt')):
    sys.exit('\nError: output file must be of type .txt\n')

# Check that the FASTA and BLAST files exist. Create empty list
# non_existent_files to store non existent filepaths in.
non_existent_files = []

# Loop through file paths passed to the program, checking if they exist and
# appending them to non_existent_files if they do not.
for file in [fasta_file, blast_file]:
    if not os.path.exists(file):
        non_existent_files.append(file)

# Print the non existent file paths if there are any and interrupt the program,
# controlling for grammar.
if len(non_existent_files) > 0:
    if len(non_existent_files) == 1:
        print('\nError: the following file does not exist:')
    else:
        print('\nError: the following files do not exist:')
        
    for i, file in enumerate(non_existent_files):
        if i < len(non_existent_files) - 1:
            print(file)
        else:
            sys.exit(file + '\n')

# Ensure that the BLAST data file is tab delimited. Read only the first line to
# save compute, since every line needs to be tab delimited for the program to
# work.
with open(blast_file, 'r') as blast:
    header = blast.readline()

if '\t' not in header:
    sys.exit('\nError: BLAST data file is not tab delimited.\n')
    


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

if len(headers_fasta) != len(seqs_fasta):
    sys.exit('\nError: FASTA file corrupted. Unequal number of headers and '
             'sequences found.\n')

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
ID_colname = '#queryName'
desc_colname = 'hitDescription'

ID_blast_col = blast_header.index(ID_colname)
desc_blast_col = blast_header.index(desc_colname)


# Create an empty dictionary to store protein IDs and their corresponding
# descriptions based on the contents of blast_file
custom_strings_dict = {}

# Loop through the nested lists inside the list data_blast.
for i, row in enumerate(data_blast):
    
    # Assign the protein ID and its description to variables ID_blast and
    # desc_blast and add them to the dictionary custom_strings_dict only if
    # desc_blast does not contain 'null'.
    ID_blast = data_blast[i][ID_blast_col]
    desc_blast = data_blast[i][desc_blast_col]
    if 'null' not in desc_blast:
        custom_strings_dict[ID_blast] = (f'protein={desc_blast}\n')

        
# Open output_path provided by the user and write the output.
with open(output_path, 'w') as output:
    
    # Loop through the list of fasta headers to write the output.
    for i, header_fasta in enumerate(headers_fasta):
        
        # Check if the current ID is in the list of keys in the dictionary
        # custom_strings_dict. If it is not, that protein IDs function was
        # listed as 'null' and will not be included in the output file.
        if IDs_fasta[i] in custom_strings_dict.keys():
            
            # Construct the output file.
            output.write(header_fasta
                         + custom_strings_dict[IDs_fasta[i]]
                         + seqs_fasta[i])

# Print completion message.
print(f'Output written to {output_path}')