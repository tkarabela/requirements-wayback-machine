[![CI - build](https://img.shields.io/github/actions/workflow/status/tkarabela/requirements-wayback-machine/main.yml?branch=master)](https://github.com/tkarabela/requirements-wayback-machine/actions)
[![CI - coverage](https://img.shields.io/codecov/c/github/tkarabela/requirements-wayback-machine)](https://app.codecov.io/github/tkarabela/requirements-wayback-machine)
[![MyPy checked](http://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/tkarabela/requirements-wayback-machine/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/requirements-wayback-machine.svg?style=flat-square)](https://pypi.org/project/requirements-wayback-machine/)
[![PyPI - Status](https://img.shields.io/pypi/status/requirements-wayback-machine.svg?style=flat-square)](https://pypi.org/project/requirements-wayback-machine/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requirements-wayback-machine.svg?style=flat-square)](https://pypi.org/project/requirements-wayback-machine/)
![License](https://img.shields.io/pypi/l/requirements-wayback-machine.svg?style=flat-square)

# Requirements.txt Wayback Machine 🚂🕒️

_Note: This script is not developed nor endorsed by the
[Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/)
or other official Python body._

```sh
$ requirements_wayback_machine -r requirements.txt -d 2021-02-03

# requirements_wayback_machine: reference date 2021-02-03
# requirements_wayback_machine: torch<=1.7.1
torch
# requirements_wayback_machine: torchvision<=0.8.2
torchvision
# requirements_wayback_machine: imageio<=2.9.0
imageio
```

Installing correct dependencies for an older Python project can be tricky, since
`pip install -r requirements.txt` can easily __install a package version that is too recent and
incompatible with the old project__. This can happen even if the `requirements.txt` file
specifies an exact version (eg. `torch==1.7.1`), since __Python packages often only specify
minimum versions of their dependencies__ (which does not prevent a new major dependency version
to be installed).

One solution to this problem is exact specification of all transitive dependencies as provided
by `pip freeze` or Pipenv/Poetry lockfiles. __If you don't have a lockfile__, this is where
Requirements.txt Wayback Machine comes in to tell you __what was the last available version
of each dependency__ by given date. Presumably __at some time in the past,
`pip install` grabbed the correct versions__, so giving an approximate date when the project
was working will help you pin the correct versions.

Tip: If you're still having trouble after adding constraints for maximum versions for all
entries in your `requirements.txt`, try listing all transitive dependencies with `pip freeze`
and running Requirements.txt Wayback Machine again on this larger `requirements.txt`
(a suggestion by u/hai_wim on Reddit). Note that you will need to remove the `==` exact
constraints that `pip freeze` adds before doing this (the Wayback Machine is trying to satisfy the existing constraints,
so using `==` doesn't really make sense, it would find no suitable version if the `==` version
is too new).

## Installation

```sh
$ pip install requirements-wayback-machine
```

## Usage

```sh
$ requirements_wayback_machine -r <path_to_requirements.txt> -d <YYYY-MM-DD>
```
For more information and options, run `requirements_wayback_machine -h`.

Example:

```sh
$ cat requirements.txt
torch
torchvision
imageio

$ requirements_wayback_machine -r requirements.txt -d 2021-02-03
# requirements_wayback_machine: reference date 2021-02-03
# requirements_wayback_machine: torch<=1.7.1
torch
# requirements_wayback_machine: torchvision<=0.8.2
torchvision
# requirements_wayback_machine: imageio<=2.9.0
imageio
```

## License

MIT - see [LICENSE.txt](./LICENSE.txt).
