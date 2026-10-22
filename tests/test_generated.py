from __future__ import annotations

import importlib
import pkgutil

from distrans_client import api, models


def _modules(package: object) -> list[str]:
    path = package.__path__
    name = package.__name__
    return [module.name for module in pkgutil.walk_packages(path, f"{name}.")]


def test_all_operations_are_generated() -> None:
    endpoints = [name for name in _modules(api) if name.count(".") == 3]
    assert len(endpoints) == 86


def test_tag_packages_import() -> None:
    tags = {module.name for module in pkgutil.iter_modules(api.__path__) if module.ispkg}
    assert tags == {
        "auth",
        "channels",
        "emojis",
        "files",
        "gateway",
        "guilds",
        "messages",
        "meta",
        "notifications",
        "roles",
        "sync",
        "system",
        "users",
        "webhooks",
    }


def test_every_generated_module_imports() -> None:
    failures: list[tuple[str, BaseException]] = []
    for name in _modules(api) + _modules(models):
        try:
            importlib.import_module(name)
        except BaseException as exc:  # pragma: no cover - diagnostic
            failures.append((name, exc))
    assert not failures, failures
