import pytest
import io
import os
from onqlave.encryption import options
from onqlave.encryption.encryption import Encryption
from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings

def encrypt_engine(access_key, arx_url, server_signing_key, server_secret_key):
    debug_option = options.DebugOption(enable_debug=True) # toggle the debug option
    # init the configuration for the encryption service
    arx_option = options.ArxOption(arx_url=arx_url)
    credential_option = Credential(
            access_key=access_key,
            signing_key=server_signing_key,
            secret_key=server_secret_key
        )
    retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2) # retry when server fails

    encryption_engine = Encryption( # init an encryption service
            debug_option=debug_option,
            arx_option=arx_option,
            credential_option=credential_option,
            retry_setting=retry_option
        )

    return encryption_engine

def compare_encrypted_decrypted_text(encryption_engine):
    plaintext = "hello world" # your data goes here
    associated_data = "auth" # your authentication data goes here
    cipher_text = encryption_engine.encrypt(plaintext.encode(), associated_data.encode())
    decrypted_cipher = encryption_engine.decrypt(cipher_text,associated_data.encode())
    assert decrypted_cipher.decode() == plaintext
    
def compare_encrypted_decrypted_stream(encryption_engine):
    # create a file
    with open("plaintext.txt","w") as f:
        f.write("hello world")
    plain_file_stream = open("plaintext.txt","rb")
    associated_data = "auth" # your authentication data goes here
    plain_stream = io.BytesIO(plain_file_stream.read())
    cipher_stream = io.BytesIO()
        
    encryption_engine.encrypt_stream(plain_stream,cipher_stream,associated_data.encode())
    cipher_stream.seek(0) # rewind your pointer to the beginning position

    decrypted_stream = io.BytesIO()
    encryption_engine.decrypt_stream(
            cipher_stream=cipher_stream,
            plain_stream=decrypted_stream,
            associated_data=associated_data.encode()
    )
    decrypted_stream.seek(0)

    with open(
            "decrypted.txt",
            "wb"
    ) as result:
        result.write(decrypted_stream.read())

    plaintext_in_stream = None
    decrypted_text_in_stream = None
    with open("decrypted.txt","r") as f:
        decrypted_text_in_stream = f.readline()
    with open("plaintext.txt","r") as f:
        plaintext_in_stream = f.readline()

    assert plaintext_in_stream == decrypted_text_in_stream
    
    # remove the files
    os.remove("plaintext.txt")
    os.remove("decrypted.txt")

def compare_flow(access_key, arx_url, server_signing_key, server_secret_key):
    if not access_key or not arx_url or not server_signing_key or not server_secret_key:
        # skip test if the environment variables are not set
        pytest.skip("Environment variables are not set")
        
    encryption_engine = encrypt_engine(access_key, arx_url, server_signing_key, server_secret_key)
    compare_encrypted_decrypted_text(encryption_engine)
    compare_encrypted_decrypted_stream(encryption_engine)

def test_encrypt_aes_128(): 
    access_key = os.getenv('AES_128_ACCESS_KEY')
    arx_url = os.getenv('AES_128_ARX_URL')
    server_signing_key = os.getenv('AES_128_SIGNING_KEY')
    server_secret_key = os.getenv('AES_128_SECRET_KEY')
    
    compare_flow(access_key, arx_url, server_signing_key, server_secret_key)
    
def test_encrypt_aes_256():
    access_key = os.getenv('AES_256_ACCESS_KEY')
    arx_url = os.getenv('AES_256_ARX_URL')
    server_signing_key = os.getenv('AES_256_SIGNING_KEY')
    server_secret_key = os.getenv('AES_256_SECRET_KEY')
    
    compare_flow(access_key, arx_url, server_signing_key, server_secret_key)
    
def test_encrypt_xchacha():
    access_key = os.getenv('XCHACHA_ACCESS_KEY')
    arx_url = os.getenv('XCHACHA_ARX_URL')
    server_signing_key = os.getenv('XCHACHA_SIGNING_KEY')
    server_secret_key = os.getenv('XCHACHA_SECRET_KEY')
    
    compare_flow(access_key, arx_url, server_signing_key, server_secret_key)

    