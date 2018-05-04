# coding=utf8
from setuptools import setup, find_packages

from borax import __version__, __author__

lib_classifiers = [
    "Development Status :: 5 - Production/Stable",
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
    author=__author__,
    author_email='kinegratii@gmail.com',
    classifiers=lib_classifiers,
    description='A util collections for Python3.',
)
