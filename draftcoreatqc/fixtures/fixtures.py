from draftcoreatqc.wrappers.rest import Rest
from draftcoreatqc.wrappers.browser import Browser


def rest_fixture():
    return Rest().rest


def browser_fixture(request):
    browser_name = request.config.getoption('--browser')
    is_selenoid = request.config.getoption('--selenoid')
    is_video = request.config.getoption('--video')
    if is_selenoid:
        browser_driver = Browser().selenoid_browser(browser_name=browser_name,
                                                    enable_video=is_video,
                                                    video_name=f"{request.module.__name__}-{request.node.name}")
    else:
        browser_driver = Browser().browser_driver(browser_name=browser_name)
    return browser_driver
