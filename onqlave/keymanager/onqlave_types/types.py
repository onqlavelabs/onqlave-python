import struct

from ctypes import c_int32, c_uint32

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
    def encrypt(plain_text, associated_data: bytearray) -> bytearray:
        raise NotImplementedError

    def decrypt(cipher_text, associated_data: bytearray) -> bytearray:
        raise NotImplementedError


class KeyOperation:
    def get_format(self):
        raise NotImplementedError

    def get_factory(self):
        raise NotImplementedError


class KeyData:
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
    def key_id(self):
        raise NotImplementedError

    def operation(self):
        raise NotImplementedError

    def data(self) -> KeyData:
        raise NotImplementedError


class KeyFormat:
    def size(self) -> int:
        raise NotImplementedError


class KeyFactory:
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
        return AlgorithmTypeName[int(self._algo)]

    def version(self):
        return self._version

    def serialise(self) -> bytearray:
        """Write the data in an Algorithm instance to a bytearray
        """
        buffer = bytearray()
        header_len = struct.pack(">I", 7 + len(self.key()))
        buffer.extend(header_len)
        buffer.append(self.version())
        buffer.append(self.algorithm())
        buffer.append(len(self.key()).to_bytes())
        buffer.append(self.key())
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


class AlgorithmSerialiser:
    def __init__(self, version: bytes, algo: str, key: bytearray):
        self._version = version
        self._algo = AlgorithmTypeValue[algo].to_bytes(1,byteorder='big')
        self._key = key

    def serialise(self):  # return a bytearray
        raise NotImplementedError


class AlgorithmDeserialiser:
    def deserialise(self, buffer: bytearray) -> int:
        raise NotImplementedError

    def key(self) -> bytearray:  # return a bytearray
        raise NotImplementedError

    def version(self) -> bytes:
        raise NotImplementedError

    def algorithm(self) -> str:
        raise NotImplementedError
