import os
import click
import pathlib
import subprocess

try:
    _ENVS = pathlib.Path(os.environ["HOMEPATH"]) / ".envs"
except KeyError:
    _ENVS = pathlib.Path(os.environ["PATH"]) / ".envs"
_VNV = "vnv"
_PATH_OPTION_USED = "_path_option_used"
_VENV_PATH_TYPE = click.Path(exists=False, file_okay=False, allow_dash=False)


class MyVenvError(Exception):
    pass


def handle_path(ctx, param, value):
    """Use as a callback for venv path parameters because multiple venv paths should not be specified.
    The path is also patched to be under the user/.envs directory.
    """
    ctx.ensure_object(dict)
    if value:
        # check if another option was already specified
        try:
            used_param = ctx.obj[_PATH_OPTION_USED]
        except KeyError:
            ctx.obj[_PATH_OPTION_USED] = param
            value = _ENVS / value
        else:
            raise MyVenvError(f"Conflicting options: {param!r} and {used_param!r}")
    return value


@click.command(_VNV)  # click 7.1 only: ## , no_args_is_help=True)
@click.option("--create", "-c", type=_VENV_PATH_TYPE, nargs=1, callback=handle_path)
@click.option("-ls", nargs=0, callback=handle_path)
@click.pass_context
def main(ctx, **kwargs):
    try:
        option = ctx.obj[_PATH_OPTION_USED].human_readable_name
    except KeyError:
        pass
    else:
        value = ctx.params[option]
        globals()[option](value)


def create(vnv_path):
    return subprocess.run(["virtualenv", str(vnv_path.resolve())], check=True, capture_output=True)


def ls():
    return subprocess.run(["ls", str(_ENVS.resolve())], check=True, capture_output=True, encoding="UTF8")
