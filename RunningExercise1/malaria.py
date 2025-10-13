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
# 2. Save command line inputs to variables and handle initial errors.
# -----------------------------------------------------------------------------

# Assign user inputs to variables.
try:
    fasta_file, blast_file, output_path = sys.argv[1:5]

# Handle argument number error.
except ValueError:
    sys.exit('Error: too few or too many arguments passed. Please pass a '
             'FASTA file, a tab-\ndelimited BLAST data file, and output path '
             'after the script name.')

# Check that fasta_file is a FASTA file. '.txt' files are not accepted.
fasta_exts = ('.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn')
if not fasta_file.endswith(fasta_exts):
    sys.exit('Error: a non-FASTA file has been passed to the program.')
        
# Check that output_path is a text file.
if not output_path.endswith(('.txt')):
    sys.exit('Error: output file must be of type .txt')

# Check that the FASTA and BLAST data files exist.
non_existent_files = []
for file in [fasta_file, blast_file]:
    if not os.path.exists(file):
        non_existent_files.append(file)
        
if len(non_existent_files) > 0:
    if len(non_existent_files) == 1:
        print('Error: the following file does not exist:')
        
    else:
        print('Error: the following files do not exist:')
        
    for i, file in enumerate(non_existent_files):
        if i < len(non_existent_files) - 1:
            print(file)
            
        else:
            sys.exit(file)

# Ensure that the BLAST data file is tab delimited.
with open(blast_file, 'r') as blast:
    blast_header = blast.readline()

if '\t' not in blast_header:
    sys.exit('Error: BLAST data file is not tab delimited.')

else:
    blast_colnames = blast_header.split('\t')
    
# Check that the column names match expectations.
id_colname = '#queryName'
desc_colname = 'hitDescription'

try:
    id_blast_col = blast_colnames.index(id_colname)
    desc_blast_col = blast_colnames.index(desc_colname)

except ValueError:
    sys.exit('Error: BLAST data file does not contain appropriate column '
             'names. The protein\nID column must be named `#queryName` and '
             'the description column must be named\n`hitDescription`.')
    

# -----------------------------------------------------------------------------
# 3. Updated program.
# -----------------------------------------------------------------------------

with (open(fasta_file, 'r') as fasta,
      open(blast_file, 'r') as blast,
      open(output_path, 'w') as output):
    
    line_index = 0
    
    blast_dict = {}
    fasta_dict = {}
    
    seq = ''
    
    # skip blast header
    next(blast)
    
    while True:
        
        # if line index is even, read fasta header
        if line_index % 2 == 0:
        
            # read blast row
            row = blast.readline().split('\t')
            
            # check if description is null
            if row[desc_blast_col] != 'null': # might need to use 'null' not in ...
    
                null_entry = False
    
                id_blast = row[id_blast_col]            
                desc_string = row[desc_blast_col] + '\n'
                
                blast_dict[id_blast] = desc_string
            
        
                header = fasta.readline().replace('\n', '\t').split()[0][1:]
                
            else:
                null_entry = True
                
        elif not null_entry:
            
            seq = fasta.readline()
            fasta_dict[header] = seq
            
            common_ids = set(blast_dict.keys) & set(fasta_dict.keys())
            
            for i in common_ids:
                
                added_seq = fasta_dict.pop(i)
                added_string = blast_dict.pop(i)
                
                output.write(i + added_string + added_seq)
                
        else:
            
            next(fasta)
                    
                
        # update counter
        line_index = line_index + 1
        
        if not seq:
            break
            
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# # -----------------------------------------------------------------------------
# # 3. Run data operations.
# # -----------------------------------------------------------------------------

# # 3.1. Read the FASTA file.   
    
# # Create the empty lists IDs_fasta, headers_fasta, and seqs_fasta.
# IDs_fasta = []
# headers_fasta = []
# seqs_fasta = []

# # Open the FASTA file using with to ensure that it is closed after completion.
# with (open(fasta_file, 'r') as fasta:   
#     while True:
#         line = fasta.readline()
        
#         if line.startswith('>'):
#             headers_fasta.append(line.replace('\n', '\t'))
            
#             IDs_fasta.append(line.split()[0][1:])
            
#         else:
#             seqs_fasta.append(line)
                
#         if not line:
#             break

# # Check if FASTA file is corrupted.
# if len(headers_fasta) != len(seqs_fasta):
#     sys.exit('Error: FASTA file corrupted. Unequal number of headers and '
#              'sequences found.')


# # 3.2. Read the BLAST data file.

# data_blast = []

# # Open the BLAST data file using with to ensure that it is closed after
# # completion.
# with open(blast_file, 'r') as blast:
    
#     next(blast)
#     while True:
#         row = blast.readline()
        
#         row_split = row.split('\t')
        
#         if 'null' not in row_split[desc_blast_col]:
#             data_blast.append(row_split)
        
#         if not row:
#             break


# # 3.3. Create a dictionary to store protein IDs and custom strings.

# custom_strings_dict = {}

# for i, row in enumerate(data_blast):
    
#     ID_blast = data_blast[i][ID_blast_col]
#     desc_blast = data_blast[i][desc_blast_col]
#     custom_strings_dict[ID_blast] = (f'protein={desc_blast}\n')


# # -----------------------------------------------------------------------------
# # 4. Construct output file and conclude program.
# # -----------------------------------------------------------------------------

# # Open output_path provided by the user and write the output.
# with open(output_path, 'w') as output:
    
#     for i, header_fasta in enumerate(headers_fasta):
        
#         if IDs_fasta[i] in custom_strings_dict.keys():
            
#             # Construct the output file.
#             output.write(header_fasta
#                          + custom_strings_dict[IDs_fasta[i]]
#                          + seqs_fasta[i])

# # Print completion message.
# print(f'Output written to {output_path}')