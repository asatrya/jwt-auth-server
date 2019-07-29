# Simple JWT Auth Server

A simple application demonstrating an implementation of JWT server in Python.

## Set virtual environment and install dependency

```bash
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the webserver

```bash
gunicorn web:app --bind localhost:8082 --worker-class aiohttp.worker.GunicornWebWorker --reload
```

## Try to make a request

Create a login request

```bash
curl --request POST   \
    --url http://localhost:8082/login   \
    --header 'Content-Type: application/json'   \
    --header 'X-Api-Key: secret'   \
    --header 'cache-control: no-cache'   \
    --data '{"account": "admin", "password": "password"}'
```

The response should be similar to this

```bash
{
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1NjQzNzM4NTJ9.8eRX7j1mfE269rNfi2ndSbgKeofqDXq748x6RUhuw3k"
}
```
