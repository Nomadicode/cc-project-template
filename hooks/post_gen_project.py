"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).
TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

import shutil


def remove_client_files():
    shutil.rmtree("client")
    shutil.rmtree("ops/client")

def remove_server_files():
    shutil.rmtree("server")
    shutil.rmtree("ops/server")
    shutil.rmtree("ops/database")

def main():
    if "{{ cookiecutter.include_client }}".lower() == "n":
        remove_client_files()

    if "{{ cookiecutter.include_server }}".lower() == "n":
        remove_server_files()

if __name__ == "__main__":
    main()