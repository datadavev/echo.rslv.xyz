"""
FastAPI application that reflects the request.
"""

import json
import typing

import fastapi
import fastapi.middleware.cors

from . import __version__, __date__


class HumanJsonResponse(fastapi.Response):
    media_type = 'application/json'

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(', ', ': '),
        ).encode('utf-8')


app = fastapi.FastAPI(
    title='Echo',
    description=f'{__doc__}\nDate: {__date__}',
    version=__version__,
    license_info={
        'name': 'GPLv3',
        'url': 'https://www.gnu.org/licenses/gpl-3.0.en.html',
    },
    openapi_url='/api/v1/openapi.json',
    docs_url='/api',
)

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=[
        '*',
    ],
    allow_credentials=True,
    allow_methods=[
        'GET',
        'HEAD',
    ],
    allow_headers=[
        '*',
    ],
)


def request_to_response(
    request: fastapi.Request, path: str
) -> typing.Dict[str, typing.Any]:
    headers = {}
    for k, v in request.headers.items():
        if not k.lower().startswith('x-vercel'):
            headers[k] = v

    response = {
        'url': request.url._url,
        'method': request.method,
        'path': path,
        'query': request.query_params,
        'headers': headers,
    }
    return response


@app.get('/favicon.ico', include_in_schema=False)
async def get_favicon():
    raise fastapi.HTTPException(status_code=404, detail='Not found')


@app.get('/{path:path}', response_class=HumanJsonResponse)
def echo_get(request: fastapi.Request, path: str):
    return request_to_response(request, path)


@app.head('/{path:path}', response_class=HumanJsonResponse)
def echo_head(request: fastapi.Request, path: str):
    return request_to_response(request, path)


@app.post('/{path:path}', response_class=HumanJsonResponse)
def echo_post(request: fastapi.Request, path: str):
    return request_to_response(request, path)


@app.put('/{path:path}', response_class=HumanJsonResponse)
def echo_put(request: fastapi.Request, path: str):
    return request_to_response(request, path)
