from .Student import Student

class StudentForm:
    def __init__(self, student: Student, votes: list[Student]):
        self.student = student
        self.votes = votes
    
    def __str__(self):
        votes_str = ', '.join(str(vote) for vote in self.votes)
        return f"StudentForm(student={self.student}, votes=[{votes_str}])"