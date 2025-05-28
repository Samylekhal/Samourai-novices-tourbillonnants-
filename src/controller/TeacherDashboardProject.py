# TeacherDashboardProject.py
from ..dao.DAO import DAO
from ..model.Teacher import Teacher
from ..model.Project import Project
from ..model.Student import Student
from ..utils.Result import Result

from datetime import datetime

class TeacherDashboardProject:
    def __init__(self, teacher: Teacher, dao: DAO, project: Project):
        self.teacher = teacher
        self.dao = dao
        self.project = project

    def set_project_num_votes(self, num_votes: int):
        """
        Set the number of votes for the project.
        """
        self.project.num_votes = num_votes
        self.dao.update_project(self.project)

    def add_student(self, student_username: str) -> Result[Student]:
        result = self.dao.get_student_by_username(student_username)
        if not result.success:
            return Result(False, result.message)

        student = result.data
        if any(s.username == student.username for s in self.project.students):
            return Result(False, f"Student '{student_username}' is already in the project.")
        
        self.project.students.append(student)
        self.dao.update_project(self.project)
        return Result(True, f"Student '{student_username}' added successfully.", data=student)

    def remove_student(self, student_username: str) -> Result[Student]:
        for student in self.project.students:
            if student.username == student_username:
                self.project.students.remove(student)
                return Result(True, f"Student '{student_username}' removed successfully.", data=student)
        
        self.dao.update_project(self.project)
        return Result(False, f"Student '{student_username}' is not in the project.")

    def close_votes_manually(self) -> Result[None]:
        if self.project.closed_vote:
            return Result(False, "Votes are already closed for this project.")
        
        self.project.closed_vote = True
        self.project.vote_close_time = None
        self.dao.update_project(self.project)
        return Result(True, f"Votes for project '{self.project.name}' have been manually closed.")

    def set_vote_close_time(self, close_time: datetime) -> Result[None]:
        if self.project.closed_vote:
            return Result(False, "Cannot set vote close time because votes are already closed.")

        self.project.vote_close_time = close_time
        return Result(True, f"Vote close time set to {close_time.isoformat()} for project '{self.project.name}'.")


    def __str__(self):
        return f"Project Dashboard for {self.teacher.username}.\nProject: {self.project}\n"
