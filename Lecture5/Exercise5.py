#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 15:19:11 2025

@author: inf-33-2025
"""

#%% 5.3: make functions taking 2 names and returning string with greeting.

# Define function.
def greet(name1, name2):
    return f'Hello {name1} and {name2}!'

# Run function and print output.
print(greet('Björn', 'Dag'))

#%% 5.4: modify greet so that when names aren't passed, question marks are
# returned.

# Define new function.
def greet(name1='?', name2='?'):
    return f'Hello {name1} and {name2}!'

# Run function and print output.
print(greet())
print(greet('Petr'))
print(greet('Björn', 'Dag'))

#%% 5.5: make 2 functions, one for addition and one for multiplication of 2
# numbers.

# Define functions.
def multiply(term1, term2):
    return term1*term2

def add(term1, term2):
    return term1+term2

# RUn functions and print outputs.
print(multiply(2, 3))
print(add(2, 3))

#%% 5.11: create dictionary from sample FASTA file.

# Open the file, read line by line to save memory, storing lines in dictionary
# fasta_dict.
fasta_dict = {}
line_index = 0
with open ('sequences.fasta', 'r') as fasta:
    while True:
        line = fasta.readline().strip()
        if line_index % 2 == 0:
            key = line
        else:
            value = line
            fasta_dict[key] = value
        line_index = line_index + 1
        if not line:
            break

#%% 5.12: Iterate through dictionary printing each key and value pair.

for i, key in enumerate(fasta_dict.keys()):
    print(f'Entry {i+1} has header: {key[2:]} and sequence: {fasta_dict[key]}')
    
#%% 5.13: Write a function taking a filepath and returning a dictionary.

def fasta_dict_maker(filepath):
    fasta_dict = {}
    line_index = 0
    with open (filepath, 'r') as fasta:
        while True:
            line = fasta.readline().strip()
            if line_index % 2 == 0:
                key = line
            else:
                value = line
                fasta_dict[key] = value
            line_index = line_index + 1
            if not line:
                break
    return fasta_dict

print(fasta_dict_maker('sequences.fasta'))

#%% 5.14: Calculate GC content for each sequence in sequences.fasta.
# Save all sequences to a list.
# The function should calculate the GC content of one sequence, and I should
# use the function in a loop.

# Define single sequence GC calculator function.
def calcGC(seq):
    seq.upper()
    gc = (seq.count('G') + seq.count('C')) / len(seq)
    return gc

# Create list of sequences from dictionary.
fasta_dict = fasta_dict_maker('sequences.fasta')
sequenceList = fasta_dict.values()

# Print GC content of all sequences in sequenceList.
for sequence in sequenceList:
    gc = calcGC(sequence)
    print(f'{sequence}: {round(gc * 100, 1)}%')
    
#%% Bonus: calculate GC for every sequence in a file directly.

def calcGC_direct(filepath):
    fasta_dict = {}
    line_index = 0
    with open (filepath, 'r') as fasta:
        while True:
            line = fasta.readline().strip()
            if line_index % 2 == 0:
                key = line
            else:
                value = line
                fasta_dict[key] = value
            line_index = line_index + 1
            if not line:
                break
    return fasta_dict