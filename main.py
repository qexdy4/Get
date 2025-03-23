from telethon.sync import TelegramClient
import asyncio
import random
import time
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import FloodWaitError, RPCError

# Укажите ваши данные API
API_ID = 29739265  # Замените на ваш API_ID
API_HASH = "9475db10c792d716e97a51f608871263"  # Замените на ваш API_HASH
SESSION_NAME = "joiner_session"

async def send_messages():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        await client.connect()
        with open("chats.txt", "r", encoding="utf-8") as file:
            chats = [line.strip() for line in file if line.strip()]
        
        for chat in chats:
            try:
                message = await client(SendMessageRequest(chat, "Привет!"))
                print(f"Сообщение отправлено в {chat}")
                delay = random.uniform(1200, 1800)  # Интервал от 20 до 30 минут
                print(f"Ожидание {delay / 60:.2f} минут перед следующим сообщением...")
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                print(f"FloodWait: необходимо подождать {e.seconds} секунд.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Ошибка при отправке в {chat}: {e}")
                
if __name__ == "__main__":
    asyncio.run(send_messages())
