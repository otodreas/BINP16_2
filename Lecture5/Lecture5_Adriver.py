#Lecutre 5 - Driver
"""
Created on Mon Oct  9 23:59:16 2023

@author: erane
"""

#%% Our first function
#Function that takes a parameter and returns a value
def say_hi(name):
    response = 'Hello ' + name + '!'
    return response
0
#Main code    
print(say_hi("Moses"))
print(say_hi("Deborah"))

#A Driver
print(say_hi("1")) #'Hello 1!'
print(say_hi(1)) #Error
print(say_hi("1", "2")) #Error
print(say_hi(["1", "2"])) #Error
print(say_hi("1" + "2")) #Hello 12!
print(say_hi("")) #Hello !
print(say_hi()) #Error


