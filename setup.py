# coding=utf8
from setuptools import setup, find_packages

from borax import __version__


def read_long_description():
    with open('long_description.md', encoding='utf8') as f:
        return f.read()


lib_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3 :: Only",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    'Operating System :: OS Independent'
]

setup(
    name='borax',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/kinegratii/borax',
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    classifiers=lib_classifiers,
    description='A util collections for Python3.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
)
