# Code adapted from Daniel Hernandez and Peter York's MCTS code

import numpy as np
import random

import colorama
from colorama import Fore, Back

class GameState:
    """
        A GameState represents a valid configuration of the 'state' of a game.
        For instance:
            - the position of all the active pieces on a chess board.
            - The position and velocities of all the entities in a 3D world.
        This interface presents the minimal functionality required to implement
        an MCTS-UCT algorithm for a 2 player game.        
    """

    def __init__(self):
        self.playerJustMoved = 2 # Game starts with Player 1.

    def Clone(self):
        """ 
        :returns: deep copy of this GameState
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """
        !! This is the environment's model !!
        Changes the GameState by carrying out the param move.
        :param move: (int) action taken by an agent.
        """
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ :returns: int array with all available moves at this state
        """
        pass
        
    def IsGameOver(self):
        """ :returns: whether this GameState is a terminal state
        """
        return self.GetMoves() == []

    def GetResult(self, player):
        """ 
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        pass


class Connect4State(GameState):
    """
        GameState for the Connect 4 game.
        The board is represented as a 2D array (rows and columns).
        Each entry on the array can be:
            - 0 = empty    (.)
            - 1 = player 1 (X)
            - 2 = player 2 (O)
    """

    def __init__(self, width=7, height=6, connect=4):
        self.playerJustMoved = 2
        self.winner = 0 # 0 = no winner, 1 = Player 1 wins, 2 = Player 2 wins.

        self.width = width
        self.height = height
        self.connect = connect
        self.InitializeBoard()

    def InitializeBoard(self):
        """ 
        Initialises the Connect 4 gameboard.
        """
        self.board = []
        for y in range(self.width):
            self.board.append([0] * self.height)

    def Clone(self):
        """ 
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """
        st = Connect4State(width=self.width, height=self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = [self.board[col][:] for col in range(self.width)]
        return st

    def DoMove(self, movecol):
        """ 
        Changes this GameState by "dropping" a chip in the column
        specified by param movecol.
        :param movecol: column over which a chip will be dropped
        """
        assert movecol >= 0 and movecol <= self.width and self.board[movecol][self.height - 1] == 0
        row = self.height - 1
        while row >= 0 and self.board[movecol][row] == 0:
            row -= 1

        row += 1

        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[movecol][row] = self.playerJustMoved
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved
            
    def GetMoves(self):
        """
        :returns: array with all possible moves, index of columns which aren't full
        """
        if self.winner != 0:
            return []
        return [col for col in range(self.width) if self.board[col][self.height - 1] == 0]

    def DoesMoveWin(self, x, y):
        """ 
        Checks whether a newly dropped chip at position param x, param y
        wins the game.
        :param x: column index
        :param y: row index
        :returns: (boolean) True if the previous move has won the game
        """
        me = self.board[x][y]
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            p = 1
            while self.IsOnBoard(x+p*dx, y+p*dy) and self.board[x+p*dx][y+p*dy] == me:
                p += 1
            n = 1
            while self.IsOnBoard(x-n*dx, y-n*dy) and self.board[x-n*dx][y-n*dy] == me:
                n += 1

            if p + n >= (self.connect + 1): # want (p-1) + (n-1) + 1 >= 4, or more simply p + n >- 5
                return True

        return False

    def IsOnBoard(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def GetResult(self, player):
        """ 
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return player == self.winner

    def __repr__(self):
        s = ""
        for x in range(self.height - 1, -1, -1):
            for y in range(self.width):
                s += [Back.WHITE + Fore.WHITE + '.', Back.BLACK + Fore.WHITE + 'X', Back.BLACK + Fore.WHITE + 'O'][self.board[y][x]]
                s += Fore.RESET
                s += Back.RESET
            s += "\n"
        s += "\n\n\n"
        return s


def PrintGameResults(state):
    """ 
    Print match results. Function assumes match is over.
    """
    if state.winner != 0:
      if state.GetResult(state.playerJustMoved) == 1.0:
        print(str(state))
        print("Player " + str(state.playerJustMoved) + " wins!")
      else:
        print(str(state))
        print("Player " + str(3 - state.playerJustMoved) + " wins!")

    else:
        print("Nobody wins!")




def PlayGame(initialState):
    state = initialState
    while not state.IsGameOver():
        # Render
        print(str(state))
        # Capture user input
        if state.playerJustMoved == 1:
            # Player 2 turn
            move = random.choice(state.GetMoves())
        else:
            # Player 1 turn
            move = random.choice(state.GetMoves())
        # Update game state
        state.DoMove(move)

    PrintGameResults(state)









