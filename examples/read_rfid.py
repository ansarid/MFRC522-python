#!/usr/bin/env python
import sys
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# If this key doesnt work for you, try running find_key.py to find the key for your RFID
SimpleMFRC522.KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

try:
    print("Hold a tag near the reader")
    while True:
        id, text = reader.read()
        print("SN: %s \t\tData: %s" % (id,text))
except KeyboardInterrupt:
    raise
