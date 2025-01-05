from math_utils import random_binary_inv_matrix, random_perm_matrix
from goppa_code import GoppaCode, GF2
from dataclasses import dataclass
import random, numpy as np

import time
start=time.time()
@dataclass
class SecretKey:
  S_inv: GF2
  P_inv: GF2
  goppa: GoppaCode


class McEliece:
  def __init__(self, m: int, t: int):
    self.m = m
    self.t = t

    # Fix these values for fixed-length message with padding
    self.n = 2**m  # Encrypted message length (96 bits)
    self.k = self.n - t * m  # Message length after padding (96 bits)

  def generate_key_pair(self) -> (SecretKey, GF2):
    """Generate and return the secret and public key"""

    goppa_code = GoppaCode(self.n, self.m, self.t)
    S = random_binary_inv_matrix(self.k)
    P = random_perm_matrix(self.n)

    Gp = S @ goppa_code.G @ P

    P_inv = np.linalg.inv(P)
    S_inv = np.linalg.inv(S)

    return SecretKey(S_inv, P_inv, goppa_code), Gp

  def encrypt(self, message: np.ndarray, Gp: GF2) -> np.ndarray:
    """Encrypt a message with someones public key."""

    if len(message) != self.k:
      raise Exception(f"Wrong message length. It has to be {self.k} bits (message padded to 12 characters).")

    # generate codeword by multiplying message with generator matrix
    codeword = np.array(GF2(message) @ Gp)

    # generate t random errors by generating list of all possible error locations and shuffle
    error_locations = list(range(self.n))
    random.shuffle(error_locations)

    # apply errors
    for loc in error_locations[: self.t]:
      codeword[loc] ^= 1

    return codeword

  def decrypt(self, cipher: np.ndarray, sk: SecretKey) -> np.ndarray:
    """Decrypt a received cipher with a secret key."""

    if len(cipher) != self.n:
      raise Exception(f"Wrong cipher length. It has to be {self.n} bits.")

    unshuffled_cipher = GF2(cipher) @ sk.P_inv
    decoded_cipher = sk.goppa.decode(unshuffled_cipher)
    message = GF2(decoded_cipher) @ sk.S_inv
    return message




# Initialize McEliece cryptosystem with desired parameters
mceliece = McEliece(m=8, t=20) # Example parameters, adjust as needed

# Generate key pair
secret_key, public_key = mceliece.generate_key_pair()
# Get user input with length upto 12 
message = input("Enter a message of upto 12 characters: ")

encstart=time.time()

# Fix message length to 12 characters (96 bits) with padding
message = message.ljust(12, chr(0))  # Pad with null characters

# Convert message to binary array
binary_message = np.array([int(x) for x in ''.join(format(ord(c), '08b') for c in message)])

# Encryption process
encrypted_message = mceliece.encrypt(binary_message, public_key)


print("Encrypted message:",encrypted_message)
encend=time.time()
print("Encryption runtime: ",(encend-encstart)*10**3,'ms')
# Decrypt the encrypted message
decstart=time.time()
decrypted_message = mceliece.decrypt(encrypted_message, secret_key)
decstop=time.time()

# Convert decrypted binary message back to text
text_message = ''.join(chr(int(''.join(map(str, block)), 2)) for block in np.split(decrypted_message, len(decrypted_message) // 8))

# Output decrypted text
print("Decrypted message (first 12 characters):", text_message[:12])
end=time.time()
print("Decryption runtime: ",(decstop-decstart)*10**3,'ms')
print("Total runtime: ",(end-start)*10**3,'ms')

