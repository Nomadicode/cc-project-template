"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).
TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

import os
import shutil

def remove_i18n_files():
    shutil.rmtree("client/locales")

def remove_client_files():
    shutil.rmtree("client")
    shutil.rmtree("ops/client")

def remove_server_files():
    shutil.rmtree("server")
    shutil.rmtree("ops/server")
    shutil.rmtree("ops/database")

def remove_rest_files():
    root_path = "server/apps/users/"
    file_names = [
        "tests/test_user_rest.py",
        "routes.py",
        "serializers.py",
        "views.py"
    ]

    for filename in file_names:
        os.remove(root_path + filename)

def remove_graphql_files():
    root_path = "server/apps/users/"
    file_names = [
        "tests/test_user_graphql.py",
        "mutations.py",
        "schema.py"
    ]

    for filename in file_names:
        os.remove(root_path + filename)

    os.remove("server/config/schema.py")

def main():
    if "{{ cookiecutter.include_client }}".lower() == "n":
        remove_client_files()

    if "{{ cookiecutter.include_server }}".lower() == "n":
        remove_server_files()

    if "{{ cookiecutter.use_rest }}".lower() == 'n':
        remove_rest_files()

    if "{{ cookiecutter.use_graphql }}".lower() == 'n':
        remove_graphql_files()

    if "{{ cookiecutter.use_i18n }}".lower() == 'n':
        remove_i18n_files()

if __name__ == "__main__":
    main()