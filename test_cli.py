import subprocess

import pytest
from click.testing import CliRunner
from myvenv.cli import main


@pytest.mark.parametrize('path, install', [
    ('path', []),
    ('path', ['click', 'pent']),
])
def test_main(tmp_path, path, install):
    runner = CliRunner()
    if install:
        result = runner.invoke(main, [str(tmp_path/path), '-i', *install])
    else:
        result = runner.invoke(main, [str(tmp_path/path)])
    assert result.exit_code == 0
