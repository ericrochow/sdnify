# sdnify

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
