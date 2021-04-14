"""
Base Page Object module
"""
from typing import List, Any
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from draftcoreatqc.ui.locator import Locators
import allure


class BasePageActions:
    """
    Class for working with pages
    """

    def __init__(self, driver):
        self.driver = driver
        self.locator_css = Locators.css
        self.locator_xpath = Locators.xpath
        self.keys = Keys

    def element(self,
                locator: Locators.Locator,
                element: WebElement,
                timeout=10) -> WebElement:
        """
        Returns web element accepting either Web element or it's locator
        """
        if element:
            return element
        elif locator:
            return self.find_visible_element(locator, timeout=timeout)
        else:
            raise Exception("Unknown way to define an element")

    @allure.step("Browser: Finding element (visible)")
    def find_visible_element(self,
                             locator: Locators.Locator,
                             timeout=10) -> WebElement:
        """
        Find an element
        """
        element = WebDriverWait(self.driver, timeout=timeout) \
            .until(ec.visibility_of_element_located(locator=locator))
        return element

    @allure.step("Browser: Finding element (visible)")
    def find_present_element(self,
                             locator: Locators.Locator,
                             timeout=10) -> WebElement:
        """
        Find an element
        """
        element = WebDriverWait(self.driver, timeout=timeout) \
            .until(ec.presence_of_element_located(locator=locator))
        return element

    @allure.step("Browser: Finding multiple elements (visible)")
    def find_visible_elements(self,
                              locator,
                              timeout=10) -> List[WebElement]:
        """
        Find list of elements
        """
        element = WebDriverWait(self.driver, timeout=timeout) \
            .until(ec.visibility_of_all_elements_located(locator=locator))
        return element

    @allure.step("Browser: Finding multiple elements (present)")
    def find_present_elements(self,
                              locator,
                              timeout=10) -> List[WebElement]:
        """
        Find list of elements
        """
        element = WebDriverWait(self.driver, timeout=timeout) \
            .until(ec.presence_of_all_elements_located(locator=locator))
        return element

    def navigate(self, url: str):
        """
        Navigate to url
        """
        with allure.step(f"Browser: Opening URL {url}"):
            self.driver.get(url)

    @property
    def page_title(self) -> str:
        """
        Browser page title
        """
        return self.driver.title

    @allure.step("Browser: Refreshing current screen")
    def refresh_current_screen(self):
        """
        Refresh current browser screen
        """
        self.driver.refresh()

    @allure.step("Browser: Switching to iframe")
    def switch_to_frame(self,
                        locator: Locators.Locator = None,
                        element: WebElement = None):
        """
        Switch to iframe
        Accepts either element's locator or element itself
        """
        self.driver.switch_to.frame(self.element(locator, element))

    @allure.step("Browser: Switching to default content")
    def switch_to_default_content(self):
        """
        Switch to default content
        """
        self.driver.switch_to.default_content()

    @allure.step("Browser: Executing script: {script}")
    def execute_script(self, script: str, *args) -> Any:
        """
        Execute script in browser
        """
        return self.driver.execute_script(script, *args)

    def wait_elements_invisibility(self,
                                   locator: Locators.Locator,
                                   timeout=10):
        """
        Find list of elements
        """
        with allure.step("Browser: invisibility multiple elements"):
            WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.invisibility_of_element_located(locator=locator))

    def get_elements_list(self, locator):
        return self.driver.find_elements(locator.by, locator.value)

    @allure.step("Browser: making input to element")
    def input_to_element(self,
                         locator: Locators.Locator = None,
                         element: WebElement = None,
                         input_text=""):
        """
        Input some text to element
        Accepts either element's locator or element itself
        """
        el = self.element(locator, element)
        el.send_keys(input_text)

    @allure.step("Browser: Clicking element")
    def click_element(self,
                      locator: Locators.Locator = None,
                      element: WebElement = None):
        """
        Click an element
        Accepts either element's locator or element itself
        """
        el = self.element(locator, element)
        el.click()

    @allure.step("Click outside")
    def click_outside(self):
        """
        Clicking outside, to close pop-ups
        """
        self.click_element(locator=self.locator_css("body"))

    @allure.step("Browser: Move and Clicking element")
    def moveto_and_click_element(self,
                                 locator_to_move: Locators.Locator = None,
                                 locator_to_click: Locators.Locator = None,
                                 element_to_move: WebElement = None,
                                 element_to_click: WebElement = None):
        """
        Click an element
        Accepts either element's locator or element itself
        """
        element_to_move = self.element(locator=locator_to_move,
                                       element=element_to_move)
        element_to_click = self.element(locator=locator_to_click,
                                        element=element_to_click)
        builder = ActionChains(self.driver)
        builder.move_to_element(element_to_move).click(element_to_click).perform()

    @allure.step("Browser: Move and Clicking element")
    def moveto_element(self,
                       locator_to_move: Locators.Locator = None,
                       element_to_move: WebElement = None):
        """
        Click an element
        Accepts either element's locator or element itself
        """
        element_to_move = self.element(locator=locator_to_move,
                                       element=element_to_move)
        builder = ActionChains(self.driver)
        builder.move_to_element(element_to_move).perform()

    @allure.step("Browser: Checking that element is displayed")
    def element_is_displayed(self,
                             locator: Locators.Locator = None,
                             element: WebElement = None) -> bool:
        """
        Check that element is displayed
        Accepts either element's locator or element itself2
        """
        return bool(self.element(locator, element).is_displayed())

    @allure.step("Browser: Checking that element is present in DOM")
    def element_is_present(self,
                           locator: Locators.Locator = None) -> bool:
        """
        Check that element is present in DOM (aka find element)
        """
        return bool(self.find_present_element(locator))

    @allure.step("Browser: Getting element text")
    def get_element_text(self,
                         locator: Locators.Locator = None,
                         element: WebElement = None,
                         timeout=10) -> str:
        """
        Get element's text
        Accepts either element's locator or element itself
        """
        el = self.element(locator, element, timeout=timeout)
        return el.text

    @allure.step("Browser: Clearing element\'s input value")
    def clear_element(self,
                      locator: Locators.Locator = None,
                      element: WebElement = None):
        """
        Clear element's input value
        Accepts either element's locator or element itself
        """
        el = self.element(locator, element)
        el.clear()

    @allure.step("Browser: Getting element\'s input value")
    def get_input_value(self,
                        locator: Locators.Locator = None,
                        element: WebElement = None) -> str:
        """
        Get element's input value
        Accepts either element's locator or element itself
        """
        el = self.element(locator, element)
        return el.get_attribute('value')

    @allure.step("Browser: Opening URL in new tab: {url}")
    def navigate_in_new_tab(self, url: str):
        """
        Open URL in new tab
        """
        self.execute_script(f'window.open("{url}");')

    @allure.step("Browser: Returning script execution result")
    def get_execute_script_result(self, script: str) -> Any:
        """
        Execute script and return it's result
        """
        return self.execute_script(f"return {script}")

    def get_page_source(self):
        return self.driver.page_source

    @allure.step("Browser: Accepting alert")
    def accept_alert(self):
        """
        Accept alert notification
        """
        self.driver.switch_to.alert.accept()

    @allure.step("Click Keyboard button")
    def click_keyboard_button(self, keyboard_button):
        """
        Click Escape button on keyboard
        """
        ac = ActionChains(self.driver)
        ac.send_keys(keyboard_button).perform()

    @allure.step("Scroll to element center")
    def scroll_into_element_center(self,
                                   locator: Locators.Locator = None,
                                   element: WebElement = None):
        element = self.element(locator=locator, element=element)
        script = "arguments[0].scrollIntoView({block: 'center'});"
        self.execute_script(script, element)
