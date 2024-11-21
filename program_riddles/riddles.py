"""
Эта программа обрабатывает тхт файл с задачами(ответами) и выгружает их в список загадка, ответ.
Также есть функция окна ТК которая выводит загадки, но не импортируется, а написана как начальная
"""

import random
import tkinter as tk



# Чтение файла и разбиение на блоки по разделителю
try:
    with open('riddles.txt', 'r', encoding='utf-8') as file:
        content = file.read()  # Читаем всё содержимое файла
        riddles = content.split('******')  # Разделяем по ******

    # Форматируем загадки: выделяем текст и ответ
    formatted_riddles = []
    for riddle in riddles:
        riddle = riddle.strip()
        if '(' in riddle and ')' in riddle:
            question, answer = riddle.rsplit('(', 1)  # Разделяем по последней скобке
            formatted_riddles.append((question.strip(), answer.strip(')').strip()))
except FileNotFoundError:
    print("Файл 'riddles.txt' не найден. Убедитесь, что файл находится в одной папке с программой.")
    exit(1) # Сделано для того чтобы, пользователь сразу видел где у него ошибка


def creat_riddles():
    """
    Генерация случайной загадки из списка.
    """
    random_riddle, correct_answer = random.choice(formatted_riddles)
    return random_riddle, correct_answer


def check_answer():
    """
    Проверка ответа пользователя и обновление состояния программы.
    """
    global current_riddle, current_answer

    user_answer = entry.get().strip()

    if user_answer == current_answer:
        label.config(text="Правильно! Молодец!")
        root.after(2000, root.destroy)  # Закрываем окно через 2 секунды
    else:
        current_riddle, current_answer = creat_riddles()
        label.config(
            text=(
                f"Ответ неверный! Попробуй новую загадку "
                f"(Ответ с заглавной буквы):\n\n{current_riddle}"
            )
        )
        entry.delete(0, tk.END)


if __name__ == "__main__":
    # Генерируем первую загадку и её ответ
    current_riddle, current_answer = creat_riddles()

    # Создаём окно
    root = tk.Tk()
    root.title("Загадки")

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

    # Запуск цикла обработки событий
    root.mainloop()