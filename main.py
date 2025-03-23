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

# --- Настройки прокси ---
PROXY_IP = "98.152.200.61"  
PROXY_PORT = 8081  
PROXY_TYPE = "http"  # Измени на "socks5", если используешь SOCKS5

# Подключение к прокси
if PROXY_TYPE == "socks5":
    PROXY = (PROXY_IP, PROXY_PORT, "socks5")
elif PROXY_TYPE == "http":
    PROXY = ("http", PROXY_IP, PROXY_PORT)
else:
    PROXY = None  # Без прокси

massage1 = """♻️ Хочешь зарабатывать на автомате?
Рекламируй нашего Telegram-бота и получай деньги без ограничений! 📈
🔸 Чем больше привёл людей – тем больше заработал!
🔸 Работа без вложений и опыта
🔸 Всего пару действий – и деньги начинают капать на твой баланс 💰
Пиши мне в лс и начни прямо сейчас!"""

async def send_messages():
    """Функция для рассылки сообщений в Telegram."""
    while True:
        try:
            async with TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=PROXY) as client:
                await client.start()
                if not await client.is_user_authorized():
                    print("Ошибка: клиент не авторизован.")
                    return
                
                with open("chats.txt", "r", encoding="utf-8") as file:
                    chats = [line.strip() for line in file if line.strip()]
                
                for chat in chats:
                    try:
                        await client(SendMessageRequest(chat, massage1))
                        print(f"✅ Сообщение отправлено в {chat}")
                        delay = random.uniform(30, 60)  
                        print(f"⏳ Ожидание {delay:.2f} секунд перед следующим сообщением...")
                        await asyncio.sleep(delay)
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait: необходимо подождать {e.seconds} секунд.")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        print(f"❌ Ошибка при отправке в {chat}: {e}")

        except Exception as e:
            print(f"🚨 Ошибка соединения: {e}. Перезапуск через 30 сек...")
            await asyncio.sleep(30)  

async def handle(request):
    return web.Response(text="Сервер работает!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    return app

async def main():
    asyncio.create_task(send_messages())  

    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("🌍 Веб-сервер запущен на порту 8080...")
    while True:
        await asyncio.sleep(3600)  

asyncio.run(main())
