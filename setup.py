#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from io import open
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(HERE, "VERSION")

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()
with open("HISTORY.md", mode="r", encoding="utf-8") as f:
    history = f.read()
with open("reqs/requirements.txt") as reqs:
    requires = reqs.read().splitlines()
    requires = (require for require in requires if not require.startswith("-"))
    print("requires={}".format(requires))
# with open("reqs/requirements-test.txt") as reqs:
# test_requires = reqs.read().splitlines()

test_requires = ["codecov", "pytest-cov", "pytest-mock", "pytest"]


def find_current_version():
    """
    Reads the current version number from the VERSION file.

    Args:
      None
    Returns:
      A string containing the current version number.
    """
    with open(VERSION_FILE) as v:
        return v.read()


def update_version(new_version):
    """
    Increments the version number.

    Args:
      None
    Returns:
      A string containing the updated version number.
    """
    with open(VERSION_FILE, "w+") as v:
        for line in v:
            v.write(new_version)
        return find_current_version()


def generate_version():
    """
    """
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    current_version = find_current_version()
    if current_version.startswith("{}.{}.{}".format(year, month, day)):
        minor_version = int(current_version[-1]) + 1
        new_version = update_version(
            "{}.{}.{}.{}".format(year, month, date, minor_version)
        )
    else:
        new_version = update_version("{}.{}.{}.0".format(year, month, day))
    return new_version


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
        else:
            self.pytest_args = ["-n", "auto"]
            # self.pytest_args = ["--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


about = {}
with open(
    os.path.join(HERE, "sdnify", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

packages = find_packages(exclude=["tests"])
version = find_current_version()

setup(
    author=about["__author__"],
    author_email=about["__author_email__"],
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
    cmdclass={"test": PyTest},
    description=about["__description__"],
    download_url="{}/archive/{}.zip".format(about["__github_url__"], version),
    extras_require={
        "docs": ["Sphinx", "SimpleHTTPServer", "sphinx_rtd_theme"]
    },
    entry_points={"console_scripts": ["sdnify = sdnify.interfaces.cli:main"]},
    include_package_data=True,
    install_requires=requires,
    license=[""],
    long_description=readme,
    name=about["__title__"],
    package_data={"": ["LICENSE", "NOTICE"], "sdnify": [""]},
    package_dir={"sdnify": "sdnify"},
    packages=packages,
    project_urls=about["__urls__"],
    python_requires=">=3.5",
    tests_require=test_requires,
    url=about["__url__"],
    version=generate_version(),
    zip_safe=False,
)
