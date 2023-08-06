# PyPI empty package generator

This is an empty repository which only purpose is to occupy the supplied package name in public
repositories in order to avoid dependency confusion attacks via PyPI.

## Uploading to PyPi

This module is uploaded to PyPy under `darwin-eng-dlg` account (see 1password Data Science vault for credentials)

Instructions to upload:

1. `python -m pip install --user --upgrade setuptools wheel twine`
2. `python setup.py sdist bdist_wheel`
3. `python -m twine upload --repository pypi dist/*`
    * When prompted, enter `__token__` as Username and `darwin-eng-dlg` API token as password

## Checking version

The generated empty module is version 0.1, so any real module of the same available in a private artifact  
repository should take precedence.