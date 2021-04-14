"""
Response validator wrapper
"""
from json import loads as json_loads, dumps as json_dumps
import os
from collections import namedtuple
import jsonschema
from bs4 import BeautifulSoup
import allure


Validation = namedtuple('Validation', ['status', 'errors'])


class JsonSchemaValidator:
    """
    Class of JSON schema validator
    """

    def __init__(self):
        self.validator = jsonschema.Draft7Validator

    def validate_json(self, json_response, schema_path, encoding=None):
        """
        Method to validate JSON according to the schema
        :param json_response: Response received from API in JSON format
        :param schema_path:
        :param encoding: Encoding (None by default)
        :return: Validation result with status (True or False) and errors (if any)
        """
        try:
            resp = json_loads(json_response)
        except Exception:
            raise TypeError("Response is not in JSON format")

        with open(schema_path, encoding=encoding) as schema_file:
            schema = json_loads(schema_file.read())
        validator = self.validator(schema)
        errors = validator.iter_errors(resp)
        errors_examples = []
        unique_schema_path = []
        for e in errors:
            if set(e.relative_schema_path) not in unique_schema_path:
                unique_schema_path.append(set(e.relative_schema_path))
                errors_examples.append({
                    "schema_path": list(e.relative_schema_path),
                    "error_message": e.message,
                    "response_path": "[\'" + "\'][\'".join(
                        str(i) for i in list(e.relative_path)) + "\']"
                })
        if errors_examples:
            errors_examples.insert(0, {"abspath": schema_path})
            allure.attach(body=json_dumps(resp, indent=2), name="Response JSON")
        return Validation(True if not errors_examples else False, json_dumps(errors, indent=3))


class AuthorizationValidate:
    """
    Class of validator for HTML response
    """
    def __init__(self):
        self.beautiful_soup = BeautifulSoup

    def is_response_unauthorized(self, response):
        soup = self.beautiful_soup(response, "html.parser")
        return Validation(True if soup.find('meta', attrs={'name': 'google-site-verification'}) else False,
                          "Cannot find Google Authorization element")
