#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    setup_requires=['setuptools-markdown', 'setuptools-scm'],
    name='timew',
    use_scm_version=True,
    author='Tjaart van der Walt',
    author_email='tjaart@tjaart.org',
    summary='Python bindings for your timewarrior database',
    long_description_markdown_filename='README.md',
    project_urls={
        'Homepage': 'https://tjaart.gitlab.io/python-timew',
        'Bug Tracker': 'https://gitlab.com/tjaart/python-timew/issues',
        'Documentation': 'https://gitlab.com/tjaart/python-timew',
        'Source Code': 'https://gitlab.com/tjaart/python-timew'
    },
    packages=find_packages('timew'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment:: Console',
        'Intended Audience:: Developers',
        'Operating System:: POSIX',
        'Programming Language :: Python :: 3'],
    keywords='timewarrior',
    license='MIT'
)
