import hashlib
import base64
from Crypto.Cipher import AES

SEED = ''
UUID = ''
DEVICE_ID = ''

SERIAL = 'TOKENSERIALunknown'

# fill these with values explained in README.md
android_ssaid = b''
seed = b""

def unpad(s):
    return s[0:-ord(s[-1])]

def decrypt(cipher, key):
    sha256 = hashlib.sha256()
    sha256.update(bytes(key, 'utf-8'))
    digest = sha256.digest()
    iv = bytes([0] * 16)
    aes = AES.new(digest, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(base64.b64decode(cipher))
    return unpad(str(decrypted, "utf-8"))

uuid_key = DEVICE_ID + SERIAL[11:]
print("UUID KEY: %s" % uuid_key)
decoded_uuid = decrypt(UUID, uuid_key)
print("UUID: %s" % decoded_uuid)

seed_decryption_key = uuid_key + decoded_uuid
print("SEED KEY: %s" % seed_decryption_key)
decrypted_seed = decrypt(SEED, seed_decryption_key)

totp_secret = bytes.fromhex(decrypted_seed)

totp_secret_encoded = str(base64.b32encode(totp_secret), "utf-8")
print("TOTP SECRET: %s" % totp_secret_encoded)