from importlib.metadata import version
from subprocess import CalledProcessError

import pytest

from pip_sync_faster.cli import cli


def test_cli(pip_sync_faster):
    cli(["requirements/dev.txt", "--foo", "bar"])

    pip_sync_faster.assert_called_once_with(["requirements/dev.txt"])


def test_version(capsys):
    cli(["--version"])

    assert (
        capsys.readouterr().out.strip()
        == f"pip-sync-faster, version {version('pip-sync-faster')}"
    )


def test_if_pip_sync_fails(pip_sync_faster):
    pip_sync_faster.side_effect = CalledProcessError(23, ["pip-sync"])

    exit_code = cli(["requirements/dev.txt"])

    # It echoes pip-sync's exit code.
    assert exit_code == 23


@pytest.fixture(autouse=True)
def pip_sync_faster(mocker):
    return mocker.patch("pip_sync_faster.cli.pip_sync_faster", autospec=True)
