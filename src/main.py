from flask import Flask, request, abort
from functools import wraps
from secret import secret
from auth.flask import TokenAuth

app = Flask(__name__)

service_auth = TokenAuth(secret)

@app.before_request
def authenticate_request():
    service_auth.authenticate_request()

@app.after_request
def apply_auth_header(resp):
    return service_auth.apply_auth_header(resp)

@app.route("/", methods=["GET", "POST"])
def hello():
    app.logger.info("A successful request!")
    return "You did it!"

if __name__ == "__main__":
    app.run(port=8007)
