from ..dao.DAO import DAO
from ..model.Teacher import Teacher
from ..model.Student import Student
from .TeacherDashboardHome import TeacherDashboardHome
from .StudentDashboardHome import StudentDashboardHome
from ..utils.Result import Result
import os
import json

class LoginDashboard:
    def __init__(self, dao: DAO, user_auth_path: str = "data/users/users_auth.json"):
        self.dao = dao
        self.auth_path = user_auth_path

    def login(self, username: str, password: str) -> Result[object]:
        if not os.path.exists(self.auth_path):
            return Result(False, f"Auth file not found: {self.auth_path}")

        try:
            with open(self.auth_path, "r") as f:
                users = json.load(f).get("users", [])
        except json.JSONDecodeError:
            return Result(False, "Failed to decode users_auth.json")

        for user in users:
            if user["username"] == username and user["password"] == password:
                role = user.get("roles")
                first_name = user.get("first_name")
                last_name = user.get("last_name")

                if role == "teacher":
                    teacher = Teacher(username, first_name, last_name)
                    dashboard = TeacherDashboardHome(teacher, self.dao)
                    return Result(True, "Login successful (teacher).", dashboard)

                elif role == "student":
                    student = Student(username, first_name, last_name)
                    dashboard = StudentDashboardHome(student, self.dao)
                    return Result(True, "Login successful (student).", dashboard)

                else:
                    return Result(False, f"Unknown role: {role}")

        return Result(False, "Invalid username or password.")
