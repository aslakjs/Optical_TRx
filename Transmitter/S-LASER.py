#-----------------------------------------------------------|
# Transmitter code                                          |
# Version: v0.0.2                                           |
# Authors: Aslak J. Strand & Sindre Wæringsaasen            |
#                                                           |
#                                                           |
# Build notes:                                              |
# 0.0.1: Main code w/ basic functions                       |
#        Convert string of text to 8bit binary              |
#        Transmit each character as 8bit groups             |
#        Added End Of Transmission code at end of message   |
#        Added functionabillity for test-button for easy    |
#             allignment of transmitter and reciever        |
#        Added idle/start code to sync reciever             |
#        Added text input for customized messages           |
#                                                           |
# 0.0.2: Added commentary for easy visualization of code    |
#        Added message for succesfull transmission          |
#        Fixed issue with testing laser after transmission  |
#        Added functionabillity to cancel transmission by   |
#             running test button durig transmission        |
#                                                           |
#-----------------------------------------------------------|

# Code starts at bottom****

# Main-function start---------------------------------------
def main():
    testLaser = Button(2)    # Initialize GPIO pin 2 as input
    
    # Check for test-button
    # If button = pressed, transmit constant high value
    while testLaser.is_pressed:
        transmit("1")
    
    sendData = inputMessage()  # Input custom message
    
    # Check for exit-command
    # If NOT exit => check for test command
    # If test command => transmit constant high untill button is pressed
    #    When button is pressed => input new message
    # Else continue to transmitt message
    while not sendData == "exit":
        if sendData == "test":
            while sendData == "test":
                while not testLaser.is_pressed:
                    transmit("1")
                sendData = inputMessage()
        
        
        # If new input = exit => quit program   
        if sendData == "exit":
            quit()
        
        
        # If input NOT = test => continue
        # Get length of string
        while not sendData == "test":
            sDataLength = len(sendData)
            
            # Format string to 8 bit binary string:
            #    ie.: '00101101 01100101 ...'
            binSData = (' '.join(format(ord(x), 'b').zfill(8) for x in sendData))
            
            # Split string into array of 8bit groups:
            #    ie.: [00101101, 01100101, ...]
            # Print array
            sDataArray = binSData.split()
            print(sDataArray)
            
            idleStart()   #Sync reciever
            
            breakTest = False              # Initiate testvariable for test-functions
            # Transmit all characters, one by one
            # Start with first character, end with final (length of string)
            for i in range(0, sDataLength):
                # Transmit each bit value from current character (8 bits)
                # "[::-1] = start with bit#8 (Least Significant Bit),
                #           then bit#7 ...
                #           end with bit#1 (Most Significant Bit)
                # Check for test-button:
                #    If test-button is pressed => transmit constant high, and cancel original transmission
                for bin in sDataArray[i][::-1]:
                    if testLaser.is_pressed:
                        while testLaser.is_pressed:
                            transmit("1")  # Transmit constant high
                        transmit("0")      # When button is unpressed => turn off laser
                        breakTest = True   # Initializing breakout logic
                        break              # Cancel current transmission
                    else:
                        transmit(bin)      # Transmit current binary value
                        
                if breakTest == True:      # If test-button has been used => Break from next loop
                    break
                
                idleStart()   #Sync reciever for next character
                
                
            # Check if test-button has been used
            # If not => continue to EOT
            if not breakTest == True:
                # At end of message transmission, send End Of Transmission (EOT)
                # EOT value = 0000 0100
                # When recieved at reciever, this will stop the program and present the message previously sent
                eotArray = ['00000100']
                eotLength = len(eotArray)
                for e in range(0, eotLength):
                    for eotBin in eotArray[e][::-1]:
                        transmit(eotBin)
                
                # Print info regarding transmission
                # Input next message
                # If new input = exit => quit program
                print("\n\nMessage sent succesfully \nPrevious message: {0}\n\nNext message:".format(sendData))
                sendData = inputMessage()   
                if sendData == "exit":
                    quit()
            
            # If test-button has been used => print info, ask for new input
            elif breakTest == True:
                print("\n\nTransmission halted, test-button has been used\nUnsuccesfull message: {0}\n\nNext message:".format(sendData))
                breakTest = False
                sendData = inputMessage()
                if sendData == "exit":
                    quit()


# Input-function start--------------------------------------
def inputMessage():
    # Print input info
    # Return input
    print("[test] - turn on laser  --  [exit] - exit program")
    return input("Enter your message: ")


# TransmissionSpeed-function start--------------------------
def syncTransmission():
    # Sync transmission speed with reciever
    
    print("Transmit speed: {0}\n".format(transmitSpeed))
    
    
    

# Wait-function start---------------------------------------
def idleStart():
    # Sync transmitter and reciever
    # Starts with high pulse for 4times transmitSpeed
    # Then low pulse for 1.5times transmitSpeed
    
    print("\n sync \n")   # Print "sync" to show process
    
    idleWait = (transmitSpeed*4)   # Initialize idleWait speed = 4times transmitSpeed
    idleLaser = LED(17)            # Initialize GPIO pin 17 as output
    
    idleLaser.off()        # Laser OFF
    sleep(transmitSpeed)   # Hold
    idleLaser.on()         # Laser ON
    sleep(idleWait)        # Hold
    idleLaser.off()        # Laser OFF
    sleep(transmitSpeed + (transmitSpeed/2))   # Hold before transmission
    

# Transmission-function start---------------------------------------
def transmit(sendBit):
    # Transmit data via laser
    # Test each bit before turning laser ON or OFF
    
    laser = LED(17)   # Initialize GPIO pin 17 as output
    print(sendBit)    # Print current bit value
    
    # If current bit = 1, turn ON laser
    if (sendBit == "1"):
        laser.on()
        sleep(transmitSpeed) # Hold before next bit
        return               # Return to main-function
    
    # If current bit = 0, turn OFF laser
    if (sendBit == "0"):
        laser.off()
        sleep(transmitSpeed) # Hold before next bit
        return               # Return to main function




# START-----------------------------------------------------

from gpiozero import LED       # dling gpiozero LED library for output pin
from gpiozero import Button    # dling gpiozero button library for input pin
from time import sleep         # dling sleep library for time-management
transmitSpeed = 0.01            # Globaly initalize transmitSpeed for all functions

main()   # Go to main-function
