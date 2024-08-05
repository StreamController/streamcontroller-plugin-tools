from venv import create
from os.path import join, abspath
from subprocess import run

def create_venv(path: str = ".venv", path_to_requirements_txt: str = None) -> None:
    create(path, with_pip=True)

    if path_to_requirements_txt is None:
        return
    print(f". {join(path, 'bin', 'activate')} && pip install -r {path_to_requirements_txt}")
    run(f". {join(path, 'bin', 'activate')} && pip install -r {path_to_requirements_txt}", start_new_session=True, shell=True)
