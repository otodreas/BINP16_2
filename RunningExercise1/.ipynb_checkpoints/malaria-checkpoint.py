#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:17:40 2025

@author: inf-33-2025
"""

# import libraries
import sys

# inputs:

try:
    script_name, fasta, blast, output_path = sys.argv[0:5]
except ValueError:
    sys.exit('Please enter a fasta file, blast file, and output path after the script name')

print(script_name)
print(fasta)
print(blast)
print(output_path)