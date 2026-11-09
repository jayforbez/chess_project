import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: plays full games (run with -m slow)")


def pytest_collection_modifyitems(config, items):
    if config.getoption("-m"):
        return
    skip = pytest.mark.skip(reason="slow; run with -m slow")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip)
