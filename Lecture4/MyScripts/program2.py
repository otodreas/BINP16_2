#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 14:43:55 2025

@author: inf-33-2025
"""

"""
program that outputs all inputs to terminal
"""

# import libraries
import sys

# create list to store inputs in
inputs = []

# loop through all args passed in the command line besides the program name
# appending args to input lists
for i in range(1, len(sys.argv)):
    inputs.append(sys.argv[i])
    
# make string out of the input list
output_str = ' '.join(inputs)
    
# print output
print(f'\n\n{output_str}\n\n')