#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:17:40 2025

@author: inf-33-2025
"""

# import libraries
import sys

# save command line inputs to variables
try:
    script_name, fasta_file, blast_file, output_path = sys.argv[0:5]

# exit the program and throw an error if the number of arguments passed is wrong
except ValueError:
    sys.exit('Please enter a fasta file, blast file, and output path after the script name')

IDs_blast = []
with open(blast_file, 'r') as blast:
    lines = blast.readlines()
    for i, l in enumerate(lines):
        if i == 0:
            blast_header = l.split('\t')
        else:
            IDs_blast.append(l.split('\t'))


ID_blast_index, desc_blast_index = blast_header.index('#queryName'), blast_header.index('hitDescription')

custom_strings_dict = {}

for i, row in enumerate(IDs_blast):
    ID_blast, desc_blast = IDs_blast[i][ID_blast_index], IDs_blast[i][desc_blast_index]
    custom_strings_dict[ID_blast] = (f'\tprotein={desc_blast}')
        # at this stage we have the string and the ID number that has an equivalent in the fasta file
        # we want to write it into the output file
        





# get ID's corresponding with queryName in the blast file

IDs_fasta = []
headers_fasta = []
seqs_fasta = []
with open(fasta_file, 'r') as fasta:
    lines = fasta.readlines()
    for l in lines:
        if l.startswith('>'):
            headers_fasta.append(l.strip())
            IDs_fasta.append(l.split()[0][1:])
        else:
            seqs_fasta.append(l.strip())

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









if (len(IDs_fasta) == len(headers_fasta) == len(seqs_fasta) == len(custom_strings_dict)) != 1:
    print('data length error')


    

with open(output_path, 'w') as output:
    for i, header_fasta in enumerate(headers_fasta):
        output.write(header_fasta + custom_strings_dict[IDs_fasta[i]] + '\n')
        output.write(seqs_fasta[i] + '\n')