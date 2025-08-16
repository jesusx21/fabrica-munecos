# La Fabrica de Muñecos

The purpose of this project is the server for La Fabrica de Muñecos,.

## Setup

### Requirements

To make it easier for us to test and maintain code, we should have a clean python environment dedicated for the project.
For this, we can install pyenv and pyenv-virtualenv to manage virtual python environments.

```sh
brew install pyenv pyenv-virtualenv
```

Now add the next lines to the bottom of your shell configuration file (e.g. `.bashrc` or `.zshrc`) and restart the terminal after.

```sh
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

First we need to install python 3.9.0 in pyenv

```sh
pyenv install 3.9.0
```

To create and activate a python virtual environment excecute

```sh
pyenv virtualenv 3.9.0 <env_name>
pyenv activate <env_name>
```

Once activated, we can install the project dependencies to that environment

```sh
make install
```

To install dev dependencies

```sh
make install-dev
```

### Configuration

To add configuration values:

```sh
cp config.sample.ini config.ini
```

### Database

To setup a local database for the platform we must first create a database in postgres. The default name is `hotties_factory_dev`

```sh
createdb hotties_factory_dev
```

#### Autogenerating a migration

If we modify the database structure, we can use alembic or make to auto-generate a script for this new migration with the following command:

```sh
alembic revision --autogenerate -m "What this migration does"
```

This will generate a new script that will create the modifications of the database.
In case we need to tune the migration further, we can modify the auto-generated script to include all the required changes

#### Run a migration

```sh
alembic upgrade head
```

and

```sh
make run-migrations
```

if we want to run until a specific migration we pass the revision id

```sh
alembic upgrade <revision id>
```
