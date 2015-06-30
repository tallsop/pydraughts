# PyDraughts
## What is this?
This is a draughts game written in Python that has a simple AI that can play as an opponent. It was written for my extended project during my A-Levels and looking back on it, it could really be improved. So I am using this as an opportunity to see how much it can be improved.

## How does it currently work?
At the moment, the AI that is implemented uses alpha-beta pruning with minimax to deicide on what move to take. I had also originally planned to have a move database, that would hold moves that were both advantageous and disadvantageous to the opponent, but was not finished, due to the time constraints of the project.

## What needs improving?
In it's current state it is completely playable, but there are quite a few issues in my mind that need to be improved:
* Defining, the board, tiles and checkers as objects means when copying the board in the game tree, deep copy had to be used, which is a huge hit to the performance of the agent. The plan is to use a matrix with characters with move undoing.
* Change the search cut off from a depth limit to a more sophisticated method, such as Quiescence search.
* Implement the move database.
* Improve code quality.
