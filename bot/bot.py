from balethon import Client, conditions
from dotenv import load_dotenv
import os
import requests

load_dotenv(".env")
bot = Client(os.getenv("BALE_TOKEN"))
eitaa_token = os.getenv("EITAA_TOKEN")
rubika_token = os.getenv("RUBIKA_TOKEN")
eitaa_channel = int(os.getenv("EITAA_CHANNEL"))

@bot.on_message(conditions.channel)
async def automation(*,message):
    # rubika
    chat_id = (
        os.getenv("RUBIKA_CHAT_ID")
    )

    text = message.text
    url = f"https://botapi.rubika.ir/v3/{rubika_token}/sendMessage"

    data = {"chat_id": chat_id, "text": text}

    response = requests.post(url, json=data)

    # eitaa
    url = f"https://eitaayar.ir/api/{eitaa_token}/sendMessage?chat_id={eitaa_channel}&text={text}&date=0&pin=off"

    response = requests.get(url)


bot.run()