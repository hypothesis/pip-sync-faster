
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

pip-sync-faster does this by saving hashes of the given requirements files in a
JSON file within the virtualenv and not calling pip-sync if the hashes haven't
changed.
If any of the given requirements files doesn't have a matching cached hash then
pip-sync-faster calls pip-sync forwarding all command line arguments and
options.

## pip-sync-faster doesn't sync modified virtualenvs

If you modify your requirements files pip-sync-faster will notice the change
and call pip-sync. But if you modify your virtualenv without modifying your
requirements files (for example by running a manual `pip install` command in
the virtualenv) pip-sync-faster will *not* call pip-sync because the
requirements files haven't changed and still match their cached hashes.

Calling pip-sync directly in this case would re-sync your virtualenv with your
requirements files, but calling pip-sync-faster won't.

If you can live with this limitation then you can use pip-sync-faster and save
yourself a few hundred milliseconds.  If not you should just use pip-sync.
