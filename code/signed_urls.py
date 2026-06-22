import hmac
import hashlib
import time
import base64
import secrets

SECRET_KEY = secrets.token_hex(32)

def generate_signed_url(filename: str, expiry_minutes: int = 15):
    """Signed URL generate karo file access ke liye"""
    expiry_time = int(time.time()) + (expiry_minutes * 60)
    
    # Signature banao
    message = f"{filename}:{expiry_time}"
    signature = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    signed_url = f"http://localhost:5000/download/{filename}?expires={expiry_time}&signature={signature}"
    
    print(f"\n[+] Signed URL Generated:")
    print(f"    File: {filename}")
    print(f"    Expires: {expiry_minutes} minutes")
    print(f"    Signature: {signature[:20]}...")
    print(f"    URL: {signed_url[:60]}...")
    
    return signed_url, expiry_time, signature

def verify_signed_url(filename: str, expiry_time: int, signature: str):
    """Signed URL verify karo"""
    # Expiry check
    if int(time.time()) > expiry_time:
        print("[-] URL EXPIRED")
        return False
    
    # Signature verify
    message = f"{filename}:{expiry_time}"
    expected = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if hmac.compare_digest(signature, expected):
        print(f"[+] URL VALID - Access GRANTED")
        return True
    else:
        print("[-] INVALID SIGNATURE - Access DENIED")
        return False
