
from .Format import Format
from .model.Student import Student
from .StudentForm import StudentForm
from .model.Group import Group
import json

class Generator:
    def __init__(self, source: str, format: Format):
        self.source = source
        self.format = format
        self.student_forms: list[StudentForm] = []
    
    def generate_by_nb_group(self, nb_group: int) -> list[Group]:
        return

    # On fait ça après la generation de groupes par nb_group
    def generate_by_nb_students(self, nb_students: int) -> list[Group]:
        return
    
    def load_student_forms(self) -> None:
        # Load data to get all students including the student form for each student
        if self.format == Format.JSON:
            with open(self.source, 'r') as file:
                data = json.load(file)

            student_forms_data = data["formulaire"]["data"]
            # First, create a mapping from ID to partial Student objects (no votes yet)
            id_to_student = {}
            for entry in student_forms_data:
                # Temporary form placeholder to be replaced later
                id_to_student[entry["id"]] = Student(
                    id=entry["id"],
                    firstname=entry["firstname"],
                    surname=entry["lastname"],
                    student_class=entry["student_class"],
                )

            # Now, fill in each student's votes and finalize their forms
            for entry in student_forms_data:
                student_id = entry["id"]
                vote_ids = entry["Votes"].values()
                #voted_students = [id_to_student[vote_id] for vote_id in vote_ids if vote_id in id_to_student]
                voted_students = []
                for vote_id in vote_ids:
                    if vote_id in id_to_student:
                        voted_students.append(id_to_student[vote_id])
                # Create the StudentForm with the student and their votes
                student_form = StudentForm(
                    student=id_to_student[student_id],
                    votes=voted_students
                )
                self.student_forms.append(student_form)

    #Get the affinity between two students
    def get_affinity():
        return
    
    #Get the repartition score globaly (avg affinity score of all groups)
    def get_repartition_score():
        return
    
