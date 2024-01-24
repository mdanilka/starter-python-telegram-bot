import config
import telebot
from aiohttp import web
import ssl
WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = 8181
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot
from pydantic import BaseModel

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
API_TOKEN = config.Token
bot = telebot.TeleBot(API_TOKEN)

app = web.Application()

# process only requests with correct bot token
async def handle(request):
    if request.match_info.get("token") == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post("/{token}/", handle)

help_string = []
help_string.append("*Some bot* - just a bot.\n\n")
help_string.append("/start - greetings\n")
help_string.append("/help - shows this help")

# - - - messages

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ololo, I am a bot")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")

# - - -

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# start aiohttp server (our bot)
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
