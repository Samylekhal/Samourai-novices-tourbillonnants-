class Teacher:
    def __init__(self, username: str, firstname: str, surname: str):
        self.username = username
        self.name = firstname
        self.surname = surname

    def __str__(self):
        return f"{self.name} {self.surname}"