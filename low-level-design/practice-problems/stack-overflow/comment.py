from abc import ABC, abstractmethod
import uuid


class Comment: 
    def __init__(self, author_id: uuid.UUID, post_id: uuid.UUID, content: str):
        self.id = uuid.uuid4()
        self.post_id = post_id
        self.author_id = author_id
        self.content = content

    def update_content(self, content: str): 
        self.content = content