# MCTS
Python Implementations of Monte Carlo Tree Search for experimentation.  

Monte Carlo tree search (MCTS) is a newly emerging and promising algorithm in the AI literature.  See http://pubs.doc.ic.ac.uk/survey-mcts-methods/survey-mcts-methods.pdf for a survey on MCTS. 

I built this implementation just to play with the algorithm.  While MCTS can apply to many settings, in the code I apply it to a pretty simple but nonetheless interesting state.  

The State is just a game where you have NUM_TURNS and at turn i you can make
a choice from [-2,2,3,-3]*i and this to to an accumulated value.  The goal is for the accumulated value to be as close to 0 as possible.

The game is not very interesting but it allows one to study MCTS which is.  Some features 
of the example by design are that moves do not commute and early mistakes are more costly.  

USAGE:
python mcts.py --num_sims 10000 --levels 8

num_sims is the number of simulations to perform, and levels is the number of times to use MCTS to pick a best child 


