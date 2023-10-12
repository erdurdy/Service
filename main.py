from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
import json

class Credentials(BaseModel):
    number: int = Field(title="Phone number")
    code: int = Field(title="Private number code")



app = FastAPI()

@app.post("/")
def cheker(cred: Credentials):
    
    csrf_url = "https://astu.tm/api/auth/csrf"
    csrf_res = requests.get(csrf_url)
    
    csrf_token = csrf_res.json()
    
    
    payload = {
        "redirect": "false", 
        "phoneNumber": cred.number,
        "password": cred.code,
        "csrfToken": csrf_token["csrfToken"], 
        "callbackUrl": "https://astu.tm/login?callbackUrl=https://astu.tm/profile",
        "json": "true"
    }

    cred_url = "https://astu.tm/api/auth/callback/credentials?"
    cred_res = requests.post(cred_url, data=payload, cookies=dict(csrf_res.cookies))
    
    res_content = cred_res.content
    res_dict = json.loads(res_content.decode('utf-8'))
    
    res_url = res_dict["url"]
    
    if "login" in res_url:
        return {"status": 200} 

    if "auth" in res_url:
        return {"status": 400} 

