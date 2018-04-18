# coding=utf8
import re
from setuptools import setup, find_packages
from pathlib import Path


def retrieve_version():
    p = Path('borax', '__init__.py')
    with p.open(encoding='utf8') as f:
        version_file_content = f.read()
        version_match = re.findall(r"__version__\s=\s'([\d.]+)'", version_file_content)
        if version_match:
            return version_match[0]
        return RuntimeError("No version retrieved in package file.")


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
    version=retrieve_version(),
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
