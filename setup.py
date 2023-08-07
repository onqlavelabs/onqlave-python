from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

package_name = 'onqlave-python'
download_url = format('https://pypi.org/project/%s/#history' % package_name)

setup(
    name=package_name,
    version='0.1.2',
    author='Onqlave Pty',
    author_email='product@onqlave.com',
    maintainer='DC',
    maintainer_email='dc@onqlave.com',
    description='This Python SDK is designed to help developers easily integrate Onqlave Encryption As A Service into their python backend.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/onqlavelabs/onqlave-python/', 
    download_url=download_url,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
    ],
    project_urls = {
        "Home Page":"https://www.onqlave.com/",
        "Issue Tracker": "https://github.com/onqlavelabs/onqlave-python/issues",
        "Source Code": "https://github.com/onqlavelabs/onqlave-python/",
        
    },

    keywords=['encryption','privacy','sdk'],
    license='MIT',

    install_requires=requirements
)
