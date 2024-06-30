import importlib
import types

__all__ = ["import_modules"]


def _get_submodules(root: str) -> list[str]:
    submodules = importlib.import_module(root)

    return [
        f"{root}.{child_name}"
        for child_name, child in submodules.__dict__.items()
        if isinstance(child, types.ModuleType)
    ]


def import_modules(path: str):
    """
    Same as `importlib.import_module` but support '*' as "any submodule" syntax

    Example:
        >>> import_modules("website.pages.*.script")
        >>> import_modules("website.pages.*")
    """

    if "*" not in path:
        return importlib.import_module(path)

    root, after_star = path.split("*", 1)
    root = root.rstrip(".")

    if root:
        raise ImportError(
            f"Invalid input {path=!r}. "
            "Value of 'path' parameter can not starts with '*' symbol, "
            "because it may cause cyclic import."
        )

    for child in _get_submodules(root):
        if after_star:
            child = ".".join([child, after_star])
        return import_modules(child)
