import inspect
import os
from pathlib import Path
import pytest

from readmegen import readme_gen


@pytest.fixture(autouse=True)
def change_cwd(tmp_path):
    current_dir: str = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(current_dir)
    pkg_install_path: str = inspect.getfile(readme_gen)
    config_file_install_dir: Path = Path(pkg_install_path).parent / "readmegenconf.yaml"
    if config_file_install_dir.exists():
        os.remove(config_file_install_dir)
