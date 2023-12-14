import uvicorn

from fastapi import FastAPI

from routers import roles, user, token, executors, orders

app = FastAPI()

for item in [roles, user, token, executors, orders]:
    app.include_router(item.router)

if __name__ == '__main__':
    uvicorn.run(app)
