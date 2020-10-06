#-----------------------------------------------------------|
# Reciever code                                             |
# Version: v0.0.3                                           |
# Authors: Aslak J. Strand & Sindre Wæringsaasen            |
#                                                           |
#                                                           |
# Build notes:                                              |
# 0.0.1: Main code w/ basic functions                       |
#        Recieve least significant bit first                |
#        Group 8 bits at a time, decode to ASCII character  |
#        Add new character to end of message string         |
#        Check for end of transmission bit-code             |
#        Present recieved message on screen                 |
#                                                           |
# 0.0.2: Added commentary to easier visualize code          |
#        Moved idle/wait to seperate function               |
#                                                           |
# 0.0.3: Added functionabillity to automaticly sync speed   |
#            from transmitter                               |
#                                                           |
#-----------------------------------------------------------|

# Code starts at bottom****


# Main-function start---------------------------------------
def main():
    txtString = ""        # Reset message string
    #recieveSpeed = syncTransmission()     # Sync recieve speed with transmitter (optional)
    recieveSpeed = 0.5    # Initialize recieveSpeed (change to correspond with transmitter)
    
    while True:
        binValue = ''         # Reset binary value
        bits = ''             # Reset 8 bit binary group
        bitNumber=1           # Reset binary group position
        
        idleWait(recieveSpeed)                # Starting program, waiting for sync with sender
    
        # Collecting 8 bits at a time
        # If laser is on => bit value = 1, else bit value = 0
        # Generates string of 8 bits:
        #    ie.: 01001011
        # LSB recieved first, adds next bit in front of old bits
        while bitNumber <= 8:
            if reciever.is_pressed:        # Laser ON
                binValue = '1'
            elif not reciever.is_pressed:  # Laser OFF
                binValue = '0'
            bits = binValue + bits         # Adding new bit in front
            print(bits)                    # Printing current bit-string
            bitNumber = bitNumber+1        # Increment binary group position
            sleep(recieveSpeed)            # Hold for next bit
        
        # Checking for End Of Transmission (EOT):
        # EOT value: '0000 0100'
        # If EOT => print full message, else add next character to string
        # If EOT => choose to restart or exit program
        if (bits == '00000100'):
            txtString = txtString
            print("End of transmission. \nYour message: " + txtString)
            eof = input("Press enter to restart or <<end>> to exit: ")
            if (eof == 'end'):
                quit()
            else:
                txtString = ''
        else:
            txtString = txtString + bitsToChar(bits)  # Add new character to string, conversion from bin to ASCII in bitsToChar-function
            print(txtString)
        
        
# TransmissionSpeed-function start--------------------------
def syncTransmission():
    # Sync transmission speed with transmitter
    syncNmbr = 0      # reset sync-loop value
    timeStart = 0.0   # reset sync-start time
    timeStop = 0.0    # reset sync-stop time
    syncTime = 0.0    # reset sync time
    
    # Waiting for laser to turn ON
    while not reciever.is_pressed:
        if ((syncNmbr/100000.0).is_integer() or syncNmbr == 0):
            print("Waiting to start speed-sync")
        syncNmbr = syncNmbr + 1
    syncNmbr = 0
    
    # If laser turned ON => log timestamp
    if reciever.is_pressed:
        timeStart = time.time()
        
    # Wait for laser to turn OFF
    # When laser is OFF => log timestamp
    while reciever.is_pressed:
        if ((syncNmbr/100000.0).is_integer() or syncNmbr == 0):
            print("Waiting to complete speed-sync")
        syncNmbr = syncNmbr + 1
    timeStop = time.time()   
    
    # Print timing info
    # Return (stoptime - starttime) as a float digit with 5 decimals
    print("start: {0} \nstop: {1} \ntime: {2}".format(timeStart, timeStop, round((timeStop-timeStart), 5)))
    return round((float(timeStop - timeStart)), 5)
    
    
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
    sleep(recieveSpeed + (recieveSpeed/1.5))
    
    
    
# BitsToChar-function start---------------------------------     
def bitsToChar(bitString = None):
    # Recieve bits from main code
    # Convert 8bit group to ASCII
    # Return ASCII character
    return chr(int(bitString, 2))



# START-----------------------------------------------------

from gpiozero import Button   # dling gpiozero button library for input pin
import time                   # dling time library for time-management
from time import sleep        # dling sleep library for hold commands
import os                     # dling os library for control functions
reciever = Button(2)          # Initialize GPIO pin 2 as input

main()  # go to main-function
