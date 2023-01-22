"""Make pyproject.toml"""

import mergedeep
import toml
from typing import Union

def make_pyproject(pkg_name: str, files: Union[str, list[str], None]) -> None:
    merged: dict = {
        "tool": {
            "poetry": {
                "name": f"{pkg_name}",
                "version": "0.1.0",
                "description": "Short project description",
                "authors": ["R. Justin Davis"],
                "license": "MIT",
                "readme": "README.md",
                "packages": [{"include": f"{pkg_name}"}],
                "dependencies": {"python": "^3.10"},
            }
        },
        "build-system": {
        "requires": "poetry-core",
        "build-backend": "poetry.core.masonry.api"
        }
    }

    # Define helper
    def write_pyproject(result: dict) -> None:
        with open("pyproject.toml", "w") as output_path:
            toml.dump(result, output_path)
    
    if files is None:
        write_pyproject(merged)
        return#
    elif not isinstance(files, list):
        files = [files]
    for fn in files:
        mergedeep.merge(merged, toml.load(fn))
    write_pyproject(merged)
    return

if __name__ == "__main__":
    import argparse
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="Make pyproject.toml",
        description="Compose pyproject.toml from templates"
    )
    parser.add_argument(
        "-n", "--name", type=str, help="Package name"
    )
    parser.add_argument(
        "-f", "--files",
        required=False,
        default=None,
        nargs="+",
        help="Toml file or list of toml files for merging"
    )
    args: argparse.Namespace = parser.parse_args()
    make_pyproject(args.name, args.files)