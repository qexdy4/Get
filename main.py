
import subprocess
import time
import asyncio
from aiohttp import web

URL = "https://awake-yolanthe-qexdy3-f008b061.koyeb.app/"

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

        await asyncio.sleep(600)  # Ожидание 2 минуты

async def handle(request):
    """Ответ сервера на запросы."""
    return web.Response(text="Сервер работает!")

async def web_server():
    """Создание и запуск веб-сервера."""
    app = web.Application()
    app.router.add_get("/", handle)
    return app

async def main():
    """Запуск веб-сервера и проверки URL параллельно."""
    # Запускаем проверку URL
    asyncio.create_task(check_url())

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
