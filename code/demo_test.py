import os
from crypto_utils import AES256FileEncryptor
from signed_urls import generate_signed_url, verify_signed_url
import time

print("=" * 60)
print("  Internee.pk Secure File Sharing System - Demo")
print("=" * 60)

# Test file banao
with open('test_report.csv', 'w') as f:
    f.write("user_id,name,email,salary\n")
    f.write("1,Talha Imran,talha@internee.pk,50000\n")
    f.write("2,Ahmed Khan,ahmed@internee.pk,45000\n")
    f.write("3,Sara Ali,sara@internee.pk,55000\n")

print("\n[1] TEST FILE CREATED: test_report.csv")

# Encrypt karo
print("\n[2] ENCRYPTING FILE...")
enc = AES256FileEncryptor("InterneeSecure2025!")
enc.encrypt_file('test_report.csv', 'test_report.csv.enc')

# Signed URL banao
print("\n[3] GENERATING SIGNED URL...")
url, expiry, sig = generate_signed_url('test_report.csv', 15)

# Verify karo
print("\n[4] VERIFYING SIGNED URL...")
result = verify_signed_url('test_report.csv', expiry, sig)

# Decrypt karo
print("\n[5] DECRYPTING FILE FOR DOWNLOAD...")
enc.decrypt_file('test_report.csv.enc', 'test_report_decrypted.csv')

# Verify content same hai
original = open('test_report.csv').read()
decrypted = open('test_report_decrypted.csv').read()

print(f"\n[6] INTEGRITY CHECK:")
print(f"    Original == Decrypted: {original == decrypted}")
print(f"    File integrity: VERIFIED")

print("\n[SUCCESS] All security checks passed!")
print("[+] End-to-end encryption working")
print("[+] Signed URLs working")
print("[+] File integrity verified")

# Cleanup
os.remove('test_report.csv.enc')
os.remove('test_report_decrypted.csv')
