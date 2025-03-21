import subprocess
import time

URL = "https://awake-yolanthe-qexdy3-f008b061.koyeb.app/"

while True:
    try:
        result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", URL], capture_output=True, text=True)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Статус код: {result.stdout.strip()}")
    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(120)  # Ожидание 10 минут (600 секунд)
    
