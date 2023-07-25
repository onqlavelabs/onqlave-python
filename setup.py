from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='onqlave-python-sdk-pilot',
    version='0.0.15',
    author='Onqlave Pty',
    author_email='dc@onqlave.com',
    description='A SDK to use the encryption service provided by The Onqlave Platform',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/onqlavelabs/onqlave-python/tree/dev',  # Replace with your package URL
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='encryption',
    install_requires=requirements
)
