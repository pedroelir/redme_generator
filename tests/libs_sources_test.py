from pathlib import Path
from readmegen.readme_gen import generate_readme

import pytest


def test_libs_sources():
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
    libs_sources:
    - github.com/awsesome/source
    - github.com/best/source_indeed
"""
    yaml_file.write_text(content)
    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|source|[github.com/awsesome/source](github.com/awsesome/source)|" in lines_in_readme
    assert "|source_indeed|[github.com/best/source_indeed](github.com/best/source_indeed)|" in lines_in_readme
