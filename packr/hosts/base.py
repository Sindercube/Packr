from typing import List, Literal
from requests import request

from .. import Resource_Pack

class AuthorizationError(Exception):
    pass
class NotFoundError(Exception):
    pass

exception_codes = {
    403: AuthorizationError,
    404: NotFoundError,
}

class Host:

    api_url: str = ''
    headers: dict = {}

    auth_header_key: str
    auth_header_prefix: str = ''

    rp: Resource_Pack
    id: str
    token: str
    upload_url: str

    def __init__(self, resource_pack: Resource_Pack, host_token: str, project_id: str):

        self.rp = resource_pack
        self.id = project_id
        self.token = host_token

        self.headers[self.auth_header_key] = self.auth_header_prefix + host_token
        self.headers['User-Agent'] = 'sindercu.be/packr'

    def publish(self,
        version: str = None,
        title: str = None,
        changelog: str = None,
        minecraft_versions: List[str] = None,
        prerelease: bool = False,
    ):
        pass

    def get(self, url, **data):
        return self.request('get', url, **data)

    def post(self, url, **data):
        return self.request('post', url, **data)

    def patch(self, url, **data):
        return self.request('patch', url, **data)

    def put(self, url, **data):
        return self.request('put', url, **data)

    def delete(self, url, **data):
        return self.request('delete', url, **data)

    def request(self, method, url, headers=None, **data):
        if headers:
            headers = {**self.headers, **headers}
        req = request(method, url, timeout=10, headers=self.headers, **data)
        #if req.status_code in exception_codes:
        #    raise exception_codes[req.status_code]("Couldn't open URL: " + req.reason + f" ({url})")
        return req
