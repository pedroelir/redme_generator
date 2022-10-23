import inspect
from pathlib import Path

import yaml
from readmegen import readme_gen
import pytest


@pytest.fixture()
def save_configuration():
    org_artifactory_url: str = readme_gen.ProjectDefConst.ARTIFACTORY_URL
    org_des: str = readme_gen.ProjectDefConst.DESCRIPTION
    org_libs: str = readme_gen.ProjectDefConst.LIBS_SOURCES
    org_name: str = readme_gen.ProjectDefConst.NAME
    org_prereq: str = readme_gen.ProjectDefConst.PREREQUISITES
    org_pypkgs: str = readme_gen.ProjectDefConst.PY_PKGS_FILE
    org_simple: str = readme_gen.ProjectDefConst.SIMPLE_PATH
    org_yaml: str = readme_gen.ProjectDefConst.YAML_FILE

    yield

    readme_gen.ProjectDefConst.ARTIFACTORY_URL = org_artifactory_url
    readme_gen.ProjectDefConst.DESCRIPTION = org_des
    readme_gen.ProjectDefConst.LIBS_SOURCES = org_libs
    readme_gen.ProjectDefConst.NAME = org_name
    readme_gen.ProjectDefConst.PREREQUISITES = org_prereq
    readme_gen.ProjectDefConst.PY_PKGS_FILE = org_pypkgs
    readme_gen.ProjectDefConst.SIMPLE_PATH = org_simple
    readme_gen.ProjectDefConst.YAML_FILE = org_yaml


def test_config_file_cwd_empty():
    config_file: Path = Path.cwd() / "readmegenconf.yaml"
    config_file.touch()
    readme_gen.ReadmeGenConfig.load_configuration()
    with open(config_file) as fp:
        config = yaml.safe_load(fp)
    assert config is not None


def test_config_file_site_empty():
    pkg_install_path: str = inspect.getfile(readme_gen)
    config_file_install_dir: Path = Path(pkg_install_path).parent / "readmegenconf.yaml"
    config_file_install_dir.touch()
    readme_gen.ReadmeGenConfig.load_configuration()
    with open(config_file_install_dir) as fp:
        config = yaml.safe_load(fp)
    assert config is not None
    config_file_cwd: Path = Path.cwd() / "readmegenconf.yaml"
    assert not config_file_cwd.exists()


def test_config_file_populated(save_configuration):
    config_file: Path = Path.cwd() / "readmegenconf.yaml"
    config_file.touch()
    content = """ARTIFACTORY_URL: myartifactpry.personal.com/home
DESCRIPTION: steps
LIBS_SOURCES: github_repos
NAME: title
PREREQUISITES: binary_dependencies
PY_PKGS_FILE: dependencies.txt
SIMPLE_PATH: simple/path
YAML_FILE: Definition.yaml
"""
    config_file.write_text(content)
    readme_gen.ReadmeGenConfig.load_configuration()
    assert readme_gen.ProjectDefConst.ARTIFACTORY_URL == "myartifactpry.personal.com/home"
    assert readme_gen.ProjectDefConst.DESCRIPTION == "steps"
    assert readme_gen.ProjectDefConst.LIBS_SOURCES == "github_repos"
    assert readme_gen.ProjectDefConst.NAME == "title"
    assert readme_gen.ProjectDefConst.PREREQUISITES == "binary_dependencies"
    assert readme_gen.ProjectDefConst.PY_PKGS_FILE == "dependencies.txt"
    assert readme_gen.ProjectDefConst.SIMPLE_PATH == "simple/path"
    assert readme_gen.ProjectDefConst.YAML_FILE == "Definition.yaml"
