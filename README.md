<a href="https://github.com/hypothesis/pip-sync-faster/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/hypothesis/pip-sync-faster/CI/main"></a>
<a href="https://pypi.org/project/pip-sync-faster"><img src="https://img.shields.io/pypi/v/pip-sync-faster"></a>
<a><img src="https://img.shields.io/badge/python-3.10 | 3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/pip-sync-faster/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# pip-sync-faster

A wrapper that makes pip-sync faster.

For installation instructions see [INSTALL.md](https://github.com/hypothesis/pip-sync-faster/blob/main/INSTALL.md).

For how to set up a pip-sync-faster development environment see
[HACKING.md](https://github.com/hypothesis/pip-sync-faster/blob/main/HACKING.md).

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
