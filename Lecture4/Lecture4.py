#Lecture 4

#Press F9 to run a single line
#Press CTRL+ETNER to run the whole code

#%% Reading input from the user
print(input('What is your name? ')) 


data = input('Do some math: (e.g., 1+1) ')
print("The answer is %.5f" % eval(data))

#%% Reading files – open() and close()

#Note, f is a file handle (or file object), meaning it is a reference to the file that was opened. It represents a reference to a system resource (e.g., a file, memory, or a window)

#Open and close files (1)
f = open('Test_read.txt', 'r')
data = f.read()
print(data)
f.close()


#%%

#Open and close files with the with command (2)
with open("Test_read.txt", 'r') as txt:
    for line in txt:
        #print('. ' + line)
        print(line.strip('\n'))


#%% Reading files – read(), readline(), and readlines()

#read
f = open('Test_readlines.txt', 'r')
data = f.read()
print(data)
f.close()

#%%
#readline
f = open('Test_readlines.txt', 'r')
line = f.readline()
while line:
    line = f.readline()
    print(line)
f.close()

#%% readline (number)
f = open('Test_readlines.txt', 'r')
print(f.readline(3))
f.close()

#%% readline  (using for loop)
#An elegant way of reading the file
f = open('Test_readlines.txt', 'r')
for line in f:
    print(line)
f.close()

#%%
#readlines
f = open('Test_readlines.txt', 'r')
lines = f.readlines()
f.close()
for line in lines:
    print(line)

#%% Reading whitespace-separated files

#Reading bim.txt
r = open('bim.txt')
pos_vec = []
header = r.readline() #don't need the header

for line in r:
    #line = r.readline()
    data = line.split()
    print(data);
    
    chr, SNP, temp, pos, a1, a2 = data
    pos_vec.append(int(pos))

print('The file contains #', len(pos_vec), ' rows')
print('The file positions are: ', pos_vec)

#%% Reading FASTA files

r = open('Fasta_example_3_seq.txt', 'r')
seq = [] #Holds the final combined sequences
seq_fragments = [] #Holds the current subsequence
counter = 1;

#Use the elegant way of reading the file
for line in r:
    print(str(counter) + '.') #prints line number
    print(line)

    #Is this the header line? if so, 
    if line.startswith('>'):
        print('Found a >') #Found start of a sequence
        
        #If this is NOT the first sequence
        if seq_fragments:
            print('Concatenating the sequences.')
            #Add sequence to a list of sequences, keep them separate
            curr_seq = ''.join(seq_fragments)
            seq.append(curr_seq)
        seq_fragments = []
    else:
        print('Not a > sign. Sequence or space.\n')
        #Found more of existing sequence
        curr_seq = line.rstrip() #remove new line character
        print(curr_seq)
        seq_fragments.append(curr_seq)

    counter+=1
else:
    print('Exiting the loop')
    
#Appending the last fasta sequence (same code as above, which is not executed, becasue there are no more headers)
if seq_fragments:
    print('Concatenating the last sequence.\n')

    #if the file is not empty
    curr_seq = ''.join(seq_fragments)
    seq.append(curr_seq)

r.close()

print("Printing the concatenated file:")
print(seq)

#%%
#An alternative shorter way to reading FASTA files
r = open('Fasta_example_3_seq.txt', 'r')
seq = [] #Holds the final combined sequences
temp=''

for line in r:
    if line.startswith('>'):
        #Found start of a sequence
        if temp:
            seq.append(temp); #Keep the previous sequence in seq
        temp='' #zero temp
    else:
        #Found an existing sequence
        temp += line.rstrip() #remove new line character

if temp:
    #if the file is not empty
    seq.append(temp)

r.close()

print("Printing the concatenated file:")
print(seq)

#%% Catching errors before they wreck your code
#checks that a file exists

import os
filename = 'Fasta_example_3_seq.txt'
if os.path.exists(filename):
    print('File exists')
