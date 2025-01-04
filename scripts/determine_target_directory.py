# Determine the path of module.

import argparse
from util.util import resolve_module_path


def determine_target_directory(name: str) -> str:
    return resolve_module_path(name=name).parents[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    print(determine_target_directory(name=args.name), flush=True)
