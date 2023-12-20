import uvicorn

from fastapi import FastAPI
from fastapi.routing import APIRoute
from os import environ

from routers import roles, user, token, executors, statuses, orders

app = FastAPI()

for item in [roles, user, token, executors, statuses, orders]:
    for route in item.router.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

    app.include_router(item.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', root_path=environ.get('UVICORN_ROOT_PATH', ''))
