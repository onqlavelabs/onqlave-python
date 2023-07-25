import sys

from Crypto.Cipher import AES

from onqlave.keymanager.onqlave_types.types import Key
from onqlave.keymanager.random_service import CSPRNG
from onqlave.errors.errors import OnqlaveError, InvalidKeyException
from onqlave.messages import messages

AESGCMIVSize = 12 # aes-gcm init vector size
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
            raise InvalidKeyException(
                message=messages.INVALID_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        self._prependIV = True

    def encrypt(
        self, 
        plaintext: bytearray, 
        associated_data: bytearray
    ):
        iv = self._random_service.get_random_bytes(AESGCMIVSize)
        if len(iv) != AESGCMIVSize:
            return None # unexpected IV size
        max_plain_text_size = MaxIntPlainTextSize
        if max_plain_text_size > AESGCMMaxPlaintextSize:
            max_plain_text_size = AESGCMMaxPlaintextSize
        if len(plaintext) > max_plain_text_size:
            return None # plain text size too long
        
        cipher = AES.new(
            key=self._key_value,
            mode=AES.MODE_GCM,
            nonce=iv
        )
        cipher.update(assoc_data=associated_data)
        cipher_text = cipher.encrypt(plaintext)
        tag_bytes = cipher.digest()
        if self._prependIV:
            return iv + cipher_text + tag_bytes
        else:
            return cipher_text
        
    def new_cipher(self):
        aes_cipher = AES.new(
            key=self._key_value,
            mode=AES.MODE_GCM,
        )
        return aes_cipher 
        
    def decrypt(
        self,
        ciphertext: bytearray,
        associated_data: bytearray
    ):
        """Decrypts ciphertext with iv and associated data
        If prependIV is true, the iv argument and the first AESGCMIVSize bytes of the ciphertext
        must be equal. The ciphertext argument is as follows:
        |iv|actual cipher text|tag|
        if false, the ciphertext argument is:
        |actual ciphertext|tag|

        Args:
            ciphertext: the ciphertext, formatted as a bytearray
            associated_data: the data included in the encrypt/decrypt process, formatted as a bytearray
        Returns:
            The decrypted ciphertext
        """
        if len(ciphertext) < AESGCMIVSize:
            return None # cipher text too short
        
        iv = ciphertext[:AESGCMIVSize]
        if len(iv) != AESGCMIVSize:
            return None # unexpected IV Size 

        actual_cipher_text = bytearray()

        if self._prependIV:
            if len(ciphertext) < MinPrependIVCiphertextSize:
                return None # ciphertext too short
            if iv != ciphertext[:AESGCMIVSize]:
                return None # unequal IVs:
            actual_cipher_text = ciphertext[AESGCMIVSize:len(ciphertext)-AESGCMTagSize]
        else:
            if len(ciphertext) < MinNoIVCiphertextSize:
                return None # cipher text too short 
            actual_cipher_text = ciphertext

        # should try-catch
        cipher = AES.new(
            key=self._key_value,
            mode=AES.MODE_GCM,
            nonce=iv
        )
        cipher.update(assoc_data=associated_data)

        plain_text = cipher.decrypt(actual_cipher_text)
        return plain_text


def validate_aes_key_size(size_in_bytes: int) -> bool:
    if size_in_bytes in [16,32]:
        return True
    return False