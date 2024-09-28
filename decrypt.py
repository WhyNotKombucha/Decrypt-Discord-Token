from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from regex import findall

def decrypt(buff, master_key):
    try:
        decrypted_data = AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        return decrypted_data
    except Exception as e:
        return f"An error has occurred: {str(e)}"

def get_discord_tokens():
    tokens = []
    cleaned = []
    try:
        with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local State", "r") as file:
            key = loads(file.read())['os_crypt']['encrypted_key']
        
        for file in listdir(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\"):
            if not (file.endswith(".ldb") or file.endswith(".log")):
                continue
            try:
                with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                    for line in files:
                        line.strip()
                        for value in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            tokens.append(value)
            except PermissionError:
                continue
        
        cleaned = list(set(tokens))  # Remove duplicates
        return cleaned, key
    except Exception as e:
        return [], str(e)

def main():
    askUser = input("[1] Decrypt Custom Token\n[2] Decrypt token from Discord files\n\n> ")

    if "1" in askUser:
        val = input("Encrypted Token: ")
        password = input("Password to Token: ")
        print(decrypt(b64decode(val.split('dQw4w9WgXcQ:')[1]), b64decode(password)[5:]))

    elif "2" in askUser:
        tokens, key = get_discord_tokens()
        if not tokens:
            print("No tokens found or an error occurred.")
            return
        for token in tokens:
            print(decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:]))

if __name__ == "__main__":
    main()
