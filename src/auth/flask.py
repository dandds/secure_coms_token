from flask import request, abort
from flask import current_app as app
from email.utils import formatdate
from auth.http_token import validate_token, make_token

class TokenAuth():
    def __init__(self, secret):
        self._secret = secret

    def authenticate_request(self):
        def bail(reason):
            app.logger.warning(reason)
            return abort(401)

        auth_token = request.headers.get("X-ATAT-Auth")
        date = request.headers.get("Date")
        host = request.headers.get("Host")
        body = request.data.decode()
        if not (auth_token and date and host):
            return bail("The client was missing headers we expected!")

        if validate_token(auth_token, self._secret, [date, host, body]):
            return

        else:
            return bail("The client sent an invalid token!")

    def apply_auth_header(self, resp):
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        code = str(resp.status_code)
        body = resp.data.decode()
        resp.headers["X-ATAT-Auth"] = make_token(self._secret, [date, code, body])

        return resp
