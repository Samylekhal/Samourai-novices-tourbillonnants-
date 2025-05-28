class Student :
    def __init__(self, username: str, firstname: str, surname: str):
        self.username = username
        self.name = firstname
        self.surname = surname

    def __str__(self):
        return f"({self.username}) {self.name} {self.surname}"