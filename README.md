# Description
This Python SDK is designed to help developers easily integrate Onqlave `Encryption As A Service` into their python backend.


[![License](https://img.shields.io/github/license/onqlavelabs/onqlave-go)](https://github.com/onqlavelabs/onqlave-go/blob/main/LICENSE)


# Table of Contents

- [Description](#description)
- [Table of Contents](#table-of-contents)
	- [Features](#features)
	- [Installation](#installation)
		- [Requirements](#requirements)
		- [Configuration](#configuration)
		- [Usage](#usage)
		- [Encrypt](#encrypt)
		- [Decrypt](#decrypt)
		- [Encrypt Stream](#encrypt-stream)
		- [Decrypt Stream](#decrypt-stream)
	- [Reporting a Vulnerability](#reporting-a-vulnerability)

## Features
- Encrypt/decrypt pieces of information
- Encrypt/decrypt stream of data

## Installation

### Requirements

- Python 3.8 and above

### Configuration
To install, simply using this command:

```bash
pip install onqlave-python-sdk-pilot
```
You can also check the [package detail on PyPI](https://pypi.org/project/onqlave-python-sdk-pilot)

## Usage
To use this SDK, you firstly need to obtain credentials to access an Onqlave Arx by signing up to [Onqlave](https://onqlave.com) and following instruction to create your first Onqlave Arx. Documentation can be found at [Onqlave Technical Documentation](https://docs.onqlave.com).

The [Onqlave Python](https://github.com/onqlavelabs/onqlave-python) module is used to perform operations on the configured Arx such as encrypting and decryptin for an Onqlave Arx. 

To use this module, an Onqlave client should be initialized as follows.
(Please note that there are 3 ways of loading configurations specified in the **examples/** directory.)

```python
from onqlave.encryption import options
from onqlave.encryption.encryption import Encryption
from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings

cred_file_path = "credentials.json"

arx_option = options.ArxOption()
credential_option = Credential()

arx_option.load_arx_url_from_json(cred_file_path)
credential_option.load_config_from_json(cred_file_path)

retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2) 

encryption_engine = Encryption(
    debug_option=debug_option,
    arx_option=arx_option,
    credential_option=credential_option,
    retry_setting=retry_option
)
```


### Encrypt

To encrypt data, use the **encrypt(plaintext: bytearray, associated_data: bytearray)** method of the `Encryption` service. The **plaintext** parameter is the `bytearray` representation of data you are wishing to encrypt. The **associated_data** parameter the `bytearray` representation of associated data which can be used to improve the authenticity of the data (it is not mandatory), as shown below.

```python
plaintext = "hello world" # your data goes here
associated_data = "auth" # your authentication data goes here
cipher_text = encryption_engine.encrypt(plaintext.encode(), associated_data.encode())
```

### Decrypt

To decrypt data, use the **decrypt(cipher_data: bytearray, associated_data: bytearray)** method of the `Encryption` service. The **cipher_data** parameter is the `bytearray` representation of data you are wishing to decrypt (previousely encrypted). The **associated_data** parameter the `bytearray` representation of associated data which can be used to improve the authenticity of the data (it is not mandatory), as shown below.

```python
decrypted_ciphertext = encryption_engine.decrypt(cipher_text,associated_data.encode())
```

### Encrypt Stream
To encrypt stream of data, use the **encrypt_stream(plain_stream io.Reader, cipher_stream io.Writer, associated_data bytearray)** method of the `Encryption` service. The **plain_stream** parameter is the `io.Reader` stream of data you are wishing to encrypt. The **cipher_stream** parameter is the `io.Write` stream you are wishing to write the cipher data to. The **associated_data** parameter the `bytearray` representation of associated data which can be used to improve the authenticity of the data (it is not mandatory), as shown below.

```python
plain_file_stream = open("path to your plaintext file","rb")
plain_stream = io.BytesIO(plain_file_stream.read())
cipher_stream = io.BytesIO()
    
encryption_engine.encrypt_stream(plain_stream,cipher_stream,associated_data.encode())
cipher_stream.seek(0)
```

### Decrypt Stream
To decrypt data, use the **decrypt_stream(cipher_stream io.io.BytesIO, plain_stream io.BytesIO, associated_data []byte)** method of the `Encryption` service. The **cipher_stream** parameter is the `io.BytesIO()` stream of data you are wishing to decrypt and it was originally encrypted using [encrypt_stream](#encrypt-stream). The **plain_stream** parameter is the `io.BytesIO()` stream you are wishing to write the plain data back to. The **associated_data** parameter the `bytearray` representation of associated data which can be used to improve the authenticity of the data (it is not mandatory), as shown below.

```python
decrypted_stream = io.BytesIO()
encryption_engine.decrypt_stream(
    cipher_stream=cipher_stream,
    plain_stream=decrypted_stream,
    associated_data=associated_data.encode()
)
decrypted_stream.seek(0)

with open(
    "path to your decrypted file",
    "wb"
) as result:
    result.write(decrypted_stream.read())
```

## Reporting a Vulnerability

If you discover a potential security issue in this project, please reach out to us at security@onqlave.com. Please do not create public GitHub issues or Pull Requests, as malicious actors could potentially view them.