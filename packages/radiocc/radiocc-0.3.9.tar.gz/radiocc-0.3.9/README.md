# radiocc

[![license badge]][license file]
[![version badge]][repo url]
[![python badge]][python url]
[![coverage badge]][coverage url]
[![pre-commit badge]][pre-commit url]

> Radio occulation

---

[Installation](#installation) |
[Roadmap](#roadmap) |
[Contributing](#contributing) |
[License](#license)

---

## Installation

The code is still in development, hence you can only get it on
[ROB Gitlab repo][repo url]

You need to:

+ clone it
+ download [poetry][poetry url] (a tool for dependency management and packaging
  in Python)
+ run
  ```sh
  poetry install
  ```
  inside the project to install the dependencies in a virtual environment (it
  should be done automatically, long time I didn't do it, if it does not let us
  know and we will do it together)
+ to check the virtual env is correctly set, use
  ```sh
  poetry env info
  ```
  and confirm you have something similar to:
  ```sh
  Virtualenv
  Python:         3.9.6
  Implementation: CPython
  Path:           /home/greg/.cache/pypoetry/virtualenvs/radiocc-6zeAPCek-py3.9
  Valid:          True
  ```
+ run
  ```sh
  poetry shell
  ```
  to activate the virtual environment, it can be useful for IDE
  and linters but not necessary because it is automatically activated at runtime.
+ create a folder `RESULTS` and a folder `TO_PROCESS` and place in the latter
  your *MEX* or *MVN* scenarios to be run run `poetry run radiocc` to run the code
  automatically on the scenarios to be processed.

## Roadmap

+ improve old code for lisibility, portability and testing
+ improve CLI interface for parameter tuning
+ provide GUI interface for parameter tuning
+ provide GUI tool on graphs to set thresholds and corrections
+ provide a [`pip`][pip url] library and binary installation

## Contributing

### Evaluate code before commiting

We use the powerful tool [pre-commit][pre-commit url] to automatically run a
battery of tests on the code at commit runtime to:

+ avoid pushing code with warnings and errors
+ unify code formatting between developpers

The list of tests and hook scripts can be found here.

They consist in:

+ few git and file-system checks
+ [`flake8`][flake8 url] (python static linter)
+ [`isort`][isort url] (python imports linter & fixer)
+ [`mypy`][mypy url] (python type checker)
+ [`black`][black url] (python code fixer)
+ running tests with [`pytest`][pytest url]

You can install this development environment using

```sh
poetry run pre-commit install
```

### Commiting

You can fork and ask for pull request on the `dev` branch (or any other excepted
the `main` branch).

Depending on your access rights, you can also create a new
branch from `dev`, develop on it and ask for a merge into the `dev` branch.

## License

Licensed under the [Apache 2.0 license][license file].

[repo url]: https://gitlab-as.oma.be/gregoireh/radiocc
[pre-commit file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/.pre-commit-config.yaml
[license file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/LICENSE
[license badge]: https://img.shields.io/badge/License-Apache%202.0-blue.svg
[coverage badge]: https://img.shields.io/badge/coverage-0%25-red
[coverage url]: https://github.com/pytest-dev/pytest-cov
[version badge]: https://img.shields.io/badge/version-0.3.9-blue
[python url]: https://www.python.org/
[python badge]: https://img.shields.io/badge/python->=3.9,<3.10-blue
[pre-commit url]: https://pre-commit.com
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[poetry url]: https://python-poetry.org/docs
[flake8 url]: https://flake8.pycqa.org/en/latest
[isort url]: https://github.com/timothycrosley/isort
[mypy url]: http://mypy-lang.org
[black url]: https://github.com/psf/black
[pytest url]: https://docs.pytest.org/en/latest
[pip url]: https://pip.pypa.io/en/stable/
