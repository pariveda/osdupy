import os
import setuptools

# Get version.
with open(os.path.join('VERSION')) as f:
    version = f.read().strip()

# Get long description.
with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name="osdupy",
    version=version,
    author="Pariveda Solutions, Inc.",
    author_email="mike.duffy@parivedasolutions.com",
    description="A simple python client for interacting with the OSDU API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pariveda/osdupy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)