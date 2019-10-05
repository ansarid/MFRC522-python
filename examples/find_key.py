#!/usr/bin/env python
import sys
from mfrc522 import SimpleMFRC522

KEYCHAIN = [
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
    [0x00, 0x11, 0x22, 0x33, 0x44, 0x55],
    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05],
    [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5],
    [0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5],
    [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
    [0xBB, 0xBB, 0xBB, 0xBB, 0xBB, 0xBB],
    [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF],
    [0XD3, 0XF7, 0XD3, 0XF7, 0XD3, 0XF7],
    [0XB0, 0XB1, 0XB2, 0XB3, 0XB4, 0XB5],
    [0X4D, 0X3A, 0X99, 0XC3, 0X51, 0XDD],
    [0X1A, 0X98, 0X2C, 0X7E, 0X45, 0X9A],
    [0X00, 0X00, 0X00, 0X00, 0X00, 0X00],
    [0XAB, 0XCD, 0XEF, 0X12, 0X34, 0X56]
]

reader = SimpleMFRC522()

print("Hold a tag near the reader")

for KEY in KEYCHAIN:

    SimpleMFRC522.KEY = KEY
    # KEY = [0XD3,0XF7,0XD3,0XF7,0XD3,0XF7]

    data = reader.read()


    if data[1] == "AUTH_ERROR":
        pass
    else:
        print("Found", KEY)
        exit()

print("Unable to find key!")