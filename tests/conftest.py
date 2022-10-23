import inspect
import os
from pathlib import Path
import pytest

from readmegen import readme_gen


def pytest_configure(config):
    pytest.yaml_filename = readme_gen.ProjectDefConst.YAML_FILE
    pytest.conf_finename = readme_gen.ProjectDefConst.README_CONF


@pytest.fixture(autouse=True)
def change_cwd(tmp_path):
    current_dir: str = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(current_dir)
    pkg_install_path: str = inspect.getfile(readme_gen)
    config_file_install_dir: Path = Path(pkg_install_path).parent / pytest.conf_finename
    if config_file_install_dir.exists():
        os.remove(config_file_install_dir)
