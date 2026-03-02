from abc import ABC, abstractmethod
import uuid

from question import Question

class ISearchStrategy(ABC):
    def filter(self, questions: list[Question]) -> list[Question]:
        pass


class UserSearchStrategy(ISearchStrategy): 
    def __init__(self, user_ids: list[uuid.UUID]): 
        self.user_ids = user_ids

    def filter(self, questions: list[Question]) -> list[Question]:
        result = [] 
        for user_id in self.user_id: 
            for question in questions: 
                if question.author_id == user_id: 
                    result.append(question)
        return result
    

class KeywordSearchStrategy(ISearchStrategy): 
    def __init__(self, keywords: list[str]): 
        self.keywords = keywords

    def filter(self, questions: list[Question]) -> list[Question]:
        result = [] 
        for keyword in self.keywords: 
            for question in questions: 
                if keyword in question.title or keyword in question.content: 
                    result.append(question)
        return result


class TagSearchStrategy(ISearchStrategy): 
    def __init__(self, tags: list[str]): 
        self.tags = tags

    def filter(self, questions: list[Question]) -> list[Question]:
        result = [] 
        for tag in self.tags: 
            for question in questions: 
                if tag in question.tags: 
                    result.append(question)
        return result
            