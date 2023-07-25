import sys

from Crypto.Cipher import ChaCha20_Poly1305
from onqlave.keymanager.random_service import CSPRNG
from onqlave.keymanager.onqlave_types.types import Key, AEAD

Poly1305TagSize = 16
ChaCha20Poly1305NonceSizeX = 24
MAX_INT = sys.maxsize


class XChaCha20Poly1305AEAD(AEAD):
    def __init__(self, key: Key, random_service: CSPRNG) -> None:
        self._key = key
        self._random_service = random_service

    def encrypt(self, plaintext: bytearray, associated_data: bytearray) -> bytearray:
        if len(plaintext) > MAX_INT - ChaCha20Poly1305NonceSizeX - Poly1305TagSize:
            return None  # plain_text too long
        key_data = self._key.data()
        key_value = key_data.get_value()
        nonce = self._random_service.get_random_bytes(24)
        cipher = ChaCha20_Poly1305.new(key=key_value, nonce=nonce)

        cipher.update(associated_data)
        cipher_text = cipher.encrypt(plaintext)
        return nonce + cipher_text

    def decrypt(self, ciphertext: bytearray, associated_data: bytearray) -> bytearray:
        key_data = self._key.data()
        key_value = key_data.get_value()
        actual_cipher_text = ciphertext[24:]
        cipher = ChaCha20_Poly1305.new(key=key_value, nonce=ciphertext[:24])
        cipher.update(associated_data)

        plain_text = cipher.decrypt(actual_cipher_text)
        return plain_text
