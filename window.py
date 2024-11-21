"""
Эта программа выводит окно с загадками для macOS
"""

import tkinter as tk
from riddles import creat_riddles
from AppKit import (
    NSApplication,
    NSApplicationPresentationHideDock,
    NSApplicationPresentationHideMenuBar,
    NSApp,
    NSWindow,
)

# Генерируем первую загадку и её ответ
current_riddle, current_answer = creat_riddles()


def off_close():
    """Блокируем стандартное закрытие окна."""
    pass


def off_minimize():
    """Отключаем возможность сворачивания окна."""
    app = NSApplication.sharedApplication()
    options = (
        NSApplicationPresentationHideDock
        | NSApplicationPresentationHideMenuBar
    )
    app.setPresentationOptions_(options)


def make_window_topmost():
    """Делаем окно всегда сверху остальных окон."""
    window = NSApp.windows()[0]
    window.setLevel_(NSWindow.LevelFloating)


def check_answer():
    """Обрабатываем ввод пользователя и проверяем ответ."""
    global current_riddle, current_answer #Задаем глобальные переменные это дальше пригодиться
    user_answer = entry.get().strip()
    if user_answer == current_answer:
        # Если ответ правильный
        label.config(text="Правильно! Молодец!")
        root.after(2000, root.destroy)  # Закрываем окно через 2 секунды, чтобы пользователь увидел как мы его хвалим
    else:
        # Если ответ неправильный
        current_riddle, current_answer = creat_riddles()  # Генерируем новую загадку, благодоря глобал
        label.config(
            text=f"Ответ неверный! Попробуй новую загадку "
                 f"(Ответ с заглавной буквы):\n\n{current_riddle}"
        )
        entry.delete(0, tk.END)


# Создаем окно
root = tk.Tk()
root.title("Загадки")

# Блокируем стандартное закрытие окна
root.protocol("WM_DELETE_WINDOW", off_close)

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Растягиваем окно на весь экран
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Убираем рамку окна
root.overrideredirect(True)

# Устанавливаем окно поверх всех остальных
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', True))

# Принудительно фокусируем окно
root.after(200, lambda: root.focus_force())

# Отключаем возможность сворачивания окна
root.after(100, off_minimize)

# Устанавливаем окно "всегда сверху" через функцию
root.after(300, make_window_topmost)

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