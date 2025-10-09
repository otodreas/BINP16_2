#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 12:57:44 2025

@author: inf-33-2025
"""

#%%

import os
os.getcwd()
# change to local
os.chdir('/home/inf-33-2025/Desktop/Courses/BINP16_2/Lecture4')

#%% exercise: writing column delimited formats

data = [['chr1', 'rs121', 0, 100, '1', '1'], ['chr2', 'rs111', 0, 101, '2', '3']]
heading = ['chr', 'rs#', 'cM', 'Pos','Allele1', 'Allele2']
formats = ['%s', '%s', '%d', '%d', '%c', '%c']
separator = '\t'
fileobj=open('output.txt', 'w');


line = separator.join(heading)
fileobj.write('%s\n' %line)

print(line)

#keep the format in a variable
format = separator.join(formats)

#For each row in data
for i, row in enumerate(data):
    line = data[i]
    fileobj.write('%s\n' %line)


fileobj.close()