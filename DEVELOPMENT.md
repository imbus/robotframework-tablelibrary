# Development

## Unit Testing

We are measuring the coverage of the unit tests & expect a minimum coverage of 95% - otherwise the pipeline job for the unit test execution will fail accordingly.    
Please ensure you've added unit tests whenever adding new source code to the project.

## Release Creation

### Precondition

- You are required to have an account for **[PyPi](https://pypi.org/)**.
- Additionally, check that you have required permissions for the projects at ``PyPi & GitHub``!
- Check that all pipeline-checks did pass, your code changes are ready and everything is already merged to the main branch!
- Your local git configuration must work - check your authentication!

### *Preferred* - Using Shell Script for Release Creation

In the ``root directory`` of this repository you will find a script called ``create_release.sh``.
When executing this script, it expects exactly one argument: the new name of the release / tag.
Here you need to provide always the syntax ``X.X.X``, e.g. ``0.1.9``, ``0.5.0`` or ``1.0.0``.

The package version is read from the Git tag. No version file needs to be changed or committed. Create and push a tag from the desired commit:

```
cd <project-root-directory>
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

After pushing the tag, three pipeline jobs are triggered automatically:
1. First job creates a new ``Release`` in github with the name of the created ``Tag``.
2. Second job builds the wheel with the version from the Git tag and uploads it to ``PyPi``.
3. Third job generates a new keyword documentation via ``libdoc`` on the main branch, but pushes it to the ``gh_pages`` where it is available as public ``GitHub Page``.

### *Backup* - Manual Version Bump & Tag Creation

If the preferred way using the ``create_release.sh`` script does not work, you can also manually create a new release.
Therefore, execute the following steps.

#### Create a new tag

Create a new tag from the desired commit with the syntax ``vX.X.X``. The version must be unique in PyPI and GitHub Releases.

Use the following commands to create & push the tag:
```
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

#### Creating GitHub Release & Deploy Wheel Package to PyPi

After pushing the new tag, three pipeline jobs are getting triggered automatically:
1. First job creates a new ``Release`` in github with the name of the created ``Tag``.
2. Second job builds the wheel with the version from the Git tag and uploads it to ``PyPi``.
3. Third job generates a new keyword documentation via ``libdoc`` on the main branch, but pushes it to the ``gh_pages`` where it is available as public ``GitHub Page``.

## Installing Dev Dependencies

Contributing to this project & working with it locally, requires you to install some ``dev dependencies`` - use the following command in the project root directory:
```
pip install -e .[dev]
```

Afterwards, the table library gets installed in ``editable mode`` & you will have a ``dev dependencies`` installed.

## Hatch

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

### Execute Tests Against the Version Matrix

Install Python 3.10 through 3.14 locally and make sure Hatch can find these interpreters. The test matrix covers Python 3.10-3.14 and Robot Framework 7.0 and 7.4.2.

Run all unit and acceptance tests against every matrix combination:

```shell
hatch run test:all
```

To test one combination only, for example Python 3.14 with Robot Framework 7.4.2:

```shell
hatch run test.py3.14-7.4.2:all
```

Use `hatch env show` to list the generated matrix environments.

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
