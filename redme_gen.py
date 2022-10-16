from pathlib import Path
from typing import Dict

import yaml
import requests


class ProjectDefConst:
    YAML_FILE: str = "sample.yaml"
    PY_PKGS_FILE: str = "requirements.txt"
    TITLE: str = "Title"
    DESCRIPTION: str = "Description"
    ARTIFACTORY_URL: str = "myartifactpry.mycompany.com/myorganization"
    SIMPLE_PATH: str = "python/coolpackages/simple"


def get_friendly_name(path: str) -> str:
    parts: list[str] = path.split("/")
    return parts[-1]


def get_link_name(path: str) -> str:
    parts: list[str] = path.split("/")
    if len(parts) == 1:
        return "Artifactory/InstallationSetups"
    else:
        return f"Artifactory/{parts[0]}"


def get_link(path: str) -> str:
    parts: list[str] = path.split("/")
    if len(parts) == 1:
        return f"{ProjectDefConst.ARTIFACTORY_URL}/InstallationSetups/{path}"
    else:
        return f"{ProjectDefConst.ARTIFACTORY_URL}/{path}"


def get_python_link(package: str):
    # pack_url: str = f"https://pypi.org/simple/{package}/"
    pack_req = requests.get(f"https://pypi.org/simple/{package}/")
    if pack_req.status_code == 200:
        return f"https://pypi.org/project/{package}/"
    return f"{ProjectDefConst.ARTIFACTORY_URL}/{ProjectDefConst.SIMPLE_PATH}/{package}"


def get_python_src(package: str):
    # pack_url: str = f"https://pypi.org/simple/{package}/"
    pack_req = requests.get(f"https://pypi.org/simple/{package}/")
    if pack_req.status_code == 200:
        return f"PYPI {package}"
    return "Artifactory/python_packages"


def generate_readme():
    yaml_file: str = ProjectDefConst.YAML_FILE
    req_file: str = ProjectDefConst.PY_PKGS_FILE
    with open(yaml_file) as file:
        project_def: Dict = yaml.safe_load(file)
    with open(req_file) as file:
        packages: list[str] = [line.strip().split("=")[0] for line in file]
    content: str = ""
    content += f"# {project_def[ProjectDefConst.TITLE]}\n"
    content += f" {project_def[ProjectDefConst.DESCRIPTION]}\n\n"
    content += "## Dependencies\n"
    content += "Dependencies got from Artifactory\n"
    content += "|Dependency|Link|\n|-|-|\n"
    # content += "|for|loop|\n"
    lnk_ref: int = 1
    links_content: str = ""
    for prerequisite in project_def["prerequisites"]:
        content += f"|{get_friendly_name(prerequisite)}|[{get_link_name(prerequisite)}][{lnk_ref}]|\n"
        links_content += f"[{lnk_ref}]: {get_link(prerequisite)}\n"
        lnk_ref += 1
    content += "\n"

    content += "## Python Dependencies\n"
    content += "Dependencies from python\n"
    content += "|Dependency|Link|\n|-|-|\n"
    # content += "|for|loop|\n"
    for pkg in packages:
        content += f"|{pkg}|[{get_python_src(pkg)}][{lnk_ref}]|\n"
        links_content += f"[{lnk_ref}]: {get_python_link(pkg)}\n"
        lnk_ref += 1
    content += "\n"

    content += links_content
    #     content = """# <repo_name>\n\n\
    # ## Dependencies\n\n\
    # <dependencies_table>\n\n\
    # ## Python dependencies\n\n\
    # <python_dependecies_table>\n\n\
    # Links
    # <list_of_links>
    # """
    readme_file: Path = Path.cwd() / "README.md"
    readme_file.touch()
    readme_file.write_text(content)


if __name__ == "__main__":
    generate_readme()
