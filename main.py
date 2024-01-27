import os
import telebot
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot
from pydantic import BaseModel
from telebot import types
class TelegramUpdate(BaseModel):
    update_id: int
    message: dict

app = FastAPI()

# Load variables from .env file if present
load_dotenv()

# Read the variable from the environment (or .env file)
bot_token = os.getenv('BOT_TOKEN')
secret_token = os.getenv("SECRET_TOKEN")
#webhook_url = os.getenv('CYCLIC_URL', 'http://localhost:8181') + "/webhook/"
bot = Bot(token=bot_token)
bot1 = telebot.TeleBot(bot_token)
#bot.set_webhook(url=webhook_url)
#webhook_info = bot.get_webhook_info()
#print(webhook_info)

def auth_telegram_token(x_telegram_bot_api_secret_token: str = Header(None)) -> str:
    print(x_telegram_bot_api_secret_token, secret_token,'1')# return true # uncomment to disable authentication
    if x_telegram_bot_api_secret_token != secret_token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return x_telegram_bot_api_secret_token
    

@app.post("/webhook/")
async def handle_webhook(update: TelegramUpdate, token: str = Depends(auth_telegram_token)):
    chat_id = update.message["chat"]["id"]
    text = update.message["text"]
    # print("Received message:", update.message)

    if text == "/start":
        with open('hello.gif', 'rb') as photo:
            await bot.send_message(chat_id=chat_id, text="Welcome to Cyclic Starter Python Telegram Bot!")
            bot1.send_message(message.chat.id, f'*Пользовательское соглашение*\nДанный чат-бот (далее - Бот) принадлежит небанковской кредитно-финансовой организации "Данмарт" (далее - Организация) и заключается с пользователем мессенджера Телеграм (далее - Пользователь).\n\n*Условия*\n\n*Организация имеет право на:*\n•Открытие и закрытие нового долга Пользователя\n•Оповещение Пользователя о непогашенном долге посредством Бота\n•Хранение персональных данных Пользователя в базе данных Организации\n•Изменение услуг, предоставляемых Ботом\n\n*Пользователь имеет право на:*\n•Использование услуг Бота\n•Расторжение договора в одностороннем порядке по инициативе Пользователя\n\n`Нажимая кнопку "✅Принимаю!" Вы подтверждаете, что полностью ознакомлены и согласны с условиями Пользовательского соглашения`')
    else:
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text="Yo!")

    return {"ok": True}

