# Determine the path of module.

import argparse
from util.util import resolve_relative_module_path


def determine_target_directory(name: str) -> str:
    return resolve_relative_module_path(name=name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    print(determine_target_directory(name=args.name), flush=True)
