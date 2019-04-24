#
# From work of David Schuetz and Joël Franusic
# https://github.com/dschuetz/1password
# https://github.com/jpf/okta-jwks-to-pem

from sys import exit as sys_exit
from base64 import b64decode as base64_b64decode, urlsafe_b64decode
from binascii import a2b_hex as binascii_a2b_hex
from json import loads as json_loads
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.ciphers.base import Cipher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers, RSAPrivateNumbers
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import six
import struct


def aes_decrypt(ct, key, iv, tag):
    cipher = Cipher(AES(key), GCM(iv), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize_with_tag(tag)


def intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))


def rsa_decrypt(key_raw, ct):
    jwk = json_loads(key_raw)
    public_numbers = RSAPublicNumbers(
        base64_to_long(jwk['e']),
        base64_to_long(jwk['n'])
    )
    private_numbers = RSAPrivateNumbers(
        base64_to_long(jwk['p']),
        base64_to_long(jwk['q']),
        base64_to_long(jwk['d']),
        base64_to_long(jwk['dp']),
        base64_to_long(jwk['dq']),
        base64_to_long(jwk['qi']),
        public_numbers
    )
    private_key = private_numbers.private_key(backend=default_backend())

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    decryptor = serialization.load_pem_private_key(
        pem,
        password=None,
        backend=default_backend()
    )
    plain = decryptor.decrypt(
        get_binary_from_string(ct),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return plain


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