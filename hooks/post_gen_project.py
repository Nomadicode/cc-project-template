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
    shutil.rmtree("client/src/locales")

def remove_client_files():
    shutil.rmtree("client")
    shutil.rmtree("ops/client")

def remove_server_files():
    shutil.rmtree("server")
    shutil.rmtree("ops/server")
    shutil.rmtree("ops/database")

def remove_rest_files():
    file_names = [
        "server/apps/users/tests/test_user_rest.py",
        "server/apps/users/routes.py",
        "server/apps/users/serializers.py",
        "server/apps/users/views.py",
        "client/src/api/rest.js"
    ]

    for filename in file_names:
        os.remove(filename)

def remove_graphql_files():
    file_names = [
        "server/apps/users/tests/test_user_graphql.py",
        "server/apps/users/mutations.py",
        "server/apps/users/schema.py",
        "server/config/schema.py",
        "client/src/api/apollo.js"
    ]

    for filename in file_names:
        os.remove(filename)

def main():
    if "{{ cookiecutter.use_graphql }}".lower() == 'n':
        remove_graphql_files()

    if "{{ cookiecutter.use_rest }}".lower() == 'n':
        remove_rest_files()
    
    if "{{ cookiecutter.include_client }}".lower() == "n":
        remove_client_files()

    if "{{ cookiecutter.include_server }}".lower() == "n":
        remove_server_files()

    if "{{ cookiecutter.use_i18n }}".lower() == 'n':
        remove_i18n_files()

if __name__ == "__main__":
    main()