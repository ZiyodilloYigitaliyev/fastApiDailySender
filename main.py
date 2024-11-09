from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import os
from dotenv import load_dotenv
import pytz  # Yangi kutubxona

# .env faylini yuklash
load_dotenv()

app = FastAPI()
secret_key = os.getenv("SECRET_KEY")
scheduler = BackgroundScheduler()
# Django API URL manzili
DJANGO_API_URL = os.getenv("DJANGO_API_URL")  # Django API URL manzilini o'zingizga moslang

# Har kuni yuboriladigan vazifa
def send_daily_request():
    try:
        # Asia/Tashkent vaqt zonasini olish
        tz = pytz.timezone('Asia/Tashkent')
        now = datetime.datetime.now(tz)  # O'zbekiston vaqtiga moslangan vaqt
        
        response = requests.get(DJANGO_API_URL, params={"message": "Har kunlik so'rov yuborildi"})
        if response.status_code == 200:
            print(f"{now}: So'rov muvaffaqiyatli yuborildi")
        else:
            print(f"{now}: Xato - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"{datetime.datetime.now()}: So'rovda xatolik: {e}")

@app.on_event("startup")
def start_scheduler():
    # Har kuni soat 17:00 (Toshkent vaqti) da yuborilsin
    scheduler.add_job(send_daily_request, 'cron', hour=0, minute=0, timezone='Asia/Tashkent')
    scheduler.start()

# Ilova yopilganda scheduler ham to'xtaydi
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

# Test uchun asosiy sahifa
@app.get("/")
async def root():
    return {"message": "FastAPI va Apscheduler ilovasi ishga tushdi"}
