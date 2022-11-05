from pathlib import Path
from readmegen import readme_gen

import pytest


def test_prerequisites():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content: str = f"""metadata:
    {readme_gen.ProjectDefConst.NAME}: The best repo in the history of the World
    {readme_gen.ProjectDefConst.DESCRIPTION}: Something
    {readme_gen.ProjectDefConst.PREREQUISITES}:
    - One
    - Media/path/two
"""
    yaml_file.write_text(content)
    readme_gen.generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert f"|One|[Artifactory/{readme_gen.ProjectDefConst.INSTALL_SETUP_PATH}][1]|" in lines_in_readme
    assert "|two|[Artifactory/Media][2]|" in lines_in_readme
    assert (
        f"[1]: {readme_gen.ProjectDefConst.ARTIFACTORY_URL}/{readme_gen.ProjectDefConst.INSTALL_SETUP_PATH}/One"
        in lines_in_readme
    )
    assert f"[2]: {readme_gen.ProjectDefConst.ARTIFACTORY_URL}/Media/path/two" in lines_in_readme


def test_prerequisites_tool():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content: str = f"""metadata:
    {readme_gen.ProjectDefConst.NAME}: The best repo in the history of the World
    {readme_gen.ProjectDefConst.DESCRIPTION}: Something
    {readme_gen.ProjectDefConst.PREREQUISITES}:
    - One
"""
    yaml_file.write_text(content)
    readme_gen.generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert f"|One|[Artifactory/{readme_gen.ProjectDefConst.INSTALL_SETUP_PATH}][1]|" in lines_in_readme
    assert (
        f"[1]: {readme_gen.ProjectDefConst.ARTIFACTORY_URL}/{readme_gen.ProjectDefConst.INSTALL_SETUP_PATH}/One"
        in lines_in_readme
    )


def test_prerequisites_media():
    yaml_file: Path = Path.cwd() / pytest.yaml_filename
    yaml_file.touch()
    content: str = f"""metadata:
    {readme_gen.ProjectDefConst.NAME}: The best repo in the history of the World
    {readme_gen.ProjectDefConst.DESCRIPTION}: Something
    {readme_gen.ProjectDefConst.PREREQUISITES}:
    - Media/path/two
"""
    yaml_file.write_text(content)
    readme_gen.generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|two|[Artifactory/Media][1]|" in lines_in_readme
    assert f"[1]: {readme_gen.ProjectDefConst.ARTIFACTORY_URL}/Media/path/two" in lines_in_readme
