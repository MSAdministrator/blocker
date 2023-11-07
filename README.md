# blocker

[![PyPI](https://img.shields.io/pypi/v/blocker.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/blocker.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/blocker)][pypi status]
[![License](https://img.shields.io/pypi/l/blocker)][license]

[![Code Quality & Tests](https://github.com/MSAdministrator/blocker/actions/workflows/tests.yml/badge.svg)](https://github.com/MSAdministrator/blocker/actions/workflows/tests.yml)

[![Codecov](https://codecov.io/gh/MSAdministrator/blocker/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/blocker/
[tests]: https://github.com/MSAdministrator/blocker/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/MSAdministrator/blocker
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## What is blocker?

`blocker` is a Python package to check if a indicator is in a blocklist.

There are two main data definitions at this time that drive the blocker package. These defined the different locations to check against.

## Features

- Retrieve blocklist data from multiple sources
- Check if a IP address is on a DNSBL (DNS Block List)
- Collects data using multi-threading

## Installation

You can install blocker via [pip] from [PyPI]:

```console
$ pip install blocker
```

If you are using `poetry` (recommended) you can add it to your package using

```console
poetry add blocker
```

## Usage

Below is the command line reference but you can also use the current version of `blocker` to retrieve the help by typing ```blocker --help```.

```console
NAME
    blocker - Lookup is the main method to check if a given value can be identified in block lists.

SYNOPSIS
    blocker VALUE <flags>

DESCRIPTION
    The consumer of this method can toggle the different checks as needed.

POSITIONAL ARGUMENTS
    VALUE
        Type: str
        A value to lookup. This is typically going to be a domain, ip address, etc.

FLAGS
    -t, --text_list=TEXT_LIST
        Type: bool
        Default: False
        Whether or not to check text based lists. Defaults to False.
    -d, --dns_list=DNS_LIST
        Type: bool
        Default: False
        Whether or not to check dns lists. Defaults to False.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](CONTRIBUTING.md).

## Developmemt

You can clone the repositry and begin development using

```bash
git clone https://github.com/MSAdministrator/blocker.git
cd blocker
poetry install
```

If you are using `pyenv` to manage your enviroments you can set a config option in poetry to use the set pyenv version of python by running this:

```bash
poetry config virtualenvs.create true
poetry install
```

## License

Distributed under the terms of the [MIT license][LICENSE.md],
_blocker_ is free and open source software.

## Security

Security concerns are a top priority for us, please review our [Security Policy](SECURITY.md).

## Issues

If you encounter any problems,
please [file an issue](https://github.com/MSAdministrator/blocker/issues/new) along with a detailed description.

## Credits

This project was generated from [@MSAdministrator]'s [Hypermodern Python Cookiecutter] template.

[@MSAdministrator]: https://github.com/MSAdministrator
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/MSAdministrator/blocker/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/MSAdministrator/blocker/blob/main/LICENSE
[contributor guide]: https://github.com/MSAdministrator/blocker/blob/main/CONTRIBUTING.md
