import random
import string
import pprint_jhs

def getRandomName(length = 4, exclude_list = []):
    # return a random text string of length `length`
    thisName = ''.join([random.choice(string.ascii_lowercase) for _ in range(length)])
    while thisName in exclude_list:
        thisName = ''.join([random.choice(string.ascii_lowercase) for _ in range(length)])
    
    return thisName
    
def mergeTrees(tree1, tree2, permitDuplicateNames = False):
    
    # go through the entire dictionary `tree2` and merge each element with the matching element in `tree1`
    
    for (k,v) in tree2.items():
        if tree1.get(k) is None:
            tree1.update([(k, v)])
        else:
            if permitDuplicateNames:
                tree1[k].append(v)
            else:
                # need to rename k
                name = getRandomName(len(k), tree1.keys())
                tree1.update([(name, v)])
    
    return tree1
                
    
    
def getTree(ID, minDepth = 3, maxDepth = 3, 
                minBranch = 2, maxBranch = 3):
    random.seed(ID)
    return getTree_aux(ID, depth = random.randint(minDepth, maxDepth), 
                           branch = random.randint(minBranch, maxBranch))
    
    
    
def getTree_aux(ID, depth, branch):

    if depth == 0:    # inequality isn't correct
        return {}
    
    
    # because we are recursing, we can assume this is the root of the tree:
    name = getRandomName()
    tree = {name : []}   # random name of node? if this is long enough then we *shouldn't* 
                         # get any duplicates, but these can be picked up during the unroll...
    

    
    for b in range(branch):
        t = getTree_aux(ID, depth - 1, branch)
        # need to attach the new tree, rather than just merging it...
        # is it enough to get the root of the branched trees and form those into the list for this tree? 
        tree = mergeTrees(tree, t, permitDuplicateNames = False)
        if len(list(t.keys())) > 0:
            tree[name].append(list(t.keys())[0])
    
    return tree


