# This class will handle the data access operations for the application.
# It is abstract class and should be implemented by concrete classes

# It will contain the following methods:
# - get_projects_by_teacher(teacher: Teacher) -> list[Project] .
#
# - save_project(teacher: Teacher, project: Project) -> None .

from abc import ABC, abstractmethod
from ..model.Teacher import Teacher
from ..model.Project import Project
from ..model.Student import Student
from ..utils.Result import Result

class DAO(ABC):
    @abstractmethod
    def get_projects_by_teacher(self, teacher: Teacher) -> list[Project]:
        """
        Retrieve a list of projects associated with a teacher.
        """
        pass

    @abstractmethod
    def new_project(self, teacher: Teacher, project_name: str, num_votes: int) -> Project:
        """
        Create a new project with a unique ID and return the created Project.
        """
        pass

    @abstractmethod
    def update_project(self, project: Project) -> None:
        """
        Update an existing project's attributes (like num_votes).
        """
        pass

    @abstractmethod
    def get_student_by_username(self, username: str) -> Result[Student]:
        """
        Retrieve a student by their username.
        If the student does not exist, return a Result with success=False and an appropriate message.
        If there is an error in retrieving the student, return a Result with success=False and an error message.
        """
        pass
