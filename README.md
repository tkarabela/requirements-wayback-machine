# Requirements.txt Wayback Machine

_Note: This is script is not developed or endorsed by the
[Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/)
or other official Python body._

## Usage

Suppose your `requirements.txt` looks like this:

```
requests
packaging
```

If you'd like to know what additional specifications you should add
to get similar resolution as on (for example) 3rd December 2021,
run `requirements_wayback_machine` like this:

```sh
requirements_wayback_machine.py -r requirements.txt -d 2021-12-03
```

It will print your `requirements.txt` with helpful annotations:

```
# requirements_wayback_machine: reference date 2021-12-03
# requirements_wayback_machine: requests<=2.26.0
requests
# requirements_wayback_machine: packaging<=21.3
packaging
```

## License

MIT - see [LICENSE.txt](./LICENSE.txt).
