import sys
import os
sys.path.append(os.path.dirname(os.path.realpath("{}/..".format(__file__))))
from flask import Flask, request, abort
from functools import wraps
from secret import secret
from service_auth.flask import AuthHeader

app = Flask(__name__)

service_auth = AuthHeader(secret)

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
