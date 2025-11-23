#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 14:54:43 2025

@author: inf-33-2025
"""

"""
script that pastes the first input to the command line
"""

# import libraries
import sys

# save the second argument passed on the command line (right after the name of
# the program) to the variable `output`
output = sys.argv[1]

# print the output
print(f'\n\n{output}\n\n')