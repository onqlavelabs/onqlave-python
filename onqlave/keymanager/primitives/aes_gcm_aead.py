import sys
import io

from Crypto.Cipher import AES

from keymanager.onqlave_types.types import Key
from keymanager.random_service import CSPRNG

AESGCMIVSize = 12
AESGCMTagSize = 16
AESGCMMaxPlaintextSize = (1 << 36) - 31
MAX_INT = sys.maxsize
MaxIntPlainTextSize = MAX_INT - AESGCMIVSize - AESGCMTagSize
MinNoIVCiphertextSize = AESGCMTagSize
MinPrependIVCiphertextSize = AESGCMIVSize + AESGCMTagSize

class AESGCMAEAD:
    def __init__(
        self, 
        key: Key, 
        random_service: CSPRNG
    ) -> None:
        self._random_service = random_service
        self._key_value = key.data().get_value()
        if not validate_aes_key_size(len(self._key_value)):
            raise Exception # should be detailed
        
        self.prependIV = True

    def encrypt(
        self, 
        plaintext: bytearray, 
        associated_data: bytearray
    ):
        iv = self._random_service.get_random_bytes(AESGCMIVSize)
        if len(iv) != AESGCMIVSize:
            raise Exception # unexpected IV size
        max_plain_text_size = MaxIntPlainTextSize
        if max_plain_text_size > AESGCMMaxPlaintextSize:
            max_plain_text_size = AESGCMMaxPlaintextSize
        if len(plaintext) > max_plain_text_size:
            raise Exception # plain text size too long
        cipher = self.new_cipher()
        cipher.update(assoc_data=associated_data)
        cipher_text = cipher.encrypt(plaintext)

        cipher_stream = io.BytesIO()
        # processor = PlainStreamProcessor

        return cipher_text
        
    def new_cipher(self):
        aes_cipher = AES.new(
            key=self._key_value,
            mode=AES.MODE_GCM
        )
        return aes_cipher 
        



def validate_aes_key_size(size_in_bytes: int) -> bool:
    if size_in_bytes in [16,32]:
        return True
    return False