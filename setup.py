#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    setup_requires=['pbr', 'setuptools-markdown'],
    pbr=True,
    packages=find_packages('timew'),
    long_description_markdown_filename='README.md'
)