else:
    print('File does not exists')
        
        
#%%  XML  
#Parsing XML file

from urllib.request import urlopen #module to open the url
from lxml import etree #module to read xml files

baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
query = "db=pubmed&id=36046618&format=xml"
url = baseurl+query
f = urlopen(url) #opens the url with urlopen module
resultxml = f.read() #reads the url content
xml = etree.XML(resultxml) #parses the content into xml format

#The paper is here: #https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=36046618&format=xml
resultelements = xml.xpath("//LastName") #search for all 'last name' tags in the given xpath

for element in resultelements:
    print ([element.text])

#%%
#Get the last 3 pubmed IDs for Dan Graur
from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree

author_name = "Dan Graur"

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
url = base_url + urlencode({"db": "pubmed", "term": author_name+"[author]"})

f = urlopen(url)
resultxml = f.read()
xml = etree.XML(resultxml)
resultelements = xml.xpath("//Id")

for element in resultelements[:3]:
    print([element.text])
    
#%% File output – write() and writelines()

#Write results to file
f = open("filename.txt", 'w') 
f.write("Writing exercise 1\n") 
f.write("Here is a string that ends with " + str(2022) + '\n\n') 
f.close()

#Write results to file in a loop
f = open("filename.txt", 'a') 
f.write("Writing exercise 2\n") 
f.write('%s\n%s\n' % ('sequence number 1', 'sequence number 2\n'))
f.close()

f = open("filename.txt", 'a') 
f.write("Writing exercise 3\n") 
f.writelines(['sequence number 1', '\nsequence number 2\n'])
f.close()


#%% Writing a FASTA file using enumerate()

#Writing FASTA file
comment = 'This is a FASTA file'
sequence = 'AGCGACGATCGCTAGATCGCTAGGAGCGACGATCGCTAG'\
           'ATCGCTAGGAGCGACGATCGCTAGATCGCTAGGAGCGAC'\
           'AAAAAAAAaTCGCTAGATCGCTAGGAGCGACGATCGCTA'\
           'GGAGCGACGATCGCTAGATCGCTAGGAGCGACGATCGC'\
           'AGATCGCTAGGAGCGACGATCGCTAGATCGCTAGG'

print(sequence)

fileObj = open('FASTA_write.txt', 'w')
fileObj.write('> %s\n' %comment) #Write the header

#Read char-by-char from sequence
for (n, code) in enumerate(sequence):
    print([str(n) + ' ' + code]);
    
    #IF this is the first char (we are after the header) or the 60's
    if n>0 and n%60==0:
        print("\n")
        fileObj.write('\n')
    
    #write the char to the file
    fileObj.write(code)
    
#If this is not the 60s char, add \n    
if n%60 != 0:
    fileObj.write('\n')
fileObj.close()

#%% Writing column delimited formats - EXCERCISE

data = [['chr1', 'rs121', 0, 100, '1', '1'], ['chr2', 'rs111', 0, 101, '2', '3']]
heading = ['chr', 'rs#', 'cM', 'Pos','Allele1', 'Allele2']
formats = ['%s', '%s', '%d', '%d', '%c', '%c']
separator = '\t'

#Open fileobj for writing
fileobj = open('output.txt', 'w');

#Writing headers
line = separator.join(heading)

#Writes the value of line, followed by a newline, into the file connected to fileobj.
fileobj.write('%s\n' %line)

#keep the format style in a single variable
format = separator.join(formats) #'%s\t%s\t%d\t%d\t%c\t%c'

#For each row in data
for row in data:
    
    #row = data[0]
    print(row)
    
    #% Format the variables in row enclosed in a "tuple", together with a format string (format). Conversion to tuple was necessary for 'format % ...' to work
    #Notice the conversion to tuple, % doesn't know how to work with lists
    line = format % tuple(row) #e.g., 'chr2\trs111\t0\t2\t3'
    print(line)
    fileobj.write('%s\n' %line)

fileobj.close()

    