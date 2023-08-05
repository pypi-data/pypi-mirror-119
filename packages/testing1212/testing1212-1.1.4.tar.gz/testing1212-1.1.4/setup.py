import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Rahul Kumar",
    author_email="rahul@trell.in",
    name='testing1212',
    description='Utility code',
    version="v1.1.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/Rahultrel/testing',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)
