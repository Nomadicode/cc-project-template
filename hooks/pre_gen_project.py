"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.
TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import sys


project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), "'{}' project slug is not a valid Python identifier.".format(project_slug)

assert (
    project_slug == project_slug.lower()
), "'{}' project slug should be all lowercase".format(project_slug)

assert (
    "\\" not in "{{ cookiecutter.author }}"
), "Don't include backslashes in author name."

if (
    "{{ cookiecutter.include_server}}".lower() == 'y'
    and "{{ cookiecutter.use_rest }}".lower() == 'n'
    and "{{ cookiecutter.use_graphql }}".lower() == 'n'
):
    print("You need to select either rest or graphql")
    sys.exit(1)

if (
    "{{ cookiecutter.include_client }}".lower() == 'n'
    and "{{ cookiecutter.include_server }}".lower() == 'n'
):
    print("Come on now, you need to include either the client or server")
    sys.exit(1)