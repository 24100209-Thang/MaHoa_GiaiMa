import string
import random
import hashlib
from collections import Counter

ALPHABET = string.ascii_uppercase
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"  # thu tu tan suat tieng Anh giam dan


# 1. MA CAESAR
def caesar_encrypt(text: str, k: int) -> str:
    """C = (P + k) mod 26"""
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + k) % 26 + base))
        else:
            result.append(c)
    return "".join(result)


def caesar_decrypt(text: str, k: int) -> str:
    """P = (C - k) mod 26"""
    return caesar_encrypt(text, -k)


def caesar_brute_force(cipher: str) -> list[tuple[int, str]]:
    """Thu tat ca 25 khoa (k = 1..25), tra ve danh sach (k, ban ro)."""
    return [(k, caesar_decrypt(cipher, k)) for k in range(1, 26)]


# 2. MONOALPHABETIC CIPHER (ma thay the don bang)
def mono_generate_key(seed: int | None = None) -> dict[str, str]:
    """Tao bang thay the ngau nhien 26 chu cai, khong trung lap."""
    rng = random.Random(seed)
    shuffled = list(ALPHABET)
    rng.shuffle(shuffled)
    # dam bao khong anh xa chu cai thanh chinh no (de tranh ban ro lo ra)
    while any(a == b for a, b in zip(ALPHABET, shuffled)):
        rng.shuffle(shuffled)
    return dict(zip(ALPHABET, shuffled))


def mono_encrypt(text: str, key: dict[str, str]) -> str:
    return "".join(key.get(c, c) for c in text.upper())


def mono_decrypt(text: str, key: dict[str, str]) -> str:
    inverse = {v: k for k, v in key.items()}
    return "".join(inverse.get(c, c) for c in text.upper())


def mono_frequency(cipher: str) -> list[tuple[str, int]]:
    """Dem tan suat chu cai trong ban ma, sap xep giam dan."""
    counts = Counter(c for c in cipher.upper() if c.isalpha())
    return counts.most_common()


def mono_guess_mapping(cipher: str) -> dict[str, str]:
    """Phan tich tan suat: gan chu cai hay gap nhat trong ban ma voi chu cai hay gap nhat tieng Anh."""
    ranked = [c for c, _ in mono_frequency(cipher)]
    return {c: p for c, p in zip(ranked, ENGLISH_FREQ_ORDER)}


# 3. VIGENERE
def vigenere_encrypt(text: str, key: str) -> str:
    """C = (P + K) mod 26, K lap lai theo tu khoa. Ky tu khong phai chu giu nguyen."""
    key = key.upper()
    out, j = [], 0
    for c in text.upper():
        if c.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            out.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
            j += 1
        else:
            out.append(c)
    return "".join(out)


def vigenere_decrypt(text: str, key: str) -> str:
    """P = (C - K) mod 26"""
    key = key.upper()
    out, j = [], 0
    for c in text.upper():
        if c.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            out.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            j += 1
        else:
            out.append(c)
    return "".join(out)


