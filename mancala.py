#!/usr/bin/env python
import random
import math
import hashlib
import logging
import argparse
from copy import deepcopy
from mcts import *

"""
Mancala using MCTS.

First to get >=25 points wins
Board starts as rows =[r1,r2] with ri = [4,4,4,4,4,4]
r1 = [0,1,2,3,4,5]
r2 = [0,1,2,3,4,5]
"""

NUM_TURNS = 3

class MancalaState():
  def __init__(self,player1_points=0,player2_points=0,board=[[4,4,4,4,4,4],[4,4,4,4,4,4]],played_moves=[]):
    self.player1_points = player1_points
    self.player2_points = player2_points
    self.board = board
    self.num_moves = 6
    self.played_moves=played_moves

  def play2(self):
    logger.info("PLAYING 2:: %s"%self)
    moves2 = []
    for ind,val in enumerate(self.board[1]):
      if val>0:
        moves2.append((ind,val))
    if not moves2:
      return
    ind2,val2 = random.choice(moves2)
    logger.info("Moving %d,%d"%(ind2,val2))
    self.played_moves.append("PLAYER2: ind:%d,val:%d"%(ind2,val2))
    lind = "NEGATIVE"
    #pickup 
    self.board[1][ind2]=0
    #play
    while val2>0 and ind2>0:
      ind2-=1
      val2-=1
      self.board[1][ind2]+=1
      lind = ind2
    if val2>0:
      self.player2_points+=1
      val2-=1
      ind2=-1
      lind = "HOME"
    while val2>0 and ind2<5:
      ind2+=1
      val2-=1
      self.board[0][ind2]+=1
      lind = "NEGATIVE"
    if val2>0:
      ind2=6
    while val2>0 and ind2>0:
      ind2-=1
      val2-=1
      self.board[1][ind2]+=1
      lind = ind2
    if val2>0:
      self.player2_points+=1
      val2-=1
      ind2=-1
      lind = "HOME"
    while val2>0 and ind2<5:
      ind2+=1
      val2-=1
      self.board[0][ind2]+=1
      lind = "NEGATIVE"
    if lind == "HOME":
      if self.check_for_remaining():
        self.play2()
    elif lind != "NEGATIVE":
      if self.board[1][lind]==1:
        captured = self.board[0][lind]
        self.player2_points += captured + 1
        self.board[0][lind] = 0
        self.board[1][lind] = 0
        self.check_for_remaining()

  def play1(self):
    logger.info("PLAYING 1:: %s"%self)
    moves1 = []
    for ind,val in enumerate(self.board[0]):
      if val>0:
        moves1.append((ind,val))
    if not moves1:
      return
    ind1,val1 = random.choice(moves1)
    logger.info("Moving %d,%d"%(ind1,val1))
    self.played_moves.append("PLAYER1: ind:%d,val:%d"%(ind1,val1))
    lind = "NEGATIVE"
    #pickup 
    self.board[0][ind1]=0
    #play
    while val1>0 and ind1<5:
      ind1+=1
      val1-=1
      self.board[0][ind1]+=1
      lind = ind1
    if val1>0:
      self.player1_points+=1
      val1-=1
      ind1=6
      lind = "HOME"
    while val1>0 and ind1>0:
      ind1-=1
      val1-=1
      self.board[1][ind1]+=1
      lind = "NEGATIVE"
    if val1>0:
      ind1=-1
    while val1>0 and ind1<5:
      ind1+=1
      val1-=1
      self.board[0][ind1]+=1
      lind = ind1
    if val1>0:
      self.player1_points+=1
      val1-=1
      ind1=6
      lind = "HOME"
    while val1>0 and ind1>0:
      ind1-=1
      val1-=1
      self.board[1][ind1]+=1
      lind = "NEGATIVE"
    if lind == "HOME":
      if self.check_for_remaining():
        self.play1()
    elif lind != "NEGATIVE":
      if self.board[0][lind]==1:
        captured = self.board[1][lind]
        self.player1_points += captured + 1
        self.board[0][lind] = 0
        self.board[1][lind] = 0
        self.check_for_remaining()
    
  def check_for_remaining(self):
    s1 = sum(self.board[0])
    s2 = sum(self.board[1])
    if s1==0 or s2 ==0:
      self.player1_points+=s1
      self.player2_points+=s2
      self.board=[[0,0,0,0,0,0],[0,0,0,0,0,0]]
      return False
    return True

  def next_state(self):
    if self.check_for_remaining():
      self.play1()
    if self.check_for_remaining():
      self.play2()
    return MancalaState(self.player1_points,self.player2_points,deepcopy(self.board),deepcopy(self.played_moves))
  
  def terminal(self):
    self.check_for_remaining()
    p1_wins = self.player1_points>=25
    p2_wins = self.player2_points>=25
    if p1_wins or p2_wins:
      return True
    if sum(self.board[0]+self.board[1])==0:
      return True
    return False

  def reward(self):
    if self.player1_points>=25:
      return 1
    elif self.player1_points==24:
      return 0.5
    else:
      return 0

  def __hash__(self):
    return int(hashlib.md5(str(self.board).encode('utf-8')).hexdigest(),16)
  
  def __eq__(self,other):
    return hash(self)==hash(other)

  def __repr__(self):
    return "CurrentState: %s; points1: %d, points2: %d\nplayed_moves:\n%s"%(self.board,self.player1_points,self.player2_points,"\n".join(self.played_moves))


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='MCTS research code')
  parser.add_argument('--num_sims', action="store", required=True, type=int, help="Number of simulations to run")
  args=parser.parse_args()
  
  current_node=Node(MancalaState())
  num_moves_lambda = lambda node: len([x for x in node.state.board[0] if x>0])
  for l in range(NUM_TURNS):
    current_node=UCTSEARCH(args.num_sims/(l+1),current_node,num_moves_lambda)
    print("level %d"%l)
    print("Num Children: %d"%len(current_node.children))
    for i,c in enumerate(current_node.children):
      print(i,c,c.state.board)
    print("Best Child: %s"%current_node.state)
    print("--------------------------------")	
