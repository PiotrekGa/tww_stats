#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='twws',
    author='Piotr Gabryś',
    author_email='piotrek.gabrys@gmail.com',
    description='',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.1.1'],
    license='MIT',
    long_description=open('README.md').read(),
    url="https://github.com/PiotrekGa/tww_stats"
)