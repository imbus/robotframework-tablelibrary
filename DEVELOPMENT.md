# Development

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

### Execute Acceptance & Unit Tests via Robot Framework & PyTest

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


## Release Creation

Follow those steps to create a new release.

### Precondition

- You are required to have an account for **[PyPi](https://pypi.org/)**.
- Additionally, check that you have required permissions for the projects at ``PyPi & GitHub``!
- Check that all pipeline-checks did pass, your code changes are ready and everything is already merged to the main branch!

### 1. Increase Version

Open the file **[\_\_about\_\_.py](src/Tables/__about__.py)** and increase the version (``0.0.5 = major.minor.path``) before building & uploading the new python wheel package!

The new version **must be unique** & **not already existing** in ``PyPi`` & ``GitHub Releases``!!!

Commit & push the changed version into the ``main`` branch of the repository.

### 2. Create new Tag

Now, create a new tag from the main branch with the syntax ``vX.X.X`` -> example: ``v1.0.5``.

Use the following commands to create & push the tag:
```
git tag v0.0.5
git push origin v0.0.5
```

### 2.1. Creating GitHub Release & Deploy Wheel Package to PyPi

After pushing the new tag, two pipeline jobs are getting triggered automatically:
1. First job creates a new ``Release`` in github with the name of the created ``Tag``.
2. Second job uploads the new wheel package to ``PyPi`` with the ``__version__`` from the ``__about__.py`` file.

### 3. Upload new Keyword Documentation

Switch to the main branch & execute the following command to generate a new libdoc keyword documentation:

```
cd <project-root-directory>
libdoc src/Tables ./index.html
```

Save this generated html file on your local file system.\n
Next, checkout the branch ``gh_pages``. Replace the actual ``index.html`` in the ``docs`` directory & push the new keyword documentation to GitHub into this branch!
