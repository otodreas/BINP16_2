#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 13:04:22 2025

@author: inf-33-2025
"""

#%% finding indecies of each string

import re

text = 'Forever young I want to be forever young Do you really want to live forever? Forever, and ever';


#If you want to get the positions do, use "list comprehension"
#General term: [expression for item in iterable if condition]
positions = [(match.start(), match.end()) for match in re.finditer("Forever", text)]
print(positions)

