import requests


CSRF_URL = "https://astu.tm/api/auth/csrf"
AUTH_URL = "https://astu.tm/api/auth/callback/credentials?"

def get_csrf_token():
    response = requests.get(CSRF_URL)
    response.raise_for_status()
    data = response.json()
    return data["csrfToken"]

def authenticate(phone, code, csrf_token):
    payload = {
        "redirect": "false", 
        "phoneNumber": phone,
        "password": code,
        "csrfToken": csrf_token,
        "callbackUrl": "https://astu.tm/login?callbackUrl=https://astu.tm/profile",
        "json": "true"
    }

    response = requests.post(AUTH_URL, data=payload, allow_redirects=False)
    response.raise_for_status()

    data = response.json()
    if "profile" not in data["url"]:
        raise requests.exceptions.HTTPError(response=response)
