from pathlib import Path
import sys
from typing import Dict

import yaml
import requests


class ProjectDefConst:
    README_CONF = "readmegenconf.yaml"
    YAML_FILE: str = "sample.yaml"
    PY_PKGS_FILE: str = "requirements.txt"
    NAME: str = "name"
    DESCRIPTION: str = "description"
    PREREQUISITES: str = "prerequisites"
    LIBS_SOURCES: str = "libs_sources"
    INSTALL_SETUP_PATH: str = "Installation_and_Setup"
    ARTIFACTORY_URL: str = "myartifactpry.mycompany.com/myorganization"
    SIMPLE_PATH: str = "python/coolpackages/simple"


class ReadmeGenConfig:
    @staticmethod
    def load_configuration() -> None:
        def create_conf(path: Path):
            configuration: dict[str, str] = {
                "YAML_FILE": ProjectDefConst.YAML_FILE,
                "PY_PKGS_FILE": ProjectDefConst.PY_PKGS_FILE,
                "NAME": ProjectDefConst.NAME,
                "DESCRIPTION": ProjectDefConst.DESCRIPTION,
                "PREREQUISITES": ProjectDefConst.PREREQUISITES,
                "LIBS_SOURCES": ProjectDefConst.LIBS_SOURCES,
                "INSTALL_SETUP_PATH": ProjectDefConst.INSTALL_SETUP_PATH,
                "ARTIFACTORY_URL": ProjectDefConst.ARTIFACTORY_URL,
                "SIMPLE_PATH": ProjectDefConst.SIMPLE_PATH,
            }
            with open(path, "w") as conf_file:
                yaml.dump(configuration, conf_file, default_flow_style=False)

        conf_in_cwd: Path = Path.cwd() / ProjectDefConst.README_CONF
        conf_in_site_pkg: Path = Path(__file__).parent / ProjectDefConst.README_CONF
        conf_path: Path = conf_in_cwd
        if not conf_in_cwd.exists():
            if not conf_in_site_pkg.exists():
                create_conf(conf_in_cwd)
                return None
            conf_path = conf_in_site_pkg
        with open(conf_path) as conf_file:
            project_conf: Dict = yaml.safe_load(conf_file)
        project_conf = {} if project_conf is None else project_conf
        ProjectDefConst.YAML_FILE = (
            ProjectDefConst.YAML_FILE if project_conf.get("YAML_FILE") is None else project_conf["YAML_FILE"]
        )
        ProjectDefConst.PY_PKGS_FILE = (
            ProjectDefConst.PY_PKGS_FILE if project_conf.get("PY_PKGS_FILE") is None else project_conf["PY_PKGS_FILE"]
        )
        ProjectDefConst.NAME = ProjectDefConst.NAME if project_conf.get("NAME") is None else project_conf["NAME"]
        ProjectDefConst.DESCRIPTION = (
            ProjectDefConst.DESCRIPTION if project_conf.get("DESCRIPTION") is None else project_conf["DESCRIPTION"]
        )
        ProjectDefConst.PREREQUISITES = (
            ProjectDefConst.PREREQUISITES
            if project_conf.get("PREREQUISITES") is None
            else project_conf["PREREQUISITES"]
        )
        ProjectDefConst.LIBS_SOURCES = (
            ProjectDefConst.LIBS_SOURCES if project_conf.get("LIBS_SOURCES") is None else project_conf["LIBS_SOURCES"]
        )
        ProjectDefConst.INSTALL_SETUP_PATH = (
            ProjectDefConst.INSTALL_SETUP_PATH
            if project_conf.get("INSTALL_SETUP_PATH") is None
            else project_conf["INSTALL_SETUP_PATH"]
        )
        ProjectDefConst.ARTIFACTORY_URL = (
            ProjectDefConst.ARTIFACTORY_URL
            if project_conf.get("ARTIFACTORY_URL") is None
            else project_conf["ARTIFACTORY_URL"]
        )
        ProjectDefConst.SIMPLE_PATH = (
            ProjectDefConst.SIMPLE_PATH if project_conf.get("SIMPLE_PATH") is None else project_conf["SIMPLE_PATH"]
        )
        create_conf(conf_path)


def get_friendly_name(path: str) -> str:
    parts: list[str] = path.split("/")
    return parts[-1]


def get_link_name(path: str) -> str:
    parts: list[str] = path.split("/")
    if len(parts) == 1:
        return f"Artifactory/{ProjectDefConst.INSTALL_SETUP_PATH}"
    else:
        return f"Artifactory/{parts[0]}"


def get_link(path: str) -> str:
    parts: list[str] = path.split("/")
    if len(parts) == 1:
        return f"{ProjectDefConst.ARTIFACTORY_URL}/{ProjectDefConst.INSTALL_SETUP_PATH}/{path}"
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
    if not Path(yaml_file).exists():
        sys.exit(1)
    with open(yaml_file) as file:
        project_def: Dict = yaml.safe_load(file)
    if project_def is None:
        sys.exit(1)
    if project_def.get("metadata") is None:
        sys.exit(1)
    project_def = project_def.get("metadata")
    if Path(req_file).exists():
        with open(req_file) as file:
            packages: list[str] = [line.strip().split("=")[0] for line in file]
    else:
        packages = None
    content: str = ""
    if not (project_def.get(ProjectDefConst.NAME) is None):
        content += f"# {project_def[ProjectDefConst.NAME]}\n"
        if not (project_def.get(ProjectDefConst.DESCRIPTION) is None):
            content += f" {project_def[ProjectDefConst.DESCRIPTION]}\n\n"

    # Arifactory prerequisites dependencies section
    content += "## Dependencies\n"
    content += "Dependencies got from Artifactory\n"
    content += "|Dependency|Link|\n|-|-|\n"
    links_content: str = ""
    lnk_ref: int = 1
    if not (project_def.get(ProjectDefConst.PREREQUISITES) is None):
        for prerequisite in project_def[ProjectDefConst.PREREQUISITES]:
            content += f"|{get_friendly_name(prerequisite)}|[{get_link_name(prerequisite)}][{lnk_ref}]|\n"
            links_content += f"[{lnk_ref}]: {get_link(prerequisite)}\n"
            lnk_ref += 1
    content += "\n"

    # Libriaries dependencies section
    content += "## Libs Sources\n"
    content += "Library sources\n"
    content += "|Lib|Link|\n|-|-|\n"
    sources: list[str] = project_def.get(ProjectDefConst.LIBS_SOURCES)
    if sources:
        for link in sources:
            content += f"|{get_friendly_name(link)}|[{link}]({link})|\n"
    content += "\n"

    # Python dependencies section
    content += "## Python Dependencies\n"
    content += "Dependencies from python\n"
    content += "|Dependency|Link|\n|-|-|\n"
    if packages:
        for pkg in packages:
            content += f"|{pkg}|[{get_python_src(pkg)}][{lnk_ref}]|\n"
            links_content += f"[{lnk_ref}]: {get_python_link(pkg)}\n"
            lnk_ref += 1
    content += "\n"

    content += links_content

    readme_file: Path = Path.cwd() / "README.md"
    readme_file.touch()
    readme_file.write_text(content)


def main() -> None:
    ReadmeGenConfig.load_configuration()
    generate_readme()


if __name__ == "__main__":
    main()
