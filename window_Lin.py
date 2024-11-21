"""
Эта программа выводит окно с загадками для Linux OS
"""

import tkinter as tk
import os
import ctypes
from riddles import creat_riddles

# Генерация первой загадки
current_riddle, current_answer = creat_riddles()



def make_window_topmost():
    """Делаем окно всегда сверху."""
    root.attributes('-topmost', True)


# Настройки для X11
def set_x11_window_properties():
    """Настройка окна через X11."""
    try:
        x11 = ctypes.CDLL("libX11.so")
        x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
        x11.XOpenDisplay.restype = ctypes.c_void_p

        display = x11.XOpenDisplay(None)
        if not display:
            raise EnvironmentError("Не удалось открыть X11 Display.")

        # Установка свойств окна
        x11.XStoreName(display, ctypes.c_ulong(root.winfo_id()), b"Linux Fullscreen Window")
        x11.XSync(display, False)
    except Exception as e:
        print(f"Ошибка настройки X11: {e}")


# Проверяем текущую оконную систему
session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
if session_type == "x11":
    print("Используется X11.")
elif session_type == "wayland":
    print("Используется Wayland. Программа может работать иначе.")


def check_answer():
    """Обрабатываем ввод пользователя и проверяем ответ."""
    global current_riddle, current_answer

    # Получаем текст из поля ввода
    user_answer = entry.get().strip()

    if user_answer == current_answer:
        # Если ответ правильный
        label.config(text="Правильно! Молодец!")
        root.after(2000, root.destroy)  # Закрываем окно через 2 секунды
    else:
        # Если ответ неправильный
        current_riddle, current_answer = creat_riddles()  # Генерируем новую загадку
        label.config(
            text=f"Ответ неверный! Попробуй новую загадку "
                 f"(Ответ с заглавной буквы):\n\n{current_riddle}"
        )
        entry.delete(0, tk.END)  # Очищаем поле ввода


# Создаем окно
root = tk.Tk()
root.title("Linux Fullscreen Riddles")

# Блокируем стандартное закрытие окна
root.protocol("WM_DELETE_WINDOW")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Растягиваем окно на весь экран
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Убираем рамку окна
root.overrideredirect(True)

# Делаем окно всегда сверху
make_window_topmost()

# Принудительно фокусируем окно
root.after(200, lambda: root.focus_force())

# Настраиваем окно через X11, если оно используется
if session_type == "x11":
    root.after(300, set_x11_window_properties)

# Добавляем текстовую метку с загадкой
label = tk.Label(
    root,
    text=f"Реши загадку (Ответ с заглавной буквы):\n\n{current_riddle}",
    font=("Arial", 16),
    fg="white",
    bg="black",
)
label.pack(expand=True, fill=tk.BOTH)

# Добавляем поле ввода
entry = tk.Entry(root, width=20, font=("Arial", 14))
entry.pack(pady=10)

# Добавляем кнопку для обработки ввода
button = tk.Button(root, text="Ответить", command=check_answer)
button.pack(expand=False, padx=20, pady=30)

# Запуск основного цикла окна
root.mainloop()