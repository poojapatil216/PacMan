# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from operator import indexOf
import string
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Also Implemented a recursive solution for DFS

# def dfss(node, problem, visited, result):

#     if problem.isGoalState(node):
#         return True
    
#     visited.add(node)
#     successors = problem.getSuccessors(node)

#     for successor in successors:
#         if(successor[0] not in visited):
#             result.append(successor[1])
#             if(dfss(successor[0], problem, visited, result)):
#                 return True
#             else:
#                 result.pop()

#     return False

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """ print("I am here")
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Is the start a goal?", problem.isGoalState((1,1))
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    print("Now i am here") """
    #start stores the node with its parent so that the path can be constructed later
    start = {"point": problem.getStartState(), "parent": problem.getStartState()}
    #a set to store all the visited nodes to avoid looping through the same nodes
    visited = set()
    #this will hold the final directions list for the pacman to follow
    result = []
    #stack to hold the nodes to be explored
    stack = util.Stack()

    stack.push(start)
    node = stack.pop()

    while(node):
        #if the current node is unvisited and not goal state we fetch its neighbors to push them to stack
        if not (problem.isGoalState(node["point"]) and node["point"] not in visited):
            visited.add(node["point"])

            connected_elements = problem.getSuccessors(node["point"])

            for element in connected_elements:
                child = {"point": element[0], "parent": node, "direction": element[1]}
                if(child["point"] not in visited):
                    stack.push(child)
        #if we reach the goal state then using the parent-node relation the path is constructed by going in reverse manner and getting the directions
        if(problem.isGoalState(node["point"])):
            
            while(node["parent"] != node["point"]):
                result.append(node["direction"])
                node = node["parent"]
            result.reverse()
            return result
        node = stack.pop()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # the if condition either checks if the states are string as is given by the autograder 
    #or checks if the state is a single node(PositionSearchProblem) or a dictionary (CornersProblem)
    
    #Code for PositionSearchproblem
    startState=problem.getStartState();
    if type(startState) is str or (type(startState[1]) is not dict) :
        start = {"point": startState, "parent": startState}
        visited = set() #{start: True}
        
        result = []
        queue = util.Queue()

        queue.push(start)
        node = queue.pop()

        while(node):
            
            if node["point"] not in visited:
                visited.add(node["point"])
                # if the current node is not goal state we fetch the neighbors and push them into the queue
                if not problem.isGoalState(node["point"]):
                    connected_elements = problem.getSuccessors(node["point"])

                    for element in connected_elements:
                        child = {"point": element[0], "parent": node, "direction": element[1]}
                        if(child["point"] not in visited):
                            queue.push(child)
                #if the node is goal we use the parent-node relation to construct the path with directions in the reverse manner
                if(problem.isGoalState(node["point"])):
                    
                    while(node["parent"] != node["point"]):
                        result.append(node["direction"])
                        node = node["parent"]
                    result.reverse()
                    return result
            node = queue.pop()
    #Code for CornersProblem
    else:
        # startState((starting_position),{dictionary of corner nodes and their visit status})
        # we fetch a list of corners and try making every corner as first corner to be visited to find which path will be the shortest
        cornerVisitedGlobal = startState[1]
        #list storing all possible paths to travel all four corners
        possiblePaths = []

        #the following for loop runs 4 times each time considering a different corner to visit first
        for firstCornerToVisit in cornerVisitedGlobal:
            #list to store the path 
            fullPath = []
            corner = []
            start = {"point": startState[0], "parent": startState[0]}
            cornerVisited = startState[1]
            visited = set()
        
            result = []
            queue = util.Queue()

            queue.push(start)
            node = queue.pop()
            flag = 0
            # the goal state is defined as a list of two values, the first parameter returns whether the current node is one of the corners or not 
            #and the second returns whether all the corners are visited or not yet
            
            #the following while loop keeps running until all four corners are visited
            while(problem.isGoalState((node["point"],cornerVisited))[1] == False):
                if node["point"] not in visited:
                    visited.add(node["point"]) 
                    if True:
                        connected_elements = problem.getSuccessors(node["point"])

                        for element in connected_elements:
                            if(element[0] not in visited):
                                child = {"point": element[0], "parent": node, "direction": element[1]}
                                if(child["point"] not in visited):
                                    queue.push(child)
                    # This condition checks whether we have visited our first corner and sets flag to true if yes
                    if(node["point"] == firstCornerToVisit and node["point"] not in corner):
                        flag = 1 
                        cornerVisited[node["point"]] = True
                        corner.append(node["point"])
                        visited = set() # Reinitializing Visited Set as we have to restart our BFS traversal to vist the next corner
                        nextStart = node["point"]
                        
                        # Here we are creating the path from start to the first corner point
                        while(node["parent"] != node["point"]):
                            result.append(node["direction"])
                            node = node["parent"]
                        result.reverse()
                        fullPath.extend(result)
                        result = []

                        #Empyting Queue to restart BFS to visit other nodes
                        while(queue.isEmpty() == False):
                            queue.pop()
                        queue.push({"point": nextStart, "parent": nextStart})
                    # this section of code is visited when atleast one corner is visited and we're trying to visit the rest of the corners
                    elif(problem.isGoalState((node["point"],cornerVisited))[0] == True and node["point"] not in corner and flag == 1):
                        cornerVisited[node["point"]] = True
                        corner.append(node["point"])
                        visited = set()
                        nextStart = node["point"]
                        
                        while(node["parent"] != node["point"]):
                            result.append(node["direction"])
                            node = node["parent"]
                        result.reverse()
                        fullPath.extend(result)
                        result = []
                        while(queue.isEmpty() == False):
                            queue.pop()
                        queue.push({"point": nextStart, "parent": nextStart})
                node = queue.pop()
            possiblePaths.append(fullPath) #adding the path to list of all possible paths
            startState=problem.getStartState() #reinitializing the start state coz we're trying all over again with a different first corner to visit

        #sending the shortest path of all possible paths
        return min(possiblePaths,key=len)
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = set() #{start: True}
    
    result = [] #list to store the path
    priorityQ = util.PriorityQueue()

    priorityQ.push({"point": problem.getStartState(), "parent": problem.getStartState(), "cost" : 0},0)
    node = priorityQ.pop()
    # the following node runs until the queue is empty(impossible to reach goal) or the goal is reached
    while(node):
        
        if node["point"] not in visited:
            visited.add(node["point"])
            #get the neighbors if current node is not goal
            if not problem.isGoalState(node["point"]):
                connected_elements = problem.getSuccessors(node["point"])
                for element in connected_elements:    
                    #push the nodes with priority being the cost so far
                    if(element[0] not in visited):
                        priorityQ.push({"point": element[0], "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},node["cost"]+element[2])
            #if goal is reached construct the path with parent-node relation in the reverse manner
            if(problem.isGoalState(node["point"])):
                while(node["parent"] != node["point"]):
                    result.append(node["direction"])
                    node = node["parent"]
                result.reverse()
                return result
        node = priorityQ.pop()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # the if condition either checks if the states are string as is given by the autograder 
    #or checks if the state is a single node(PositionSearchProblem) or a dictionary (CornersProblem)
    
    #Code for PositionSearchProblem
    startState=problem.getStartState()
    if type(startState) is str or (type(startState[1]) is not dict):
        visited = set() 
    
        result = []
        priorityQ = util.PriorityQueue()
        #initiaizing the priority queue with initial cost=0 and heuristic 0
        priorityQ.push({"point": startState, "parent": startState, "cost" : 0},0)
        node = priorityQ.pop()

        while(node):
            
            if node["point"] not in visited:
                visited.add(node["point"])
                #if the current state not goal we fetch the neighbors
                if not problem.isGoalState(node["point"]):
                    connected_elements = problem.getSuccessors(node["point"])
                    # the neighbors are appended to the priority queue with the priority set as (cost so far + estimated heuristic value to the reach the goal)
                    for element in connected_elements:
                        if(element[0] not in visited):
                            priorityQ.push({"point": element[0], "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},heuristic(element[0],problem)+node["cost"]+element[2])
                #if goal state reached then construct the path using the parent-node relation in reverse manner
                if(problem.isGoalState(node["point"])):                    
                    while(node["parent"] != node["point"]):
                        result.append(node["direction"])
                        node = node["parent"]
                    result.reverse()
                    return result
            node = priorityQ.pop()
    # Code for CornersProblem
    else:  

        fullPath = []
        corner = []
        cornerVisited = startState[1]
        visited = set() #{start: True}
    
        result = []
        queue = util.PriorityQueue()

        queue.push({"point": startState[0], "parent": startState[0], "cost" : 0},0)
        node = queue.pop()
        
        # the goal state is defined as a list of two values, the first parameter returns whether the current node is one of the corners or not 
        # and the second returns whether all the corners are visited or not yet
        # Running A* Till we reach all 4 corner points
        while(problem.isGoalState((node["point"],cornerVisited))[1] == False):
            if node["point"] not in visited:
                visited.add(node["point"]) 
                if True:
                    connected_elements = problem.getSuccessors(node["point"])

                    for element in connected_elements:
                        if(element[0] not in visited):
                            queue.push({"point": element[0], "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},heuristic((element[0],cornerVisited),problem)+node["cost"]+element[2])

                # Creating a path from starting to a particular corner point and then starting A* algorithm 
                # Again considering that corner as Start till we cover all corners
                if(problem.isGoalState((node["point"],cornerVisited))[0] == True and node["point"] not in corner): 
                    cornerVisited[node["point"]] = True
                    corner.append(node["point"])
                    visited = set() # Reinitializing visited to restart algorithm again
                    nextStart = node["point"]
                    
                    # Creating path from start to corner
                    while(node["parent"] != node["point"]):
                        result.append(node["direction"])
                        node = node["parent"]
                    result.reverse()
                    fullPath.extend(result) #adds path after every corner visit to construct the entire path
                    result = []
                    while(queue.isEmpty() == False):
                        queue.pop()
                    queue.push({"point": nextStart, "parent": nextStart, "cost" : 0},0)
            node = queue.pop()

        return fullPath


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
