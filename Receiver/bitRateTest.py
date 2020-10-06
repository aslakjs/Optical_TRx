#-----------------------------------------------------------|
# Bitrate test code                                         |
# Version: v0.0.2                                           |
# Authors: Aslak J. Strand & Sindre Wæringsaasen            |
#                                                           |
#                                                           |
# Build notes:                                              |
# 0.0.1: Main code w/ basic test function                   |
#        Add recieved bits in array                         |
#        Check for faulty bits                              |
#        (ie. bits not following basic 1-0-1-0.. pattern    |
#        Result given as successrate percentage             |
#                                                           |
# 0.0.2: Moved idle/wait code to own function               |
#        Added commentary to easier visualize code          |
#                                                           |
#-----------------------------------------------------------|

# Code starts at bottom****


# Main-function start---------------------------------------
def main():
    
    while True:                # infinite loop to restart test w/o restarting program
        faultBits = 0   # reset number of faulty bits
        y = 1           # reset y-loop-variable
        t = 1           # reset t-loop-variable
        
        # input vaiables below:
        recieveSpeed = float(input("Enter your reciever speed [s] : ")) 
        numberOfBits = int(input("Number of bits to recieve: "))
        startTest = input("Start test? [y]-yes / [n]-no / [e]-exit: ")
        
        
        # if startTest = exit -> quit program
        if startTest == "e" or startTest == "exit":
            quit()      
        
        
        rArray = numpy.zeros((2,numberOfBits))    # reset bit array with "numberOfBits" collumns and 2 rows, all zeroes
        
        
        # check for start / stop command -- (stop resets program and new input required)
        if startTest == "n" or startTest == "N":
            break
            
        elif startTest == "y" or startTest == "Y":
            idleWait(recieveSpeed) # starting program, waiting for sync with sender
                
            
            # START RECIEVEING
            # adding recieved bit-value to corresponding spot in array:
            # ------------------------------
            # | bit#: 1, 2, 3, 4, 5, 6, ...|
            # |value: 1, 0, 1, 0, 1, 0, ...|
            # ------------------------------
            # prints recieved bits during transmission AND full array at end of transmission
            while y <= numberOfBits:
                print("Bit {0} of {1}".format(y, numberOfBits))
                rArray[0, y-1] = y
                
                if reciever.is_pressed:
                    print("1")
                    rArray[1, y-1] = 1
                else:
                    print("0")
                    rArray[1, y-1] = 0
                    
                sleep(recieveSpeed)
                y = y+1
            
            print(rArray)
            
            
            # PROCESS ARRAY
            # checks if current value is equal to previous value
            # if equal, mistakes have been made => increment faultyBits
            # if not equal (ie. value-1 = 0, value = 1) then asume correct transmission, check next value
            # at end of array, calculate successRate as percentage
            while t < numberOfBits:
                if rArray[1,t-1] == rArray[1,t]:
                    faultBits = faultBits + 1
                t = t+1
            successRate = (((numberOfBits - faultBits)/numberOfBits)*100) 
            
            
            # Print result:
            # Ask for restart
            # Check for restart command
            print("\n\n{0} faulty bit(s) at speed = {1}\n{2} of {3} bits recieved\nSuccessrate of {4}%".format(faultBits, recieveSpeed, y-1, numberOfBits, successRate))
            startTest = input("\n\nrestart test? [y]-yes / [n] or [e]-exit: ")
            if startTest == "e" or startTest == "exit" or startTest == "n" or startTest == "no":
                quit()
               
               
# Wait-function start---------------------------------------
def idleWait(recieveSpeed):
    msgNmbr = 0       #reset idle-loop value
    wait4start = 0    #reset start-loop value
    
    # Waiting for idle/mark bit
    # Print waiting-message @ every 100 000 runthrough
    while not reciever.is_pressed:
        if ((msgNmbr/100000.0).is_integer() or msgNmbr == 0):
            print("Waiting for idle/mark bits")
        msgNmbr = msgNmbr + 1
    msgNmbr = 0
    
    
    # Waiting for start bit
    # Print waiting-message @ every 100 000 runthrough
    while reciever.is_pressed:
        if ((wait4start/100000.0).is_integer() or wait4start == 0):
            print("Waiting for start bit")
        wait4start = wait4start + 1
    wait4start = 0
    
    # Hold-on before transmission start
    sleep(recieveSpeed + (recieveSpeed/2))
    
    
    
#-----START-------------------------------------------------
from gpiozero import Button   # dling gpiozero button library for input pin
from time import sleep        # dling sleep library for time-management
import os                     # dling os library for control functions
import numpy                  # dling numpy library for array control
reciever = Button(2)          #initiate GPIO pin 2 as input for signal

main()  # go to main-function
