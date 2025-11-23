#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 16:07:13 2025

@author: inf-33-2025
"""

"""
Section 4.1
"""

#%% 4.1.a-f

# skipped because it wants me to use Path instead of os

#%% 4.2.a
# ascii encoding string

string = 'är det du som har kaffebrödet, Gösta?'

ascii_string = str.encode(string)

# print(type(ascii_string), ascii_string)

# using utf-8 (this is identical, but the syntax is easier and there is a decode option)
encoded = string.encode('utf-8')
decoded = encoded.decode('utf-8')

print(encoded, '\n', decoded)

print(encoded == ascii_string)

#%% 4.2.b
# make csv from data, read it back in, make it back into python data

import os
import pandas as pd
import numpy as np

np.random.seed(0)
print('dir:\n', os.getcwd(), '\n')

data = {
        'id': ['foo'] * 2 + ['bar'] * 2,
        'value': list(np.random.normal(0, 1, 4)),
        'group': [1, 2] * 2
        }

df = pd.DataFrame(data)

print('dataframe:\n', df, '\n')

df.to_csv('42b_data.csv', index=False)

print('files in dir:\n', os.listdir(), '\n')

with open('42b_data.csv', 'r') as file:
    imported_data = file.read()
    print('imported csv:\n', imported_data, '\n')
    
print('imported csv as df:\n', pd.read_csv('42b_data.csv'))