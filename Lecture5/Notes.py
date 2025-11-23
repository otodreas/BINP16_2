#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 13:09:48 2025

@author: inf-33-2025
"""

#%% exercise: reverse transcrive dna

# define function reverse_transc
def reverse_transc(seq, isDNA=True):
    
    # Convert sequences to DNA or RNA depending on the user input and generate
    # list of pairs
    if isDNA:
        seq = seq.replace('U', 'T')
        pairs = [['G', 'C'], ['A', 'T']]
    else:
        seq = seq.replace('T', 'U')
        pairs = [['G', 'C'], ['A', 'U']]
    
    # Initialize reverse sequence
    seq_reverse = ''
    
    # Loop through the sequence in reverse, adding complements to seq_reverse
    for base in seq[::-1]:
        for pair in pairs:
            if base in pair:
                seq_reverse += pair[not pair.index(base)]
    
    # Return sequence
    return seq_reverse

#%%

print(reverse_transc('GAUUGCU', isDNA=False))

#%%

'dfadfad'.replace('y', 'x')