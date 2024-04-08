# Othello

As a side project to hone my programming skills, I aim to develop a fully functional Othello game application. 
The primary objectives include enabling local co-op gameplay on the same computer and implementing an AI opponent for single-player mode.

# Technologies & Features
  - Frontend: React will serve as the frontend framework, providing a dynamic and interactive user interface.
  - Backend: Java will power the backend logic, handling game mechanics and player interactions.
  - Database: PostgreSQL will be utilized for efficient data management, storing game states and player information.
  - Containerization: Docker will facilitate seamless integration between the frontend and backend components, streamlining deployment and scalability.
  - AI Opponent: Incorporating Alpha-Beta pruning, the AI opponent will be capable of making strategic decisions to challenge players in single-player mode.


# Update 08.04.2024
After considering how to implement the AI opponent, I came to the conclusion that self-play reinforcement learning might be better than Alfa-Beta pruning. 
This poses a challenge; there are few public libraries available for Java regarding RL. As such I need to write the AI model in Python. 
In order to streamline the process, it would be more efficent to re-write the current game logic in the backend in Python instead of Java. 
As such, I have decided to move over to Python.
