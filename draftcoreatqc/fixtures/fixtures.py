import pytest
from draftcoreatqc.wrappers.rest import Rest
from draftcoreatqc.wrappers.browser import Browser


@pytest.fixture(scope='function')
def rest():
    return Rest().rest


@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption('--browser')
    browser_driver = Browser().browser_driver(browser_name=browser_name)
    return browser_driver
