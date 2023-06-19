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
    "SHA1":         1,
    "SHA384":       2,
    "SHA256":       3,
    "SHA512":       4,
    "SHA224":       5,
}

Aesgcm128 = "aes-gcm-128"
Aesgcm256 = "aes-gcm-256"
XChacha20poly1305 = "xcha-cha-20-poly-1305"
RsaSsapkcs12048sha256f4 = "RSA_SSA_PKCS1_2048_SHA256_F4"

# HashType = type('HashType', (c_int32), {})
class HashType(c_uint32):
    pass

HashTypeUNKNOWNHASH = HashType(0)
HashTypeSHA1        = HashType(1)
HashTypeSHA384      = HashType(2)
HashTypeSHA256      = HashType(3)
HashTypeSHA512      = HashType(4)
HashTypeSHA224      = HashType(5)

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
    def get_value() -> bytearray:
        raise NotImplementedError
    
    def from_value(data: bytearray):
        raise NotImplementedError
    
    def get_type_url() -> str:
        raise NotImplementedError
    
    def get_key_material_type():
        raise NotImplementedError
    
    def get_version() -> c_uint32:
        raise NotImplementedError
    
class Key:
    def key_id(self):
        raise NotImplementedError
    
    def operation(self):
        raise NotImplementedError
    
    def data(self) -> KeyData:
        raise NotImplementedError
    
class KeyFormat:
    def size(self) -> c_uint32:
        raise NotImplementedError
        

class KeyFactory:
    def new_key(operation: KeyOperation) -> Key:
        raise NotImplementedError
    
    def new_key_from_data(operation: KeyOperation, key_data: bytearray) -> Key:
        raise NotImplementedError
    
    def primitive(key: Key) -> AEAD:
        raise NotImplementedError