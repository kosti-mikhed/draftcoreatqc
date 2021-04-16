from collections import namedtuple

Response = namedtuple('Response', ['status_code', 'body'])


class Requests:

    def __init__(self, rest):
        """
        Initializing Requests object
        :param rest: Rest session
        """
        self.rest = rest

    def send_request(self,
                     method: str,
                     url: str,
                     **kwargs) -> Response:
        """
        Basic method for sending request
        :param method: HTTP method
        :param url: URL where request is to be sent
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        response = self.rest.request(method=method,
                                     url=url,
                                     **kwargs)
        resp = Response(status_code=response.status_code,
                        body=response.text)
        return resp

    def get(self,
            url: str,
            params: dict = None,
            **kwargs) -> Response:
        """
        GET request
        :param url: URL where request is to be sent
        :param params: request query parameters
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        return self.send_request(method="GET",
                                 url=url,
                                 params=params,
                                 **kwargs)

    def post(self,
             url: str,
             body: dict = None,
             **kwargs) -> Response:
        """
        POST request
        :param url: URL where request is to be sent
        :param body: Request body
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        return self.send_request(method="POST",
                                 url=url,
                                 json=body,
                                 **kwargs)
