# coding=utf8
import pathlib
import re

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

txt = (here / 'borax' / '__init__.py').read_text()
version = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]

lib_classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    'Operating System :: OS Independent'
]

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='borax',
    version=version,
    python_requires='>=3.5',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT',
    author='kinegratii',
    author_email='zhenwei.yan@hotmail.com',
    classifiers=lib_classifiers,
    description='A tool collections.(Chinese-Lunar-Calendars/Python-Patterns)',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
