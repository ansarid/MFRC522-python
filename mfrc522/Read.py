#!/usr/bin/env python
# -*- coding: utf8 -*-

#import RPi.GPIO as GPIO
import MFRC522
import signal
import binascii


continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    exit()
    # GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    for sector in range(100):
        for key in MFRC522.MIFARE_CLASSIC_1K_KEYS:
            # Scan for cards
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            # if status == MIFAREReader.MI_OK:
            # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    data = MIFAREReader.MFRC522_Read(sector)
                    # Print sector data

                    data['data'] = data['data'].strip('][').split(', ')
                    data['data'] = [ int(x) for x in data['data'] ]

                    # data['data'] = bytes(data['data']).decode("utf-8")
                    # data['data'] = bytes(data['data']).decode("ascii")

                    # print(data)
                    # print(data['data'])
                    print("Sector:",data['sector'],"\t Data:", data['data'])
                    # print(bytes(data['data']))
                    # print(type(data['data']), data['data'])


                    # print(data,'\t ASCII:',binascii.hexlify(bytearray(data['data'])))





                    MIFAREReader.MFRC522_StopCrypto1()

                    if sector == 100:
                        exit()
