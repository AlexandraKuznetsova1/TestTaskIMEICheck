from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

IMEI_API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'


def check_imei(imei: str):
    url = f"https://imeicheck.net/api/check-imei"
    headers = {'Authorization': f'Bearer {IMEI_API_TOKEN}'}
    response = requests.post(url, json={'imei': imei}, headers=headers)
    return response.json()


@app.post("/api/check-imei")
async def api_check_imei(imei: str, token: str = Depends(oauth2_scheme)):
    if not validate_token(token):  # Логика проверки токена
        raise HTTPException(status_code=403, detail="Неавторизованный доступ")

    if len(imei) != 15 or not imei.isdigit():
        raise HTTPException(status_code=400, detail="Некорректный IMEI")

    return check_imei(imei)


def validate_token(token: str) -> bool:
    # Логика проверки токена
    return token in ["YOUR_VALID_TOKENS"]


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)