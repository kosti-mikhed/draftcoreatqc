"""
Helpers for all UI Tabular data
"""
from typing import List, Union
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import allure
from draftcoreatqc.ui.locator import Locators


class TableHelper:
    """
    UI Tabular data Helper class
    """

    def __init__(self, base):
        self.base = base

    @allure.step("Get table data using selenium")
    def get_table_data_using_selenium(self,
                                      table_values_locator: Locators.Locator,
                                      table_header_locator: Locators.Locator,
                                      table_total_locator: Locators.Locator = None,
                                      columns_strings: List = None) -> pd.DataFrame:

        """
        Generic Method for receiving data from all standard tables using selenium
        Is slower than get_table_data_using_soup, but is more flexible with table elements

        :param table_values_locator: Locator for all cells in the table
        :param table_header_locator: Locator for all columns headers in the table
        :param table_total_locator: Locator for total cells in the table (if any)
        :param columns_strings: Names of the columns in case it has to be customized
                                or cannot be received from the table header elements
        :return: Dataframe with table cells values
        """

        values_txt = self.get_table_txt(  # get text of all table values in list [V1, V2, V3, ... Vn]
            table_values_locator
        )
        columns_txt = self.get_table_txt(  # get text of all table columns in list [C1, C2, C3, ... Cn]
            table_header_locator
        )
        if table_total_locator:
            table_total = self.get_table_txt(  # get text of all table totals in list [T1, T2, T3, ... Tn]
                table_total_locator
            )
        else:
            table_total = None
        columns_per_values = self.transform_values_to_column_rows(
            # transform values and columns to rows [{C1: V1, C2: V2}, {C1: V3, C2: V4}, ... {Cn: Vn, Cn: Vn}]
            columns=columns_txt,
            values=values_txt,
            totals=table_total,
            columns_strings=columns_strings
        )
        return pd.DataFrame(columns_per_values)

    @allure.step("Get Table Data Frame using Beautiful Soup library")
    def get_table_data_using_soup(self,
                                  table_locator_css: Locators.Locator,
                                  page_source: str,
                                  return_all_df: bool = False):

        """
        Generic Method for receiving data from all standard tables using beautiful soup. \n
        Is significantly faster than get_table_data_using_selenium, but can be used
        ONLY when the whole table element can be found with css selector. \n
        If multiple tables can be found, by default values from the first table are returned. \n
        In order to return values combined from the all found table, set return_all_df as True.

        :param table_locator_css: Locator (by css selector) to find the table
        :param page_source: Stringified HTML page source where table can be found
        :param return_all_df: Boolean value whether all tables, found with the locator,
                              should be combined into resulting dataframe
        :return: Dataframe with table cells values
        """

        if table_locator_css.by != 'css selector':
            raise ValueError("You can use css selector only !")
        soup = BeautifulSoup(page_source, "html.parser")

        ts = soup.select(selector=table_locator_css.value)  # tables source
        df_list = pd.read_html(str(ts))  # the list of all Data Frames
        if not return_all_df:
            return df_list[0]
        else:
            return df_list

    @allure.step("Get Table Elements")
    def get_table_elements(self,
                           table_values_locator: Locators.Locator = None,
                           table_values_elements: List[WebElement] = None,
                           table_header_locator: Locators.Locator = None,
                           table_header_elements: List[WebElement] = None,
                           table_total_locator: Locators.Locator = None,
                           columns_strings: List[str] = None):

        """
        Method for receiving Dataframe with Web Elements from the table

        :param table_values_locator: Locator for all cells in the table
        :param table_values_elements: List of table cells elements
        :param table_header_locator: Locator for all columns headers in the table
        :param table_header_elements: List of table header elements
        :param table_total_locator: Locator for total cells in the table
        :param columns_strings: Names of the columns in case it has to be customized
                                or cannot be received from the table header elements
        :return: Dataframe with table cells web elements
        """

        if table_values_locator:
            values = self.base.find_elements(locator=table_values_locator)
        else:
            values = table_values_elements

        if table_header_locator:
            columns_txt = self.get_table_txt(  # get texts of all table columns in list [C1, C2, C3, ... Cn]
                table_header_locator
            )
        else:
            columns_txt = [x.text for x in table_header_elements]

        if table_total_locator:
            table_total_elements = self.base.find_elements(locator=table_total_locator)
        else:
            table_total_elements = None

        columns_per_values_els = self.transform_values_to_column_rows(
            # transform values and columns to rows [{C1: V1, C2: V2}, {C1: V3, C2: V4}, ... {C1: Vn, C2: Vn}]
            columns=columns_txt,
            values=values,
            totals=table_total_elements,
            columns_strings=columns_strings
        )

        return pd.DataFrame(columns_per_values_els)

    @staticmethod
    def transform_values_to_column_rows(columns: List[str],
                                        values: List[Union[WebElement, str]],
                                        totals: List[Union[WebElement, str]] = None,
                                        columns_strings=None) -> List[dict]:
        """
        This function combines values and columns to rows, is reused by other functions
        that return Dataframe with

        :param columns: List of columns names
        :param values: List of values (either elements or text values)
        :param totals: List of total cells (either elements or text values)
        :param columns_strings: Names of the columns in case it has to be customized
                                or cannot be received from the table header elements
        the number of columns should match to the number of values
        """
        if columns_strings:
            columns = columns_strings
        if totals:
            values.extend(totals)
            # add totals to values list
        if len(values) % len(columns) != 0:
            # the error appears if the number of columns does not match the number of rows
            raise ValueError("The number of values does not match the number of columns"
                             f"Values: {values}"
                             f"Colummns: {columns}")
        if len(set(columns)) != len(columns):
            # the names of columns will be renamed if all names are not unique
            columns = [f"column_{x}" for x in range(len(columns))]
            # transform one-dimensional array to two-dimensional array.
            # The length of 2nd dimension according to columns number
        texts_array = [values[x:x + len(columns)] for x in range(0, len(values), len(columns))]
        res = []
        # assign each value the name of the corresponding column
        for t in texts_array:
            di = dict()
            for x in range(len(columns)):
                di[columns[x]] = t[x]

            res.append(di)
        return res

    def get_table_txt(self, locator: Locators.Locator) -> List[str]:
        """
        Generic function to return list of values elements texts found per locator

        :param locator: Locator to element(s) from which text value is to be returned
        :return: List of elements' text values, found by locator
        """
        els = self.base.find_elements(locator=locator)
        return list(map(lambda x: x.text, els))
