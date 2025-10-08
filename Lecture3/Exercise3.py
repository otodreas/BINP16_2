# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

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