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

    start = {"point": problem.getStartState(), "parent": problem.getStartState()}
    visited = set()
    
    result = []
    stack = util.Stack()

    stack.push(start)
    node = stack.pop()

    while(node):
        
        if not (problem.isGoalState(node["point"]) and node["point"] not in visited):
            visited.add(node["point"])

            connected_elements = problem.getSuccessors(node["point"])

            for element in connected_elements:
                child = {"point": element[0], "parent": node, "direction": element[1]}
                if(child["point"] not in visited):
                    stack.push(child)

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
    
    start = {"point": problem.getStartState(), "parent": problem.getStartState()}
    visited = set() #{start: True}
    
    result = []
    queue = util.Queue()

    queue.push(start)
    node = queue.pop()

    while(node):
        
        if node["point"] not in visited:
            visited.add(node["point"])

            if not problem.isGoalState(node["point"]):
                connected_elements = problem.getSuccessors(node["point"])

                for element in connected_elements:
                    child = {"point": element[0], "parent": node, "direction": element[1]}
                    if(child["point"] not in visited):
                        queue.push(child)

            if(problem.isGoalState(node["point"])):
                
                while(node["parent"] != node["point"]):
                    result.append(node["direction"])
                    node = node["parent"]
                result.reverse()
                return result
        node = queue.pop()
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = set() #{start: True}
    
    result = []
    priorityQ = util.PriorityQueue()

    priorityQ.push({"point": problem.getStartState(), "parent": problem.getStartState(), "cost" : 0},0)
    node = priorityQ.pop()

    while(node):
        
        if node["point"] not in visited:
            visited.add(node["point"])

            if not problem.isGoalState(node["point"]):
                connected_elements = problem.getSuccessors(node["point"])

                for element in connected_elements:
                    if(element[0] not in visited):
                        priorityQ.push({"point": element[0], "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},node["cost"]+element[2])

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
    visited = set() #{start: True}
    
    result = []
    priorityQ = util.PriorityQueue()

    priorityQ.push({"point": problem.getStartState(), "parent": problem.getStartState(), "cost" : 0},0)
    node = priorityQ.pop()

    while(node):
        
        if node["point"] not in visited:
            visited.add(node["point"])

            if not problem.isGoalState(node["point"]):
                connected_elements = problem.getSuccessors(node["point"])

                for element in connected_elements:
                    if(element[0] not in visited):
                        priorityQ.push({"point": element[0], "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},heuristic(element[0],problem)+node["cost"]+element[2])

            if(problem.isGoalState(node["point"])):
                
                while(node["parent"] != node["point"]):
                    result.append(node["direction"])
                    node = node["parent"]
                result.reverse()
                return result
        node = priorityQ.pop()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
