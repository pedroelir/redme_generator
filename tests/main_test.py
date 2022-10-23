from pathlib import Path
from readmegen.readme_gen import main

import pytest


def test_main_no_yaml():
    with pytest.raises(SystemExit):
        main()


def test_main_yaml_no_metadata():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = """name: The best repo in the history of the World
description: Something
prerequisites:
- One
- Two
- path/one
- path/two
- second/path/one
- second/path/two
"""
    yaml_file.write_text(content)
    with pytest.raises(SystemExit):
        main()


def test_main_yaml_no_content():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    with pytest.raises(SystemExit):
        main()


def test_main_populated_yaml():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Two
    - path/one
    - path/two
    - second/path/one
    - second/path/two
"""
    yaml_file.write_text(content)
    main()
    readme_file: Path = Path.cwd() / "README.md"
    configfile: Path = Path.cwd() / pytest.conf_finename
    assert configfile.exists()
    assert readme_file.exists()
