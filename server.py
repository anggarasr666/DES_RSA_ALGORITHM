import socket
import program_algoritma_des
from rsa import RSA

PRIVATE_PKA, PUBLIC_PKA = RSA.generate_rsa_keys()
PUB_UTF8 = RSA.public_key_to_text(PUBLIC_PKA)

PUBLIC_KEY_AUTHORITY = {}

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(2)
    print("Server menunggu koneksi dari client...")

    # Menerima koneksi dari client 1 dan client 2
    client1_conn, client1_addr = server_socket.accept()
    print(f"Client 1 terhubung dari: {client1_addr}")
    client1_conn.send(PUB_UTF8.encode())
    # menerima public key yang di kirimkan oleh client 1
    PUBLIC_KEY_AUTHORITY["client1"] = client1_conn.recv(1024).decode()
    print(f"Public Key Client 1: {PUBLIC_KEY_AUTHORITY['client1']}")


    client2_conn, client2_addr = server_socket.accept()
    print(f"Client 2 terhubung dari: {client2_addr}")
    client2_conn.send(PUB_UTF8.encode())
    # menerima public key yang di kirimkan oleh client 1
    PUBLIC_KEY_AUTHORITY["client2"] = client2_conn.recv(1024).decode()
    print(f"Public Key Client 2: {PUBLIC_KEY_AUTHORITY['client2']}")

    # mengirimkan public key client1 ke client2 dan sebaliknya
    client1_conn.send(PUBLIC_KEY_AUTHORITY["client2"].encode())
    # client1_conn.send(RSA.sign_message(PRIVATE_PKA, PUBLIC_KEY_AUTHORITY["client2"]).encode())

    client2_conn.send(PUBLIC_KEY_AUTHORITY["client1"].encode())
    # client2_conn.send(RSA.sign_message(PRIVATE_PKA, PUBLIC_KEY_AUTHORITY["client1"]).encode())

    while True:
        # Menerima pesan dari client 1
        encrypted_text = client1_conn.recv(1024).decode()
        if not encrypted_text:
            break
        print(f"Menerima pesan terenkripsi dari client 1: '{encrypted_text}'")

        # Meneruskan pesan ke client 2
        client2_conn.send(encrypted_text.encode())
        print(f"Meneruskan pesan terenkripsi ke client 2.")

        # Menerima pesan dari client 2
        encrypted_text = client2_conn.recv(1024).decode()
        if not encrypted_text:
            break
        print(f"Menerima pesan terenkripsi dari client 2: '{encrypted_text}'")

        # Meneruskan pesan ke client 1
        client1_conn.send(encrypted_text.encode())
        print(f"Meneruskan pesan terenkripsi ke client 1.")

    client1_conn.close()
    client2_conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()