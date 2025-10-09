#Use the debug to follow these commands
#Use CTRL+F5 and CTRL+10

r = open('Fasta_example_3_seq_short.txt', 'r')
seq = []
temp=''

for line in r:
    if line.startswith('>'):
        #Found start of a sequence
        if temp:
            seq.append(temp); #Keep the previous sequence in seq
        temp='' #zero temp
    else:
        #Found more of existing sequence
        temp += line.rstrip() #remove new line character

if temp:
    #if the file is not empty
    seq.append(temp)

r.close()
print("Printing the concatenated file:")
print(seq)