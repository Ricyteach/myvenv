from click.testing import CliRunner
import myvenv.cli as cli
import pytest
import pathlib


@pytest.fixture()
def tmp_envs_path(tmp_path):
    envs_path = tmp_path / ".envs"
    return envs_path


@pytest.fixture()
def patched_envs(monkeypatch, tmp_envs_path):
    monkeypatch.setattr(cli, "_ENVS", tmp_envs_path, raising=True)


@pytest.fixture()
def gen_tracked_f():
    def gen_calltracker():
        """Generates a function that tracks whether it has been called."""

        def call_tracker(*args, **kwargs):
            call_tracker.called = True

        call_tracker.called = False
        return call_tracker

    return gen_calltracker


@pytest.fixture()
def tracked_create(monkeypatch, gen_tracked_f):
    monkeypatch.setattr(cli, "create", gen_tracked_f())
    return cli.create


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.main, catch_exceptions=False)
    assert result.exit_code == 0


def test_create(patched_envs, tracked_create):
    arg2 = "test_create"
    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", arg2], catch_exceptions=False)
    assert result.exit_code == 0
    assert tracked_create.called


@pytest.fixture()
def tracked_ls(monkeypatch, gen_tracked_f):
    monkeypatch.setattr(cli, "ls", gen_tracked_f())
    return cli.ls


def test_ls(patched_envs, tracked_ls):
    arg2 = ""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["-ls", arg2], catch_exceptions=False)
    assert result.exit_code == 0
    assert tracked_ls.called


def is_a_venv(path):
    """An activate script in an expected location determines of it's a venv."""
    return (
        pathlib.Path(path, "Scripts", "activate").is_file()
        ^ pathlib.Path(path, "bin", "activate").is_file()
    )


@pytest.mark.skip
def test_create_func(tmp_envs_path):
    vnv_path = tmp_envs_path / "test_create_func"
    cli.create(vnv_path)
    assert is_a_venv(vnv_path)


@pytest.fixture()
def subdir_path(tmp_envs_path):
    """Make sure there is something in the temp envs directory."""
    foo = pathlib.Path(tmp_envs_path, "foo")
    foo.resolve().mkdir(parents=True)
    return foo


def test_ls_func(patched_envs, subdir_path):
    result = cli.ls()
    assert result.returncode == 0
    assert result.stdout == f"{subdir_path.name}\n"
