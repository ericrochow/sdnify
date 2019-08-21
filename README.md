# sdnify

![GitHub](https://img.shields.io/github/license/ericrochow/sdnify)
![CircleCI](https://img.shields.io/circleci/build/github/ericrochow/sdnify/master)
![TravisCI](https://img.shields.io/travis/ericrochow/sdnify/master)
[![codecov](https://codecov.io/gh/ericrochow/sdnify/branch/such_refactor/graph/badge.svg)](https://codecov.io/gh/ericrochow/sdnify)
[![codestyle](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## Overview

sdnify is meant as a quick way of gather information by running several commands, parsing the outputs, the returning values in an easily-digestible format.


This is currently a re-write of the original sdnify script that was CLI-only. The write is being done with the intention of providing more flexibility, which has brought to light no shortage of refactoring and modularity requirements.

## Installation

inside your virtual environment:

``pip install -r requirements.txt``


## Device Credentials

There are a few different options to pass device credentials:

### CLI Prompt

If no other method of credential storage is used, sdnify will fall back on prompting for a username and password. This is not only the least efficient in terms of time to results, it may also cause things to fall over for devices using 2fa, etc.

### Configuration File

Copy ``config.default`` to ``.config.yml`` in the root directory of the project and fill out with the appropriate username and password. For the love of God, ``chmod 400`` that file. Like, for real. It has a plaintext password in it.

This only really works if cloned from git right now.

### Environment Variables

sdnify will read credentals from environment variables `NETUSERNAME` and `NETPASSWORD` if they are set. These will take precedence over the configuration file.

### CLI Arguments

If you are running sdnify from the cli, it is possible to pass the `--username` and `--password` arguments. If both are passed, these will take precedence over all the above.

## Usage

### CLI

for help /path/to/python sdnify.py -h

You can add the following to your .bashrc:

``alias sdnify='/path/to/env/bin/python /path/to/sdnify/sdnify.py'``

### Slack

Planned feature enhancement to allow use as a module for use in Slack integrations.

Will require major refactors.

## FAQs

Q: What is the point of this project?
A: Mainly for fun and my own edification. If I (or others) find it useful in
   real-life, then that's a bonus.

Q: Doesn't this seem like you're trying to re-create NAPALM?
A: Yes and no. Napalm doensn't have drivers for every platform I'm looking to
   cover, nor does it have getters for everything I'm looking to track.

Q: Some of the platforms that are covered have options other than screen
   scraping available. Why stick to screen scraping?
A: Mostly to get off the ground as quickly as possible. By using screen
   scraping for everything, I can avoid needing to add additional methods. My
   goal is to move toward NETCONF/gRPC/REST where possible, but that's down the
   road.
