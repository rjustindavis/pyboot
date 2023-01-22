# pyboot

Python environments for bootstrapping / sandboxing. Environments are managed through [micromamba]() and [poetry](). Specifically, we use `micromamba` to manage the python ecosystem and virtual environments, and we use `poetry` to manage dependencies (`poetry` has superior dependency resolution and a larger package repo). The goal is to quickly create reproducible environments for various applications/APIs.

## First-time setup

Create a temporary environment:

```bash
micromamba create -p /tmp/bootstrap -c conda-forge micromamba conda-lock poetry
micromamba activate /tmp/bootstrap
```

Create conda lock file:

```bash
conda-lock -k explicit --conda micromamba -f bootstrap.yaml
```

Remove temporary environment:

```bash
micromamba deactivate
rm -rf /tmp/bootstrap
```

## Usage

The resulting `conda-linux-64.lock` file serves as the starting point for new projects and sandboxes. You can create an environment from it using the following command:

```bash
micromamba create --name MY_ENV --file conda-linux-64.lock
micromamba activate MY_ENV
```

where `MY_ENV` should be replaced by an appropriate environment name. For instance, you could create a bootstrap environment like so:

```bash
micromamba create --name bootstrap_python310 --file conda-linux-64.lock
micromamba activate bootstrap_python310
```

Then, you can create new environments from the `conda-linux-64.lock` file or clone the bootstrap environment itself:

```bash
micromamba ccreate --name NEW_ENV --clone bootstrap_python310
```

You can update the bootstrap (or any other environment) using the following:

```shellscript
micromamba update --name MY_ENV --all
```

Once you create the new environment, you can add dependencies using poetry:

```bash
poetry init python=3.10 # Should match the python version in your micromamba environment
poetry add networkx # Adds project dependency
poetry add --group dev pytest-black # Add development dependencies
poetry add --group dev poetry poethepoet # Overwrites micromamba's dependencies
```

You can also add arbitrary tasks using
[poethepoet](https://github.com/nat-n/poethepoet). Specify tasks in
`pyproject.toml` like so:

```toml
[tool.poe.tasks]
test = "pytest --cov=. tests/"
```

or hierarchically if you want to specify more attributes:

```toml
[tool.poe.tasks]
    [tool.poe.tasks.test]
    help = "Run pytest and pytest-cov"
    cmd = "pytest --cov=. tests/"
```

Then, you can run tasks on the command line using `poe`:

```bash
poe test
```

### Example 1: Pyg project for python=3.10 and cuda=11.7.

Create environment and install core packages

```bash
micromamba create --name pytorch_310_cuda_117 --file conda-linux-64.lock
mimcromamba activate pytorch_310_cuda_117
poetry init --python=3.10
poetry add --group dev poetry poethepoet pytest-black pytest-cov mkdocs xonsh
poetry add torch pytorch-lightning
```

Unfortunately, [pyg](https://pytorch-geometric.readthedocs.io) for cuda=11.7
isn't currently the default install; therefore, in order to install the required
version, we need to specify a `pyg` wheel. Poetry can't do this natively yet,
but we can call `pip` through a dedicated, `poethepoet` runner.

```toml
# Define poethepoet task in pyproject.toml
[tool.poe.tasks]
    [tool.poe.tasks.install-pyg]
    help = "Install pyg dependencies"
    cmd = "pip install pyg-lib torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.13.0+cu117.html"
```
```bash
# Command line (make sure you've activated your environment)
poe install-pyg
```

## Templates

Composable templates are located in the `templates/` directory. These represent commonly used entries for `pyproject.toml`, depending on the tech stack. Examples include `dev_deps.toml` and `pytorch-pyg.toml` which create common development dependencies. There is also a helper module, `make_pyproject.py` which merges different toml configurations, making the templates composable.

### Example 2: Create a pyproject.toml for a pyg project

```bash
python make_project --name pyg_proj --files dev_deps.toml pytorch_pyg.toml
```