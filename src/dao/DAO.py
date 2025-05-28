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
from ..model.StudentForm import StudentForm
from ..utils.Result import Result

class DAO(ABC):
    @abstractmethod
    def get_projects_by_teacher(self, teacher: Teacher) -> list[Project]:
        """
        Retrieve a list of projects associated with a teacher.
        """
        pass

    @abstractmethod
    def new_project(self, teacher: Teacher, project_name: str, num_points: int) -> Project:
        """
        Create a new project with a unique ID and return the created Project.
        """
        pass

    @abstractmethod
    def update_project(self, project: Project) -> None:
        """
        Update an existing project's attributes (like num_points).
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

    @abstractmethod
    def get_students_by_project(self, project_id: int) -> Result[list[Student]]:
        """
        Retrieve a list of students associated with the given project ID.
        """
        pass

    @abstractmethod
    def get_student_forms_by_project(self, project_id: int) -> Result[list[StudentForm]]:
        """
        Retrieve all student forms for a given project ID.
        """
        pass

    @abstractmethod
    def student_i_voted_j(self, project_id: int, student_i: Student, student_j: Student) -> bool:
        """
        Return True if student_i voted for student_j in the given project, else False.
        """
        pass

    @abstractmethod
    def get_projects_by_student(self, student: Student) -> list[Project]:
        """
        Retrieve a list of projects associated with a student.
        """
        pass

    @abstractmethod
    def update_student_form(self, project_id: int, updated_form: StudentForm) -> Result[None]:
        """
        Update the student form in forms.json for the specified project.
        Replaces the form entry corresponding to the student with updated votes.
        """
        pass

    @abstractmethod
    def get_remaining_points_for_student(self, project_id: int, student: Student) -> Result[int]:
        """
        Returns the number of points the student has left to allocate in a given project.
        """
        pass
