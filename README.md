This article assumes Python 3.5 to use nice asyncio coroutine syntax.

```bash
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
gunicorn web:app --bind localhost:8082 --worker-class aiohttp.worker.GunicornWebWorker --reload
```

As it is a demo application, there is not much error handling, but only essential code to show how to use JWT.

Request

```bash
curl --request POST   \
    --url http://localhost:8082/login   \
    --header 'Content-Type: application/json'   \
    --header 'X-Api-Key: secret'   \
    --header 'cache-control: no-cache'   \
    --data '{"account": "admin", "password": "password"}'
```
