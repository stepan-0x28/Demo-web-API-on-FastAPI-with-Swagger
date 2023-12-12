import uvicorn

from fastapi import FastAPI

from routers import token, user, orders

app = FastAPI()

for item in [token, user, orders]:
    app.include_router(item.router)

if __name__ == '__main__':
    uvicorn.run(app)
