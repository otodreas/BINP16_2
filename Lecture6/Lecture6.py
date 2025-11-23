#Lecture 6

#Press F9 to run a single line
#Press CTRL+ETNER to run the whole code


#Check out https://regex101.com/

    
#%% Using re.search 

import re

# Checks if pattern matches anywhere in <string>
# pattern.search(<string>)               

text = 'This survival of the fittest, which I have here sought to express in mechanical terms, is that which Mr. Darwin has called "natural selection," or the preservation of favoured races in the struggle for life';

#Finding substring with RE
matchstr0 = re.search('survival', text); print(matchstr0)
print(matchstr0.start())
print(matchstr0.end())

matchstr1 = re.search('selection', text); print(matchstr1)
matchstr2 = re.search('evolution', text); print(matchstr2)

#finds the first in, not the seocnd
matchstr3 = re.search('in', text); print(matchstr3) 

#Finding substring *without* RE
text.find('survival') 
text.find('xxx') 

#Replacing a substring
text.replace('survival', 'failure') 

#Some things may be easier with RE
matchstr0 = re.search("(s\w+)", text); print(matchstr0)
matchstr1 = re.search("(of\s)", text); print(matchstr1)

#%% Using re.match

#result = re.match(pattern, string, flags=0);

text = 'Forever young I want to be forever young Do you really want to live forever? Forever, and ever';

#Found a match at the beginning of the string
matchstr0 = re.match("Forever", text); print(matchstr0)
matchstr0 = re.match("Forever young", text); print(matchstr0)

#Returns none, because young is not at the beginning
matchstr1 = re.match("young", text); print(matchstr1)


#%% Using re.findall

#The re.findall() function returns a list containing all matches.

#result = re.findall(pattern, string);

text = 'Forever young I want to be forever young Do you really want to live forever? Forever, and ever';

#Found a match at the beginning of the string
matchstr0 = re.findall("Forever", text); 
print(matchstr0)

#Compare re.findall to re.search, which stops after the first occurrence
matchstr1 = re.search("Forever", text); 
print(matchstr1)

#%% Using re.finditer

text = 'Forever young I want to be forever young Do you really want to live forever? Forever, and ever';


#If you want to get the positions do, use "list comprehension"
#General term: [expression for item in iterable if condition]
positions = [(match.start(), match.end()) for match in re.finditer("Forever", text)]
print(positions)

'''
Explanation: This for loop iterates over each match object returned by re.finditer().
Each match represents a found occurrence of the specified pattern (in this case, "Forever").
match.start() returns the starting index of the match in the text.
match.end() returns the index just past the end of the match.
[(...)] - This syntax creates a list. Each element in the list is a tuple containing the start and end positions of a match found in the text.

'''

#%% Using re.sub

#result = re.sub(pattern, repl, string, count=0, flags=0);

regex = "less"
test_str = ("I am a harmless regex pattern, so harmless\n")
subst = "ful"

print('\nOriginal string')
print (test_str)

#Delete pattern harm
print('\nDeletion "harm"')
result = re.sub('harm',  '', test_str) 
print(result)

#Replace pattern less->harmless
print('\nReplacement: less->harmful')
result = re.sub('less',  '   harmful  ', result) 
print(result)

#Eliminate duplicate white spaces using wildcards
print('\nEliminate duplicate whitespaces')
result = re.sub('\s+', ' ',   'xxx  xxx  xxxx      xx') 
print(result)

print('\nEliminate only the first duplicate')
result = re.sub('\s+', ' ',   'xxx  xxx  xxxx      xx', 1) 
print(result)


# Using re.DOTALL on a text with \n
text = '''Forever young I want to be forever young\n Do you really want to live forever?\n Forever, and ever'''

pattern = r'.*' #matches any sequence of characters (excluding \n) 

#Using DOTALL changes means "including \n"
#it will treat the entire text as one match, including newline characters
result_dotall = re.findall(pattern, text, re.DOTALL)
print("With re.DOTALL:")
print(result_dotall)

# Without re.DOTALL, dot does not match newlines
#this is the default behavior of re.findall (not considering newline characters (\n) when matching). Instead, it treats each line or segment of the text as a separate match.
result_no_dotall = re.findall(pattern, text)
print("\nWithout re.DOTALL:")
print(result_no_dotall)


#%% Using re.split

#The re.split() function splits the string by the occurrences of the regex pattern, returning a list containing the resulting substrings.

