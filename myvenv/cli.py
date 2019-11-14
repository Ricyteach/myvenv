import pathlib
import click
import subprocess


@click.group()
@click.argument("path", type=click.Path(exists=False, file_okay=False, allow_dash=False))
@click.pass_context
def main(ctx, path):
    path = pathlib.Path(path)
    ctx.obj = dict(path = path)
    subprocess.run(["mkdir", str(path)], check=True)
    subprocess.run(["virtualenv", str(path/"venv")], check=True)


@main.command()
@click.argument("install", nargs=-1)
@click.pass_context
def install(ctx, install):
    path = ctx.obj['path']
    windows = isinstance(path, pathlib.WindowsPath)
    if windows:
        if install:
            subprocess.run([str(path/"venv/Scripts/python"), "-m", "pip", "install", *install], check=True)
        # TODO: this does not activate the virtual environment as expected in Windows
        subprocess.run([str(path / r"venv/Scripts/activate.bat")], check=True)
    else:
        # assume posix
        if install:
            subprocess.run([str(path/"venv/bin/python"), "-m", "pip", "install", *install], check=True)
        # TODO: this does not activate the virtual environment as expected in Posix
        subprocess.run(["source", str(pathlib.Path(r"venv\bin\activate"))], check=True)
