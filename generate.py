import hashlib
import base64
from Crypto.Cipher import AES
import pathlib
from ccl_abx import AbxReader
import xml.etree.ElementTree as etree

SETTINGS_SSAID_XML = 'settings_ssaid.xml'
FORTITOKEN_DB = 'FortiToken.db'
FORTITOKEN__SHARED_PREF__NAME_XML = 'FortiToken_SharedPrefs_NAME.xml'

class InvalidDecryptionKeyError(Exception):
    pass

def unpad(s):
    return s[0:-ord(s[-1])]

def decrypt(cipher, key):
    sha256 = hashlib.sha256()
    sha256.update(bytes(key, 'utf-8'))
    digest = sha256.digest()
    iv = bytes([0] * 16)
    aes = AES.new(digest, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(base64.b64decode(cipher))
    try:
        return unpad(str(decrypted, "utf-8"))
    except UnicodeDecodeError:
        raise InvalidDecryptionKeyError("Invalid decryption key: " + key)

def get_device_id():
    with pathlib.Path(SETTINGS_SSAID_XML).open("rb") as f:
        if(f.read(len(AbxReader.MAGIC)) == AbxReader.MAGIC):
            f.seek(0)
            reader = AbxReader(f)
            doc = reader.read(is_multi_root=True)
        else:
            doc = etree.parse(SETTINGS_SSAID_XML).getroot()
    return doc.find(".//setting[@package='com.fortinet.android.ftm']").attrib['value']

def get_serial():
    prefs = etree.parse(FORTITOKEN__SHARED_PREF__NAME_XML)
    return prefs.find(".//*[@name='SerialNumberPreAndroid9']").text[11:]

def get_UUID():
    prefs = etree.parse(FORTITOKEN__SHARED_PREF__NAME_XML)
    return prefs.find(".//*[@name='UUID']").text

def get_seeds():
    if not pathlib.Path(FORTITOKEN_DB).exists():
        raise FileExistsError("No such file: '%s'" % FORTITOKEN_DB)
    import sqlite3
    con = sqlite3.connect(FORTITOKEN_DB)
    cur = con.cursor()
    res = cur.execute("SELECT name,seed FROM Account")
    return res.fetchall()

def main():
    uuid_key = get_device_id() + get_serial()
    decoded_uuid = decrypt(get_UUID(), uuid_key)
    seed_decryption_key = uuid_key + decoded_uuid
    for (name,seed) in get_seeds():
        decrypted_seed = decrypt(seed, seed_decryption_key)
        totp_secret = bytes.fromhex(decrypted_seed)
        totp_secret_encoded = str(base64.b32encode(totp_secret), "utf-8")
        print("TOTP secret for '%s': %s" % (name, totp_secret_encoded))

if __name__ == '__main__':
    main()