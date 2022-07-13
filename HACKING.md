# Setting up Your pip-sync-faster Development Environment

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
cd pip_sync_faster
make help
```

Releasing a New Version of the Project
--------------------------------------

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

Changing the Project's Python Versions
--------------------------------------

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

Changing the Project's Python Dependencies
------------------------------------------

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
run `pip-sync requirements.txt` as a subprocess and `pip-sync` will sync the
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
