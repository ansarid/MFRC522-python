# Code by Simon Monk https://github.com/simonmonk/

from . import MFRC522
import time
# import RPi.GPIO as GPIO

class SimpleMFRC522:

    READER = None

    # KEY = [0XD3,0XF7,0XD3,0XF7,0XD3,0XF7]
    # 160 161 162 163 164 165
    KEY = [211, 247, 211, 247, 211, 247]


    #
    # KEYCHAIN = [
    #     [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
    #     [0x00, 0x11, 0x22, 0x33, 0x44, 0x55],
    #     [0x00, 0x01, 0x02, 0x03, 0x04, 0x05],
    #     [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5],
    #     [0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5],
    #     [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
    #     [0xBB, 0xBB, 0xBB, 0xBB, 0xBB, 0xBB],
    #     [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF],
    #     [0XD3, 0XF7, 0XD3, 0XF7, 0XD3, 0XF7],
    #     [0XB0, 0XB1, 0XB2, 0XB3, 0XB4, 0XB5],
    #     [0X4D, 0X3A, 0X99, 0XC3, 0X51, 0XDD],
    #     [0X1A, 0X98, 0X2C, 0X7E, 0X45, 0X9A],
    #     [0X00, 0X00, 0X00, 0X00, 0X00, 0X00],
    #     [0XAB, 0XCD, 0XEF, 0X12, 0X34, 0X56]
    # ]

    BLOCK_ADDRS = [8, 9, 10]

    def __init__(self):
        self.READER = MFRC522()

    def read(self):
        id, text = self.read_no_block()
        while not id:
            data = self.read_no_block()
            if data == 2:
                id, text = (None, "AUTH_ERROR")
            else:
                id, text = data
        return id, text

    def read_id(self):
        id = self.read_id_no_block()
        while not id:
            id = self.read_id_no_block()
        return id

    def read_id_no_block(self):
            (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
            if status != self.READER.MI_OK:
                    return None
            (status, uid) = self.READER.MFRC522_Anticoll()
            if status != self.READER.MI_OK:
                    return None
            return self.uid_to_num(uid)

    def read_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
                return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
                return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
        data = []
        text_read = ''
        if status == self.READER.MI_OK:
                for block_num in self.BLOCK_ADDRS:
                        block = self.READER.MFRC522_Read(block_num)
                        if block:
                        		data += block
                if data:
                         text_read = ''.join(chr(i) for i in data)
        self.READER.MFRC522_StopCrypto1()
        if status == 0:
            return id, text_read
        else:
            return id, "AUTH_ERROR"

    def write(self, text):
            id, text_in = self.write_no_block(text)
            while not id:
                    id, text_in = self.write_no_block(text)
            return id, text_in

    def write_no_block(self, text):
            (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
            if status != self.READER.MI_OK:
                    return None, None
            (status, uid) = self.READER.MFRC522_Anticoll()
            if status != self.READER.MI_OK:
                    return None, None
            id = self.uid_to_num(uid)
            self.READER.MFRC522_SelectTag(uid)
            status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
            self.READER.MFRC522_Read(11)
            if status == self.READER.MI_OK:
                    data = bytearray()
                    data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
                    i = 0
                    for block_num in self.BLOCK_ADDRS:
                        self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
                        i += 1
            self.READER.MFRC522_StopCrypto1()
            if status == 0:
                return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
            else:
                return status


    def uid_to_num(self, uid):
            n = 0
            for i in range(0, 5):
                    n = n * 256 + uid[i]
            return n
