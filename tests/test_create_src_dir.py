from pathlib import Path

from create_python_project import create_src_dir


def test(tmp_path: Path) -> None:
    create_src_dir(tmp_path)

    assert (tmp_path / 'src').exists()
    assert (tmp_path / 'src').is_dir()

    assert (tmp_path / 'src/__init__.py').exists()
    assert (tmp_path / 'src/__init__.py').is_file()

    assert (tmp_path / 'src/main.py').exists()
    assert (tmp_path / 'src/main.py').is_file()
