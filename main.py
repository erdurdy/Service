from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from clients import auth
from requests.exceptions import HTTPError

app = FastAPI()


class Credentials(BaseModel):
    phone: int = Field(title="Phone number")
    code: int = Field(title="Private number code")


@app.post("/authenticate", status_code=200)
def authenticate(credentials: Credentials):
    try:
        csrf_token = auth.get_csrf_token()
        auth.authenticate(credentials.phone, credentials.code, csrf_token)
    except HTTPError:
        raise HTTPException(status_code=400)

    return {}
