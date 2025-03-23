import subprocess
import time
import asyncio
import random
from aiohttp import web
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import FloodWaitError, RPCError

# --- Telegram API ---
API_ID = 29739265  # Замените на ваш API_ID
API_HASH = "9475db10c792d716e97a51f608871263"  # Замените на ваш API_HASH
SESSION_NAME = "joiner_session"

# --- URL для проверки ---
URL = "zygomorphic-suellen-qexdy4-56b26d2d.koyeb.app/"

async def send_messages():
    """Функция для рассылки сообщений в Telegram."""
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        await client.connect()
        with open("chats.txt", "r", encoding="utf-8") as file:
            chats = [line.strip() for line in file if line.strip()]
        
        for chat in chats:
            try:
                message = await client(SendMessageRequest(chat, "Только у нас ты найдешь эксклюзивный товар и самый свежий стафф по очень привлекательной цене.😜🤟! Шоп в описании профиля!"))
                print(f"Сообщение отправлено в {chat}")
                delay = random.uniform(1200, 1800)  # Интервал от 20 до 30 минут
                print(f"Ожидание {delay / 60:.2f} минут перед следующим сообщением...")
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                print(f"FloodWait: необходимо подождать {e.seconds} секунд.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Ошибка при отправке в {chat}: {e}")

async def check_url():
    """Функция для проверки доступности URL."""
    while True:
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", URL], 
                capture_output=True, 
                text=True
            )
            status = result.stdout.strip()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Статус код: {status}")
        except Exception as e:
            print(f"Ошибка: {e}")

        await asyncio.sleep(120)  # Ожидание 2 минуты

async def handle(request):
    """Ответ веб-сервера на запросы."""
    return web.Response(text="Сервер работает!")

async def web_server():
    """Создание и запуск веб-сервера."""
    app = web.Application()
    app.router.add_get("/", handle)
    return app

async def main():
    """Запуск всех процессов: Telegram, проверка URL и веб-сервер."""
    asyncio.create_task(send_messages())  # Рассылка сообщений
    asyncio.create_task(check_url())  # Проверка URL

    # Запускаем веб-сервер
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("Веб-сервер запущен на порту 8080...")
    while True:
        await asyncio.sleep(3600)  # Бесконечный цикл для работы сервера

# Запуск асинхронного кода
asyncio.run(main())
