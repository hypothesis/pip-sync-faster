<a href="https://github.com/hypothesis/pip-sync-faster/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/pip-sync-faster/ci.yml?branch=main"></a>
<a href="https://pypi.org/project/pip-sync-faster"><img src="https://img.shields.io/pypi/v/pip-sync-faster"></a>
<a><img src="https://img.shields.io/badge/python-3.12 | 3.11 | 3.10 | 3.9-success"></a>
<a href="https://github.com/hypothesis/pip-sync-faster/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# pip-sync-faster

A wrapper that makes pip-sync faster.

pip-sync-faster makes
[pip-sync](https://pip-tools.readthedocs.io/en/latest/#example-usage-for-pip-sync)
run faster in the case where there's nothing to do because the virtualenv is
already up to date with the requirements files. On my machine, with my
requirements files, it shaves off over 500ms in the time taken to run pip-sync:

```terminal
$ time pip-sync requirements/foo.txt
Everything up-to-date

real    0m0.569s
user    0m0.525s
sys     0m0.045s

$ time pip-sync-faster requirements/foo.txt

real    0m0.037s
user    0m0.029s
sys     0m0.008s
```

`pip-sync-faster` does this by saving hashes of the given requirements files in a
JSON file within the virtualenv and not calling pip-sync if the hashes haven't
changed.
If any of the given requirements files doesn't have a matching cached hash then
pip-sync-faster calls pip-sync forwarding all command line arguments and
options.

## You need to add `pip-sync-faster` to your requirements file

A command like `pip-sync-faster requirements.txt` will call
`pip-sync requirements.txt` which will uninstall anything not in
`requirements.txt` from the active venv, including `pip-sync-faster` itself!

You can add `pip-sync-faster` to `requirements.txt` so that it doesn't get
uninstalled.

### Running `pip-sync-faster` directly instead

Alternatively as long as `pip-tools` is installed in the active venv you can
run `pip-sync-faster` directly with a command like:

```bash
PYTHONPATH=/path/to/pip-sync-faster/src python3 -m pip_sync_faster requirements.txt
```

This doesn't rely on `pip-sync-faster` being installed so there's no issue with
`pip-sync` uninstalling it.

## pip-sync-faster doesn't sync modified virtualenvs

If you modify your requirements files pip-sync-faster will notice the change
and call pip-sync. But if you modify your virtualenv without modifying your
requirements files (for example by running a manual `pip install` command in
the virtualenv) pip-sync-faster will *not* call pip-sync because the
requirements files haven't changed and still match their cached hashes.

Calling pip-sync directly in this case would re-sync your virtualenv with your
requirements files, but calling pip-sync-faster won't.

If you can live with this limitation then you can use pip-sync-faster and save
yourself a few hundred milliseconds. If not you should just use pip-sync.

## Installing

We recommend using [pipx](https://pypa.github.io/pipx/) to install
pip-sync-faster.
First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

```terminal
pipx install pip-sync-faster
```

You now have pip-sync-faster installed! For some help run:

```
pip-sync-faster --help
```

## Upgrading

To upgrade to the latest version run:

```terminal
pipx upgrade pip-sync-faster
```

To see what version you have run:

```terminal
pip-sync-faster --version
```

## Uninstalling

To uninstall run:

```
pipx uninstall pip-sync-faster
```

## Setting up Your pip-sync-faster Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/pip-sync-faster.git
cd pip-sync-faster
make help
```

## Releasing a New Version of the Project

1. First, to get PyPI publishing working you need to go to:
   <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
   and add pip-sync-faster to the `PYPI_TOKEN` secret's selected
   repositories.

2. Now that the pip-sync-faster project has access to the `PYPI_TOKEN` secret
   you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
   Publishing a new GitHub release will automatically trigger
   [a GitHub Actions workflow](.github/workflows/pypi.yml)
   that will build the new version of your Python package and upload it to
   <https://pypi.org/project/pip-sync-faster>.

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

Testing Manually
----------------

Normally if you wanted to test a command manually in dev you'd do so through
tox, for example:

```terminal
$ tox -qe dev --run-command 'pip-sync-faster --help'
usage: pip-sync-faster [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --version
```

But there's a problem with running `pip-sync-faster` commands in this way: a
command like `tox -e dev --run-command 'pip-sync-faster requirements.txt'` will
run `pip-sync requirements.txt` and `pip-sync` will sync the
current virtualenv (`.tox/dev/`) with the `requirements.txt` file. Everything
in `requirements.txt` will get installed into `.tox/dev/`, which you probably
don't want. Even worse everything _not_ in `requirements.txt` will get
_removed_ from `.tox/dev/` including `pip-sync-faster` itself!

To avoid this problem run `pip-sync-faster` in a temporary virtualenv instead.
This installs the contents of `requirements.txt` into the temporary venv so
your `.tox/dev/` env doesn't get messed up. And it does not install
`pip-sync-faster` into the temporary venv so there's no issue with `pip-sync`
uninstalling `pip-sync-faster`:

```terminal
# Make a temporary directory.
tempdir=$(mktemp -d)

# Create a virtualenv in the temporary directory.
python3 -m venv $tempdir

# Activate the virtualenv.
source $tempdir/bin/activate

# Install pip-tools in the virtualenv (pip-sync-faster needs pip-tools).
pip install pip-tools

# Call pip-sync-faster to install a requirements file into the temporary virtualenv.
PYTHONPATH=src python3 -m pip_sync_faster /path/to/requirements.txt

# When you're done testing deactivate the temporary virtualenv.
deactivate
```
