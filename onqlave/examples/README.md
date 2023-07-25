These are 3 examples about how to use Onqlave Python SDK:

## Using env variables
**python-sdk-example_1.py**
This example will take the environment variables as inputs to init the encryption service. There are 4 env variables as follows:
- ONQLAVE_PYTHON_SDK_ACCESS_KEY
- ONQLAVE_PYTHON_SDK_ARX_URL
- ONQLAVE_PYTHON_SDK_SERVER_SIGNING_KEY
- ONQLAVE_PYTHON_SDK_SERVER_SECRET_KEY

These values are located in the **credentials.json** file.

How to run:
```python
python python-sdk-example_1.py
```

## Using commandline args
**python-sdk-example_2.py**
This example will take command line arguments as inputs to init the encryption service. There are 4 args as follows:
- --access_key
- --arx_url
- --server_signing_key
- --server_secret_key


How to run:
```python
python python-sdk-example_1.py  --access_key value --arx_url value --server_signing_key --server_secret_key value
```

Before run it, make sure that your installed the python sdk package:

```python
pip install onqlave-python-sdk-pilot
```

## Using configuration from JSON file
**python-sdk-example_3.py**
This example will take configuration data from a json file. Basically, when developers created APIKey in The Onqlave Platform, they are able to have a copy of the keys in JSON format and it should be saved as a secret json file. To load these configuration, take a look at the code in the provided example.