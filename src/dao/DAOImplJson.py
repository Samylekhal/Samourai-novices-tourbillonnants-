# This class is an implementation of the DAO interface for JSON files.

# - get_projects_by_teacher(teacher: Teacher) -> list[Project] .
# To do this, the program needs to cycle through the subfolders within the directory data/projects and look at the users.json files and see if the teacher is in there
#
# - save_project(teacher: Teacher, project: Project) -> None .
# To do this, the program needs to create a new subfolder in data/projects with the name of the project and save the users.json file in there.
# Since we just created the project, we make the users.json file with the teacher as the only user in it.

import os
import json
from .DAO import DAO
from ..model.Project import Project
from ..model.Teacher import Teacher
from ..model.Student import Student
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
                        project_num_votes = attributes["num_votes"]
                        project = Project(project_id, project_name, project_num_votes)
                        projects.append(project)

        return projects

    def new_project(self, teacher: Teacher, project_name: str, num_votes: int) -> Project:
        project_id = self.getFreeProjectId()
        project_path = os.path.join(self.filepath, "projects", str(project_id))
        os.makedirs(project_path, exist_ok=True)

        # Write projet_attributes.json
        attributes_path = os.path.join(project_path, "projet_attributes.json")
        with open(attributes_path, "w") as f:
            json.dump({
                "id": str(project_id),
                "name": project_name,
                "num_votes": num_votes
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

        return Project(project_id, project_name, num_votes)
    
    def update_project(self, project: Project) -> None:
        project_path = os.path.join(self.filepath, "projects", str(project.id))
        attributes_path = os.path.join(project_path, "projet_attributes.json")

        if not os.path.exists(attributes_path):
            raise FileNotFoundError(f"No attributes file found for project ID {project.id}")

        # Load existing attributes
        with open(attributes_path, "r") as f:
            attributes = json.load(f)

        # Update relevant fields
        attributes["num_votes"] = project.num_votes

        # Save back to file
        with open(attributes_path, "w") as f:
            json.dump(attributes, f, indent=4)

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



