#!/usr/bin/env python
import sys
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader")
    while True:
        id, text = reader.read()
        print("SN: %s \t\tData: %s" % (id,text))
except KeyboardInterrupt:
    raise
