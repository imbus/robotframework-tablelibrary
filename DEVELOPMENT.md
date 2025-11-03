# Development

## Table of Content

- Hatch
- Pre-commit
- Twine Upload to Pypi / TestPypi

## hatch

You will need the python package tool ``hatch`` for several operations in this repository.
Hatch can be used to execute the linter, the tests or to build a wheel package.

Use the following command:
```shell
pip install hatch
```

### Ececute Linting Checks via ruff

```shell
hatch run dev:lint
```

### Execute Acceptance Tests via Robot Framework

```shell
hatch run dev:atest
hatch run dev:utest
```

### Generate Docs via libdoc

```shell
hatch run dev:docs
```

## pre-commit

When starting to work on this library, please ensure you have installed the development requirements from the ``readme.md``.    

Once you have them installed, please execute the following shell command:    

```shell
pre-commit install
```

This will activate the ``.pre-commit-config.yaml`` from your ``root``directory.

### Run pre-commit manually from shell

You can run the configured pre-commit hook manually with the following shell command:

```shell
pre-commit run --all-files
```

### VS Code Git vs. Shell Git

If you're working with a virtual environment, you might get problems with committing changes with the VS Code Git Controls.     
In that case, please open a shell where your virtual environment is activated & add, commit & push your changes via git shell commands!

## Upload to PyPi / Release Creation

### Requirements

You are required to have a account for each pypi server - production & test server.   
- **[Test PyPi](https://test.pypi.org/)**
- **[Prod PyPi](https://pypi.org/)**

Additionally, check that you have permissions for the project at PyPi & GitHub!

### PyPi - Authentication

Please generate an ``API Token`` for each ``PyPi`` instance (prod & test server).

Create the following ``.pypirc`` file in your ``HOME`` directory:

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```


> [!CAUTION]
> Set ``password`` with your real ``API Token``, but do not publish this file to GitHub!!!

### Tools

To upload a package to pypi, you need to install ``twine`` using the following command:
```shell
pip install twine
```

### Increase Version

Open the file [_about__.py](src/Tables/__about__.py) and increase the version (0.0.5 = major.minor.path) before building & uploading the new python wheel package!

Commit & push the changed version into the repository.

### Build Python Package

Navigate to the repository root directy and execute the following command:
```shell
hatch build
```

The built package is stored into the directory ``dist``.

### Upload Package to PyPi

Use the one of the following commands to upload the package to ``prod pypi`` or ``test pypi``.

```shell
twine upload -r testpypi dist/*
```

```shell
twine upload -r pypi dist/*
```

The parameter ``-r`` takes the configued registry from your ``.pypirc`` file.

### Create new Tag

Please create a new tag in GitHub with the syntax ``vX.X.X`` -> example: ``v1.0.5``.

### Upload new Keyword Documentation

Switch to the main branch & execute the following command to generate a new libdoc keyword documentation:

```
cd <project-root-directory>
libdoc src/Tables ./TableLibraryDocumentation.html
```

Save this generated html file on your local file system.\n
Next, checkout the branch ``gh_pages``. Replace the actual ``TableLibraryDocumentation`` in the ``docs`` directory & push the new keyword documentation to GitHub into this branch!
