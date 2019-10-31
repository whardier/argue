#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    README = readme_file.read()


setup(
    name='argue',
    version='2019.10.30',
    description='Simple tool to execute commands after rearranging command line arguments',
    long_description=README,
    author='Shane R. Spencer',
    author_email='shane@bogomip.com',
    url='https://github.com/whardier/argue',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    #package_data={'argue': ['*.json']},
    #include_package_data=True,
    #zip_safe=False,
    keywords='argue argument',
    entry_points={
        'console_scripts': [
            'argue = argue.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
