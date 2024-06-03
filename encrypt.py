from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


key = get_random_bytes(16)  # For AES-128

cipher = AES.new(key, AES.MODE_CBC)


data = b"Hello, World!"
padded_data = pad(data, AES.block_size)

ct_bytes = cipher.encrypt(padded_data)


decipher = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext = unpad(decipher.decrypt(ct_bytes), AES.block_size)
print(plaintext)