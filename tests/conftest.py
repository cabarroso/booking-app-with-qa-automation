from framework.utils.logger import setup_logger

setup_logger()

pytest_plugins = [
                    "framework.fixtures.api_fixtures",
                    "framework.fixtures.ui_fixtures"
                 ]