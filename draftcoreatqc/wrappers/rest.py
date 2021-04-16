"""
REST API client wrapper module
"""
from requests import Session


class Rest:
    """
    Class of REST API client wrapper
    """
    def __init__(self):
        self.rest = Session()
        self.clear_cookies()

    def clear_cookies(self):
        """
        Clear cookies
        """
        self.rest.cookies.clear()
