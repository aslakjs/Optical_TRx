#-----------------------------------------------------------|
# Bitrate test code for transmitter                         |
# Version: v0.0.1                                           |
# Authors: Aslak J. Strand & Sindre Wæringsaasen            |
#                                                           |
# Build notes:                                              |
# 0.0.1: Main code w/ basic test function                   |
#        Sends every other bits as high, and others as low  |
#        User input amount of bits and transmission speed   |
#-----------------------------------------------------------|

# Code starts at bottom****


# Main-function start---------------------------------------
def main():
    startTest = "y"     # Initialise startTest variable
    laser = LED(17)     # Initialise pin 17 as output
    while not startTest == "e":     # Check for exit command
        transmitSpeed = float(input("Enter your transmit speed [s] : "))    # User input: transmission speed
        numberOfBits = int(input("Number of bits to send: "))               # User input: number of bits to send
        startTest = input("Start test? [y]-yes / [n]-no / [e]-exit: ")      # User input: Start/Exit
        
        if startTest == "y" or startTest == "Y" or startTest == "yes" or startTest == "YES":  # Check for start
            y=1     # Initialise count variable
            
            print("\n sync \n")   # Print "sync" to show process
    
            idleWait = (transmitSpeed*4)   # Initialize idleWait speed = 4times transmitSpeed
            idleLaser = LED(17)            # Initialize GPIO pin 17 as output
    
            idleLaser.off()        # Laser OFF
            sleep(transmitSpeed)   # Hold
            idleLaser.on()         # Laser ON
            sleep(idleWait)        # Hold
            idleLaser.off()        # Laser OFF
            sleep(transmitSpeed)   # Hold before transmission
            
            
            # Run from 0 to number of bits
            # Print to see which bit currently transmitting
            while y <= numberOfBits:
                print("bit {0} of {1}".format(y, numberOfBits))
                if y % 2 == 1:                  # Check for uneven bit number
                    print("1 \n")              # If uneven bit, print 1 to signilise Laser ON
                    laser.on()                 # Turn laser ON
                    sleep(transmitSpeed)       # Hold for duration of transmit 
                elif y % 2 == 0:               # Check for even bit number
                    print("0 \n")              # If even, print 0 to signilise Laser OFF
                    laser.off()                # Turn laser OFF
                    sleep(transmitSpeed)       # Hold for duration of transmit
                y = y+1                        # Increment bit number
            laser.off()                        # End of transmission, power down laser


            # Print EOT message, ask for new test
            print("\n{0} of {1} bits sent \n\n\n".format(y-1, numberOfBits))
            startTest = input("Run new test? [y]-yes / [e]-exit: ")
        
        # Check for cancel or restart input
        elif startTest == "n" or startTest == "N" or startTest == "no" or startTest == "NO":
            print("\n\n*Restart*\n\n")

        elif startTest == "e" or startTest == "E" or startTest == "exit" or startTest == "EXIT":
            exit()


    
#-----START-------------------------------------------------
from gpiozero import LED        # dling LED framework from gpiozero
from time import sleep          # dling sleep library for time-management
from gpiozero import Button     # dling gpiozero button library for input pin

main()  # go to main-function
