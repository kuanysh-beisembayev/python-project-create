#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess
from urllib.request import urlopen

DOCKERFILE_CONTENT = """
FROM python:3.13-slim-bullseye

RUN useradd --create-home --home-dir /app --shell /bin/bash app
WORKDIR /app

COPY requirements ./requirements
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements/{}.txt

COPY . .
USER app
"""

DOCKERIGNORE_SOURCE = 'https://raw.githubusercontent.com/GoogleCloudPlatform/getting-started-python/main/optional-kubernetes-engine/.dockerignore'  # noqa: E501

DOCKER_COMPOSE_CONTENT = """
services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    volumes:
      - .:/app
    tty: true
    command: python -m src.main
"""

DEV_REQUIREMENTS_CONTENT = """
-r base.txt
flake8
flake8-print
flake8-multiline-containers
flake8-builtins
flake8-import-order
flake8-commas
flake8-quotes
flake8-broken-line
flake8-clean-block
flake8-walrus
"""

FLAKE8_CONTENT = """
[flake8]
max-line-length = 100
import-order-style = google
application-import-names = src
exclude = venv
"""

PYRIGHT_CONTENT = """
{
  "venvPath": ".",
  "venv": "venv"
}
"""

GITIGNORE_SOURCE = 'https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore'

GIT_BRANCH = 'develop'

GIT_COMMIT = 'initial commit'


def main() -> None:
    parser = argparse.ArgumentParser(description='Create project directory structure')
    parser.add_argument('project_name', type=str, help='Name of the project')
    args = parser.parse_args()

    project_dir = Path(args.project_name)

    create_src_dir(project_dir)
    _create_requirements_dir(project_dir)
    _create_docker_dir(project_dir)
    _create_dockerignore(project_dir)
    _create_docker_compose(project_dir)
    _create_flake8_config(project_dir)
    _create_pyright_config(project_dir)
    _create_gitignore(project_dir)
    _init_git(project_dir)


def create_src_dir(project_dir: Path) -> None:
    code_dir = project_dir / 'src'
    code_dir.mkdir(parents=True)

    (code_dir / '__init__.py').touch()
    (code_dir / 'main.py').touch()


def _create_requirements_dir(project_dir: Path) -> None:
    requirements_dir = project_dir / 'requirements'
    requirements_dir.mkdir()

    (requirements_dir / 'base.txt').touch()

    with open(requirements_dir / 'dev.txt', 'w') as file:
        file.write(DEV_REQUIREMENTS_CONTENT.lstrip())


def _create_docker_dir(project_dir: Path) -> None:
    docker_dir = project_dir / 'docker'
    docker_dir.mkdir()

    with open(docker_dir / 'Dockerfile', 'w') as file:
        file.write(DOCKERFILE_CONTENT.format('base').lstrip())

    with open(docker_dir / 'Dockerfile.dev', 'w') as file:
        file.write(DOCKERFILE_CONTENT.format('dev').lstrip())


def _create_dockerignore(project_dir: Path) -> None:
    with urlopen(DOCKERIGNORE_SOURCE) as response:
        gitignore_content = response.read().decode('utf-8')

    with open(project_dir / '.dockerignore', 'w') as file:
        file.write(gitignore_content)


def _create_docker_compose(project_dir: Path) -> None:
    with open(project_dir / 'docker-compose.yml', 'w') as file:
        file.write(DOCKER_COMPOSE_CONTENT.lstrip())


def _create_flake8_config(project_dir: Path) -> None:
    with open(project_dir / '.flake8', 'w') as file:
        file.write(FLAKE8_CONTENT.lstrip())


def _create_pyright_config(project_dir: Path) -> None:
    with open(project_dir / 'pyrightconfig.json', 'w') as file:
        file.write(PYRIGHT_CONTENT.lstrip())


def _create_gitignore(project_dir: Path) -> None:
    with urlopen(GITIGNORE_SOURCE) as response:
        gitignore_content = response.read().decode('utf-8')

    with open(project_dir / '.gitignore', 'w') as file:
        file.write(gitignore_content)


def _init_git(project_dir: Path) -> None:
    subprocess.run(['git', 'init', project_dir, '--initial-branch', GIT_BRANCH])
    subprocess.run(['git', '-C', project_dir, 'add', '.'])
    subprocess.run(['git', '-C', project_dir, 'commit', '-m', GIT_COMMIT])


if __name__ == '__main__':
    main()
