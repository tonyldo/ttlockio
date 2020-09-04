import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttlockio", 
    version="0.1.5",
    scripts=['bin/create_access_token','bin/create_user_and_access_token','bin/refresh_access_token'],
    author="Antonio Campos",
    author_email="tonyldo@gmail.com",
    description="Python wrapper for TTLock API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonyldo/ttlock.io",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        l.strip() for l in Path('requirements.txt').read_text('utf-8').splitlines()
    ],
)