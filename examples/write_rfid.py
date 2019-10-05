#!/usr/bin/env python
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(text)
    print("Written")

finally:
	exit()
