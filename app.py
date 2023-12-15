from flask import Flask, render_template, request

app = Flask(__name__)

def encrypt_custom(plaintext_hex, key_binary):
    # Mengonversi plaintext dari heksadesimal ke biner
    plaintext_binary = bin(int(plaintext_hex, 16))[2:]

    # Padding biner plaintext untuk memastikan panjangnya kelipatan 4
    plaintext_binary = '0' * (4 - len(plaintext_binary) % 4) + plaintext_binary

    # Memisahkan biner plaintext menjadi blok-blok 4 bit
    plaintext_blocks = [plaintext_binary[i:i+4] for i in range(0, len(plaintext_binary), 4)]

    # Mengonversi kunci dari biner menjadi daftar integer
    key = [int(bit) for bit in key_binary]

    # Enkripsi setiap blok
    encrypted_blocks = []
    for block in plaintext_blocks:
        # XOR blok dengan kunci
        xor_result = [int(block[i]) ^ key[i] for i in range(4)]

        # Geser setiap bit ke kiri
        shifted_result = xor_result[1:] + [xor_result[0]]

        # Mengonversi hasil ke heksadesimal
        encrypted_block = hex(int(''.join(map(str, shifted_result)), 2))[2:]
        encrypted_blocks.append(encrypted_block)

    # Menggabungkan blok-blok terenkripsi menjadi ciphertext akhir
    ciphertext_hex = ''.join(encrypted_blocks)

    return ciphertext_hex

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext_hex = request.form['plaintext_hex']
    key_binary = request.form['key_binary']
    ciphertext_hex = encrypt_custom(plaintext_hex, key_binary)
    return render_template('index.html', ciphertext_hex=ciphertext_hex)

if __name__ == '__main__':
    app.run(debug=True)
