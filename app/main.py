from fastapi import FastAPI
from pydantic import BaseModel
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from app.dao import SecretsDAO


class Sgenerate_secret(BaseModel):
    body: str
    password: str

class Sget_secret(BaseModel):
    password: str

app = FastAPI()

@app.get('/')
async def home():
    return 'Hello'

@app.post('/generate')
async def generate_secret(body: Sgenerate_secret) -> str:
    result = await SecretsDAO.add(body.password, body.body)
    return result.url

@app.post('/secrets/{secret_key}')
async def get_secret(secret_key: str, body: Sget_secret):
    return await SecretsDAO.get_and_delete(body.password, secret_key)


def main():
    import uvicorn

    uvicorn.run(
        app="app.main:app",
        reload=True,
    )


if __name__ == "__main__":
    main()
