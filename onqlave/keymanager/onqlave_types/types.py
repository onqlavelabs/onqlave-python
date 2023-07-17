import struct
import io

from ctypes import c_int32, c_uint32

from onqlave.errors.errors import OnqlaveError, AlgorithmSerialisingException, InvalidCipherDataException
from onqlave.messages import messages

HashTypeName = {
    0: "UNKNOWN_HASH",
    1: "SHA1",
    2: "SHA384",
    3: "SHA256",
    4: "SHA512",
    5: "SHA224",
}

HashTypeValue = {
    "UNKNOWN_HASH": 0,
    "SHA1": 1,
    "SHA384": 2,
    "SHA256": 3,
    "SHA512": 4,
    "SHA224": 5,
}

Aesgcm128 = "aes-gcm-128"
Aesgcm256 = "aes-gcm-256"
XChacha20poly1305 = "xcha-cha-20-poly-1305"
RsaSsapkcs12048sha256f4 = "RSA_SSA_PKCS1_2048_SHA256_F4"


# HashType = type('HashType', (c_int32), {})
class HashType(c_uint32):
    pass


class KeyMaterialType(int):
    pass


class KeyID(c_uint32):
    pass


KeyMaterialUNKNOWNKEYMATERIAL = KeyMaterialType(0)
KeyMaterialSYMMETRIC = KeyMaterialType(1)
KeyMaterialASYMMETRICPRIVATE = KeyMaterialType(2)
KeyMaterialASYMMETRICPUBLIC = KeyMaterialType(3)
KeyMaterialREMOTE = KeyMaterialType(4)

HashTypeUNKNOWNHASH = HashType(0)
HashTypeSHA1 = HashType(1)
HashTypeSHA384 = HashType(2)
HashTypeSHA256 = HashType(3)
HashTypeSHA512 = HashType(4)
HashTypeSHA224 = HashType(5)

AlgorithmTypeName  = {
    0: "unknown_algorithm",
    1: "aes-gcm-128",
    2: "aes-gcm-256",
    3: "xcha-cha-20-poly-1305"
}

AlgorithmTypeValue = {
    "unknown_algorithm": 0,
    "aes-gcm-128": 1,
    "aes-gcm-256": 2,
    "xcha-cha-20-poly-1305": 3,
}


class AEAD:
    """An interface for creating classes that implement the 
    Authenticated Encryption with Associated Data primitives which
    combines both encryption and authentication into a single operation.    
    """
    def encrypt(self, plaintext: bytearray, associated_data: bytearray) -> bytearray:
        raise NotImplementedError

    def decrypt(self, ciphertext: bytearray, associated_data: bytearray) -> bytearray:
        raise NotImplementedError


class KeyOperation:
    """An interface for creating classes that specify key operation
    """
    def get_format(self):
        raise NotImplementedError

    def get_factory(self):
        raise NotImplementedError


class KeyData:
    """An interface for creating classes that work with Key Data
    """
    def get_value(self) -> bytearray:
        raise NotImplementedError

    def from_value(self, data: bytearray):
        raise NotImplementedError

    def get_type_url(self) -> str:
        raise NotImplementedError

    def get_key_material_type(self):
        raise NotImplementedError

    def get_version(self) -> c_uint32:
        raise NotImplementedError


class Key:
    """An interface for creating Key classes 
    """
    def key_id(self):
        raise NotImplementedError

    def operation(self):
        raise NotImplementedError

    def data(self) -> KeyData:
        raise NotImplementedError


class KeyFormat:
    """An inteface for creating classes that handles various KeyFormat
    """
    def size(self) -> int:
        raise NotImplementedError


class KeyFactory:
    """An interface for creating various KeyFactory
    """
    def new_key(self, operation: KeyOperation) -> Key:
        raise NotImplementedError

    def new_key_from_data(self, operation: KeyOperation, key_data: bytearray) -> Key:
        raise NotImplementedError

    def primitive(self, key: Key) -> any:
        raise NotImplementedError


class Algorithm:
    def __init__(self, version: bytes, algo: bytes, key: bytearray):
        self._version = version
        self._algo = algo
        self._key = key

    def key(self):
        return self._key

    def algorithm(self):
        return AlgorithmTypeName[
            int.from_bytes(self._algo,byteorder='big')
        ]

    def version(self):
        return self._version

    def serialise(self) -> bytearray:
        """Write the data in an Algorithm instance to a bytearray
        """
        buffer = bytearray()
        header_len = struct.pack(">I", 7 + len(self.key()))
        buffer.extend(header_len)
        buffer.append(self.version())
        buffer.append(self._algo)
        buffer.append(len(self.key()).to_bytes())
        buffer.extend(self.key())
        return buffer

    def deserialise(self, buffer: bytearray):
        """Read the data as bytearray in a buffer then assign it to the Algorithm instance
        """
        if len(buffer) < 7:
            return None # errors invalid cipher data
        header_len = struct.unpack(">I",buffer[:4])[0]
        if len(buffer) < len(header_len):
            return None # raise error invalid cipher data
        self._version = buffer[4]
        self._algo = buffer[5]
        key_len = buffer[6]
        self._key = buffer[7:7+key_len]

        return int(header_len)


class AlgorithmSerialiser():
    """An object used in the encryption process that specifies
    the information of the selected encryption algorithm
    """
    def __init__(self, version: bytes, algo: str, key: bytearray):
        self._version = version
        self._algo = AlgorithmTypeValue[algo].to_bytes(1,byteorder='big')
        self._key = key

    def serialise(self) -> bytearray:
        """Write the data of an Algorithm instance to a bytearray

        Args:
            Nothing

        Returns:
            an bytearray contains the data related to an algorithm
        """
        try:
            buffer = io.BytesIO()
            header_len = struct.pack(">I", 7 + len(self._key))
            buffer.write(header_len)
            buffer.write(bytes([self._version]))
            buffer.write(bytes([int.from_bytes(self._algo,byteorder='big')]))
            buffer.write(bytes([len(self._key)]))
            buffer.write(self._key)
        except Exception:
            raise AlgorithmSerialisingException(
                message=messages.ALGORITHM_SERIALISING_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )

        return buffer.getvalue()


class AlgorithmDeserialiser():
    """An object used in the decryption process that specifies
    the information of the selected encryption algorithm
    """
    def __init__(self) -> None:
        self._version = None
        self._algo = None
        self._key = None

    def deserialise(self, buffer: bytearray) -> int:
        """Read the information of the selected algorithm written
        in the buffer

        Args:
            buffer: a bytearray contains the encoded data of the selected
            algorithm

        Returns:
            Nothing
        """
        if len(buffer) < 7:
            raise InvalidCipherDataException(
                message=messages.INVALID_CIPHER_DATA_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        header_len = int.from_bytes(buffer[:4],'big')
        if len(buffer) < header_len:
            raise InvalidCipherDataException(
                message=messages.INVALID_CIPHER_DATA_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        self._version = buffer[4]
        self._algo = buffer[5]
        key_len = buffer[6]

        self._key = buffer[7:7+key_len]
        
        return header_len

    def key(self) -> bytearray: 
        raise NotImplementedError

    def version(self) -> bytes:
        raise NotImplementedError

    def algorithm(self) -> str:
        return AlgorithmTypeName[self._algo]
