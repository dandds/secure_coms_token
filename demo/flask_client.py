import sys
import os

sys.path.append(os.path.dirname(os.path.realpath("{}/..".format(__file__))))
import requests as rq
from secret import secret
from email.utils import formatdate
from service_auth.http_token import make_token, validate_token

url = "http://localhost:8007"
data = "this is a request!"
auth_header = "X-Token-Auth"
s = rq.Session()


def prepare_request():
    headers = {
        "Host": "localhost:8007",
        "Date": formatdate(timeval=None, localtime=False, usegmt=True),
    }
    req = rq.Request("POST", url, data=data, headers=headers)
    return s.prepare_request(req)


def add_auth(request):
    request.headers[auth_header] = make_token(
        secret, [request.headers["Date"], request.headers["Host"], request.body]
    )
    return request


class BadHostError(Exception):
    pass


def validate_response(resp, *args, **kwargs):
    print("Validating response from host...")
    auth_token = resp.headers.get(auth_header)
    date = resp.headers.get("Date")
    code = str(resp.status_code)
    body = resp.text
    if validate_token(auth_token, secret, [date, code, body]):
        print("We got a valid token in return!")
        return

    else:
        raise BadHostError("the host did not provide authentication!")


print("***Sending a bad request no auth header")
req = prepare_request()
resp = s.send(req)
print("response code: {}".format(resp.status_code))


print("\n***Sending a bad request with an invalid auth header")
req = prepare_request()
req.headers["X-ATAT-Auth"] = "abc123"
resp = s.send(req)
print("response code: {}".format(resp.status_code))


print("\n***Sending valid request!")
# append response callback
s.hooks["response"].append(validate_response)
req = prepare_request()
add_auth(req)
resp = s.send(req)
print("response code: {}".format(resp.status_code))
