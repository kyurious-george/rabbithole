from enum import Enum
from abc import ABC, abstractmethod
import uuid

from user import User

class VoteType(Enum): 
    UPVOTE = 1
    DOWNVOTE = -1


class Vote: 
    def __init__(self, author_id: uuid.UUID, type: VoteType):
        self.id: uuid.UUID = uuid.uuid4()
        self.author_id: uuid.UUID = author_id
        self.type: VoteType = type 
    