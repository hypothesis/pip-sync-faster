from importlib.metadata import version
from subprocess import CalledProcessError

import pytest

from pip_sync_faster.cli import cli


def test_cli(sync):
    exit_code = cli(["requirements/dev.txt", "--foo", "bar"])

    sync.assert_called_once_with(["requirements/dev.txt"])
    assert not exit_code


def test_version(capsys):
    exit_code = cli(["--version"])

    assert (
        capsys.readouterr().out.strip()
        == f"pip-sync-faster, version {version('pip-sync-faster')}"
    )
    assert not exit_code


def test_if_pip_sync_fails(sync):
    sync.side_effect = CalledProcessError(23, ["pip-sync"])

    exit_code = cli(["requirements/dev.txt"])

    # It echoes pip-sync's exit code.
    assert exit_code == 23


@pytest.fixture(autouse=True)
def sync(mocker):
    return mocker.patch("pip_sync_faster.cli.sync", autospec=True)
