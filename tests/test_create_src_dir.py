from pathlib import Path

from create_python_project import create_src_dir


def test(project_dir: Path) -> None:
    create_src_dir(project_dir)

    assert (project_dir / 'src').exists()
    assert (project_dir / 'src').is_dir()

    assert (project_dir / 'src/__init__.py').exists()
    assert (project_dir / 'src/__init__.py').is_file()

    assert (project_dir / 'src/main.py').exists()
    assert (project_dir / 'src/main.py').is_file()
