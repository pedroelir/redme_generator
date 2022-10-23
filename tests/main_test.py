from pathlib import Path
from readmegen import readme_gen

import pytest


def test_main_no_yaml():
    with pytest.raises(SystemExit):
        readme_gen.main()


def test_main_yaml_no_metadata():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = f"""{readme_gen.ProjectDefConst.NAME}: The best repo in the history of the World
{readme_gen.ProjectDefConst.DESCRIPTION}: Something
{readme_gen.ProjectDefConst.PREREQUISITES}:
- One
- Two
- path/one
- path/two
- second/path/one
- second/path/two
"""
    yaml_file.write_text(content)
    with pytest.raises(SystemExit):
        readme_gen.main()


def test_main_yaml_no_content():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    with pytest.raises(SystemExit):
        readme_gen.main()


def test_main_populated_yaml():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = f"""metadata:
    {readme_gen.ProjectDefConst.NAME}: The best repo in the history of the World
    {readme_gen.ProjectDefConst.DESCRIPTION}: Something
    {readme_gen.ProjectDefConst.PREREQUISITES}:
    - One
    - Two
    - path/one
    - path/two
    - second/path/one
    - second/path/two
"""
    yaml_file.write_text(content)
    readme_gen.main()
    readme_file: Path = Path.cwd() / "README.md"
    configfile: Path = Path.cwd() / pytest.conf_finename
    assert configfile.exists()
    assert readme_file.exists()
