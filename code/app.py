from flask import Flask, request, jsonify, send_file, render_template_string
import os
import time
import secrets
from crypto_utils import AES256FileEncryptor
from signed_urls import generate_signed_url, verify_signed_url
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted_files'
ENCRYPTION_PASSWORD = "InterneeSecure2025!"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'png', 'jpg', 'xlsx'}

encryptor = AES256FileEncryptor(ENCRYPTION_PASSWORD)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Internee.pk Secure File Portal</title>
    <style>
        body { 
            font-family: Arial; 
            max-width: 800px; 
            margin: 50px auto; 
            background: #1a1a2e;
            color: #eee;
        }
        .container { 
            background: #16213e; 
            padding: 30px; 
            border-radius: 10px;
            border: 1px solid #0f3460;
        }
        h1 { color: #e94560; }
        h2 { color: #0f3460; background: #e94560; padding: 8px; border-radius: 5px; }
        input, button { 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 5px;
            border: none;
            width: 100%;
        }
        button { 
            background: #e94560; 
            color: white; 
            cursor: pointer;
            font-size: 16px;
        }
        .status { 
            background: #0f3460; 
            padding: 15px; 
            border-radius: 5px;
            margin: 10px 0;
        }
        .success { border-left: 4px solid #00ff00; }
        .info { border-left: 4px solid #00bfff; }
        .security-badge {
            background: #e94560;
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin: 3px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Internee.pk Secure File Portal</h1>
    
    <div class="status info">
        <span class="security-badge">AES-256-CBC</span>
        <span class="security-badge">End-to-End Encrypted</span>
        <span class="security-badge">Signed URLs</span>
        <span class="security-badge">Secure Transfer</span>
    </div>

    <h2>Upload Encrypted File</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload & Encrypt</button>
    </form>

    {% if message %}
    <div class="status success">
        <strong>{{ message }}</strong><br>
        {% if signed_url %}
        <small>Signed URL: {{ signed_url[:80] }}...</small>
        {% endif %}
    </div>
    {% endif %}

    <h2>Download Decrypted File</h2>
    <form action="/list" method="GET">
        <button type="submit">View Uploaded Files</button>
    </form>

    {% if files %}
    <div class="status">
        <strong>Available Files:</strong>
        {% for f in files %}
        <div>
            <a href="/download/{{ f }}?decrypt=true" style="color:#e94560">{{ f }}</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No filename"}), 400
    
    filename = secure_filename(file.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename + '.enc')
    
    # Save original
    file.save(upload_path)
    
    # Encrypt karo
    encryptor.encrypt_file(upload_path, encrypted_path)
    
    # Original delete karo (security)
    os.remove(upload_path)
    
    # Signed URL generate karo
    signed_url, expiry, sig = generate_signed_url(filename, expiry_minutes=15)
    
    message = f"File '{filename}' uploaded and encrypted with AES-256!"
    
    return render_template_string(
        HTML_TEMPLATE,
        message=message,
        signed_url=signed_url
    )

@app.route('/list', methods=['GET'])
def list_files():
    files = [f.replace('.enc', '') 
             for f in os.listdir(ENCRYPTED_FOLDER) 
             if f.endswith('.enc')]
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename + '.enc')
    decrypted_path = os.path.join(UPLOAD_FOLDER, 'decrypted_' + filename)
    
    if not os.path.exists(encrypted_path):
        return jsonify({"error": "File not found"}), 404
    
    # Decrypt karo
    encryptor.decrypt_file(encrypted_path, decrypted_path)
    
    return send_file(decrypted_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
    print("[+] Internee.pk Secure File Portal Starting...")
    print("[+] Encryption: AES-256-CBC")
    print("[+] URL: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
