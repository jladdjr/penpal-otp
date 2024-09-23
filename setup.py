from setuptools import setup, find_packages

# TODO: fill out information, pick unused package name

setup(
    name='penpal-otp',
    version='0.1.0',
    description='CLI for encrypting and decrypting messages using one-time pads',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jladdjr/penpal',
    author='Jim Ladd',
    author_email='your_email@example.com',
    license='GPLv3',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
