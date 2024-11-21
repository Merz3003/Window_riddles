import platform
import subprocess

def run_script_for_os():
    current_os = platform.system()
    print(f"Определённая ОС: {current_os}")

    # определяем файл для каждой ОС
    if current_os == "Windows":
        script = "window_for_WNs.py"  # скрипт для Windows
    elif current_os == "Darwin":
        script = "window.py"  # скрипт для macOS
    elif current_os == "Linux":
        script = "window_Lin.py"  # скрипт для Linux
    else:
        print("Неизвестная операционная система!")
        return

    # запуск выбранного скрипта
    try:
        # используем subprocess для запуска
        subprocess.run(["python", script], check=True)
    except Exception as e:
        print(f"Ошибка при запуске {script}: {e}")

if __name__ == "__main__":
    run_script_for_os()







