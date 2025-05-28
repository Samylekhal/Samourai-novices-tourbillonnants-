# This class will handle the teacher dashboard functionalities.
# - Create new project
# - View all projects
# - View and modify project details including:
# - - Students enrolled
# - - Number of students a student can vote to be in a group with

from dao.DAO import DAO
from model.Project import Project
from model.Teacher import Teacher
from .TeacherDashboardProject import TeacherDashboardProject

class TeacherDashboardHome:
    def __init__(self, teacher: Teacher, dao: DAO):
        self.teacher = teacher
        self.dao = dao
        self.projects: list[Project] = dao.get_projects_by_teacher(self.teacher)
    
    def new_project(self, name: str, num_votes: int) -> None:
        """
        Create a new project with the given name.
        """
        project = self.dao.new_project(self.teacher, name, num_votes)
        self.projects.append(project)
    
    def get_project_dashboard_by_id(self, id: int) -> TeacherDashboardProject:
        """
        Return a TeacherDashboardProject object for a given project ID.
        """
        for project in self.projects:
            if project.id == id:
                return TeacherDashboardProject(self.teacher, self.dao, project)
        raise ValueError(f"Project with ID {id} not found.")
    
    def __str__(self):
        result = f"Home Dashboard for {self.teacher.username}.\nProjects: {[str(project) for project in self.projects]}\n"
        return result