class Node:
    """ Node of a game tree. A tree is a connected acyclic graph.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # Move that was taken to reach this game state 
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.state = state

        self.value = 0
        self.playerJustMoved = state.playerJustMoved  # To check who won or who lost.

    def Successors(self):
        """
        Adds all child nodes to this Node. 
        :returns: dictionary of newly-expanded nodes in form {action: node}
        """
        succ = {}
        moves = self.state.GetMoves()
        for action in moves:
          new_state = self.state.Clone()
          new_state.DoMove(action)
          node = Node(move=action, parent=self, state=new_state)
          succ[action] = node
          self.childNodes.append(node)

        return(succ)

    def UpdateMinimax(self, heuristic=None):
        """
        Updates the minimax value for this node based on who is playing.
        """
        if len(self.childNodes) > 0:
          if self.playerJustMoved == 1:   # player 1 is max
            self.value = max(child.value for child in self.childNodes)
          else:                           # player 2 is min
            self.value = min(child.value for child in self.childNodes)
        else:
          if heuristic is not None:
            self.value = heuristic(self)
          else:
            if self.playerJustMoved == 1:
              self.value = 4
            else:
              self.value = -4

def PlayGameMinimax(initialState, rootNode):
    state = initialState
    currentRootNode = rootNode
    while not state.IsGameOver():
        # Render
        print(str(state))
        # Capture user input
        children = currentRootNode.childNodes
        vals = [child.value for child in children]
        if state.playerJustMoved == 1:
            # Min's turn 
            minval = min(vals)
            # always selects the left-most option:
            # idx = vals.index(minval)
    
            # randomly selects from all matching options
            idx = np.argwhere(np.array(vals)==np.min(vals)).flatten().tolist()
            idx = random.choice(idx)
        else:
            # Max's turn
            maxval = max(vals)
            # always selects the left-most option:
            #idx = vals.index(maxval)
    
            # randomly selects from all matching options            
            idx = np.argwhere(np.array(vals)==np.max(vals)).flatten().tolist()
            idx = random.choice(idx)


        move = children[idx].move
        # Update game state
        state.DoMove(move)
        currentRootNode = children[idx]

    PrintGameResults(state)

def BuildGameTree(initialState):
  root = Node(state=initialState)
  # depth-first search
  root = buildSubTree(root)
  return(root)

def buildSubTree(root):
  if root.state.IsGameOver():
    root.UpdateMinimax()
    return(root)

  succs = root.Successors()
  for child in root.childNodes:
    child = buildSubTree(child)
    child.UpdateMinimax()
  return(root)



#env = Connect4State(width=7, height= 6)
#PlayGame(env)

#state = Connect4State(width=4, height=3)
#print("Building game tree...")
#root = BuildGameTree(state)
#print("Playing game...")
#PlayGameMinimax(state, root)





def BuildGameTree_DL(initialState, depth=5):
  root = Node(state=initialState)
  # depth-first search
  root = buildSubTree_DL(root, depth)
  return(root)

def buildSubTree_DL(root, depth=5):
  if root.state.IsGameOver() or depth == 0:
    root.UpdateMinimax(heuristic)
    return(root)

  root.Successors()
  for child in root.childNodes:
    child = buildSubTree_DL(child, depth-1)
    child.UpdateMinimax(heuristic)
  return(root)

def heuristic(node):
  # check who's move it is
  currentPlayer = 3 - node.playerJustMoved
  currentMax = 0

  # count highest number of adjacent/diag pieces
  for x in range(node.state.width):
     for y in range(node.state.height):
       me = node.state.board[x][y]
       if me == currentPlayer:
         for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            p = 1
            while node.state.IsOnBoard(x+p*dx, y+p*dy) and node.state.board[x+p*dx][y+p*dy] == me:
                p += 1
            n = 1
            while node.state.IsOnBoard(x-n*dx, y-n*dy) and node.state.board[x-n*dx][y-n*dy] == me:
                n += 1
            
            if p + n > currentMax:
              currentMax = p + n
 
       y += 1
     x += 1
  if currentPlayer == 1:  # max
    return(currentMax)
  else:
   return(-currentMax)


def PlayGameMinimax_heur(initialState, lookahead=4):
    state = initialState
    currentRootNode = BuildGameTree_DL(initialState, depth=lookahead)
    while not state.IsGameOver():
        # Render
        print(str(state))
        # Capture user input
        children = currentRootNode.childNodes
        vals = [child.value for child in children]
        if state.playerJustMoved == 1:
            # Min's turn 
            minval = min(vals)
            print("choice: " + str(vals))
            idx = int(input(": ")) - 1
        else:
            # Max's turn
            maxval = max(vals)
            idx = np.argwhere(np.array(vals)==np.max(vals)).flatten().tolist()
            idx = random.choice(idx)

        move = children[idx].move
        # Update game state
        state.DoMove(move)
        currentRootNode = BuildGameTree_DL(children[idx].state, depth=lookahead)

        
    PrintGameResults(state)

state_heur = Connect4State(width=7, height=6)
PlayGameMinimax_heur(state_heur, lookahead=4)





