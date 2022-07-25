import json
import sys

import pytest

from pip_sync_faster import sync


class TestPipSyncFaster:
    def test_if_the_hashes_match_it_doesnt_call_pip_sync(
        self, cache_hashes, get_hashes, run, requirements_files
    ):
        # Make sure that all the cached hashes are present and matching.
        cache_hashes(get_hashes(requirements_files))

        sync.sync(requirements_files)

        run.assert_not_called()

    def test_if_theres_no_cached_hashes(
        self, assert_hashes_cached, requirements_files, run
    ):
        sync.sync(requirements_files)

        run.assert_called_once_with(["pip-sync", *sys.argv[1:]], check=True)
        assert_hashes_cached(requirements_files)

    def test_if_theres_one_wrong_hash(
        self, assert_hashes_cached, cache_hashes, get_hashes, requirements_files, run
    ):
        # Make the cached hashes file contain one non-matching hash.
        hashes = get_hashes(requirements_files)
        hashes[list(hashes.keys())[0]] = "non_matching_hash"
        cache_hashes(hashes)

        sync.sync(requirements_files)

        run.assert_called_once_with(["pip-sync", *sys.argv[1:]], check=True)
        assert_hashes_cached(requirements_files)

    def test_if_theres_one_missing_hash(
        self, assert_hashes_cached, cache_hashes, get_hashes, requirements_files, run
    ):
        # Make the cached hashes file be missing one hash.
        cache_hashes(get_hashes(requirements_files[1:]))

        sync.sync(requirements_files)

        run.assert_called_once_with(["pip-sync", *sys.argv[1:]], check=True)
        assert_hashes_cached(requirements_files)

    def test_if_theres_a_different_files_hash_cached(
        self, assert_hashes_cached, cache_hashes, get_hashes, requirements_files, run
    ):
        # The cache contains correct hashes for both dev.txt and format.txt.
        cache_hashes(get_hashes(requirements_files))

        # pip-sync-faster is called with just format.txt.
        sync.sync(requirements_files[1:])

        # It should call pip-sync: the last time that pip-sync-faster was
        # called (and updated the cache) it was called with both dev.txt and
        # format.txt. Now it's being called with just format.txt. Any
        # requirements that're in dev.txt but not in format.txt need to be
        # removed from the venv.
        run.assert_called_once_with(["pip-sync", *sys.argv[1:]], check=True)
        # It should update the cache to contain only format.txt.
        assert_hashes_cached(requirements_files[1:])

    @pytest.fixture
    def cached_hashes_path(self, tmp_path):
        """Return the path where pip-sync-faster will look for its cached hashes file."""
        return tmp_path / "pip_sync_faster.json"

    @pytest.fixture
    def assert_hashes_cached(self, cached_hashes_path, get_hashes):
        def assert_hashes_cached(requirements_files):
            """Assert the cache contains correct hashes for the given requirements files."""
            with open(cached_hashes_path, "r", encoding="utf-8") as handle:
                cached_hashes = json.load(handle)
            assert cached_hashes == get_hashes(requirements_files)

        return assert_hashes_cached

    @pytest.fixture
    def cache_hashes(self, cached_hashes_path):
        def cache_hashes(hashes):
            """Cache the given hashes for the given paths."""
            with open(cached_hashes_path, "w", encoding="utf-8") as handle:
                json.dump(hashes, handle)

        return cache_hashes

    @pytest.fixture
    def requirements_files(self, tmp_path):
        """Create the test requirements files and return their paths."""
        dev_txt_path = tmp_path / "dev.txt"
        with open(dev_txt_path, "w", encoding="utf8") as handle:
            handle.write("This is a fake dev.txt requirements file.")

        format_txt_path = tmp_path / "format.txt"
        with open(format_txt_path, "w", encoding="utf8") as handle:
            handle.write("This is a fake format.txt requirements file.")

        return [str(dev_txt_path), str(format_txt_path)]

    @pytest.fixture
    def get_hashes(self, requirements_files):
        dev_txt_path = requirements_files[0]
        format_txt_path = requirements_files[1]

        hashes = {
            dev_txt_path: "a184dca1232bd16942dbefb72782abce7b251055e59be5458f22a6e25ad3a7bec4579a6f6c1c41953c4440dbe66fe97a7dcb47c36350e94412fc9814a650556a",
            format_txt_path: "e4837471e0008e297f2d4e37074f7b59b96cea821127ab825876bd76b7b079a0a80ff1e7ed50801295aa109b3300411b30fef42bec5346087aad63e9778ed806",
        }

        def get_hashes(paths):
            """Return a dict mapping the given paths to their correct hashes."""
            return {path: hashes[path] for path in paths}

        return get_hashes


@pytest.fixture(autouse=True)
def environ(mocker, tmp_path):
    return mocker.patch.dict(
        sync.environ,
        {
            # There isn't actually a virtualenv here but it doesn't matter:
            # this is just where pip-sync-faster will look for and create
            # its cached hashes file.
            "VIRTUAL_ENV": str(tmp_path.absolute()),
        },
    )


@pytest.fixture(autouse=True)
def run(mocker):
    return mocker.patch("pip_sync_faster.sync.run", autospec=True)
