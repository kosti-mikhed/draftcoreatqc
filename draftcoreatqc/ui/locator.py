"""
Locator object module
"""
from selenium.webdriver.common.by import By
from collections import namedtuple


class Locators:
    """
    Class of Locator object builder
    """
    Locator = namedtuple("Locator", ["by", "value"])

    @staticmethod
    def css(value: str) -> Locator:
        """
        Building Locator object by css selector
        """
        return Locators.Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def xpath(value: str) -> Locator:
        """
        Building Locator object by xpath selector
        """
        return Locators.Locator(By.XPATH, value)
