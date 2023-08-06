![Status](https://img.shields.io/badge/status-alpha-red.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![CircleCI](https://circleci.com/gh/electric-data/electric-cli/tree/main.svg?style=shield&circle-token=67d43361b7c2aa039a0eef39d3617a9f481e54c5)](https://circleci.com/gh/electric-data/electric-cli/tree/main)

# Electric Data CLI

The Electric Data CLI is the command line interface utility for the [Electric Data](https://electricdata.net) geo-distributed database hosting service. It's developed in Python and the code is published under the [MIT License](https://github.com/electric-data/electric-cli/blob/master/LICENSE) at [github.com/electric-data/electric-cli](https://github.com/electric-data/electric-cli).

## Develop

You can install the CLI for local development by installing the dependencies into a Python3 environment and developing the egg:

```sh
pip install -r requirements.txt
python setup.py develop
```

This will install a `electric` binary in your local Python environment's bin folder. You can check that this is on your path with e.g.:

```sh
which electric
```

## Build

If you want to build standalone binaries, you first need to install the extra development requirements:

```sh
pip install -r dev-requirements.txt
```

Then you can build a [Pex](https://pex.readthedocs.io) executable using:

```sh
python setup.py bdist_pex --bdist-all
```

This will create a `./dist/electric` binary which you can copy and run anywhere
on your system.

Alternatively, you can build a standalone binary with an embedded Python interpretor using [PyOxidizer](https://pyoxidizer.readthedocs.io):

```sh
pyoxidizer run
```

This will create a binary at `./build/:target/debug/install/electric` that you can run on any machine with the same architecture and OS as your build machine.

## Usage

Run the `electric` command without arguments or with the `--help` flag for usage information:

```sh
electric --help
```

You can drill down into usage information for the resources / command groups and for individual commands, e.g.:

```sh
electric auth --help
electric auth login --help
```

Further [documentation is available on the Electric Data website](https://electricdata.net/docs).

## Test

Running the tests requires `nose` and `coverage`, included in the `dev-requirements.txt`.

Then, run e.g.:

```sh
nosetests --with-coverage --cover-package electric
```
