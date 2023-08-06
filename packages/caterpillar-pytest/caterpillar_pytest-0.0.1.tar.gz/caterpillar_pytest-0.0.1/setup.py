#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

VERSION = "0.0.1"

setup(
    name="caterpillar_pytest",
    version=VERSION,
    description='pytest功能增强',
    long_description=long_description,
    author='redrose2100',
    author_email='hitredrose@163.com',
    maintainer='redrose2100',
    maintainer_email='hitredrose@163.com',
    license='MIT License',
    packages=find_packages(exclude=["tests","pytest_demo"]),
    install_requires=[
        "pytest",
    ],
    platforms=["all"],
    url='https://gitee.com/redrose2020_admin/caterpillar_pytest',
    include_package_data=True,
    entry_points={
        "pytest11": ["caterpillar_pytest_pluggin = caterpillar_pytest.main"]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
)