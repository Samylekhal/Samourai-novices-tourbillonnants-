from ..model.Student import Student
from ..model.StudentForm import StudentForm
from ..dao.DAO import DAO
from ..model.Project import Project

class StudentDashboardProject:
    def __init__(self, student: Student, project: Project, dao: DAO):
        self.student = student
        self.project = project
        self.dao = dao

        # Make sure we populate self.project.students correctly
        students_result = self.dao.get_students_by_project(project.id)
        if students_result.success:
            self.project.students = students_result.data
        else:
            self.project.students = []

        # Load the student's own form
        result = self.dao.get_student_forms_by_project(project.id)
        if result.success:
            forms = result.data
            self.student_form = next(
                (form for form in forms if form.student.username == student.username),
                StudentForm(student, [])
            )
        else:
            self.student_form = StudentForm(student, [])

        points_result = self.dao.get_remaining_points_for_student(project.id, student)
        self.points = points_result.data if points_result.success else 0



    def attribute_points_to_student(self, recipient: Student, points: int) -> str:
        if self.project.closed_vote:
            return "Voting is closed for this project."

        if points <= 0:
            return "Points must be greater than zero."

        if recipient.username == self.student.username:
            return "You cannot give points to yourself."

        # Check how many points are already allocated to this student
        existing_points = next((p for s, p in self.student_form.votes if s.username == recipient.username), 0)
        net_needed = points - existing_points

        if net_needed > self.points:
            return f"Not enough points left. You have {self.points} point(s) available to allocate."

        # Update or insert vote
        updated = False
        for i, (student, _) in enumerate(self.student_form.votes):
            if student.username == recipient.username:
                self.student_form.votes[i] = (recipient, points)
                updated = True
                break

        if not updated:
            self.student_form.votes.append((recipient, points))

        # Save to DAO
        save_result = self.dao.update_student_form(self.project.id, self.student_form)
        if not save_result.success:
            return save_result.message

        # Update self.points
        self.points -= net_needed

        return "Points successfully attributed."




    def __str__(self):
        return f"StudentDashboardProject(student={self.student}, project_id={self.project.id})"