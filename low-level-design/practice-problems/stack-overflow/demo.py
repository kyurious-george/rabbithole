from stack_overflow_system import StackOverflowSystem
from search_strategy import KeywordSearchStrategy, TagSearchStrategy
from vote import VoteType

def main():
    # Init System
    system = StackOverflowSystem()

    # Add two users
    user1 = system.add_user("user1", "user1")
    user2 = system.add_user("user2", "user2")
    assert len(system.users) == 2

    # User1 posts a question and User2 posts an answer to that question
    question1 = system.add_question(user1.id, "question1", "question1", set((("tag1"),)))
    answer1 = system.add_answer(user2.id, question1.id, "answer1@question1")
    assert len(system.questions) == 1
    assert len(system.answers) == 1
    assert answer1.id in question1.answers

    # Upvote question1 and downvote answer1
    system.vote(user1.id, question1.id, VoteType.UPVOTE)
    system.vote(user2.id, answer1.id, VoteType.DOWNVOTE)
    assert question1.vote_score == 1
    assert answer1.vote_score == -1
    assert user1.reputation_score == 1
    assert user2.reputation_score == -1

    # Test Search 
    questions1 = system.search_questions([KeywordSearchStrategy(["question1"])])
    assert question1 in questions1
    
    questions2 = system.search_questions([TagSearchStrategy(["tag1"])])
    assert question1 in questions2
    questions3 = system.search_questions([KeywordSearchStrategy(["meow"])])
    assert question1 not in questions3

if __name__ == "__main__": 
    main()