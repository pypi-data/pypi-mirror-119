#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/23/2020 8:12 PM
@Desc    :
"""

import os
import platform
import sys

from loguru import logger


class ExtraArgument:
    create_venv = False


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install tep.",
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ Create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.warning(
            f"Project folder {project_name} exists, please specify a new project name."
        )
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f"Project name {project_name} conflicts with existed file, please specify a new one."
        )
        return 1

    logger.info(f"Create new project: {project_name}")
    print(f"Project root dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file: {path}"
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "fixtures"))
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "files"))

    content = """.idea/
.pytest_cache/
.tep_allure_tmp/
__pycache__/
*.pyc
reports/
debug/"""
    create_file(os.path.join(project_name, ".gitignore"), content)

    content = """env: qa"""
    create_file(os.path.join(project_name, "conf.yaml"), content)

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

import os

import pytest

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


# Auto import fixtures
_fixtures_dir = os.path.join(_project_dir, "fixtures")
for root, _, files in os.walk(_fixtures_dir):
    for file in files:
        if os.path.isfile(os.path.join(root, file)):
            if file.startswith("fixture_") and file.endswith(".py"):
                _fixture_name, _ = os.path.splitext(file)
                try:
                    exec(f"from fixtures.{_fixture_name} import *")
                except:
                    pass
                try:
                    exec(f"from .fixtures.{_fixture_name} import *")
                except:
                    pass
"""
    create_file(os.path.join(project_name, "conftest.py"), content)

    content = """[pytest]
markers =
    smoke: smoke test
    regress: regress test
"""
    create_file(os.path.join(project_name, "pytest.ini"), content)

    content = """# Customize third-parties
# pip install --default-timeout=6000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# mysql
pandas==1.1.0
SQLAlchemy==1.3.19
PyMySQL==0.10.0
texttable==1.6.2
"""
    create_file(os.path.join(project_name, "requirements.txt"), content)

    create_file(os.path.join(project_name, "fixtures", "__init__.py"))

    create_file(os.path.join(project_name, "tests", "__init__.py"))

    if ExtraArgument.create_venv:
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv .venv")
        print("Created virtual environment: .venv")

        print("Installing tep")
        if platform.system().lower() == 'windows':
            os.chdir(".venv")
            os.chdir("Scripts")
            os.system("pip install tep")
        elif platform.system().lower() == 'linux':
            os.chdir(".venv")
            os.chdir("bin")
            os.system("pip install tep")


def main_scaffold(args):
    ExtraArgument.create_venv = args.create_venv
    sys.exit(create_scaffold(args.project_name))
