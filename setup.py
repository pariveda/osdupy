import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osdupy",
    version="0.0.1",
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