import os

def pytest_addoption(parser):
    parser.addoption(
        "--no-whitelist",
        action="store_true",
        default=False,
        help="Run tests without loading or applying whitelists"
    )

def pytest_configure(config):
    if config.getoption("--no-whitelist"):
        os.environ["OWEN_NO_WHITELIST"] = "1"
