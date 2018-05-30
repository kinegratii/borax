# coding=utf8
from pathlib import Path

from setuptools import setup, find_packages

about = dict()
p = Path('borax', '__init__.py')
with p.open(encoding='utf8') as fp:
    exec(fp.read(), about)

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
    version=about['__version__'],
    packages=find_packages(exclude=['tests']),
    url='https://github.com/kinegratii/borax',
    license='MIT',
    author='kinegratii',
    author_email='kinegratii@gmail.com',
    classifiers=lib_classifiers,
    description='A util collections for Python3.',
)
