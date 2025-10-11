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

# -----------------------------------------------------------------------------
# 1. Import libraries.
# -----------------------------------------------------------------------------
import sys
import os


# -----------------------------------------------------------------------------
# 2. Save command line inputs to variables and check for initial errors.
# -----------------------------------------------------------------------------

# Assign user inputs to variables.
try:
    fasta_file, blast_file, output_path = sys.argv[1:5]

# Exit the program and throw an error if more or fewer than 4 arguments are
# passed to the script.
except ValueError:
    sys.exit('\nError: too few or too many arguments passed. Please pass a '
             'FASTA file, a tab-\ndelimited BLAST data file, and output path '
             'after the script name.\n')

# Check that fasta_file is a FASTA file. '.txt' files are not accepted.
fasta_exts = ('.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn')
if not fasta_file.endswith(fasta_exts):
    sys.exit('\nError: a non-FASTA file has been passed to the program.\n')
        

# Check that output_path is a text file.
if not output_path.endswith(('.txt')):
    sys.exit('\nError: output file must be of type .txt\n')

# Check that the FASTA and BLAST data files exist. Create empty list
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
# work. If the file is tab delimited, the header will be used later.
with open(blast_file, 'r') as blast:
    blast_header = blast.readline()

if '\t' not in blast_header:
    sys.exit('\nError: BLAST data file is not tab delimited.\n')

else:
    blast_colnames = blast_header.split('\t')
    
# Save the indecies of the columns used for generation of the output file.
# Check that they are represented in the BLAST data file before running the
# program logic. If they are represented, save their indecies for later
# operations.
ID_colname = '#queryName'
desc_colname = 'hitDescription'

try:
    ID_blast_col = blast_colnames.index(ID_colname)
    desc_blast_col = blast_colnames.index(desc_colname)

except ValueError:
    sys.exit('\nError: BLAST data file does not contain appropriate column '
             'names. The protein\nID column must be named `#queryName` and '
             'the description column must be named\n`hitDescription`.\n')
    

# -----------------------------------------------------------------------------
# 3. Run data operations.
# -----------------------------------------------------------------------------

# 3.1. Read FASTA file

# Create the empty lists IDs_fasta, headers_fasta, and seqs_fasta to store data
# from the file fasta_file passed to the program.
IDs_fasta = []
headers_fasta = []
seqs_fasta = []

# Open the FASTA file using with to ensure that it is closed after completion.
with open(fasta_file, 'r') as fasta:
    
    # Read lines one at a time for memory efficiency. The while loop ensures
    # that each line of the file is read into the variable line.
    while True:
        line = fasta.readline()
        
        # Check that there is a line in the file for the current iteration of
        # the loop.
        if line:
        
            # Headers start with the charater '>'. Append the header to the
            # list headers_fasta, replacing the final '\n' with '\t', since
            # more data will be added to the header in the output.
            if line.startswith('>'):
                headers_fasta.append(line.replace('\n', '\t'))
                
                # Split the characters in string line into a list, appending
                # the characters of the first item follwing the leading '>' to
                # the list IDs_fasta.
                IDs_fasta.append(line.split()[0][1:])
                
            # If the string line does not start with '>' it is a sequence.
            # Append the string to the list seqs_fasta.
            else:
                seqs_fasta.append(line)
                
        # Break the while loop when the end of the FASTA file is reached.
        else:
            break

# Check that the number of headers is equal to the number of sequences. Every
# header in a FASTA file, identified by starting with '>', is associated with a
# one line sequence. Therefore, if the condition below is not met, an error
# will be thrown and the program terminated.
if len(headers_fasta) != len(seqs_fasta):
    sys.exit('\nError: FASTA file corrupted. Unequal number of headers and '
             'sequences found.\n')


# 3.2. Read BLAST data file

# Create the empty list data_blast. This list will store all the data from 
# blast_file in a list, where every line is a list nested within data_blast.
data_blast = []

# Open the BLAST data file using with to ensure that it is closed after
# completion.
with open(blast_file, 'r') as blast:
    
    # Read the lines of the BLAST data file one at a time to save memory. Skip
    # the first line since it was already read in the error handling section of
    # the program.
    next(blast)
    while True:
        row = blast.readline()
        if row:
        
            # Split data into lists delimiting by '\t' and assign the list to 
            # the variable row_split.
            row_split = row.split('\t')
            
            # Check if the current row has a null value in the protein
            # description column using the column index. Append the row to the
            # list data_blast only if it does not.
            if 'null' not in row_split[desc_blast_col]:
                data_blast.append(row_split)
        
        # Break the while loop when there are no more rows to be read.
        else:
            break


# 3.3. Write novel strings that will be added to the output file.

# Create an empty dictionary to store protein IDs and their corresponding
# descriptions based on the contents of blast_file
custom_strings_dict = {}

# Loop through the nested lists inside the list data_blast to access each BLAST
# hit iteratively.
for i, row in enumerate(data_blast):
    
    # Assign the protein ID and its description to variables ID_blast and
    # desc_blast and add them to the dictionary custom_strings_dict.
    ID_blast = data_blast[i][ID_blast_col]
    desc_blast = data_blast[i][desc_blast_col]
    custom_strings_dict[ID_blast] = (f'protein={desc_blast}\n')


# -----------------------------------------------------------------------------
# 4. Construct output file and conclude program.
# -----------------------------------------------------------------------------

# Open output_path provided by the user and write the output.
with open(output_path, 'w') as output:
    
    # Loop through the list of FASTA headers to write the output.
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
print(f'\nOutput written to {output_path}\n')