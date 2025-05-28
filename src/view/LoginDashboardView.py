import tkinter as tk
from tkinter import ttk, messagebox


class LoginDashboardView(tk.Tk):
    def __init__(self, login_callback):
        super().__init__()
        self.login_callback = login_callback
        self.title("Login")
        self.geometry("400x300")
        self.configure(bg="#2c3e50")
        self._build_interface()

    def _on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_callback(username, password)

    def _build_interface(self):
        frame = tk.Frame(self, bg="#34495e", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=200)

        tk.Label(frame, text="Username", bg="#666769", fg="white").pack(pady=(20, 5))
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack()

        tk.Label(frame, text="Password", bg="#34495e", fg="white").pack(pady=(10, 5))
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack()

        login_btn = ttk.Button(frame, text="Login", command=self._on_login)
        login_btn.pack(pady=15)