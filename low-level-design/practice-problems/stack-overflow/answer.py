import uuid

from vote import Vote, VoteType
from comment import Comment


class Answer:
    def __init__(self, author_id: uuid.UUID, question_id: uuid.UUID, content: str): 
        self.id: uuid.UUID = uuid.uuid4()
        self.author_id: uuid.UUID = author_id
        self.question_id: uuid.UUID = question_id
        self.content: str = content
        self.comments: set[uuid.UUID] = set()
        self.votes: dict[uuid.UUID, Vote] = {}

    @property
    def vote_score(self): 
        result = 0
        for vote in self.votes.values():
            if vote.type == VoteType.UPVOTE:
                result += 1
            elif vote.type == VoteType.DOWNVOTE: 
                result -= 1
        return result

    def update_content(self, content: str): 
        self.content = content

    def add_comment(self, comment: Comment):
        self.comments.add(comment.id)

    def vote(self, user_id: uuid.UUID, type: VoteType):
        if user_id in self.votes: 
            self.votes[user_id].type = type
        else: 
            self.votes[user_id] = Vote(user_id, type)
