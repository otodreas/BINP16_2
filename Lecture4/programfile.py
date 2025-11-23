import sys

#We can save the input into variables 
PythonScriptName = sys.argv[0] #programfile.py
DataScriptName = sys.argv[1] #inputFile.txt
print('The first variable is:', DataScriptName, '\n')

#We can print the variables at the same order
print('Printing the input\n')
for arg in sys.argv: 
    print(arg)
