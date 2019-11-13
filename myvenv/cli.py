import pathlib
import click
import subprocess


@click.command()
@click.argument("path", type=click.Path())
@click.option("--install", "-i", "install_list", multiple=True)
def main(path, install_list):
    path = pathlib.Path(path)
    subprocess.run(["mkdir", str(path)], check=True)
    subprocess.run(["virtualenv", str(path/"venv")], check=True)
    windows = isinstance(path, pathlib.WindowsPath)
    if windows:
        if install_list:
            subprocess.run([str(path/"venv/Scripts/python"), "-m", "pip", "install", *install_list], check=True)
        # TODO: this does not activate the virtual environement as expected in Windows
        subprocess.run([str(path / r"venv/Scripts/activate.bat")], check=True)
    else:
        # assume posix
        if install_list:
            subprocess.run([str(path/"venv/bin/python"), "-m", "pip", "install", *install_list], check=True)
        # TODO: this does not activate the virtual environement as expected in Posix
        subprocess.run(["source", str(pathlib.Path(r"venv\bin\activate"))], check=True)