#result = re.split(pattern, string);

text = 'Forever young I want to be forever young';

#Found a match at the beginning of the string
matchstr0 = re.split("young", text); 
print(matchstr0)

#Compare re.finall to re.search, which stops after the first occurance
matchstr1 = re.split(" ", text); 
print(matchstr1)

#%% Practice re.split: Exercise I

text = ('In the year of 2012 the world did not end, but maybe in the year 2025');
print(text.split('2012'))
print(text.split('year',1))
print(text.split('year',2))

print(text.split('year',1))
print(text.rsplit('year',1))

text = ('In the year of 2012 the world did not end\n, but maybe in the year 2025');
print(text.splitlines())

text = ('In the year of 2012; the world; did not; end, but maybe in the year 2025');
print(text.split(';'))

print(text.split(maxsplit=2))

#concatenate strings
print("hello" + ' ' + "world")

strings = ['hello', 'world']
print(' '.join(strings))

#slice(start, stop, step)
text = ('In the year of 2012 the world did not end, but maybe in the year 2025');
x = slice(5,12,1)
print(text[x])


#%% Using re.compile

text = 'This survival of the fittest, which I have here sought to express in mechanical terms, is that which Mr. Darwin has called "natural selection," or the preservation of favoured races in the struggle for life';

#The match object
REobj = re.compile('fittest')
matchstr3 = REobj.search(text); 
print(matchstr3)
print(matchstr3.span())

#Compile - Second part

#Did Herbert Spencer capitalize Natural Selection or not? 
text = 'Natural'
REobj = re.compile('[Nn]atural')
matchstr4 = REobj.search(text); 
print(matchstr4)

#Example of using RE characters
REobj = re.compile('\[abc\]')
matchstr5 = REobj.search('Text with exactly [abc] inside'); 
print(matchstr5)

#%% Using a range of letters and numbers

text = 'This lamp has a grade B'
REobj = re.compile('grade [ABCDE]')
matchstr7 = REobj.search(text); print(matchstr7)
REobj = re.compile('grade [A-E]')
matchstr7 = REobj.search(text); print(matchstr7)

text = 'This lamp has a grade 2'
#what is the problem here?
REobj = re.compile('\d')
matchstr8 = REobj.search(text); print(matchstr8)

#One solution...
text = 'This lamp has a grade 25'
REobj = re.compile('\d\d')
matchstr8 = REobj.search(text); print(matchstr8)
#But it's not a great solution

#%% Looking for alterative strings

#Alternative substrings
import re

text = "The genome consists of DNA molecules"
REobj = re.findall('DNA|RNA', text); print(REobj)
text = "The genome consists of RNA molecules"
REobj = re.findall('DNA|RNA', text); print(REobj)

text = "The genome consists of DNA."
REobj = re.compile('\s(DNA|RNA)\.')
matchstr9 = REobj.search(text); print(matchstr9)

text = "The genome consists of RNA."
matchstr9 = REobj.search(text); print(matchstr9)

#%% #Finding multiple instances

#Find the first number (ok to have multiple digits)
REobj = re.compile('\d+')
matchstr10 = REobj.search('In the years of 2012 or 2013 the world did not end'); print(matchstr10) #<re.Match object; span=(0, 20), match='In the years of 2012'>
print(matchstr10.group(0)) #2012

#This pattern \b\d{4}\b looks for four digits surrounded by word boundaries (\b). It will match any four-digit sequence in the text. 
pattern = r'\b\d{4}\b'
matches = re.findall(pattern, 'In the years of 2012 or 2013 the world did not end')
print(matches) #['2012', '2013']

#Find the first string (multiple words) that is followed by a number (multiple digits)
REobj = re.compile('\D+\d+') # spaces are allowed
matchstr10 = REobj.search('In the year of 2012 the world did not end'); print(matchstr10.group())

# Find the first string with any characters and any number of words
REobj = re.compile('.+')
matchstr10 = REobj.search('In the year of 2012 the world did not end'); print(matchstr10.group())

# match white space + digits
REobj = re.compile('\s\d+')
matchstr10 = REobj.search('abc 12 abc34'); 
print(matchstr10)
print(matchstr10.group())

#compare to this, where \s was removed
REobj = re.compile('\d+')
matchstr10 = REobj.search('abc 12 abc34'); 
print(matchstr10)
print(matchstr10.group())

