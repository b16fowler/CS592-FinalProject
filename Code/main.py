#####################################################
## Brett Fowler                                    ##
## Final Project- CS 592                           ##
## Shamir's Secret Sharing Generator               ##
#####################################################

import struct
import gui as gui

def main():
    # File intake
    with open("Files/file.txt", "rb") as file:
        data = file.read()
        
    # TEA TESTING
    block = b"ABCDEFGH"
    key = b"0123456789ABCDEF"

    DELTA = 0x9E3779B9
    MASK = 0xFFFFFFFF

    # Function for padding bytes
    def pad(data, block_size = 8):
        # Number of padding bytes needed
        padding_length = block_size - (len(data) % block_size)
        # Constructs actual padding bytes
        padding = bytes([padding_length] * padding_length)

        return data + padding

    def prepare_file(data, block_size = 8):
        data = pad(data, block_size)
        blocks = []

        for i in range(0, len(data), block_size):
            blocks.append(data[i:i + block_size])

        return blocks

    def encrypt_round(v0, v1, k0, k1, k2, k3, sum):
        sum = (sum + DELTA) & MASK

        v0 = (v0 + (
            ((v1 << 4) + k0) ^
            (v1 + sum) ^
            ((v1 >> 5) + k1)
        )) & MASK

        v1 = (v1 + (
            ((v0 << 4) + k2) ^
            (v0 + sum) ^
            ((v0 >> 5) + k3)
        )) & MASK

        return v0, v1, sum

    def encrypt_block(block, key):
        v0, v1 = struct.unpack(">2I", block)
        k0, k1, k2, k3 = struct.unpack(">4I", key)
        sum = 0

        # 32 TEA rounda
        for _ in range(32):        
            v0, v1, sum = encrypt_round(v0, v1, k0, k1, k2, k3, sum)

        return struct.pack(">2I", v0, v1)

    def decrypt_round(v0, v1, k0, k1, k2, k3, sum):
        v1 = (v1 - (
            ((v0 << 4) + k2) ^
            (v0 + sum) ^
            ((v0 >> 5) + k3)
        )) & MASK

        v0 = (v0 - (
            ((v1 << 4) + k0) ^
            (v1 + sum) ^
            ((v1 >> 5) + k1)
        )) & MASK

        sum = (sum - DELTA) & MASK

        return v0, v1, sum

    def decrypt_block(block, key):
        v0, v1 = struct.unpack(">2I", block)
        k0, k1, k2, k3 = struct.unpack(">4I", key)

        sum = (DELTA * 32) & MASK
        for _ in range(32):
            v0, v1, sum = decrypt_round(v0, v1, k0, k1, k2, k3, sum)

        return struct.pack(">2I", v0, v1)

    # TEST
    encrypted_block = encrypt_block(block, key)
    decrypted_block = decrypt_block(encrypted_block, key)

    print("Original block:   ", block)
    print("Encrypted block:  ", encrypted_block.hex())
    print("Decrypted block:  ", decrypted_block)
    print("Match:            ", block == decrypted_block)



    # GUI
    # gui.gui()

main()