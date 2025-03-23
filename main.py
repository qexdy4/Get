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

# --- Настройки SOCKS5 Proxy ---
PROXY_IP = "98.152.200.61"
PROXY_PORT = 8081
PROXY = (PROXY_IP, PROXY_PORT)  # Укажи логин и пароль, если требуется

massage1 = """♻️ Хочешь зарабатывать на автомате?
Рекламируй нашего Telegram-бота и получай деньги без ограничений! 📈
🔸 Чем больше привёл людей – тем больше заработал!
🔸 Работа без вложений и опыта
🔸 Всего пару действий – и деньги начинают капать на твой баланс 💰
Пиши мне в лс и начни прямо сейчас!"""

async def send_messages():
    """Функция для рассылки сообщений в Telegram."""
    while True:  # Если соединение разорвётся, перезапускаем
        try:
            async with TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=("socks5", *PROXY)) as client:
                await client.start()  # Полное подключение
                if not await client.is_user_authorized():
                    print("Ошибка: клиент не авторизован.")
                    return
                
                with open("chats.txt", "r", encoding="utf-8") as file:
                    chats = [line.strip() for line in file if line.strip()]
                
                for chat in chats:
                    try:
                        await client(SendMessageRequest(chat, massage1))
                        print(f"✅ Сообщение отправлено в {chat}")
                        delay = random.uniform(180, 300)  # Интервал 30-60 секунд
                        print(f"⏳ Ожидание {delay:.2f} секунд перед следующим сообщением...")
                        await asyncio.sleep(delay)
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait: необходимо подождать {e.seconds} секунд.")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        print(f"❌ Ошибка при отправке в {chat}: {e}")

        except Exception as e:
            print(f"🚨 Ошибка соединения: {e}. Перезапуск через 30 сек...")
            await asyncio.sleep(30)  # Подождать 30 секунд и повторить попытку

async def handle(request):
    """Ответ веб-сервера на запросы."""
    return web.Response(text="Сервер работает!")

async def web_server():
    """Создание и запуск веб-сервера."""
    app = web.Application()
    app.router.add_get("/", handle)
    return app

async def main():
    """Запуск всех процессов: Telegram и веб-сервер."""
    asyncio.create_task(send_messages())  # Рассылка сообщений

    # Запускаем веб-сервер
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("🌍 Веб-сервер запущен на порту 8080...")
    while True:
        await asyncio.sleep(3600)  # Бесконечный цикл для работы сервера

# Запуск асинхронного кода
asyncio.run(main())
