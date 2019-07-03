import json
from datetime import datetime, timedelta

import asyncio
from aiohttp import web
import jwt

from models import User

User.Objects.create(email='admin', password='password')

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600


def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)


@asyncio.coroutine
async def login(request):
    post_data = await request.json()

    try:
        API_KEY = request.headers.get('X-Api-Key', JWT_SECRET)
        user = User.Objects.get(email=post_data['account'])
        user.match_password(post_data['password'])
    except (User.DoesNotExist, User.PasswordDoesNotMatch):
        return json_response({'message': 'Wrong credentials'}, status=400)

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    jwt_token = jwt.encode(payload, API_KEY, JWT_ALGORITHM).decode('utf-8')
    res = json_response({'jwt': jwt_token})
    return res


app = web.Application()
app.router.add_route('POST', '/login', login)
