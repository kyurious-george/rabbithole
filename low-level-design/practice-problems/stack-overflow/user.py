import uuid
from typing import Iterator

class User: 
    def __init__(self, username: str, email: str): 
        self.id = uuid.uuid4()
        self.username = username
        self.email = email 
        self.reputation_score = 0
    
    def update_rep_score(self, score: int):
        self.reputation_score = score