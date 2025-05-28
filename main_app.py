import tkinter as tk
from src import *
import json
import os


class MainApp:
    def __init__(self):
        self.dao = DAOImplJson("data")
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.show_login()

    def show_login(self):
        self.login_view = LoginDashboardView(self.handle_login)

    def handle_login(self, username, password):
        username = self.login_view.username_entry.get()
        password = self.login_view.password_entry.get()

        user = self.authenticate_user(username, password)
        if not user:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")
            return

        self.login_view.destroy()

        if isinstance(user, Teacher):
            dashboard = TeacherDashboardHome(user, self.dao)
            TeacherDashboardHomeView(self.root, dashboard)
        elif isinstance(user, Student):
            dashboard = StudentDashboardHome(user, self.dao)
            StudentDashboardHomeView(self.root, dashboard)

    def authenticate_user(self, username, password):
        auth_path = os.path.join("data", "users", "users_auth.json")
        try:
            with open(auth_path, "r") as f:
                users = json.load(f)["users"]
        except Exception:
            return None

        for u in users:
            if u["username"] == username and u["password"] == password:
                if u["roles"] == "teacher":
                    return Teacher(u["username"], u["first_name"], u["last_name"])
                elif u["roles"] == "student":
                    return Student(u["username"], u["first_name"], u["last_name"])
        return None


if __name__ == "__main__":
    app = MainApp()
    tk.mainloop()
