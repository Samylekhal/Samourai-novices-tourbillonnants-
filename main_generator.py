from src import *

generator = Generator("data/formulaires.json", Format.JSON)
generator.load_student_forms()
for form in generator.student_forms:
    print(form)
