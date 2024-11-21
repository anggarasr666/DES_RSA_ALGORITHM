# Program Algoritma DES (Data Encryption Standard

# Tabel permutasi awal
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Tabel permutasi akhir (inverse IP)
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Ekspansi ke 48-bit
E_BOX = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

# S-Box untuk substitusi
S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# Permutasi akhir pada fungsi f
P_BOX = [16, 7, 20, 21,
         29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2, 8, 24, 14,
         32, 27, 3, 9,
         19, 13, 30, 6,
         22, 11, 4, 25]

# Permutasi kunci awal
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permutasi kunci kedua
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Fungsi untuk mengatur pergeseran (shifts) pada kunci
SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 1]

# Fungsi permutasi menggunakan tabel permutasi yang diberikan
def permute(block, table):
    return [block[i - 1] for i in table]

# Fungsi untuk melakukan XOR dua list biner
def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]

# Fungsi untuk melakukan pemisahan blok
def split(block):
    return block[:len(block) // 2], block[len(block) // 2:]

# Fungsi rotasi kiri (left circular shift)
def rotate_left(block, n):
    return block[n:] + block[:n]

# Fungsi konversi teks ke biner (string ke list of integers)
def string_to_bits(text):
    bits = []
    for char in text:
        binval = bin(ord(char))[2:].rjust(8, '0')
        bits.extend([int(x) for x in binval])
    return bits

# Fungsi konversi biner ke teks (list of integers ke string)
def bits_to_string(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

# Fungsi untuk membuat kunci dari input string
def generate_keys(key):
    key = string_to_bits(key)
    key = permute(key, PC1)
    C, D = split(key)
    keys = []
    for shift in SHIFT_TABLE:
        C = rotate_left(C, shift)
        D = rotate_left(D, shift)
        combined_key = C + D
        round_key = permute(combined_key, PC2)
        keys.append(round_key)
    return keys

# Fungsi substitusi S-Box
def s_box_substitution(block):
    subblocks = [block[k * 6:(k + 1) * 6] for k in range(8)]
    result = []
    for i, subblock in enumerate(subblocks):
        row = int(f"{subblock[0]}{subblock[5]}", 2)
        col = int(''.join([str(x) for x in subblock[1:5]]), 2)
        s_val = S_BOX[i][row][col]
        binval = bin(s_val)[2:].rjust(4, '0')
        result.extend([int(x) for x in binval])
    return result

# Fungsi f untuk menggabungkan dengan kunci dan melakukan transformasi
def function_f(R, K):
    expanded_R = permute(R, E_BOX)
    xor_result = xor(expanded_R, K)
    substituted = s_box_substitution(xor_result)
    return permute(substituted, P_BOX)

# Proses enkripsi satu blok 64-bit menggunakan 16 putaran DES
def des_encrypt_block(block, keys):
    block = permute(block, IP)
    L, R = split(block)
    for i in range(16):
        L, R = R, xor(L, function_f(R, keys[i]))
    return permute(R + L, IP_INV)

# Proses dekripsi satu blok 64-bit menggunakan 16 putaran DES
def des_decrypt_block(block, keys):
    block = permute(block, IP)
    L, R = split(block)
    for i in range(15, -1, -1):
        L, R = R, xor(L, function_f(R, keys[i]))
    return permute(R + L, IP_INV)

# Fungsi untuk mengubah biner ke representasi hexadecimal
def bits_to_hex(bits):
    bit_string = ''.join(str(bit) for bit in bits)
    hex_string = hex(int(bit_string, 2))[2:]  # Mengubah ke hexadecimal
    return hex_string.upper()  # Uppercase untuk konsistensi

# Fungsi untuk mengubah representasi hexadecimal kembali ke biner
def hex_to_bits(hex_string):
    bit_string = bin(int(hex_string, 16))[2:]  # Mengubah ke biner
    padded_bit_string = bit_string.zfill(len(hex_string) * 4)  # Padding
    return [int(bit) for bit in padded_bit_string]

# Fungsi utama untuk enkripsi pesan teks menggunakan kunci
def des_encrypt(plaintext, key):
    keys = generate_keys(key)
    plaintext_bits = string_to_bits(plaintext)
    while len(plaintext_bits) % 64 != 0:
        plaintext_bits.extend([0])  # Padding dengan 0 jika tidak cukup
    ciphertext_bits = []
    for i in range(0, len(plaintext_bits), 64):
        block = plaintext_bits[i:i + 64]
        encrypted_block = des_encrypt_block(block, keys)
        ciphertext_bits.extend(encrypted_block)
    # Encode as Hexadecimal
    return bits_to_hex(ciphertext_bits)

# Fungsi utama untuk dekripsi pesan teks menggunakan kunci
def des_decrypt(ciphertext, key):
    keys = generate_keys(key)
    # Decode from Hexadecimal
    decoded_bits = hex_to_bits(ciphertext)
    plaintext_bits = []
    for i in range(0, len(decoded_bits), 64):
        block = decoded_bits[i:i + 64]
        decrypted_block = des_decrypt_block(block, keys)
        plaintext_bits.extend(decrypted_block)
    return bits_to_string(plaintext_bits)

# Fungsi utama untuk menjalankan program dengan loop pilihan
def main():
    print("=========================================")
    print("        DES Encryption/Decryption        ")
    print("=========================================")
    print("Selamat datang! Program ini menggunakan algoritma DES untuk enkripsi dan dekripsi teks.")
    print("Anda bisa memasukkan teks dan kunci 8 karakter untuk memulai.")

    while True:
        print("\n-----------------------------------------")
        print("Pilih mode:")
        print("[e] Enkripsi")
        print("[d] Dekripsi")
        print("[q] Keluar")
        print("-----------------------------------------")

        mode = input("Masukkan pilihan Anda: ").strip().lower()

        if mode == 'q':
            print("Program dihentikan. Terima kasih sudah menggunakan program ini!")
            break

        if mode not in ['e', 'd']:
            print("\n[!] Mode tidak valid! Gunakan 'e' untuk enkripsi atau 'd' untuk dekripsi.")
            continue

        text = input("\nMasukkan teks yang akan dienkripsi/dekripsi: ").strip()
        key = input("Masukkan kunci (8 karakter): ").strip()

        if len(key) != 8:
            print("\n[!] Kunci harus 8 karakter! Silakan coba lagi.")
            continue

        # Proses enkripsi atau dekripsi berdasarkan pilihan
        if mode == 'e':
            print("\nProses enkripsi sedang berjalan...")
            encrypted_text = des_encrypt(text, key)
            print("-----------------------------------------")
            print("Hasil Enkripsi:")
            print(encrypted_text)
            print("-----------------------------------------")
        elif mode == 'd':
            print("\nProses dekripsi sedang berjalan...")
            try:
                decrypted_text = des_decrypt(text, key)
                print("-----------------------------------------")
                print("Hasil Dekripsi:")
                print(decrypted_text)
                print("-----------------------------------------")
            except Exception as e:
                print("\n[!] Terjadi kesalahan saat proses dekripsi. Pastikan ciphertext yang dimasukkan benar.")
                print(f"Detail Kesalahan: {e}")
                continue

        # Tanyakan apakah ingin melanjutkan atau keluar
        repeat = input("\nApakah ingin melanjutkan? (y untuk lanjut, n untuk keluar): ").strip().lower()
        if repeat == 'n':
            print("\nProgram dihentikan. Terima kasih sudah menggunakan program ini!")
            break

if __name__ == "__main__":
    main()

