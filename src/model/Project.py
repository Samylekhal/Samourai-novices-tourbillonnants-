from datetime import datetime
from .Student import Student

class Project:
    def __init__(self, id: int, name: str, num_votes: int, closed_vote: bool = False, vote_close_time: datetime | None = None):
        self.id = id
        self.name = name
        self.num_votes = num_votes
        self.students: list[Student] = []
        self.closed_vote = closed_vote
        self.vote_close_time = vote_close_time

    def __str__(self):
        vote_close_str = self.vote_close_time.isoformat() if self.vote_close_time else "None"
        return (f"Project ID: {self.id}, Name: {self.name}, Number of Votes: {self.num_votes}, "
                f"Closed Vote: {self.closed_vote}, Vote Close Time: {vote_close_str}, "
                f"Students: {[str(student) for student in self.students]}")
