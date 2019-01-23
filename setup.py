#!/usr/bin/env python3

from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    setup_requires=['setuptools-scm'],
    name='timew',
    use_scm_version=True,
    author='Tjaart van der Walt',
    author_email='tjaart@tjaart.org',
    description='Python bindings for your timewarrior database',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Homepage': 'https://tjaart.gitlab.io/python-timew',
        'Bug Tracker': 'https://gitlab.com/tjaart/python-timew/issues',
        'Documentation': 'https://gitlab.com/tjaart/python-timew',
        'Source Code': 'https://gitlab.com/tjaart/python-timew'
    },
    packages=find_packages(),#should return ['timew','tests']
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3'],
    keywords='timewarrior',
    license='MIT'
)