#match whitespace followed by any letters and then a number with 4 digits
REobj = re.compile('\s[a-z]+\d{4}')
matchstr10 = REobj.search('xzy 12 abc3487678'); 
print(matchstr10)
print(matchstr10.group())

#What will this print?
REobj = re.compile('\s[a-z]+\d{2}')
matchstr10 = REobj.search('xzy 12 abc3487678'); 
print(matchstr10)
print(matchstr10.group())

#%% Group and groups
text = ('In the year of 2012 the world did not end, but maybe in 2025 or 2030');

#Find white space (\s) and digits (\d+)
REobj = re.compile('\s(\d+)')
matchstr11 = REobj.search(text); 
print(matchstr11.groups()) #returns all explicitly-captured groups
print(matchstr11.group(0)) #returns the entire substring that matched the RE
print(matchstr11.group(1)) #returns the first substring that matched the RE

#Find digits (\d+), non digits (\D+) and digits (\d+)
text = ('In the year of 2012 the world did not end, but maybe in 2025 or 2030');

REobj = re.compile('(\d+)\D+(\d+)')
matchstr11 = REobj.search(text); 
print(matchstr11.group(0)) #2012 the world did not end, but maybe in 2025
print(matchstr11.group(1)) #2012
print(matchstr11.group(2)) #2025
print(matchstr11.groups()) #('2012', '2025')

'''
Notice that print(matchstr11.group(2)) doesn't print the entire text because of how the group() method works in regex. It only returns the specific captured group defined by the parentheses in your regex pattern.
'''

REobj = re.compile('(\d+)(\D+)(\d+)')
matchstr11 = REobj.search(text); 
print(matchstr11.group(2)) #What will be printed here?


#Notice that 2030 was not captured. How can we fix that?
print(re.findall('\s(\d+)', text)) #['2012', '2025', '2030']

print(re.findall('(\d+)',text)) #['2012', '2025', '2030']

#%% Tricks when using specical character
text='C:\documents'
reobj = re.compile('\documents')
print(reobj.search(text).group()); #Fails

reobj = re.compile('\\documents')
print(reobj.search(text).group()); #Fails

reobj = re.compile('\\\\documents') #Ugly right?
print(reobj.search(text).group()); #prints: \documents

reobj = re.compile(r'\\documents') #This is much nice
print(reobj.search(text).group()); #prints: \documents

#%% Using r

#The 'r' at the start of the pattern string tells python that a "raw" string which passes through backslashes without change. It is very useful for regular expressions and some people use it all the time with pattern strings. In this case, it would also work without it.

str = 'an example \word:cat!!'
match = re.search(r'\\word:\w\w\w', str)

# If-statement after search() tests if it succeeded
if match:
    print('We found: ', match.group()) ## 'found word:cat'
else:
    print('We did not find: ')

    match = re.search(r'\\word:\w\w\w', str)


# Not lets run it without using r
match = re.search('\\word:\w\w\w', str)
if match:
    print('We found: ', match.group()) ## 'found word:cat'
else:
    print('We did not find: ')

#%% using regex101.com

regex = (r"less")

test_str = "I am a harmless string"

subst = "ful"

# You can manually specify the number of replacements by changing the 4th argument
result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

if result:
    print (result)

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.



#%% Practice Split Exercise - Solution
text = ('In the year of 2012 the world did not end, but maybe in the year 2025');
print(text.split('2012'))
print(text.split('year',1))
print(text.split('year',2))

print(re.split('2012', text))
print(re.split('year', text))



#%% Practice counting with RE - Solution

import re

Z1 = '1 2 1 1 2 2 3 3 3 2 3'

#Solution 0
#Count number of occurrences 2's in this string
print(len(re.findall('[2]+', Z1)))

#print the match objects
for match in re.finditer('[2]+', Z1):
    print(match)

#Solution 1
z1 = '1 1 1 2 2 3 3 3 3'
list = re.split('\W', z1)
print(list.count('3'))

#Solution 2
Z1 = '1 1 1 2 2 3 3 3 3'
print(len(re.findall('3', Z1)))

#Solution 3
Z1 = '1 1 1 2 2 3 3 3 3'
REobj = re.findall('3',Z1)
print(REobj)
REobj.count('2')

#Solution 4 (no RE)
Z1 = '1 1 1 2 2 3 3 3 3'
Z1.count("2")