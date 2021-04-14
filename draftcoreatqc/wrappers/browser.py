"""
Module for Browser driver instance initiating
"""
import os
from selenium import webdriver


class Browser:
    """
    Class of browser wrapper
    """

    def __init__(self):
        self.driver = webdriver

    def browser_driver(self, browser_name: str):
        """
        Common method for getting browser driver per it's name
        :param browser_name: Browser name in string format
        :return: Browser driver instance
        """
        if browser_name == "chrome":
            driver = self.chrome()
        elif browser_name == "firefox":
            driver = self.firefox()
        else:
            raise Exception("Unsupported browser")
        return driver

    def chrome(self, driver_path="drivers/chromedriver"):
        """
        Google chrome driver
        :param driver_path: Path to chromedriver
        :return: Instance of Google Chrome driver
        """
        driver = self.driver
        options = driver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        chrome_driver = driver.Chrome(options=options, executable_path=driver_path)
        return chrome_driver

    def firefox(self, driver_path="drivers/geckodriver", service_log_path=os.devnull):
        """
        Mozilla Firefox driver
        :param driver_path: Path to geckodriver
        :param service_log_path: Path for creating geckodriver.log (disabled by default)
        :return: Instance of Firefox driver
        """
        driver = self.driver
        firefox_driver = driver.Firefox(executable_path=driver_path, service_log_path=service_log_path)
        firefox_driver.set_window_size(1920, 1080)
        return firefox_driver
