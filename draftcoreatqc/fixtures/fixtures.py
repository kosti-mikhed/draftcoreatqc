from draftcoreatqc.wrappers.rest import Rest
from draftcoreatqc.wrappers.browser import Browser


def rest_fixture():
    return Rest().rest


def browser_fixture(request):
    browser_name = request.config.getoption('--browser')
    browser_driver = Browser().browser_driver(browser_name=browser_name)
    return browser_driver
