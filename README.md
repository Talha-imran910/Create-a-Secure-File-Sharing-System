
# Secure File Sharing System

A robust and secure file-sharing portal developed as part of the **Internee.pk Cybersecurity Internship**. This system ensures the confidentiality and integrity of files during transit and at rest using industry-standard encryption protocols.

## 🚀 Key Security Features
* **End-to-End Encryption:** Files are encrypted using **AES-256-CBC** before being stored.
* **Access Control:** Implements time-limited **Signed URLs** (via HMAC-SHA256) to ensure files can only be accessed by authorized users for a specific duration (15 minutes).
* **Data Integrity:** Includes verification checks to ensure the decrypted file perfectly matches the original file.
* **Secure Storage:** Keeps sensitive data in encrypted format, preventing unauthorized access even at the storage level.

## 🛠 Tech Stack
* **Backend:** Python Flask[cite: 1]
* **Encryption:** `cryptography` library (AES-256-CBC)[cite: 1]
* **Security:** HMAC-SHA256 (for Signed URLs)[cite: 1]
* **Testing:** Kaggle Cybersecurity Datasets[cite: 1]

## 📂 Project Structure
```text
secure-fileshare/
├── app.py              # Flask web server & routes
├── crypto_utils.py     # Encryption/Decryption logic
├── signed_urls.py      # HMAC URL generation & validation
├── demo_test.py        # Integrity testing script
├── uploads/            # Temporary upload storage (ignored)
└── encrypted_files/    # Secure repository for encrypted data
