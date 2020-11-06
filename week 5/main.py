from connect4 import *
import time

class game_tree_node:
    def __init__(self, move:int=None, state=None, parent=None) -> None:
        self.move = move # move taken to reach this state
        self.state = state
        self.parent = parent # None is root

        self.children = []
        self.value = 0
        self.player_just_moved = state.playerJustMoved

    def gen_children(self):
        """
        Adds all children nodes to the node
        """
        children = {}
        moves = self.state.GetMoves()
        for action in moves:
            new_state = self.state.Clone()
            new_state.DoMove(action)
            node = game_tree_node(action, new_state, self)
            children[action] = node
            self.children.append(node)
        return children

    def update_minimax(self, heuristic=None):
        if len(self.children) > 0:
            if self.player_just_moved == 1: # player 1 is max
                self.value = max(child.value for child in self.children)
            else:
                self.value = min(child.value for child in self.children)
        else:
            if heuristic is not None:
                self.value = heuristic(self)
            else:
                if self.player_just_moved == 1:
                    self.value = 4
                else:
                    self.value = -4
    
def play_game_minimax(initial_state: Connect4State, lookahead=4):
    state = initial_state
    cur_root_node = gen_game_tree_dl(initial_state, lookahead)

    while not state.IsGameOver():
        # render
        print(str(state))
        # capture user input
        children = cur_root_node.children
        vals = [child.value for child in children]
        if state.playerJustMoved == 1:
            # min's turn
            print("choice: " + str(vals))
            # idx = int(input(": ")) - 1
            idx = np.argwhere(np.array(vals)==np.min(vals)).flatten().tolist()
            idx = random.choice(idx)
        else:
            # max's turn
            idx = np.argwhere(np.array(vals)==np.max(vals)).flatten().tolist()
            idx = random.choice(idx)
            print("choice: " + str(vals))
            print(": " + str(idx - 1))
        
        move = children[idx].move
        # updating game state
        state.DoMove(move)
        cur_root_node = gen_game_tree_dl(children[idx].state, depth=lookahead)
    
    PrintGameResults(state)

def gen_game_tree(initial_state) -> game_tree_node:
    root = game_tree_node(state=initial_state)
    # depth-first search
    root = gen_sub_tree(root)
    return root

def gen_sub_tree(root: game_tree_node):
    time.sleep(1)
    print(str(root.state))
    if root.state.IsGameOver():
        root.update_minimax()
        return root
    
    root.gen_children()
    for child in root.children:
        child = gen_sub_tree(child)
        child.update_minimax(heuristic)

    return root

def gen_game_tree_dl(initial_state: Connect4State, depth=5):
    root = game_tree_node(state=initial_state)
    # depth-first search
    root = gen_sub_tree_dl(root, depth)
    return root

def gen_sub_tree_dl(root, depth=5):
    if root.state.IsGameOver() or depth == 0:
        root.update_minimax(heuristic)
        return root
    
    root.gen_children()
    for child in root.children:
        child = gen_sub_tree_dl(child, depth-1)
        child.update_minimax(heuristic)
    return root

def heuristic(node):
  # check who's move it is
  currentPlayer = 3 - node.player_just_moved
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

state = Connect4State(width=7, height=6)
# print("building game tree...")
# root = gen_game_tree_dl(state)
print("playing...")
play_game_minimax(state, 4)