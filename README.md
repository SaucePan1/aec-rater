Product rater
-------------

Product rater repository.

### Installation
In order to work on this project you need to have installed:

* [Poetry](https://python-poetry.org/docs/#installation)
* Python 3.10 (you can use [pyenv](https://github.com/pyenv/pyenv#automatic-installer))

### Development
To start developing you need to install the dependencies:

```bash
poetry install
```

Then, you can activate the virtual environment that Poetry creates for you:

```bash
poetry shell
```

Finally, **you must install the pre-commits** that will run the linters on commit:

```bash
poetry run pre-commit install
```
