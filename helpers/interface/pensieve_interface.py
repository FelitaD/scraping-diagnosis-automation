from os import getenv

import requests


class PensieveBasic:
    URL = getenv('PENSIEVE_URL', 'http://127.0.0.1:8000')
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)"
    }
    METHODS = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'HEAD': requests.head
    }

    @classmethod
    def request(cls, endpoint: str, method: str = "GET", body: dict = None, **params):
        path = cls.__build_path(endpoint, **params)
        kwargs = {'headers': cls.HEADERS}
        if body is not None:
            kwargs['json'] = body
        try:
            response = cls.METHODS[method](path, verify=False, **kwargs)
        except ConnectionError as ce:
            raise ConnectionError(
                "A connection error occured when requesting Pensieve at url %s:\n%s" % (endpoint, repr(ce))
            )
        else:
            return cls.__build_response(endpoint, response)

    @staticmethod
    def __build_response(endpoint, response):
        status_code = response.status_code
        if status_code in (200, 204):
            return response.json()
        # else:
            # raise Exception(
            #     "An error occurred when processing request  %s: %s" % (endpoint, response)
            # )

    @classmethod
    def __build_path(cls, endpoint, **kwargs):
        params = '&'.join(['%s=%s' % (key, value) for (key, value) in kwargs.items()])
        return '%s%s?%s' % (cls.URL, endpoint, params)
