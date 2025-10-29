#!/usr/bin/env python3
"""
ORBIT - Uzay Keşif Simülasyonu
by Altay Kireççi
"""

from setuptools import setup, find_packages
import os

# README dosyasını oku
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Gereksinimler dosyasını oku
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pyOrbit",
    version="1.0.0",
    author="Altay Kireççi",
    author_email="altay@gmail.com",
    description="Evrenleri keşfet,analiz et ve yaratılışın sırrını bul.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/altaykirecci/pyorbit",
    project_urls={
        "Bug Reports": "https://github.com/altaykirecci/orbit/issues",
        "Source": "https://github.com/altaykirecci/orbit",
        "Documentation": "https://github.com/altaykirecci/orbit#readme",
    },
    packages=find_packages(),
    package_data={
        "orbit": [
            "loc/*.json",
            "fonts/*.ttf",
            "*.py",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Simulation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "pyorbit=orbit.__main__:main",
        ],
    },
    keywords="space, simulation, game, pygame, exploration, universe, astronomy",
    zip_safe=False,
)
