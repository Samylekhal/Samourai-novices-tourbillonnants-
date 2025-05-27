class Student :

    def __init__(self, form, name, surname, student_class):
        self.form = form
        self.name = name
        self.surname = surname
        self.student_class = student_class

    def __str__(self):
        return f"{self.form} {self.name} {self.surname} {self.student_class}"