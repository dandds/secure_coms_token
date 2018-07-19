from flask import Flask, request, abort
from flask import current_app as app
from functools import wraps
from secret import secret
from http_token import validate_token, make_token
from email.utils import formatdate

app = Flask(__name__)


@app.before_request
def authenticate_request():

    def bail(reason):
        app.logger.warning(reason)
        return abort(401)

    auth_token = request.headers.get("X-ATAT-Auth")
    date = request.headers.get("Date")
    host = request.headers.get("Host")
    body = request.data.decode()
    if not (auth_token and date and host):
        return bail("The client was missing headers we expected!")

    if validate_token(auth_token, secret, [date, host, body]):
        return

    else:
        return bail("The client sent an invalid token!")

@app.after_request
def apply_auth_header(resp):
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    code = str(resp.status_code)
    body = resp.data.decode()
    resp.headers["X-ATAT-Auth"] = make_token(secret, [date, code, body])

    return resp



@app.route("/", methods=["GET", "POST"])
def hello():
    app.logger.info("A successful request!")
    return "You did it!"


if __name__ == "__main__":
    app.run(port=8007)
