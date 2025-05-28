from .Student import Student

class StudentForm:
    def __init__(self, student: Student, votes: list[tuple[Student, int]]):
        self.student = student
        self.votes = votes  # Each vote is a tuple: (Student, points_allocated)

    def __str__(self):
        votes_str = ', '.join(f"({vote[0]}, {vote[1]} pts)" for vote in self.votes)
        return f"StudentForm(student={self.student}, votes=[{votes_str}])"
