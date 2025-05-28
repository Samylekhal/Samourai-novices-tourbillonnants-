# This class is an implementation of the DAO interface for JSON files.

# - get_projects_by_teacher(teacher: Teacher) -> list[Project] .
# To do this, the program needs to cycle through the subfolders within the directory data/projects and look at the users.json files and see if the teacher is in there
#
# - save_project(teacher: Teacher, project: Project) -> None .
# To do this, the program needs to create a new subfolder in data/projects with the name of the project and save the users.json file in there.
# Since we just created the project, we make the users.json file with the teacher as the only user in it.

import os
import json
from datetime import datetime
from .DAO import DAO
from ..model.Project import Project
from ..model.Teacher import Teacher
from ..model.Student import Student
from ..model.StudentForm import StudentForm
from ..utils.Result import Result

class DAOImplJson(DAO):
    def __init__(self, filepath: str = "data"):
        self.filepath = filepath

    def get_projects_by_teacher(self, teacher: Teacher) -> list[Project]:
        projects = []
        base_path = os.path.join(self.filepath, "projects")

        for folder_name in os.listdir(base_path):
            project_folder = os.path.join(base_path, folder_name)

            if os.path.isdir(project_folder): # It probably will always be a directory
                users_file = os.path.join(project_folder, "users.json")
                attributes_file = os.path.join(project_folder, "projet_attributes.json")

                if not os.path.exists(users_file) or not os.path.exists(attributes_file): # Proabably won't happen
                    print(f"Skipping {users_file} as it does not contain the required files.") 
                    continue

                with open(users_file, "r") as f:
                    users_data = json.load(f)
                    teacher_usernames = [t["username"] for t in users_data.get("users", {}).get("teachers", [])]

                if teacher.username in teacher_usernames:
                    with open(attributes_file, "r") as f:
                        attributes = json.load(f)
                        project_id = int(attributes["id"])
                        project_name = attributes["name"]
                        project_num_points = attributes["num_points"]
                        vote_close_time_str = attributes.get("vote_close_time")
                        project_vote_close_time = datetime.fromisoformat(vote_close_time_str) if vote_close_time_str else None
                        project = Project(project_id, project_name, project_num_points, vote_close_time=project_vote_close_time)
                        projects.append(project)

        return projects

    def new_project(self, teacher: Teacher, project_name: str, num_points: int) -> Project:
        project_id = self.getFreeProjectId()
        project_path = os.path.join(self.filepath, "projects", str(project_id))
        os.makedirs(project_path, exist_ok=True)

        # Write projet_attributes.json
        attributes_path = os.path.join(project_path, "projet_attributes.json")
        with open(attributes_path, "w") as f:
            json.dump({
                "id": str(project_id),
                "name": project_name,
                "num_points": num_points
            }, f, indent=4)

        # Write users.json with only the teacher
        users_path = os.path.join(project_path, "users.json")
        with open(users_path, "w") as f:
            json.dump({
                "users": {
                    "teachers": [{"username": teacher.username}],
                    "students": []
                }
            }, f, indent=4)

        # Write empty forms.json skeleton (students will be added later)
        forms_path = os.path.join(project_path, "forms.json")
        with open(forms_path, "w") as f:
            json.dump({
                "forms": []
            }, f, indent=4)

        return Project(project_id, project_name, num_points)

    
    def update_project(self, project: Project) -> None:
        project_path = os.path.join(self.filepath, "projects", str(project.id))
        attributes_path = os.path.join(project_path, "projet_attributes.json")
        users_path = os.path.join(project_path, "users.json")
        forms_path = os.path.join(project_path, "forms.json")

        if not os.path.exists(attributes_path):
            raise FileNotFoundError(f"No attributes file found for project ID {project.id}")

        # --- Update project attributes ---
        with open(attributes_path, "r") as f:
            attributes = json.load(f)

        attributes["num_points"] = project.num_points
        attributes["vote_close_time"] = (
            project.vote_close_time.isoformat() if project.vote_close_time else None
        )
        attributes["closed_vote"] = project.closed_vote

        with open(attributes_path, "w") as f:
            json.dump(attributes, f, indent=4)


        # --- Update users.json with students and teachers ---
        teachers = [{"username": self.teacher.username}] if hasattr(self, "teacher") else []
        students = [{"username": s.username} for s in project.students]

        if os.path.exists(users_path):
            with open(users_path, "r") as f:
                current_users = json.load(f).get("users", {})
                teachers = current_users.get("teachers", teachers)

        new_users = {
            "users": {
                "teachers": teachers,
                "students": students
            }
        }

        with open(users_path, "w") as f:
            json.dump(new_users, f, indent=4)

        # --- Update forms.json to match student list ---
        forms_data = []
        if os.path.exists(forms_path):
            with open(forms_path, "r") as f:
                try:
                    forms_data = json.load(f).get("forms", [])
                except json.JSONDecodeError:
                    forms_data = []

        # Create map for easier lookup
        username_to_form = {form["student_username"]: form for form in forms_data if "student_username" in form}
        # Remove votes that target students no longer in the project
        valid_usernames = set(s.username for s in project.students)
        for form in username_to_form.values():
            votes = form.get("votes", {})
            cleaned_votes = {u: pts for u, pts in votes.items() if u in valid_usernames}
            form["votes"] = cleaned_votes


        current_usernames = set(s.username for s in project.students)
        updated_forms = []

        for username in current_usernames:
            if username in username_to_form:
                updated_forms.append(username_to_form[username])  # preserve existing votes
            else:
                updated_forms.append({
                    "student_username": username,
                    "votes": {}
                })

        with open(forms_path, "w") as f:
            json.dump({"forms": updated_forms}, f, indent=4)


    def getFreeProjectId(self) -> int:
        base_path = os.path.join(self.filepath, "projects")
        used_ids = set()

        if not os.path.exists(base_path):
            os.makedirs(base_path)
            return 1

        for folder_name in os.listdir(base_path):
            project_folder = os.path.join(base_path, folder_name)
            if os.path.isdir(project_folder):
                attributes_file = os.path.join(project_folder, "projet_attributes.json")
                if os.path.exists(attributes_file):
                    with open(attributes_file, "r") as f:
                        try:
                            attributes = json.load(f)
                            pid = int(attributes.get("id", -1))
                            if pid != -1:
                                used_ids.add(pid)
                        except (ValueError, json.JSONDecodeError):
                            continue

        # Find the first unused integer starting from 1
        i = 1
        while i in used_ids:
            i += 1
        return i
    
    def get_student_by_username(self, username: str) -> Result[Student]:
        auth_file = os.path.join(self.filepath, "users", "users_auth.json")
        try:
            with open(auth_file, "r") as f:
                users = json.load(f).get("users", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return Result(False, "Error loading user data.")

        for user in users:
            if user["username"] == username and user["roles"] == "student":
                student = Student(user["username"], user["first_name"], user["last_name"])
                return Result(True, "Student loaded successfully.", data=student)

        return Result(False, f"Student '{username}' not found.")

    def get_students_by_project(self, project_id: int) -> Result[list[Student]]:
        users_path = os.path.join(self.filepath, "projects", str(project_id), "users.json")
        auth_path = os.path.join(self.filepath, "users", "users_auth.json")

        if not os.path.exists(users_path):
            return Result(False, f"Project {project_id} not found (missing users.json)")

        try:
            with open(users_path, "r") as f:
                users_data = json.load(f)
                student_usernames = [s["username"] for s in users_data.get("users", {}).get("students", [])]
        except Exception as e:
            return Result(False, f"Failed to load users.json for project {project_id}: {str(e)}")

        try:
            with open(auth_path, "r") as f:
                auth_data = json.load(f).get("users", [])
        except Exception as e:
            return Result(False, f"Failed to load users_auth.json: {str(e)}")

        students = []
        for user in auth_data:
            if user["username"] in student_usernames and user["roles"] == "student":
                student = Student(user["username"], user["first_name"], user["last_name"])
                students.append(student)

        return Result(True, f"{len(students)} students found for project {project_id}", data=students)

    def get_student_forms_by_project(self, project_id: int) -> Result[list[StudentForm]]:
        forms_path = os.path.join(self.filepath, "projects", str(project_id), "forms.json")
        auth_path = os.path.join(self.filepath, "users", "users_auth.json")

        if not os.path.exists(forms_path):
            return Result(False, f"Forms file not found for project {project_id}.")

        try:
            with open(forms_path, "r") as f:
                forms_data = json.load(f).get("forms", [])
        except Exception as e:
            return Result(False, f"Error reading forms.json: {str(e)}")

        try:
            with open(auth_path, "r") as f:
                users_data = json.load(f).get("users", [])
        except Exception as e:
            return Result(False, f"Error reading users_auth.json: {str(e)}")

        # Build a username → Student object map
        username_to_student = {
            user["username"]: Student(user["username"], user["first_name"], user["last_name"])
            for user in users_data
            if user["roles"] == "student"
        }

        student_forms = []
        for entry in forms_data:
            student_username = entry.get("student_username")
            vote_dict = entry.get("votes", {})

            if student_username not in username_to_student:
                continue

            student = username_to_student[student_username]
            votes: list[tuple[Student, int]] = []

            for voted_username, points in vote_dict.items():
                voted_student = username_to_student.get(voted_username)
                if voted_student and isinstance(points, int):
                    votes.append((voted_student, points))

            form = StudentForm(student, votes)
            student_forms.append(form)

        return Result(True, f"Loaded {len(student_forms)} student forms for project {project_id}.", data=student_forms)


    def student_i_voted_j(self, project_id: int, student_i: Student, student_j: Student) -> bool:
        forms_path = os.path.join(self.filepath, "projects", str(project_id), "forms.json")

        if not os.path.exists(forms_path):
            return False

        try:
            with open(forms_path, "r") as f:
                forms_data = json.load(f).get("forms", [])
        except Exception:
            return False

        for form in forms_data:
            if form.get("student_username") == student_i.username:
                vote_usernames = list(form.get("votes", {}).values())
                return student_j.username in vote_usernames

        return False

    def get_projects_by_student(self, student: Student) -> list[Project]:
        projects = []
        base_path = os.path.join(self.filepath, "projects")

        for folder_name in os.listdir(base_path):
            project_folder = os.path.join(base_path, folder_name)

            if os.path.isdir(project_folder):
                users_file = os.path.join(project_folder, "users.json")
                attributes_file = os.path.join(project_folder, "projet_attributes.json")

                if not os.path.exists(users_file) or not os.path.exists(attributes_file):
                    continue

                with open(users_file, "r") as f:
                    users_data = json.load(f)
                    student_usernames = [s["username"] for s in users_data.get("users", {}).get("students", [])]

                if student.username in student_usernames:
                    with open(attributes_file, "r") as f:
                        attributes = json.load(f)
                        project_id = int(attributes["id"])
                        project_name = attributes["name"]
                        project_num_points = attributes["num_points"]
                        vote_close_time_str = attributes.get("vote_close_time")
                        project_vote_close_time = datetime.fromisoformat(vote_close_time_str) if vote_close_time_str else None
                        project = Project(project_id, project_name, project_num_points, vote_close_time=project_vote_close_time)
                        projects.append(project)

        return projects

    def update_student_form(self, project_id: int, updated_form: StudentForm) -> Result[None]:
        forms_path = os.path.join(self.filepath, "projects", str(project_id), "forms.json")
        if not os.path.exists(forms_path):
            return Result(False, "forms.json does not exist for this project.")

        try:
            with open(forms_path, "r") as f:
                data = json.load(f)
                forms = data.get("forms", [])
        except Exception as e:
            return Result(False, f"Failed to read forms.json: {str(e)}")

        found = False
        updated_forms = []
        for form in forms:
            if form.get("student_username") == updated_form.student.username:
                found = True
                updated_vote_map = {s.username: pts for s, pts in updated_form.votes}
                updated_forms.append({
                    "student_username": updated_form.student.username,
                    "votes": updated_vote_map
                })
            else:
                updated_forms.append(form)

        if not found:
            return Result(False, "Student form not found in project.")

        try:
            with open(forms_path, "w") as f:
                json.dump({"forms": updated_forms}, f, indent=4)
            return Result(True, "Student form updated.")
        except Exception as e:
            return Result(False, f"Failed to write forms.json: {str(e)}")

    def get_remaining_points_for_student(self, project_id: int, student: Student) -> Result[int]:
        forms_path = os.path.join(self.filepath, "projects", str(project_id), "forms.json")
        attributes_path = os.path.join(self.filepath, "projects", str(project_id), "projet_attributes.json")

        if not os.path.exists(forms_path) or not os.path.exists(attributes_path):
            return Result(False, "Required files missing.")

        try:
            with open(forms_path, "r") as f:
                forms_data = json.load(f).get("forms", [])
            with open(attributes_path, "r") as f:
                project_data = json.load(f)
        except Exception as e:
            return Result(False, f"Error reading project data: {str(e)}")

        max_points = int(project_data.get("num_points", 0))
        student_form = next((form for form in forms_data if form.get("student_username") == student.username), None)

        if not student_form:
            return Result(True, "Student has not used any points yet.", data=max_points)

        used_points = sum(student_form.get("votes", {}).values())
        remaining_points = max_points - used_points

        return Result(True, "Remaining points calculated.", data=max(remaining_points, 0))
