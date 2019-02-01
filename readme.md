## Deprecated
The package has been deprecated. If one needs similar functionality try [poetry](https://github.com/sdispater/poetry).
Also the name has been transferred to [pipx-app](https://github.com/pipxproject/pipx-app).

## Introduction
`pipx` extends `pip` with ability to automatically register packages upon installation.

## Installation

`pip install pipx`

## Usage
### Install a package
`pipx install django`

The above command will install `django` and register it at `dependencies` in `project.json` file.

For installing development dependencies pass `-d` or `--dev` flag.

`pipx install -d pytest`

The above command will install `pytest` and register it at `dev-dependencies` in `project.json` file.

### Uninstall a package
`pipx uninstall django`

### Update a package
`pipx update django`

For updating development package pass `-d` or `--dev` flag.

`pipx update -d pytest`

### Setup a project
Issue `setup` without any flags during deployment. The command will install all the packages in `dependencies` section.

`pipx setup`

If the setup is for development, pass `-d` or `--dev` flag. This will install packages in both `dependencies` and `dev-dependencies` sections.

`pipx -d setup`
