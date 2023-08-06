#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

__author__ = 'Heitor Hirose'

setup(
    name='ApTester',
    version='0.1.4',
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'aptester=Aptester.core:main',
            'Aptester=Aptester.core:main'
        ],
    },
    description='Auto Tester for Competitive programming',
    author='Heitor Hirose',
    author_email='Heitorhirose@gmail.com',
    url='https://github.com/HEKUCHAN/Auto-Python-Tester',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['Image Registration'],
    license='MIT License',
    install_requires=[
        "pathlib",
        "argparse",
        "fabric3",
        "rich"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
