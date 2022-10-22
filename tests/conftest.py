import os
import pytest


@pytest.fixture(autouse=True)
def change_cwd(tmp_path):
    current_dir: str = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(current_dir)
