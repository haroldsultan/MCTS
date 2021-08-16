#!/usr/bin/env python
import random
import math
import hashlib
import logging
import argparse
from mcts import *

"""
Another game using MCTS.  based on a comment from 
atanas1054 on Jun 27, 2017

I want to have a 2-player game where they take turns. 
In the beginning there are 114 possible actions and they decrease by 1 every time a player makes a move. 
The game is played for 10 turns (that's the terminal state). I have my own function for the reward.

Here is a sample game tree:

START- available actions to both players -> [1,2,3,4,5,6....112,113,114]
Player 1 - takes action 5 -> [5,0,0,0,0,0,0,0,0,0] -remove action 5 from available actions
Player 2 - takes action 32->[5,0,0,0,0,32,0,0,0,0] - remove action 32 from the available actions
Player 1- takes action 97 ->[5,97,0,0,0,32,0,0,0,0] - remove action 97 from the available actions
Player 2 takes action 56 -> [5,97,0,0,0,32,56,0,0,0] - remove action 56 from the available actions
....
Final (example) game state after each player makes 5 actions -> [5,97,3,5,1,32,56,87,101,8]
First 5 entries present the actions taken by Player1, second 5 entries present the actions taken by Player 2

Finally, I apply a reward function to this vector [5,97,3,5,1,32,56,87,101,8]
"""

NUM_TURNS = 5

class AntasState():
  def __init__(self, current=[0]*2*NUM_TURNS,turn=0):
    self.current=current
    self.turn=turn
    self.num_moves=(114-self.turn)*(114-self.turn-1)

  def next_state(self):
    availableActions=[x for x in range(1,115)]
    for c in self.current:
      if c in availableActions:
        availableActions.remove(c)
    player1action=random.choice(availableActions)
    availableActions.remove(player1action)
    nextcurrent=self.current[:]
    nextcurrent[self.turn]=player1action
    player2action=random.choice(availableActions)
    availableActions.remove(player2action)
    nextcurrent[self.turn+NUM_TURNS]=player2action
    next=AntasState(current=nextcurrent,turn=self.turn+1)
    return next
  
  def terminal(self):
    return self.turn == NUM_TURNS
  def reward(self):
    r = random.uniform(0,1) #ANTAS, put your own function here
    return r

  def __hash__(self):
    return int(hashlib.md5(str(self.current).encode('utf-8')).hexdigest(),16)
  
  def __eq__(self,other):
    return hash(self)==hash(other)

  def __repr__(self):
    return "CurrentState: %s; turn %d"%(self.current,self.turn)


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='MCTS research code')
  parser.add_argument('--num_sims', action="store", required=True, type=int, help="Number of simulations to run, should be more than 114*113")
  args=parser.parse_args()
  
  current_node=Node(AntasState())
  for l in range(NUM_TURNS):
    current_node=UCTSEARCH(args.num_sims/(l+1),current_node)
    print("level %d"%l)
    print("Num Children: %d"%len(current_node.children))
    for i,c in enumerate(current_node.children):
      print(i,c)
    print("Best Child: %s"%current_node.state)
    print("--------------------------------")	
