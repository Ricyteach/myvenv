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
    def gen_calltracked():
        """Generates a function that tracks whether it has been called."""

        def call_tracked(*args, **kwargs):
            call_tracked.called = True

        call_tracked.called = False
        return call_tracked

    return gen_calltracked


@pytest.fixture()
def tracked_create(gen_tracked_f):
    original, cli.create = cli.create, gen_tracked_f()
    yield cli.create
    cli.create = original


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.main, catch_exceptions=False)
    assert result.exit_code == 0


def test_create(patched_envs, tracked_create):
    vnv_name = "test_create"
    runner = CliRunner()
    result = runner.invoke(cli.main, ["create", vnv_name], catch_exceptions=False)
    assert result.exit_code == 0
    assert cli.create.called


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
