#Lecture 5

#Press F9 to run a single line
#Press CTRL+ETNER to run the whole code



#%%
#Example of a function
x=abs(-3.0)
print(x)

#%%
#Function that takes no parameters
def say_hi():
    print('Hello World!')
    
#Main code    
say_hi()
say_hi()

#%% Simple examples of functions

#Function that takes a parameter, but does not return anything
def say_hi(name):
    print('Hello ' + name)

#Main code    
say_hi('Homer')    

#%% Our first function
#Function that takes a parameter and returns a value
def say_hi(name):
    response = 'Hello ' + name + '!'
    return response

#Main code    
print(say_hi("Moses"))
print(say_hi("Deborah"))
 
#%% Another example

#Function that takes 2 parameters and returns a value
def say_hi(name1, name2):
    response = 'Hello ' + str(name1) + ' and '  + str(name2)
    return response

#Main code    
responses = say_hi('C. Darwin', 'R. Dawkins')
print(responses)
responses = say_hi('G. Mendel', 'L. Pasteur')
print(responses)

responses = say_hi(4, 5)
print(responses)

#%% Defining a function – input and default values (1)

#Stepping on a function
x=abs(-3.0); print(x)

def abs(name1, name2):
    response = 'Hello ' + name1 + ' and '  + name2
    return response

#Main code    
responses = abs('C. Darwin', 'R. Dawkins')
print(responses)

x=abs(-3.0); print(x)

del abs #releases abs

#%% Defining a function – input and default values (2)

#Assign variables as default
age=10
def runSimulasion(x, numSteps=age):
    print(x)
    print(numSteps)

runSimulasion(500, age)
runSimulasion(20)

#%% How objects are passed to functions

#Another example of the problem (“Call by reference”, I)

#The function myfun(param) appends [100] to this list in place because lists are mutable objects. As a result, each time you call myfun(param), the same list param gets modified, and 100 is appended to it.
def myfun(param):
    param+=[100]
    print(param)

#param is defined as a list ([10]) before calling the function.
param=[10]
myfun(param)
myfun(param)
myfun(param)

#%%
#Another example of the problem (“pass by value")

def myfun(param):
    param += 100  # Modify the parameter inside the function
    print(param)

# Main code
param = 10  # Immutable integer
myfun(param)  # Pass integer to the function
myfun(param)  # Pass integer to the function
myfun(param)  # Pass integer to the function
print("Outside function:", param)  # Check if the original value was affected


#%% Another example of a (“Call by reference” II) list that behaves differently
'''
This dmeonstartes the case of changes inside the function that affect the external object.
In the first case of caslling by reference (I) , we are working with the same list object.
In the second example (II), we are creating new lists each time, so each call works on its own local object, which gets modified and then discarded after the function ends.

#In this case, you are passing new lists to the function each time. Even though lists are mutable, you are creating a new list (like [1], [10], or [100]) for each function call. Each list is independent, so the changes (appending [100]) only affect the list created during that specific function call.
'''

#plain case
def myfun(param):
    param+=[100]
    print(param)

#Main code
myfun([1])
myfun([10])
myfun([100])


#%%
#Another example of the problem (“Call by reference”) - using empty as default
'''
Problem: In Python, default arguments are evaluated only once at the point of function definition, not each time the function is called. When you use a mutable object like a list as a default argument, it can persist across multiple function calls. This means that every time you call myfun(), the same list is used, and the changes made in previous calls (like appending 100) will carry over.

Solution: If you want a new list for every function call, the proper way is to set the default to None and initialize the list inside the function.
'''

# del param

def myfun(param=[]):
    param.append(100)
    print(param)

myfun()
myfun()
myfun()

#Why this doens't work?
# myfun()
# del param
# myfun()
# del param
# myfun()
# del param

#%%
#Make a copy of the mutable object (Use the variable explorer)
def myfun(x):
    x+=[100]
    print(x)

param=[10]
temp=list.copy(param); #What happens if we do temp=param?
#now there are two different lists in memory:
#   param → [10]
#   temp  → [10]    

#When you call myfun(temp), the function parameter x points to the same object as temp.
#Why?  because when you call a function in Python, the variable name you pass ( temp) doesn’t get copied — instead, the reference to the object that the variable points to is passed. So inside the function, the parameter (x) becomes a new name for the same objec
#So temp becomes [10, 100], and you print that.
myfun(temp); 
myfun(temp)
myfun(temp)
print(temp) #temp was modified

print(param) #But param did not change

#%%
#using None as default

print('\nCalling myfun *with* using the None object:')
def myfun(param=None):
   if param is None:
        param = []
   param.append(100)
   print(param)

myfun()
myfun()
myfun()

#%%

print('\nCalling myfun *without* using None:')
#Comapre the results to when None is not used
def myfun(param=[]):
   if param is None:
        param = []
   param.append(200)
   print(param)

myfun()
myfun()
myfun()

#%% Return values

#Returning values - the plain case
def calcFunc(x):
    y=2*x*x + 4*x
    return(y)
    
print(calcFunc(5))



#%%
#Returning values - multiple returns
def calcFunc(x):
    y=2*x + 4*x
    if y>0:
        return 'Positive'
    elif y<=0:
        return 'Negative'
    return
    
    print('End of function')
    
