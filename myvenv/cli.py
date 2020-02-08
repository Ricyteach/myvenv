import os
import click
import pathlib
import subprocess

# main cli app name
_VNV = "vnv"
# name of folder containing user environments
_ENVS_NAME = ".envs"

# location of user environments
try:
    _ENVS = pathlib.Path(os.environ["HOMEPATH"]) / ".envs"
except KeyError:
    _ENVS = pathlib.Path(os.environ["PATH"]) / ".envs"


class MyVenvError(Exception):
    pass


def handle_env_name(ctx, param, value):
    """Use as a callback for venv path parameters because multiple venv paths should not be specifiied.
    The path is also patched to be under the user/.envs directory.
    """
    if value:
        value = _ENVS / value
    return value


def env_path_argument(exists=False):
    """A decorator for defining the virtual environment name argument"""
    _venv_name_type = click.Path(exists=exists, file_okay=False, allow_dash=False)
    env_name_arg = click.argument("env_path", type=_venv_name_type, callback=handle_env_name)
    return env_name_arg


class _VenvPath(click.Path):

    def coerce_path_result(self, rv):
        return super().coerce_path_result(rv)


@click.group(_VNV)
def main():
    pass


@main.command()
@env_path_argument()
def create(env_path):
    env_path_str = f'"{env_path.resolve()!s}"'
    subprocess.run(["virtualenv", env_path_str], check=True)
