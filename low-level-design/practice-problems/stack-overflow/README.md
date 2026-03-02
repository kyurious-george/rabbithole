## Requirements
- Users can post questions, answer questions, and comment on questions and answers.
- Users can vote on questions and answers.
- Questions should have tags associated with them.
- Users can search for questions based on keywords, tags, or user profiles.
- The system should assign reputation score to users based on their activity and the quality of their contributions.
- The system should handle concurrent access and ensure data consistency.

## Design



## Reflection
- Gameplan
    - Think top down for systems and implement bottom up
    - Do not introduce extra abstractions (ie. me forcing a Voteable and Commentable interface)
    - Do not try to perfect implementation (ie. should have used a parent class Post and have Question and Answer be child class)
    - Keep the state of the objects in the system and reference using id (this makes switching to something like DB easier since state is all in one place)
- LLD Concepts Learned
    - Use a Strategy design pattern + interface for swapping out different implementations of algorithms (see `search_strategy.py` for example)
    - Look out for "is a" relationship as these can be opportunities to use base classes for inheritance (keep max 3 levels tho)
    - Enums are strictly supposed to be treated as CONSTANT values and never use the underlying values (ie. I was trying to do summation for the `vote_score` simply using `VoteType`)
