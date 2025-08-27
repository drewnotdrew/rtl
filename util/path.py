"""
A collection of Python utils.
"""

from pathlib import Path


def get_project_root() -> Path:
    """
    Return the root of the project based on an anchor file.
    """
    ANCHOR_FILE = ".gitignore"
    current_path = Path(__file__)
    while current_path != current_path.parent:
        if (current_path.joinpath(ANCHOR_FILE)).exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(f"Unable to find anchor file {ANCHOR_FILE}")


def resolve_module_path(name: str) -> Path:
    """
    Resolve the absolute path to a module. In the event more than one module is
    found, an error is raised.

    Args:
      name (str): The name of the module to find.

    Returns:
      An absolute path to the module.
    """
    # Process input name
    if not name.endswith(".sv"):
        name += ".sv"

    project_root = get_project_root()

    # Search for a module in project root
    hits = list(project_root.rglob(name))
    if len(hits) == 1:
        return hits[0]
    if len(hits) == 0:
        raise FileNotFoundError(f"Unable to find module {name}")
    if len(hits) > 1:
        raise RuntimeError(f"Multiple modules found for {name}: {hits}")


def resolve_relative_module_path(name: str) -> Path:
    """
    Resolve the relative path to a module, from the project root. In the event
    more than one module is found, and error is raised.
    """
    project_root_path = get_project_root()
    abs_module_path = resolve_module_path(name=name)
    return abs_module_path.relative_to(project_root_path)
