#!/usr/bin/env python
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# If this key doesnt work for you, try running find_key.py to find the key for your RFID
SimpleMFRC522.KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

try:
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(text)
    print("Written")

finally:
	exit()
