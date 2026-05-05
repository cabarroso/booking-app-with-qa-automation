import pytest
import allure

from framework.utils.logger import setup_logger

setup_logger()

pytest_plugins = [
                    "framework.fixtures.api_fixtures",
                    "framework.fixtures.ui_fixtures",
                    "framework.fixtures.utility_fixtures"
                 ]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )