from pathlib import Path
from readmegen.readme_gen import generate_readme
from readmegen.readme_gen import ProjectDefConst


def test_python_pkgs_dependencies_links():
    yaml_file: Path = Path.cwd() / "sample.yaml"
    yaml_file.touch()
    sample_content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Media/path/two
"""
    yaml_file.write_text(sample_content)
    req_file: Path = Path.cwd() / "requirements.txt"
    req_file.touch()
    req_content: str = "black\nflake8==5.0.4\nsuperfakenoterealpackage\n"
    req_file.write_text(req_content)

    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|black|[PYPI black][3]|" in lines_in_readme
    assert "[3]: https://pypi.org/project/black/" in lines_in_readme
    assert "|flake8|[PYPI flake8][4]|" in lines_in_readme
    assert "[4]: https://pypi.org/project/flake8/" in lines_in_readme
    assert "|superfakenoterealpackage|[Artifactory/python_packages][5]|" in lines_in_readme
    assert (
        f"[5]: {ProjectDefConst.ARTIFACTORY_URL}/{ProjectDefConst.SIMPLE_PATH}/superfakenoterealpackage"
        in lines_in_readme
    )


def test_python_pkgs_pypi_no_version():
    yaml_file: Path = Path.cwd() / "sample.yaml"
    yaml_file.touch()
    sample_content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Media/path/two
"""
    yaml_file.write_text(sample_content)
    req_file: Path = Path.cwd() / "requirements.txt"
    req_file.touch()
    req_content: str = "black\n"
    req_file.write_text(req_content)

    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|black|[PYPI black][3]|" in lines_in_readme


def test_python_pkgs_pypi_with_version():
    yaml_file: Path = Path.cwd() / "sample.yaml"
    yaml_file.touch()
    sample_content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Media/path/two
"""
    yaml_file.write_text(sample_content)
    req_file: Path = Path.cwd() / "requirements.txt"
    req_file.touch()
    req_content: str = "flake8==5.0.4\n"
    req_file.write_text(req_content)

    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|flake8|[PYPI flake8][3]|" in lines_in_readme


def test_python_pkgs_no_pypi():
    yaml_file: Path = Path.cwd() / "sample.yaml"
    yaml_file.touch()
    sample_content = """metadata:
    name: The best repo in the history of the World
    description: Something
    prerequisites:
    - One
    - Media/path/two
"""
    yaml_file.write_text(sample_content)
    req_file: Path = Path.cwd() / "requirements.txt"
    req_file.touch()
    req_content: str = "superfakenoterealpackage\n"
    req_file.write_text(req_content)

    generate_readme()
    readme_file: Path = Path.cwd() / "README.md"
    assert readme_file.exists()
    lines_in_readme: list[str] = readme_file.read_text().split("\n")
    assert "|superfakenoterealpackage|[Artifactory/python_packages][3]|" in lines_in_readme
