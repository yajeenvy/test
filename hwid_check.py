from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
import os

app = FastAPI()

# Инициализация Firebase (ключ берем из переменных окружения)
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "mangabuffauth",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDGVGiS43xc0QEC\njjIJRFVXigWXu9cQCixLHwR7twCDzCvUJ83Y8BAGWbQQz3RJZWz/az7/Gz6d+4iJ\nEPlQpu6DepoY51rs1Ma53x6WwS4438tcERARv3bcPVW+5+VCx8Jb2LwQz0FYP/OM\nbGGNJcQ2T3pB64elOJLS2nLZBaTiQ45C1HZtoDNeBwkaCJy5G+SMMz+b7zuHEosB\nzz3uXXFloK2lRwjULbYEpyDky1LkIhHJWBsXigAjRxKTciuVoA+NAzATEwpeYwA6\neFNq6fpYavTB8PL8hmwXSZwCPlUnrBhF5sOmePHOTN++GOqzlwN/uC+WyL3HfgEe\nWvR+HLLjAgMBAAECggEADx1OrOcWSrKI66tvh8JD6Lx1iadAkBHeZ0kxW8ZKDUFJ\nk80GxIIjDoDWlrNgrtlCccK4FdP7NSn+sUdwYKOgKLf2t3AmP0dF79NfruiA/8ea\nZWVNfrTDN6ya9MYSdEDqAHrndjZ9Sd7xziFSW+Hlbqgm7pAnEcHaeqQ4PW7PLokK\nGw1kh8UzwXRWNCH4Z0cLDo3PLGECe95HFfdmVRk/z6jWLJQUErNcKBD8k5xpPuwC\nvJICJ3HNt3UIv17A60h7MY4DJmr/lusRRvRasrk4O4QlUk6RInEazQxHCQH95TZw\nRANlNpGnYc78xz4RxTR4a8l/ErQ4ch2UZoeJeLWmHQKBgQDnAN7UjHsIwx5aLz2p\nUbiTjDdbYkwHU94B8ektgiQDsBIJy8aZLkDenDSJi7kwf2WRIrBpcNdoulyNicnY\nSzZcN6UU2zu5FxdpKuLX4TEDuSb+3RrHEPL36Ajipk+2UikMvTYkicb2LVyVTHVG\nQLfG8weUK+bwgKHtTUpXgZ8TpwKBgQDbym4A86MGb4qRhe/agZUr9lQ4YOP5Lz68\n3qrssneOUBz8zzY8GHYCxlD8PbnnYV2rjGYz0bQyoFzWJ+YTEIYflclMbYZH4JHG\nkwy/k6ujkx+7B0LP/c+dzAQ2Le2ZrBrxx7OOoo7f88AAubaoaDLHKMUQyMtYCUYZ\ntJ7tMJy+ZQKBgEJ3fKY5uZj+03ftiddzPSGvQapYsTmWhxWWLpq6jHRHMBmDeaRP\nq7ihx3ggLOvobCgDjDD6l/B5VvIeyGYk1gJYvHYw0pFiNIk9HsIw+HJyzuacZf0L\nQm3UZOIaKmtyXn9c3fxLbGUfDjmjI0dQjdB/0xluPGfNC0qFZ7OgB06XAoGBANM6\nkM3JWHvu5rVEi2br8nj1m6szMuVgSmMpfAtO2SekRreQTQckWwX/ogVJLUj5ghRE\nMlTKzOt6wr3uSmc4Ei54vaT9/XdGk9LLsAzN1r61vmD4cXWC7+0vDT0klpyBksOa\nsS37fGQu1e/ci3b97Q8KV5nx37sT7pL1y2cYuQshAoGBAN+fQ9sXSzjdS2zbV68A\nGJbqtPXXOrbobrNA+ZxQCY9StPbKhg42vNygbC6/7HNvPum11MvIBHVeldn0cYhP\ntd7qiZW7+PgcGksIeYEc/oKziRbBIUYEWrqNfZcTdHUaY2Qnk1Jg4lk+mQNJ4mGb\nIw9cVbfdMHQLHOTkjnNzpS5A\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@mangabuffauth.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()

class HWIDRequest(BaseModel):
    hwid: str

@app.post("/check")
async def check_hwid(request: HWIDRequest):
    try:
        doc = db.collection("authorized_hwids").document(request.hwid).get()
        return {"access_granted": doc.exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))