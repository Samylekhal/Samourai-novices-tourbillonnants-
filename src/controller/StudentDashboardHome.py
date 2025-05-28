from ..model.Student import Student
from ..model.Project import Project
from ..dao.DAO import DAO
from .StudentDashboardProject import StudentDashboardProject

class StudentDashboardHome:
    def __init__(self, student: Student, dao: DAO):
        self.student = student
        self.dao = dao
        self.projects: list[Project] = dao.get_projects_by_student(student)

    # Method to get the student's projects where the student is a member 
    def get_project_dashboard_by_id(self, project_id: int) -> StudentDashboardProject:
        for project in self.projects:
            if project.id == project_id:
                return StudentDashboardProject(self.student, project, self.dao)
        raise ValueError(f"Project with ID {project_id} not found for this student.")

    def __str__(self):
        return f"StudentDashboardHome(student={self.student}, projects={[str(project) for project in self.projects]})"