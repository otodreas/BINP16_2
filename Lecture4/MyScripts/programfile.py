#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 14:21:35 2025

@author: inf-33-2025
"""

# take filename from command line
# print name of script
# print name of input file
# open file, print contents
# should run on command line with `python programfile.py inputFile.txt`

import sys

# you access the terms you type into the terminal after `python ` by iterating
# over sys.argv (arguments are separated by spaces in terminal)
program = sys.argv[0]
inputfile = sys.argv[1]
print(f'\nprogram: {program}')
print(f'\nfile: {inputfile}\n')

# with open(inputfile, 'r') as f:
#     for l in f:
#         print(l.strip('\n'))

with open(inputfile, 'r') as f:
    lines_list = f.readlines()
    for l in lines_list:
        print(l)
        