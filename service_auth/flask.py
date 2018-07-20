from flask import request, abort
from flask import current_app as app
from email.utils import formatdate
from service_auth.http_token import validate_token, make_token


class AuthHeader():
    def __init__(self, secret, header_field="X-Token-Auth"):
        self._secret = secret
        self._header_field = header_field

    def bail(self, reason):
        app.logger.warning(reason)
        return abort(401)

    def authenticate_request(self):
        auth_token = request.headers.get(self._header_field)
        date = request.headers.get("Date")
        host = request.headers.get("Host")
        body = request.data.decode()
        if not (auth_token and date and host):
            return self.bail("request was missing necessary headers")

        if validate_token(auth_token, self._secret, [date, host, body]):
            return

        else:
            return self.bail("request sent an invalid token")

    def response_date(self, resp):
        return resp.headers.setdefault(
            "Date", formatdate(timeval=None, localtime=False, usegmt=True)
        )

    def response_code(self, resp):
        return str(resp.status_code)

    def apply_auth_header(self, resp):
        date = self.response_date(resp)
        code = self.response_code(resp)
        body = resp.data.decode()
        resp.headers[self._header_field] = make_token(self._secret, [date, code, body])

        return resp
