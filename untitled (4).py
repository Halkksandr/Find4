import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# Файл для хранения расходов
DATA_FILE = 'expenses.json'

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Поля ввода
        tk.Label(root, text="Сумма:").pack(pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=5)

        tk.Label(root, text="Категория:").pack(pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.pack(pady=5)

        tk.Label(root, text="Дата (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

        # Кнопка добавления расхода
        add_button = tk.Button(root, text="Добавить расход", command=self.add_expense)
        add_button.pack(pady=10)

        # Кнопка подсчета суммы
        calc_button = tk.Button(root, text="Подсчитать сумму", command=self.calculate_total)
        calc_button.pack(pady=10)

        # Список расходов
        self.expenses = self.load_expenses()
        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)
        self.show_expenses()

        # Фильтрация
        tk.Label(root, text="Фильтр по категории:").pack(pady=5)
        self.filter_category_entry = tk.Entry(root)
        self.filter_category_entry.pack(pady=5)
        filter_button = tk.Button(root, text="Применить фильтр", command=self.filter_expenses)
        filter_button.pack(pady=5)

    # Функция для добавления расхода
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()

            if amount < 0:
                raise ValueError("Сумма должна быть положительным числом.")
            self.validate_date(date)

            expense = {
                'amount': amount,
                'category': category,
                'date': date
            }
            self.expenses.append(expense)
            self.save_expenses()
            self.show_expenses()
            self.clear_entries()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    # Функция для валидации даты
    def validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD.")

    # Функция для отображения расходов
    def show_expenses(self):
        self.listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.listbox.insert(tk.END, f"{expense['date']}: {expense['amount']} (Категория: {expense['category']})")

    # Функция для подсчета суммы расходов
    def calculate_total(self):
        total = sum(expense['amount'] for expense in self.expenses)
        messagebox.showinfo("Сумма расходов", f"Общая сумма расходов: {total:.2f} ₽")

    # Функция для фильтрации расходов
    def filter_expenses(self):
        category = self.filter_category_entry.get()
        self.listbox.delete(0, tk.END)
        for expense in self.expenses:
            if expense['category'] == category or category == "":
                self.listbox.insert(tk.END, f"{expense['date']}: {expense['amount']} (Категория: {expense['category']})")

    # Функция для загрузки расходов из файла
    def load_expenses(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return []

    # Функция для сохранения расходов в файл
    def save_expenses(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.expenses, f)

    # Функция для очистки полей ввода
    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

# Создаем главное окно и запускаем приложение
root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()