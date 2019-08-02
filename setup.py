#!/usr/bin/python
# -*- coding: utf-8 -*-
from io import open
import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
import __version__

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()
with open("HISTORY.md", mode="r", encoding="utf-8") as f:
    history = f.read()
with open("reqs/requirements.txt") as reqs:
    requires = reqs.read().splitlines()
with open("reqs/requirements-test.txt") as reqs:
    test_requires = reqs.read().splitlines()

if sys.argv[-1] == "publish_dev":
    os.system("python setup.py sdist bdist_wheel")
    os.system("devpi upload")
    sys.exit()
elif sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count

            self.pytest_args = ["-n", str(cpu_count()), "--boxed"]
        except (ImportError, NotImplementedError):
            self.pytest_args = ["-n", "1", "--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


packages = ["platforms"]

setup(
    name=__version__.__title__,
    version=__version__.__version__,
    author=__version__.__author__,
    author_email=__version__.__author_email__,
    url=__version__.__url__,
    packages=packages,
    package_data={"": ["LICENSE", "NOTICE"], "requests": [""]},
    package_dir={"requests": "requests"},
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=requires,
    license=[""],
    zip_safe=False,
    description=__version__.__description__,
    long_description=readme,
    scripts=["sdnify"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    tests_require=test_requires,
    cmdclass={"test": PyTest},
    extras_require={
        "docs": ["Sphinx", "SimpleHTTPServer", "sphinx_rtd_theme"]
    },
)
