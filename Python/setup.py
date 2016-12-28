#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""setup.py
"""
import setuptools

import optlib

setuptools.setup(
    name="optlib",
    version=optlib.__version__,
    license="MIT LICENSE",
    url="https://github.com/nasyxx/Optlib",

    author="Nasy",
    author_email="sy_n@me.com",

    description="An Options Library",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=["scipy"],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
