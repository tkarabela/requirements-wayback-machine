[![CI - build](https://img.shields.io/github/actions/workflow/status/tkarabela/requirements-wayback-machine/main.yml?branch=master)](https://github.com/tkarabela/requirements-wayback-machine/actions)
[![CI - coverage](https://img.shields.io/codecov/c/github/tkarabela/requirements-wayback-machine)](https://app.codecov.io/github/tkarabela/requirements-wayback-machine)
![MyPy checked](http://www.mypy-lang.org/static/mypy_badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/requirements-wayback-machine.svg?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/requirements-wayback-machine.svg?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requirements-wayback-machine.svg?style=flat-square)
![License](https://img.shields.io/pypi/l/requirements-wayback-machine.svg?style=flat-square)

# Requirements.txt Wayback Machine 🚂🕒️

_Note: This is script is not developed nor endorsed by the
[Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/)
or other official Python body._

If you're struggling to get correct Python dependencies for an older project,
__requirements_wayback_machine__ is a script that gets you from this `requirements.txt`:

```
torch
torchvision
imageio
```

to this:

```
# requirements_wayback_machine: reference date 2021-02-03
# requirements_wayback_machine: torch<=1.7.1
torch
# requirements_wayback_machine: torchvision<=0.8.2
torchvision
# requirements_wayback_machine: imageio<=2.9.0
imageio
```

## Installation

```sh
$ pip install requirements-wayback-machine
```

## Usage

```sh
$ requirements_wayback_machine -r <path_to_requirements.txt> -d <YYYY-MM-DD>
```

This will print annotated `requirements.txt` to console, including upper bound
specifiers that approximate dependency resolution at given date
(for each requirement line, we print the last version of that dependency
released by given date that also satisfies specifiers already present
in the input requirement line, if any).

For more information and options, run `requirements_wayback_machine -h`.

Example:

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

## License

MIT - see [LICENSE.txt](./LICENSE.txt).
