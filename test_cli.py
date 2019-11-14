import pytest
from click.testing import CliRunner
from myvenv.cli import main


@pytest.mark.parametrize('path, install', [
    ('venv', []),
    ('venv', ['click', 'pent']),
])
def test_main(tmp_path, path, install):
    runner = CliRunner()
    if install:
        result = runner.invoke(main, [str(tmp_path/path), 'install', *install], catch_exceptions=False)
    else:
        result = runner.invoke(main, [str(tmp_path/path)], catch_exceptions=False)
    assert result.exit_code == 0
