import uuid

from user import User
from question import Question
from answer import Answer
from comment import Comment 
from vote import VoteType
from search_strategy import ISearchStrategy

class StackOverflowSystem: 
    def __init__(self): 
        self.users: dict[uuid.UUID, User] = {}
        self.questions: dict[uuid.UUID, Question] = {}
        self.answers: dict[uuid.UUID, Answer] = {}
        self.comments: dict[uuid.UUID, Comment] = {}

    def add_user(self, username: str, email: str) -> User:
        for user in self.users.values(): 
            if user.username == username or user.email == email: 
                raise ValueError(f"Username {username} or Email {email} are already taken.")
        user = User(username, email)
        self.users[user.id] = user
        return user
 
    def add_question(self, user_id: uuid.UUID, title: str, content: str, tags: set[str]) -> Question: 
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        question = Question(user_id, title, content, tags)
        self.questions[question.id] = question
        return question
    
    def update_question(self, user_id: uuid.UUID, question_id: uuid.UUID, **fields):
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if question_id not in self.questions: 
            raise KeyError(f"Question {question_id} does not exist in the system.")
        question = self.questions[question_id]
        if user_id != question.author_id: 
            raise RuntimeError(f"User {user_id} does not have permissions to update Question {question_id}.")
        if fields["title"]: question.update_title(fields["title"])
        if fields["content"]: question.update_content(fields["content"])
        if fields["tags"]: question.update_tags(fields["tags"])

    def add_answer(self, user_id: uuid.UUID, question_id: uuid.UUID, content: str) -> Answer: 
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if question_id not in self.questions: 
            raise KeyError(f"Question {question_id} does not exist in the system.")
        answer = Answer(user_id, question_id, content)
        self.answers[answer.id] = answer
        question = self.questions[question_id]
        question.add_answer(answer)
        return answer
    
    def update_answer(self, user_id: uuid.UUID, answer_id: uuid.UUID, **fields):
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if answer_id not in self.answers: 
            raise KeyError(f"Answer {answer_id} does not exist in the system.")
        answer = self.answers[answer_id]
        if user_id != answer.author_id: 
            raise RuntimeError(f"User {user_id} does not have permissions to update Answer {answer_id}.")
        if fields["content"]: answer.update_content(fields["content"])
    
    def add_comment(self, user_id: uuid.UUID, post_id: uuid.UUID, content: str) -> Comment: 
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if post_id not in self.questions and post_id not in self.answers: 
            raise KeyError(f"Post {post_id} does not exist in the system.")
        comment = Comment(user_id, post_id, content)
        self.comments[comment.id] = comment
        if post_id in self.questions: 
            post = self.questions[post_id]
        elif post_id in self.answers: 
            post = self.answers[post_id]
        post.add_comment(comment)
        return comment
    
    def update_comment(self, user_id: uuid.UUID, comment_id: uuid.UUID, **fields): 
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if comment_id not in self.comments: 
            raise KeyError(f"Comment {comment_id} does not exist in the system.")
        comment = self.comments[comment_id]
        if user_id != comment.author_id:
            raise RuntimeError(f"User {user_id} does not have permissions to update Comment {comment_id}.")
        if fields["content"]: comment.update_content(fields["content"])
    
    def vote(self, user_id: uuid.UUID, post_id: uuid.UUID, type: VoteType):
        if user_id not in self.users: 
            raise KeyError(f"User {user_id} does not exist in the system.")
        if post_id not in self.questions and post_id not in self.answers: 
            raise KeyError(f"Post {post_id} does not exist in the system.")
        if post_id in self.questions: 
            post = self.questions[post_id]
        elif post_id in self.answers: 
            post = self.answers[post_id]
        post.vote(user_id, type)
        self.update_user_rep_score(user_id)
        
    def update_user_rep_score(self, user_id: uuid.UUID): 
        result = 0
        for question in self.questions.values(): 
            if user_id == question.author_id:
                result += question.vote_score
        for answer in self.answers.values():
            if user_id == answer.author_id: 
                result += answer.vote_score
        self.users[user_id].update_rep_score(result)

    def search_questions(self, strategies: list[ISearchStrategy]) -> list[Question]: 
        result = []
        for strategy in strategies: 
            questions = self.questions.values()
            result.extend(strategy.filter(questions))
        return result