import socket
from program_algoritma_des import des_encrypt, des_decrypt
from rsa import RSA
import ast
import json
import base64

server_host = '127.0.0.1'
server_port = 12345

PRIVATE_KEY, PUBLIC_KEY = RSA.generate_rsa_keys()
PKA_PUBLIC_KEY = None
CLIENT_B_PUBLIC_KEY = None

def client1_send():
    global PKA_PUBLIC_KEY, CLIENT_B_PUBLIC_KEY

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    PKA_PUBLIC_KEY = RSA.text_to_public_key(client_socket.recv(1024).decode())

    client_socket.send(RSA.public_key_to_text(PUBLIC_KEY).encode())

    cbpk = client_socket.recv(1024).decode()
    print("Client B public key:", cbpk, cbpk != RSA.public_key_to_text(PUBLIC_KEY))
    CLIENT_B_PUBLIC_KEY = RSA.text_to_public_key(cbpk)
    # signature = client_socket.recv(1024).decode()
    # print("Signature verified, message is valid" if RSA.verify_signature(PKA_PUBLIC_KEY, CLIENT_B_PUBLIC_KEY, signature) else "Signature verification failed, message is invalid")
    
    while True:
        text = input("Masukkan pesan yang akan dienkripsi dan dikirim (ketik 'exit' untuk keluar): ")
        if text.lower() == 'exit':
            break

        key = RSA.randomize(8)
        encrypted_text = des_encrypt(text, key)
        encrypted_key = RSA.encrypt_pub_key(key.encode(), CLIENT_B_PUBLIC_KEY)  
        message = {
            "encrypted_text": encrypted_text,
            "encrypted_key": base64.b64encode(encrypted_key).decode()
        }
        client_socket.send(json.dumps(message).encode()) 
        print(f"Pesan terenkripsi '{encrypted_text}' dengan key {key} berhasil dikirim ke server. len {len(encrypted_key)}")
        
        # Menerima pesan terenkripsi dari server
        encrypted_text_key = client_socket.recv(1024).decode()
        
        recieved_message = json.loads(encrypted_text_key)
        recieved_message["encrypted_key"] = base64.b64decode(recieved_message["encrypted_key"])

        # print(recieved_message["encrypted_text"])
        # print(len(recieved_message["encrypted_key"]))
        
        recieved_key = RSA.decrypt_pri_key(recieved_message["encrypted_key"], PRIVATE_KEY).decode()
        if not recieved_message["encrypted_text"]:
            break
        print(f"Menerima pesan terenkripsi dari server: '{recieved_message['encrypted_text']}' dengan key '{recieved_key}'")
        
        # Mendekripsi pesan
        decrypted_text = des_decrypt(recieved_message["encrypted_text"], recieved_key)
        print(f"Pesan asli setelah dekripsi: '{decrypted_text}'")

    client_socket.close()

if __name__ == "__main__":
    client1_send()