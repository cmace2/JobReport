#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pip',
    'selenium',
    'python-dotenv',
    'robin_stocks',
    'tqdm',
    'importlib_resources',
    'chromedriver-autoinstaller',
    'boto3',
    'dynamodb_json',
    'pandas'
    ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Ryan James Walden",
    author_email='waldenr1@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An easy way to see hirring trends for any publicly listed company.",
    entry_points={
        'console_scripts': [
            'JobReport=JobReport.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='JobReport',
    name='JobReport',
    packages=find_packages(include=['JobReport', 'JobReport.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rjdoubleu/JobReport',
    version='0.1.0',
    zip_safe=False,
)