# 4. AFFINE
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a: int, m: int) -> int | None:
    """Nghich dao modulo: a * x = 1 (mod m). Tra ve None neu khong ton tai."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def affine_valid_a(a: int) -> bool:
    """a hop le khi gcd(a, 26) = 1."""
    return gcd(a, 26) == 1


def affine_encrypt(text: str, a: int, b: int) -> str:
    """C = (a*P + b) mod 26"""
    if not affine_valid_a(a):
        raise ValueError("a phai nguyen to cung nhau voi 26")
    out = []
    for c in text.upper():
        if c.isalpha():
            x = ord(c) - ord('A')
            out.append(chr((a * x + b) % 26 + ord('A')))
        else:
            out.append(c)
    return "".join(out)


def affine_decrypt(text: str, a: int, b: int) -> str:
    """P = a^-1 * (C - b) mod 26"""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("a khong co nghich dao modulo 26")
    out = []
    for c in text.upper():
        if c.isalpha():
            y = ord(c) - ord('A')
            out.append(chr((a_inv * (y - b)) % 26 + ord('A')))
        else:
            out.append(c)
    return "".join(out)


def affine_all_keys() -> list[tuple[int, int]]:
    """Tat ca cap khoa (a, b) hop le: 12 * 26 = 312 kha nang."""
    return [(a, b) for a in range(1, 26) if affine_valid_a(a) for b in range(26)]


# 5. DES (dung pycryptodome, dung che do ECB nhu tai lieu)
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad


def des_encrypt(plaintext: bytes, key8: bytes) -> bytes:
    """key8: 8 byte (64 bit, trong do 8 bit kiem tra parity)."""
    cipher = DES.new(key8, DES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, DES.block_size))


def des_decrypt(ciphertext: bytes, key8: bytes) -> bytes:
    cipher = DES.new(key8, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)


# 6. AES (AES-128, khuyen dung CBC thay vi ECB)
def aes_encrypt(plaintext: bytes, key16: bytes) -> tuple[bytes, bytes]:
    """Tra ve (iv, ciphertext). Dung CBC voi IV ngau nhien."""
    iv = AES.get_random_bytes(16)
    cipher = AES.new(key16, AES.MODE_CBC, iv)
    return iv, cipher.encrypt(pad(plaintext, AES.block_size))


def aes_decrypt(iv: bytes, ciphertext: bytes, key16: bytes) -> bytes:
    cipher = AES.new(key16, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


def aes_encrypt_ecb(plaintext: bytes, key16: bytes) -> bytes:
    """Chi de dong bo voi tai lieu thuc hanh. Khong dung ECB trong thuc te."""
    cipher = AES.new(key16, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, AES.block_size))


# 7. RSA (textbook, so nho de hieu nguyen ly)
def rsa_toy_keygen(p: int, q: int, e: int = 3):
    """Tra ve ((e, n), (d, n)) voi p, q nguyen to nho."""
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("e phai nguyen to cung nhau voi phi(n)")
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt_int(m: int, public_key) -> int:
    e, n = public_key
    return pow(m, e, n)


def rsa_decrypt_int(c: int, private_key) -> int:
    d, n = private_key
    return pow(c, d, n)


def text_to_numbers(text: str) -> list[int]:
    """A=0, B=1, ..."""
    return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]


def numbers_to_text(nums: list[int]) -> str:
    return "".join(chr(n + ord('A')) for n in nums)


def rsa_keygen_2048():
    """Sinh khoa RSA that (n ~ 2048 bit) de dung cho chu ky so."""
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)
    return key.e, key.n, key.d


# 8. HASH: MD5, SHA-1, SHA-256
def md5_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def sha1_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha1(data).hexdigest()


def sha256_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def hamming_distance_hex(h1: str, h2: str) -> int:
    """So bit khac nhau giua hai chuoi hash (de quan sat hieu ung tuyet lo)."""
    return bin(int(h1, 16) ^ int(h2, 16)).count("1")


# 9. CHU KY SO RSA-SHA256 (textbook theo tai lieu)
#    S = H(M)^d mod n ; xac thuc: H(M) == S^e mod n
def sign_message(message: str, d: int, n: int) -> int:
    h = int(sha256_hex(message), 16) % n
    return pow(h, d, n)


def verify_signature(message: str, signature: int, e: int, n: int) -> bool:
    h1 = int(sha256_hex(message), 16) % n
    h2 = pow(signature, e, n)
    return h1 == h2



# DEMO
def _demo():
    print("=" * 60)
    print("1. CAESAR")
    c = caesar_encrypt("HELLO WORLD", 3)
    print("Ma hoa:", c, "| Giai ma:", caesar_decrypt(c, 3))
    print("Brute force (5 ket qua dau):", caesar_brute_force(c)[:5])

    print("=" * 60)
    print("2. MONOALPHABETIC")
    key = mono_generate_key(seed=42)
    c = mono_encrypt("HELLO WORLD", key)
    print("Ban ma:", c, "| Giai ma:", mono_decrypt(c, key))
    print("Tan suat:", mono_frequency(c)[:5])

    print("=" * 60)
    print("3. VIGENERE")
    c = vigenere_encrypt("HELLO", "KEY")
    print("Ma hoa:", c, "| Giai ma:", vigenere_decrypt(c, "KEY"))

    print("=" * 60)
    print("4. AFFINE")
    c = affine_encrypt("HELLO", 5, 8)
    print("Ma hoa:", c, "| Giai ma:", affine_decrypt(c, 5, 8))

    print("=" * 60)
    print("5. DES (ECB)")
    k = b"8bytekey"
    c = des_encrypt(b"HELLO123", k)
    print("Ma hoa:", c.hex(), "| Giai ma:", des_decrypt(c, k))

    print("=" * 60)
    print("6. AES-128 (CBC)")
    k = b"1234567890123456"
    iv, c = aes_encrypt(b"HELLO AES 1234", k)
    print("Ma hoa:", c.hex(), "| Giai ma:", aes_decrypt(iv, c, k))

    print("=" * 60)
    print("7. RSA (toy: p=3, q=11, e=3)")
    pub, priv = rsa_toy_keygen(3, 11, 3)
    print("Public:", pub, "| Private:", priv)
    c = rsa_encrypt_int(4, pub)
    print("M=4 -> C=", c, "-> giai ma:", rsa_decrypt_int(c, priv))

    print("=" * 60)
    print("8. HASH")
    for f in (md5_hex, sha1_hex, sha256_hex):
        print(f.__name__, f("HELLO"), "|", f("HELLO!"))
    print("Hamming MD5 'HELLO' vs 'HELLO!':",
          hamming_distance_hex(md5_hex("HELLO"), md5_hex("HELLO!")), "bit khac")

    print("=" * 60)
    print("9. CHU KY SO RSA-SHA256 (2048 bit)")
    e, n, d = rsa_keygen_2048()
    msg = "Xin chao RSA"
    sig = sign_message(msg, d, n)
    print("Hop le:", verify_signature(msg, sig, e, n))
    print("Thong diep bi sua -> hop le:", verify_signature(msg + "!", sig, e, n))


if __name__ == "__main__":
    _demo()
