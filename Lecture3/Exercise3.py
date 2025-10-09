# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

#%%
# VENV TEST
import sys

if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("Inside venv")
else:
    print("Not in venv")

#%%
"""
Section 3.1
"""

#%% 3.1.6
# write a script that identifies the user, greets the user. be more positive
# if i am the user

user = input('Enter name + press enter ')

if user == 'Oliver':
    print('Nice to see you Oliver!')
else:
    print(f'Hi {user}')
    
#%% 3.1.7
# add caveat for friend

user = input('Enter name + press enter ')

if user == 'Oliver':
    print('Nice to see you Oliver!')
elif user == 'Benji':
    print('Hello again Benji!')
else:
    print(f'Hi {user}')
    
#%% 3.1.8
# create a script where a number is inputted and the output follows the rule
# number is divisible by 3: print `fizz`
# number is divisible by 5: print `buzz`
# number is divisible by 3 and 5: print `fizzbuzz`
# number is not divisible by 3 nor 5: print number

try:
    n = int(input('input number: '))

except ValueError:
    print('please input a number')

f = (n%3 == 0)
b = (n%5 == 0)

if f and b:
    print('fizzbuzz')

elif f:
    print('fizz')

elif b:
    print('buzz')

else:
    print(n)
    
#%% 3.1.9
# iterate over numbers 1-100 and compute fizzbuzz output

for n in range(1, 101):
    
    f = (n%3 == 0)
    b = (n%5 == 0)

    if f and b:
        print('fizzbuzz')

    elif f:
        print('fizz')

    elif b:
        print('buzz')

    else:
        print(n)
        
#%% 3.1.10
# create a script that takes what hole you are on and your strokes and tells
# you your score

# create lists with pars, score names, and an increasing list of numbers to
# represent the differences between the score names
pars = [4, 3, 5, 2, 5, 4, 7, 6]
score_names = ['albatross', 'eagle', 'birdie', 'par', 'bogie', 'double bogie']
named_scores = list(range(-3, 3))

# get input values from user, address inputs that are not numbers
try:
    hole = int(input('input hole: '))
    strokes = int(input('input number of strokes: '))
    
# FIX BELOW
except ValueError:
    print('please input a number')

if 0 > hole > 8:
    print('hole range: 1-8')
    
if hole or strokes <= 0:
    print('holes and strokes must be greater than 0')
    
# set score variable
score = (strokes - pars[hole - 1])
print(score)

# print output based on score
if score in named_scores:
    # set `score_name_index` by shifting the score up by 3 so that par ends up
    # at index 3 of score_names
    score_name_index = score + 3
    score_name = score_names[score_name_index]
    print(f'{strokes} strokes on hole {hole}: {score_name}')
    
elif score > 0:
    print(f'{strokes} strokes on hole {hole}: {score} above par')

else:
    print(f'{strokes} strokes on hole {hole}: {score} below par')
    
#%% 3.1.12 (skipped 3.1.11)
# find the position of tyrosine codons in a sequence

# assign seq and amino acids
seq = 'UAUAAACGAUACCAUUACUAUGACCAUGGG'
tyr = ['UAU', 'UAC']

# get reading frame shift input from user and ensure it is an integer
try:
    reading_frame_shift = int(input('input reading frame shift: '))
´except ValueError:
    print('reading frame shift must be a number. no reading frame shift applied')

# shift reading frame
if 0 < reading_frame_shift < 3:
    seq = seq[reading_frame_shift: ]

# loop through the length of seq, pringing each codon and its identity if it
# is tyrosine
for i in range(len(seq)):
    if i%3 == 0:
        codon = seq[i: i + 3]
        if codon in tyr:
            print(i, codon, 'tyrosine')
        else:
            print(i, codon)
        if len(codon) < 3:
            print(f'incomplete codon read at position {i}')
            
#%% 3.1.13
# print the first n primes, only check factors below x*.5

# import libraries, get number of primes and speed up call from from user
import math

# ensure input is a positive integer
try:
    n_primes_max = abs(int(input('how many successive primes would you like to compute? ')))
except ValueError:
    print('error: you must input a number')

# ensure `speed_up` input is an integer
try:
    speed_up = int(input('would you like to speed up by not computing factors of non-primes? (0 or 1) '))
except ValueError:
    print('error: you must input a number')
    
# create blank list to store primes
primes = []
x = 1

# loop through 
while len(primes) < n_primes_max:
    x = x + 1
    factors = []
    for i in range(1, math.ceil(x/2) + 1):
        if x%i == 0:
            factors.append(i)
        elif speed_up:
            if len(factors) > 1:
                break
        else:
            pass
        
    if len(factors) == 1:
        primes.append(x)
        print(f'{x} is prime numer {len(primes)}')
    elif speed_up == False:
        print(f'{x} is divisible by {factors}')
    else:
        pass

if speed_up:
    print('non-primes are not printed to save compute time')