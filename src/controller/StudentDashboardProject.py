from ..model.Student import Student
from ..dao.DAO import DAO
from ..model.Project import Project

class StudentDashboardProject:
    def __init__(self, student: Student, dao: DAO, project: Project):
        self.student = student
        self.dao = dao
        self.project = project

    def __str__(self):
        return f"StudentDashboardProject(student={self.student}, project_id={self.project.id})"