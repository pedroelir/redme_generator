from pathlib import Path
from readmegen.readme_gen import generate_readme
from readmegen.readme_gen import ProjectDefConst

import pytest


def test_prerequisites():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Media/path/two
"""
    yaml_file.write_text(content)
    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|One|[Artifactory/InstallationSetups][1]|" in lines_in_readme
    assert "|two|[Artifactory/Media][2]|" in lines_in_readme
    assert f"[1]: {ProjectDefConst.ARTIFACTORY_URL}/InstallationSetups/One" in lines_in_readme
    assert f"[2]: {ProjectDefConst.ARTIFACTORY_URL}/Media/path/two" in lines_in_readme


def test_prerequisites_tool():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
"""
    yaml_file.write_text(content)
    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|One|[Artifactory/InstallationSetups][1]|" in lines_in_readme
    assert f"[1]: {ProjectDefConst.ARTIFACTORY_URL}/InstallationSetups/One" in lines_in_readme


def test_prerequisites_media():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - Media/path/two
"""
    yaml_file.write_text(content)
    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|two|[Artifactory/Media][1]|" in lines_in_readme
    assert f"[1]: {ProjectDefConst.ARTIFACTORY_URL}/Media/path/two" in lines_in_readme
