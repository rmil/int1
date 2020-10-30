# import the tree generation code and pretty-printer
from randomTree_jhs import *
import pprint_jhs

#import my solution
import find

# dependency
import random

# changing this value will give you a different random tree:
tree_id = 4

# need to initialise our pretty-printer
p = pprint_jhs.PrettyPrinter(width=15)

# generate the tree
t = getTree(tree_id, 6, 6, 4, 4)

# print it out
p.pprint(t)

init = next(iter(t))
goal = random.choice(list(t))

print("init: " + init)
print("goal: " + goal)
task = find.problem(init, goal, t)

find.tree_search(task)