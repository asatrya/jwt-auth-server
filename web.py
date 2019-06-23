import json
from datetime import datetime, timedelta

from aiohttp import web
import jwt

from models import User

User.Objects.create(email='user@email.com', password='password')

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600


def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)


async def login(request):
    post_data = await request.post()

    try:
        user = User.Objects.get(email=post_data['email'])
        user.match_password(post_data['password'])
    except (User.DoesNotExist, User.PasswordDoesNotMatch):
        return json_response({'message': 'Wrong credentials'}, status=400)

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM).decode('utf-8')
    return json_response({'token': jwt_token})


async def get_user(request):
    return json_response({'user': str(request.user)})


async def auth_middleware(app, handler):
    def get_token(header):
        if not header.startswith('Bearer '):
            return header
        else:
            return header[len('Bearer '):]

    async def middleware(request):
        request.user = None
        jwt_token = get_token(request.headers.get('authorization', None))
        print('Token reveived=' + jwt_token)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except jwt.DecodeError as e:
                return json_response({'message': 'Token is invalid: ' + str(e)}, status=400)
            except jwt.ExpiredSignatureError:
                return json_response({'message': 'Token is expired'}, status=400)

            request.user = User.Objects.get(id=payload['user_id'])
        return await handler(request)

    return middleware


app = web.Application(middlewares=[auth_middleware])
app.router.add_route('GET', '/get-user', get_user)
app.router.add_route('POST', '/login', login)
