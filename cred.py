#!/usr/bin/python
#funtion to enc creds via 3des and junk... used by other scripts in this folder to get/use creds
#ex.. ASA Shared license script
from pyDes import *
import base64

def getpasswd( encstring ):
        encstring = encstring.decode('base64')
        return triple_des('CrispyW@ffl3C0n3').decrypt(encstring, padmode=PAD_PKCS5 )

def encpasswd( plaintxt ):
        ciphertext = triple_des('CrispyW@ffl3C0n3').encrypt(plaintxt, padmode=PAD_PKCS5 )
        return  ciphertext.encode('base64')