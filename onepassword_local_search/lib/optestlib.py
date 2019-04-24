#
# David Schuetz
# November 2018
#
# https://github.com/dschuetz/1password
#
# Library of functions called by all the other tools here.
#

from Cryptodome.Cipher import AES
from sys import exit as sys_exit
from base64 import b64decode as base64_b64decode
from binascii import a2b_hex as binascii_a2b_hex

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# basic crypto stuff - wrappers around PyCryptoDome, etc.
#
# * encrypt/decrypt AES-GCM with 128-bit GCM tag
# * encrypt/decrypt AES-CBC with HMAC-SHA256 tag
# * encrypt/decrypt 1Password "opdata" structure 
#   * AES-CBC with HS-256 tag
#
# All use 256-bit keys
#
# Should probably pull RSA stuff out of the other scripts
# and add them here. 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#
# Decrypt CT with AES-GCM using key and iv
#   * If iv not provided, one will be created
#   * Verifies GCM tag 
#     - if verification fails, program will terminate with error
#   * Length of GCM tag hard-coded to 16 bytes
#
def dec_aes_gcm(ct, key, iv, tag):
    C = AES.new(key, AES.MODE_GCM, iv, mac_len=16)
    PT = C.decrypt_and_verify(ct, tag)

    return PT


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
#
# Convenience functions for input/output
#
# * opb64d, opb64e - base64 decode with 1Password tricks
#    (URL safe altchars, not always including == padding, etc.)
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


#
# The strings stored by 1Password don't always have padding characters at the
#   end. So we try multiple times until we get a good result.
#
# Also, 1Password uses url-safe encoding with - and _ replacing + and /.
#
def opb64d(b64dat):
    try:
        out = base64_b64decode(b64dat, altchars='-_')
    except:
        try:
            out = base64_b64decode(b64dat + '=', altchars='-_')
        except:
            try:
                out = base64_b64decode(b64dat + '==', altchars='-_')
            except:
                print("Problem b64 decoding string: %s" % (b64dat))
                sys_exit(1)
    return out


def get_binary_from_string(str):
    try:
        bin = binascii_a2b_hex(str)
    except:
        try:
            bin = opb64d(str)
        except:
            try:
                bin = base64_b64decode(str)
            except:
                print("Unable to decode the input. Enter in hex or base64_")
                sys_exit(1)
    return bin