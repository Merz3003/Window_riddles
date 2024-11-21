"""
Эта программа выводит окно с загадками для Windows OS
"""

import tkinter as tk
from riddles import creat_riddles
import ctypes

# Windows API функции
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Константы Windows API
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_SHOWWINDOW = 0x0040
HWND_TOPMOST = -1
GWL_STYLE = -16
WS_MINIMIZEBOX = 0x20000
WS_MAXIMIZEBOX = 0x10000
WS_SYSMENU = 0x80000

# Генерируем первую загадку и её ответ
current_riddle, current_answer = creat_riddles()


def off_minimize_close(hwnd):
    """Отключаем кнопки свернуть/закрыть."""
    style = user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~(WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU)
    user32.SetWindowLongW(hwnd, GWL_STYLE, style)


def make_window_topmost(hwnd):
    """Делаем окно всегда сверху."""
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)


def stretch_window_to_screen(hwnd):
    """Растягиваем окно на весь экран."""
    screen_width = user32.GetSystemMetrics(0)  # Получаем ширину экрана
    screen_height = user32.GetSystemMetrics(1)  # Получаем высоту экрана
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, screen_width, screen_height, SWP_SHOWWINDOW)


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


# Создаём окно
root = tk.Tk()
root.title("Загадки")

# Получаем хендл окна
root.update_idletasks()
window_handle = ctypes.windll.user32.GetForegroundWindow()
if not window_handle:
    raise RuntimeError("Не удалось найти окно приложения.")

# Убираем рамки окна
root.overrideredirect(True)

# Отключаем кнопки свернуть/закрыть
off_minimize_close(window_handle)

# Делаем окно всегда сверху
make_window_topmost(window_handle)

# Растягиваем окно на весь экран
stretch_window_to_screen(window_handle)

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