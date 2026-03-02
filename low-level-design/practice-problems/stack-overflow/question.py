import uuid

from answer import Answer
from comment import Comment
from vote import Vote, VoteType

class Question: 
    def __init__(self, author_id: uuid.UUID, title: str, content: str, tags: set[str]):
        self.id: uuid.UUID = uuid.uuid4()
        self.author_id: uuid.UUID = author_id
        self.title: str = title
        self.content: str = content
        self.tags: set[str] = tags
        self.answers: set[uuid.UUID] = set()
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
    
    def update_title(self, title: str): 
        self.title = title 

    def update_content(self, content: str): 
        self.content = content 
    
    def update_tags(self, tags: set[str]): 
        self.tags = tags 

    def add_answer(self, answer: Answer):
        self.answers.add(answer.id)

    def add_comment(self, comment: Comment): 
        self.comments.add(comment.id)

    def vote(self, user_id: uuid.UUID, type: VoteType): 
        if user_id in self.votes: 
            self.votes[user_id].type = type
        else: 
            self.votes[user_id] = Vote(user_id, type)
    

    