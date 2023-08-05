import os

from setuptools import setup

from sqlitecollections import (
    __author__,
    __description__,
    __email__,
    __package_name__,
    __version__,
)

wd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(wd, "README.md")) as fin:
    __long_description__ = fin.read()

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    license="MIT",
    url="https://github.com/osoken/sqlitecollections",
    description=__description__,
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    packages=[__package_name__],
    install_requires=[],
    extras_require={
        "dev": ["flake8", "pytest", "black", "mypy", "tox", "isort"],
        "docs": ["mkdocs", "mkdocs-material"],
    },
)
