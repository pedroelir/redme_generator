from pathlib import Path
from readmegen import readme_gen

import pytest


def test_libs_sources():
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
    {readme_gen.ProjectDefConst.LIBS_SOURCES}:
    - github.com/awsesome/source
    - github.com/best/source_indeed
"""
    yaml_file.write_text(content)
    readme_gen.generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|source|[github.com/awsesome/source](github.com/awsesome/source)|" in lines_in_readme
    assert "|source_indeed|[github.com/best/source_indeed](github.com/best/source_indeed)|" in lines_in_readme
