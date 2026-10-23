# Bai 1
# def encrypt(text, k):
#     result = ""
#     for c in text:
#         if c.isalpha():
#             base = ord('A') if c.isupper() else ord('a')
#             result += chr((ord(c) - base + k) % 26 + base)
#         else:
#             result += c
#     return result

# def decrypt(text, k):
#     return encrypt(text, -k)

# text = "HELLO"
# k = 3

# cipher = encrypt(text, k)
# plain = decrypt(cipher, k)

# print("Cipher:", cipher)
# print("Decrypted:", plain)
# Bai 2
# import string
# import random

# # Tạo bảng thay thế
# letters = list(string.ascii_uppercase)
# shuffled = letters.copy()
# random.shuffle(shuffled)

# encrypt_map = dict(zip(letters, shuffled))
# decrypt_map = {v: k for k, v in encrypt_map.items()}

# def encrypt(text):
#     result = ""
#     for c in text.upper():
#         if c in encrypt_map:
#             result += encrypt_map[c]
#         else:
#             result += c
#     return result

# def decrypt(text):
#     result = ""
#     for c in text.upper():
#         if c in decrypt_map:
#             result += decrypt_map[c]
#         else:
#             result += c
#     return result

# text = "HELLO WORLD"
# cipher = encrypt(text)
# plain = decrypt(cipher)

# print("Key:", encrypt_map)
# print("Cipher:", cipher)
# print("Decrypted:", plain)
# Bai 3
# def vigenere_encrypt(text, key):
#     result = ""
#     key = key.upper()
#     j = 0
#     for c in text.upper():
#         if c.isalpha():
#             shift = ord(key[j % len(key)]) - ord('A')
#             result += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
#             j += 1
#         else:
#             result += c
#     return result
# def vigenere_decrypt(text, key):
#     result = ""
#     key = key.upper()
#     j = 0
#     for c in text.upper():
#         if c.isalpha():
#             shift = ord(key[j % len(key)]) - ord('A')
#             result += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
#             j += 1
#         else:
#             result += c
#     return result
# text = "HELLO"
# key = "KEY"
# cipher = vigenere_encrypt(text, key)
# plain = vigenere_decrypt(cipher, key)
# print("Cipher:", cipher)
# print("Decrypted:", plain)
# Bai 4
# def mod_inverse(a, m):
#     for x in range(1, m):
#         if (a * x) % m == 1:
#             return x
#     return None

# def affine_encrypt(text, a, b):
#     result = ""
#     for c in text.upper():
#         if c.isalpha():
#             x = ord(c) - ord('A')
#             result += chr((a * x + b) % 26 + ord('A'))
#         else:
#             result += c
#     return result

# def affine_decrypt(text, a, b):
#     result = ""
#     a_inv = mod_inverse(a, 26)
#     for c in text.upper():
#         if c.isalpha():
#             y = ord(c) - ord('A')
#             result += chr((a_inv * (y - b)) % 26 + ord('A'))
#         else:
#             result += c
#     return result

# text = "HELLO"
# a, b = 5, 8

# cipher = affine_encrypt(text, a, b)
# plain = affine_decrypt(cipher, a, b)

# print("Cipher:", cipher)
# print("Decrypted:", plain)
# Bai 5
# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad

# key = b'8bytekey'  # 8 bytes = 64 bits
# cipher = DES.new(key, DES.MODE_ECB)

# text = b'HELLO123'
# encrypted = cipher.encrypt(pad(text, 8))
# decrypted = unpad(cipher.decrypt(encrypted), 8)

# print("Encrypted:", encrypted)
# print("Decrypted:", decrypted)
# Bai 6
# import math

# # Tìm nghịch đảo modulo
# def mod_inverse(e, phi):
#     for d in range(1, phi):
#         if (d * e) % phi == 1:
#             return d
#     return None

# # Sinh khóa
# p, q = 3, 11
# n = p * q
# phi = (p - 1) * (q - 1)
# e = 3
# d = mod_inverse(e, phi)

# # Mã hóa
# def encrypt(m):
#     return pow(m, e, n)

# # Giải mã
# def decrypt(c):
#     return pow(c, d, n)

# m = 4
# c = encrypt(m)
# m2 = decrypt(c)

# print("Public key:", (e, n))
# print("Private key:", (d, n))
# print("Encrypted:", c)
# print("Decrypted:", m2)
# Bai 7
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad

# key = b'1234567890123456'  # 16 bytes = AES-128
# cipher = AES.new(key, AES.MODE_ECB)

# text = b'HELLO AES 1234'
# encrypted = cipher.encrypt(pad(text, 16))
# decrypted = unpad(cipher.decrypt(encrypted), 16)

# print("Encrypted:", encrypted)
# print("Decrypted:", decrypted)
# Bai 8
# import hashlib

# def md5_hash(text):
#     return hashlib.md5(text.encode()).hexdigest()

# text1 = "HELLO"
# text2 = "HELLO!"

# print("MD5 1:", md5_hash(text1))
# print("MD5 2:", md5_hash(text2))
# Bai 9
# import hashlib

# def sha1_hash(text):
#     return hashlib.sha1(text.encode()).hexdigest()

# text1 = "HELLO"
# text2 = "HELLO!"

# print("SHA-1 1:", sha1_hash(text1))
# print("SHA-1 2:", sha1_hash(text2))

