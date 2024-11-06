from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key for encryption and decryption
# You must store this key securely and share it with the recipient securely
key = Fernet.generate_key()
cipher = Fernet(key)

# POST endpoint to encrypt data
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Get JSON data from request
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Encrypt the data
    encrypted_message = cipher.encrypt(message.encode())
    return jsonify({"encrypted_message": encrypted_message.decode()})

# POST endpoint to decrypt data
@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Get JSON data from request
    data = request.get_json()
    encrypted_message = data.get("encrypted_message")

    if not encrypted_message:
        return jsonify({"error": "No encrypted_message provided"}), 400

    try:
        # Decrypt the data
        decrypted_message = cipher.decrypt(encrypted_message.encode())
        return jsonify({"decrypted_message": decrypted_message.decode()})
    except Exception as e:
        return jsonify({"error": "Decryption failed", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)