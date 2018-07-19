# Secure Communication Token Demo

This is some toy code for our HTTP token auth between services. It has a client and a Flask app.

# Run It on Your Machine

```
pipenv install
pipenv run python src/main.py
```

And then in a new terminal window:

```
pipenv run python src/client.py
```

The client will try a couple unsuccessful requests, and then a successful request where it also validates the response.

# Run It with Docker

I included Docker setup so that I could check that the implementation works when running with NGINX and uwsgi. (It does.)

Start the server:

```
docker-compose up
```

And then in a new terminal window:

```
pipenv run python src/client.py
```
