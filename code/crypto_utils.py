import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class AES256FileEncryptor:
    def __init__(self, password: str):
        # Password se 256-bit key derive karo
        self.key = hashlib.sha256(password.encode()).digest()
        
    def encrypt_file(self, input_path: str, output_path: str):
        """File encrypt karo AES-256-CBC se"""
        iv = os.urandom(16)
        
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        
        # IV + ciphertext save karo
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
        
        original_size = len(plaintext)
        encrypted_size = len(iv + ciphertext)
        
        print(f"[+] Encrypted: {input_path}")
        print(f"[+] Output: {output_path}")
        print(f"[+] Algorithm: AES-256-CBC")
        print(f"[+] Original size: {original_size} bytes")
        print(f"[+] Encrypted size: {encrypted_size} bytes")
        print(f"[+] IV: {base64.b64encode(iv).decode()}")
        return True
        
    def decrypt_file(self, input_path: str, output_path: str):
        """File decrypt karo"""
        with open(input_path, 'rb') as f:
            data = f.read()
        
        iv = data[:16]
        ciphertext = data[16:]
        
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        
        print(f"[+] Decrypted: {input_path}")
        print(f"[+] Output: {output_path}")
        print(f"[+] Decryption: SUCCESS")
        return True