print(calcFunc(5))
print(calcFunc(-5))
print(calcFunc(0))

#%% Reverse transcribe a DNA sequence - Exercise

#SOLUTION IS AT THE END OF THIS SCRIPT

#%% Variable scope: local and global variables

def mathfunc(x, y):
   z = (x+y)*(x-y) #z is defined locally
   return z

answer = mathfunc(6,5)
print(answer) #11
#print(z) #fails, z is not defined outside of the function

#%%
#Understanding variable scope: Local
a = 100 #This is a global variable

def mathfunc(x, y):
    print('printing a: ', a) #This worked, it could see it
#    a+=10 #returns an error, why? Not a local var
#    z = x + y + a #z is a local variable
#    return z

print(mathfunc(5,6)) 
#print(z)

#%%
#Variable scope: Global
a = 100 #This is a global variable
print(a)

def mathfunc(x, y):
    global a #Now its moidifable in the function
    a+=50 #Now it can be modified
    print(a)
    z = x + y + a
    return z

print(mathfunc(5,6)) 
print(a)
print(z)

#%% Nested functions

#the nested printer() function accesses the non-local msg variable of the enclosing function

def print_msg(msg):
    # This is the outer enclosing function

    def printer():
        # This is the nested function
        print(msg)

    printer()

# We execute the function
# Output: Hello
print_msg("Hello from printers")

#%%
#Nested functions – a more complex example
'''
The trick in this quesiotn is to understand two things:
    1. return num2 - this is not an activation of num2, it returns an access to it.
    2. You just put a function in res. So, when you call res, you call num2
'''

def num1(x):
   print('In num1')
   
   def num2(y):
      print('In num2')
      print(x*y)
      return (x * y)
   
   print('Returning num2')
   return num2

#When you call res = num1(10), it executes num1(10), setting x to 10 and returning the num2 function (not executing it yet). Thus, res now holds a reference to num2.
res = num1(10); 
print(res); #res is a function

#When you later call res(2), you are executing num2 with y set to 2. This triggers the print statements within num2, calculating 10 * 2 (since x is still accessible due to closure) and outputting the result.

#How does it know x? The returned function num2 retains access to x because it was defined within the same scope itself.
res(2) #20

#what evidence do wehave that python remembers x?
print(res.__closure__)           # shows the closure tuple
print(res.__closure__[0].cell_contents)  # prints what x is storing


#Now let's modify X
res = num1(2); 
res(3) #6

print(res.__closure__)           # shows the closure tuple
print(res.__closure__[0].cell_contents)  # prints what x is storing


#%% Optional topics:
    
#Anonymous arguments
def testFun(item, *nonsense_args, **nonsense_kw):
    print('This funciton takes only:', item)

#%%
def testFun(item, *args, **kw):
    print('Mandatory argument:', item)
    print('Unnamed argument:', args)
    print('Keywod argument:', kw)

testFun('Hello', 1, 'Temp', 99, valueA='ABC', valueB=7)
testFun('Hello world')


#%%
#Recursion
def tri_recursion(k):
  if(k > 0):
    #1) 6 +   tri_recursion(6 - 1) -> 6+15=21
        #2) 5 +   tri_recursion(5 - 1) -> 5+10=15
            #3) 4 +   tri_recursion(4 - 1) -> 4+6=10
                #4) 3 +   tri_recursion(3 - 1) -> 3+3=6
                    #5) 2 +   tri_recursion(2 - 1) -> 2+1=3
                        #6) 1 +   tri_recursion(1 - 1) -> 1+0=1
    result = k + tri_recursion(k - 1)
    print(result) 
  else:
    result = 0
  return result

print("\n\nRecursion Example Results")
tri_recursion(6)

#%%
#Lanbda - example 1
cube=lambda x: x*x*x
print(cube(3)) #27

#This is the same as:
def cube(x):
    return x*x*x
print(cube(3)) #27

#%%
#A useful usage of lambda is to pass functions without activating them. 
#You can use the same function (myFunc) to both double and triple a number.

#Lanbda - example 2
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))

            
#%% SOLUTION TO EXERCISE: Reverse transcribe a DNA sequence

def reverseComplement(sequence, isDNA=True):
    
    if isDNA:
        sequence = sequence.replace('U', 'T')
        transTable = sequence.maketrans('ATGC', 'TACG')
    else:
        sequence = sequence.replace('T', 'U')
        transTable = sequence.maketrans('AUGC', 'UACG')
        
    complement = sequence.translate(transTable)
    reverseComp = complement[::-1]
    
    return reverseComp

#Main code
seq1='GATTACA'
seq2='GAUUGCU'

print(reverseComplement(seq1))
print(reverseComplement(seq1, isDNA=False))
print(reverseComplement(seq2, False))

#%% Exercise Birthday
# Write a function that asks about one’s birthday. If this is the current data, it prints “Happy birthday!” Otherwise, it prints “not today”

from datetime import date
today = date.today()
print("Today's date:", today)

today = str(today)
today = today[5:10];

input_date = input('When is your borthday (mm-dd): ')

if today == input_date:
    print("Happy birthday")
else:
    print ("Not today")
    

