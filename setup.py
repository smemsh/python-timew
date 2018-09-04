#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(setup_requires=['pbr'],
      pbr=True,
      packages=find_packages('timew'),
      )
