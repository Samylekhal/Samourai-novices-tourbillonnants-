from .Student import Student

class Group:
    def __init__(self):
        self.students: list[Student] = []
    
    def add_student(self, student: Student):
        if isinstance(student, Student):
            self.students.append(student)
        else:
            raise TypeError("Expected a Student instance")
        