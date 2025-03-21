import subprocess
import time
import asyncio
from aiohttp import web

URLS = [
    "https://awake-yolanthe-qexdy3-f008b061.koyeb.app/",
    "https://zygomorphic-suellen-qexdy4-56b26d2d.koyeb.app/"
]

async def check_urls():
    """Функция для проверки доступности всех URL."""
    while True:
        for url in URLS:
            try:
                result = subprocess.run(
                    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], 
                    capture_output=True, 
                    text=True
                )
                status = result.stdout.strip()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {url} -> Статус код: {status}")
            except Exception as e:
                print(f"Ошибка при проверке {url}: {e}")

        await asyncio.sleep(120)  # Ожидание 2 минуты

async def handle(request):
    """Ответ веб-сервера."""
    return web.Response(text="Сервер работает!")

async def web_server():
    """Создание веб-сервера."""
    app = web.Application()
    app.router.add_get("/", handle)
    return app

async def main():
    """Запуск веб-сервера и проверки URL параллельно."""
    asyncio.create_task(check_urls())  # Запускаем проверку URL в фоне

    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("Веб-сервер запущен на порту 8080...")
    while True:
        await asyncio.sleep(3600)  # Бесконечный цикл для работы сервера

# Запуск
asyncio.run(main())
