#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 13:52:43 2025

@author: inf-33-2025
"""

###############################################################################
'''
class exercises
'''

#%% think of a sentence then think of 3 questions that you can answer using regex

import re

sentence = 'There were 30 observedddd cases of Listeria, 26 of them causing sepsis.'

# is listeria a proper noun?
print(f'"Listeria" found at: {re.search("Listeria", sentence)}')
print(f'"listeria" found at: {re.search("listeria", sentence)}')

# are there sticky keys on the authors keyboard?


# how many cases of each condition were found?
pattern = re.compile(r'\d+')
cases = pattern.search(sentence)
print(cases.group())

#%% count with regular expressions: exercise iii

# count occurrences of 2s in the string
Z1 = '1 1 1 2 2 3 2 3 3 3 2'
print(len(re.findall('2', Z1)))

# count occurrences of [2 3] in the string
Z2 = '1 1 1 2 2 3 2 2 3 3 3 2 3 1 2 3'
print(len(re.findall('2 3', Z2)))

###############################################################################
'''
practice exercises
'''

#%% 6.1
# write a program that takes an arbitrary string, prints number of characters
# per type, or contains none if the string is empty
# types: lower, upper, numbers, whitespace

def char_counter(string):
    
    import re
    
    type_found = False
    char_types = {"lowercase": r"[a-z]",
                  "uppercase": r"[A-Z]",
                  "digits": "\d",
                  "whitespaces": "\s"}
    
    for i, item in enumerate(char_types.items()):
        
        if re.search(item[1], string):
            type_found = True
            print(f"contains {item[0]}")
        else:
            pass
        
        if i == len(char_types)-1 and not type_found:
            print("contains none of the required character types")

#%% 6.2

