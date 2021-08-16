# MCTS
Python Implementations of Monte Carlo Tree Search for experimentation.  

Monte Carlo tree search (MCTS) is a newly emerging and promising algorithm in the AI literature.  See http://pubs.doc.ic.ac.uk/survey-mcts-methods/survey-mcts-methods.pdf for a survey on MCTS. 

This code is a toy implementation to play with the algorithm.  While MCTS can apply to many settings, in the code we apply it to a pretty simple but nonetheless interesting state.  

The State is a game where you have NUM_TURNS and at turn i you can make
a choice from an integeter [-2,2,3,-3]*(NUM_TURNS+1-i).  So for example in a game of 4 turns, on turn for turn 1 you can can choose from [-8,8,12,-12], and on turn 2 you can choose from [-6,6,9,-9].  At each turn the choosen number is accumulated into a aggregation value.  The goal of the game is for the accumulated value to be as close to 0 as possible.

The game may not be very interesting but it allows one to study MCTS which is.  Some features of the simple game by design are that moves do not commute, and early mistakes are more costly.  

USAGE:
python mcts.py --num_sims 10000 --levels 8

num_sims is the number of simulations to perform, and levels is the number of times to use MCTS to pick a best child 


In a 10 turn game here is an optimal solution
[-20, 27, -16, 14, 18, -15, -8, 6, -4, -2]

Here is a suboptimal solution that you may end up with a local plateau on for example
[20, -18, -16, 14, 12, -10, -8, 6, 4, -3]

