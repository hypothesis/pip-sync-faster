from subprocess import run


def test_help():
    """Test the pip-sync-faster --help command."""
    run(["pip-sync-faster", "--help"], check=True)


def test_version():
    """Test the pip-sync-faster --version command."""
    run(["pip-sync-faster", "--version"], check=True)
