# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import json
import os
import ctypes
from pynput import mouse, keyboard

class MinecraftAutoClicker:
    def __init__(self):
        self.is_running = False
        self.click_count = 0
        self.start_time = 0
        self.mouse_controller = mouse.Controller()
        
        # Загружаем настройки
        self.load_settings()
        
        # Создаём GUI в стиле Minecraft
        self.root = tk.Tk()
        self.root.title("Minecraft AutoClicker Pro")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#3d2c26")
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#3d2c26")
        title_frame.pack(pady=10)
        
        title = tk.Label(
            title_frame,
            text="MINECRAFT",
            font=("Courier", 24, "bold"),
            fg="#ffaa00",
            bg="#3d2c26"
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="AUTOCLICKER PRO",
            font=("Courier", 14),
            fg="#ffffff",
            bg="#3d2c26"
        )
        subtitle.pack()
        
        # Ручной ввод скорости (в секундах)
        speed_frame = tk.Frame(self.root, bg="#3d2c26")
        speed_frame.pack(pady=15)
        
        tk.Label(speed_frame, text="СКОРОСТЬ (сек):", font=("Courier", 11), fg="#ffffff", bg="#3d2c26").pack()
        self.speed_var = tk.StringVar(value=str(self.settings.get("speed", 0.1)))
        speed_entry = tk.Entry(
            speed_frame,
            textvariable=self.speed_var,
            font=("Courier", 12),
            bg="#5a4a42",
            fg="#ffffff",
            insertbackground="#ffffff",
            width=15
        )
        speed_entry.pack(pady=5)
        
        # Подсказка по диапазону
        hint = tk.Label(
            speed_frame,
            text="От 0.001 до 1000.0\n(1 мс = 0.001 сек)",
            font=("Courier", 8),
            fg="#aaaaaa",
            bg="#3d2c26"
        )
        hint.pack()
        
        # Выбор кнопки мыши
        button_frame = tk.Frame(self.root, bg="#3d2c26")
        button_frame.pack(pady=10)
        
        tk.Label(button_frame, text="КНОПКА:", font=("Courier", 10), fg="#ffffff", bg="#3d2c26").pack()
        self.button_var = tk.StringVar(value=self.settings.get("button", "left"))
        button_options = ["left", "right"]
        button_menu = tk.OptionMenu(button_frame, self.button_var, *button_options)
        button_menu.config(bg="#5a4a42", fg="#ffffff", activebackground="#7a6a62", font=("Courier", 10))
        button_menu["menu"].config(bg="#5a4a42", fg="#ffffff", font=("Courier", 10))
        button_menu.pack(pady=5)
        
        # Режим работы
        mode_frame = tk.Frame(self.root, bg="#3d2c26")
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="РЕЖИМ:", font=("Courier", 10), fg="#ffffff", bg="#3d2c26").pack()
        self.mode_var = tk.StringVar(value=self.settings.get("mode", "click"))
        mode_options = ["click", "hold"]
        mode_menu = tk.OptionMenu(mode_frame, self.mode_var, *mode_options)
        mode_menu.config(bg="#5a4a42", fg="#ffffff", activebackground="#7a6a62", font=("Courier", 10))
        mode_menu["menu"].config(bg="#5a4a42", fg="#ffffff", font=("Courier", 10))
        mode_menu.pack(pady=5)
        
        # Ограничения
        limit_frame = tk.Frame(self.root, bg="#3d2c26")
        limit_frame.pack(pady=10)
        
        tk.Label(limit_frame, text="МАКС. КЛИКОВ (0 = без лимита):", font=("Courier", 9), fg="#ffffff", bg="#3d2c26").pack()
        self.max_clicks_var = tk.StringVar(value=str(self.settings.get("max_clicks", 0)))
        max_clicks_entry = tk.Entry(
            limit_frame,
            textvariable=self.max_clicks_var,
            font=("Courier", 10),
            bg="#5a4a42",
            fg="#ffffff",
            width=10
        )
        max_clicks_entry.pack(pady=3)
        
        tk.Label(limit_frame, text="МАКС. ВРЕМЯ (мин, 0 = без лимита):", font=("Courier", 9), fg="#ffffff", bg="#3d2c26").pack()
        self.max_time_var = tk.StringVar(value=str(self.settings.get("max_time", 0)))
        max_time_entry = tk.Entry(
            limit_frame,
            textvariable=self.max_time_var,
            font=("Courier", 10),
            bg="#5a4a42",
            fg="#ffffff",
            width=10
        )
        max_time_entry.pack(pady=3)
        
        # Центральная кнопка
        self.btn_var = tk.StringVar(value="ВКЛЮЧИТЬ")
        self.main_btn = tk.Button(
            self.root,
            textvariable=self.btn_var,
            command=self.toggle_clicker,
            font=("Courier", 14, "bold"),
            bg="#4cd137",
            fg="#ffffff",
            activebackground="#2ecc71",
            activeforeground="#ffffff",
            relief="raised",
            bd=3,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.main_btn.pack(pady=15)
        
        # Статус и счётчики
        status_frame = tk.Frame(self.root, bg="#3d2c26")
        status_frame.pack(pady=10)
        
        self.status_var = tk.StringVar(value="ГОТОВ")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Courier", 10, "bold"),
            fg="#e17055",
            bg="#3d2c26"
        )
        status_label.pack()
        
        self.count_var = tk.StringVar(value="Кликов: 0")
        count_label = tk.Label(
            status_frame,
            textvariable=self.count_var,
            font=("Courier", 10),
            fg="#6ab04c",
            bg="#3d2c26"
        )
        count_label.pack()
        
        self.time_var = tk.StringVar(value="Время: 0 сек")
        time_label = tk.Label(
            status_frame,
            textvariable=self.time_var,
            font=("Courier", 10),
            fg="#6ab04c",
            bg="#3d2c26"
        )
        time_label.pack()
        
        # Инструкция
        instructions = tk.Label(
            self.root,
            text="F6 - вкл/выкл | F7 - сохранить настройки\nТолько для одиночной игры!",
            font=("Courier", 8),
            fg="#aaaaaa",
            bg="#3d2c26"
        )
        instructions.pack(side="bottom", pady=10)
        
        # Горячие клавиши
        self.setup_hotkeys()
    
    def load_settings(self):
        """Загружает настройки из файла"""
        self.settings_file = "autoclicker_settings.json"
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            except:
                self.settings = {"speed": 0.1, "button": "left", "mode": "click", "max_clicks": 0, "max_time": 0}
        else:
            self.settings = {"speed": 0.1, "button": "left", "mode": "click", "max_clicks": 0, "max_time": 0}
    
    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            self.settings.update({
                "speed": float(self.speed_var.get()),
                "button": self.button_var.get(),
                "mode": self.mode_var.get(),
                "max_clicks": int(self.max_clicks_var.get() or 0),
                "max_time": int(self.max_time_var.get() or 0)
            })
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            self.status_var.set("НАСТРОЙКИ СОХРАНЕНЫ")
            self.root.after(2000, lambda: self.status_var.set("ГОТОВ" if not self.is_running else "АКТИВЕН"))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения!")
    
    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        def on_press(key):
            try:
                if key == keyboard.Key.f6:
                    self.root.after(0, self.toggle_clicker)
                elif key == keyboard.Key.f7:
                    self.root.after(0, self.save_settings)
            except:
                pass
        
        keyboard.Listener(on_press=on_press, daemon=True).start()
    
    def click_loop(self):
        """Основной цикл автокликера"""
        self.click_count = 0
        self.start_time = time.time()
        
        while self.is_running:
            # Проверка ограничений
            current_time = time.time() - self.start_time
            if self.settings.get("max_time", 0) > 0 and current_time >= self.settings["max_time"] * 60:
                self.root.after(0, self.stop_clicker)
                break
            
            if self.settings.get("max_clicks", 0) > 0 and self.click_count >= self.settings["max_clicks"]:
                self.root.after(0, self.stop_clicker)
                break
            
            # Проверка активного окна Minecraft
            if self.is_minecraft_active():
                button = getattr(mouse.Button, self.button_var.get())
                
                if self.mode_var.get() == "click":
                    self.mouse_controller.click(button, 1)
                    self.click_count += 1
                else:  # hold
                    self.mouse_controller.press(button)
                    time.sleep(0.01)  # Минимальная задержка
                    self.mouse_controller.release(button)
                    self.click_count += 1
                
                # Обновление счётчиков
                self.root.after(0, self.update_counters)
            
            # Задержка между кликами
            try:
                delay = float(self.speed_var.get())
                delay = max(0.001, min(1000.0, delay))  # Ограничение диапазона
            except:
                delay = 0.1
            
            time.sleep(delay)
    
    def update_counters(self):
        """Обновляет счётчики в GUI"""
        elapsed = time.time() - self.start_time
        self.count_var.set(f"Кликов: {self.click_count}")
        self.time_var.set(f"Время: {int(elapsed)} сек")
    
    def is_minecraft_active(self):
        """Проверяет, активно ли окно Minecraft"""
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                return "Minecraft" in buff.value or "майнкрафт" in buff.value.lower()
        except:
            pass
        return True
    
    def toggle_clicker(self):
        """Переключение состояния автокликера"""
        if self.is_running:
            self.stop_clicker()
        else:
            self.start_clicker()
    
    def start_clicker(self):
        """Запуск автокликера"""
        try:
            speed = float(self.speed_var.get())
            if speed < 0.001 or speed > 1000.0:
                raise ValueError("Скорость должна быть от 0.001 до 1000.0")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректная скорость!\n{str(e)}")
            return
        
        if not self.is_running:
            self.is_running = True
            self.btn_var.set("ВЫКЛЮЧИТЬ")
            self.main_btn.config(bg="#e84118", activebackground="#ff6b6b")
            self.status_var.set("АКТИВЕН")
            threading.Thread(target=self.click_loop, daemon=True).start()
    
    def stop_clicker(self):
        """Остановка автокликера"""
        self.is_running = False
        self.btn_var.set("ВКЛЮЧИТЬ")
        self.main_btn.config(bg="#4cd137", activebackground="#2ecc71")
        self.status_var.set("ОСТАНОВЛЕН")
        # Сохраняем настройки при остановке
        self.save_settings()
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        import pynput
    except ImportError:
        messagebox.showerror("Ошибка", "Установите зависимости:\npy -m pip install pynput")
        exit(1)
    
    app = MinecraftAutoClicker()
    app.run()
