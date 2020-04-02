import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hacking-tools",
    version="1.0.0",
    author="raminjafary",
    author_email="raminjafary1993@gmail.com",
    description="Python utilities for ethical hacking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raminjafary/ethical-hacking",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
