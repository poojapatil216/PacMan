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

    start = {"point": problem.getStartState(), "parent": problem.getStartState()}
    visited = set()
    
    result = []
    stack = util.Stack()

    stack.push(start)
    node = stack.pop()

    while(True):
        
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
    # Using if else to segerate the case of when we have only 1 end state and when we have 4 (Corner Problem)

    length = problem.getStartState() 
    tp = type(problem.getStartState()) # to check type of start state

    # In corner problem we are send starting point as well as all 4 corner as end goal state as dictionary combined

    # Format : ((starting point), {dict of 4 end state}) ---> In case of corner problem
    
    if tp is str or (len(length) == 2 and type(length[1]) is not dict):
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

    else:  
        cornerVisitedGlobal = problem.getStartState()[1]
        minLengthPAth = []

        # Approach : We have defined our start State to return starting point as well as all the 4 corner points
        # And isGoalState function return list [Value1, Value2] where Value1 represents that for any particular point 
        # sent to this function is that point part of corner or not and Value2 represents wheather all 4 corners are visited or not 
        for firstCornerToVisit in cornerVisitedGlobal:
            fullPath = []
            corner = []
            start = {"point": problem.getStartState()[0], "parent": problem.getStartState()[0]}
            cornerVisited = problem.getStartState()[1]
            visited = set()
        
            result = []
            queue = util.Queue()

            queue.push(start)
            node = queue.pop()
            flag = 0

            # We tried starting our BFS from starting point and when it reached any 1 of ending point we considered 
            # it as new starting point and continued our BFS but this approach was not giving optimal answer 
            # So for new approach we tried combinations in which we want to visit our corners and created path from that an we were able to get optimal answer
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
                    # This condition restricts our code to go to a particular corner only in first BFS run 
                    if(node["point"] == firstCornerToVisit and node["point"] not in corner):
                        flag = 1 
                        cornerVisited[node["point"]] = True
                        corner.append(node["point"])
                        visited = set() # Reinitializing Visited Set as we have to restart our BFS traversal
                        nextStart = node["point"]
                        
                        # Here we are creating the path from start to that corner point
                        while(node["parent"] != node["point"]):
                            result.append(node["direction"])
                            node = node["parent"]
                        result.reverse()
                        fullPath.extend(result)
                        result = []

                        #Empyting Queue to restart BFS
                        while(queue.isEmpty() == False):
                            queue.pop()
                        queue.push({"point": nextStart, "parent": nextStart})
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
            minLengthPAth.append(fullPath)
        lengthsOfAllPaths = []

        # Getting Minimum length path from all our path combinations
        for paths in minLengthPAth:
            lengthsOfAllPaths.append(len(paths))
        minLength = min(lengthsOfAllPaths)
        return minLengthPAth[lengthsOfAllPaths.index(minLength)]
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = set() #{start: True}
    
    result = []
    priorityQ = util.PriorityQueue()
    state = problem.getStartState()

    # Using if else condition to segerate parts in which we have 1 end goal and when we have more than 1 end goal
    
    if(len(state) == 2 and isinstance(state[1], int) is not True):
        start = state[0]
        cornerVisited = state[1]
        fullPath = []
        cornerInPath = []

        # converting List of end goal points to Dictionary 
        if(type(cornerVisited) is not dict):
            cornerVisited2 = {}
            for corner in cornerVisited.asList():
                cornerVisited2[corner] = False

            cornerVisited = cornerVisited2

        priorityQ.push({"point": start, "parent": start, "cost" : 0},0)
        node = priorityQ.pop()
        while(problem.isGoalState((node["point"],cornerVisited))[1] == False):
            if node["point"] not in visited:
                visited.add(node["point"]) 
                if True:
                    connected_elements = problem.getSuccessors((node["point"],state[1]))
                    for element in connected_elements:
                        ele = element[0][0]
                        if(ele not in visited):
                            priorityQ.push({"point": ele, "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},node["cost"]+element[2])

                # Creating a path from starting to a particular corner point and then starting UCS algorithm 
                # Again considering that corner as Start till we cover all corners
                # print(node["point"])
                # print(cornerVisited)
                if(problem.isGoalState((node["point"],cornerVisited))[0] == True and node["point"] not in cornerInPath): 
                    cornerVisited[node["point"]] = True
                    cornerInPath.append(node["point"])
                    visited = set() # Reinitializing visited to restart algorithm again
                    nextStart = node["point"]
                    
                    # Creating path from start to corner
                    while(node["parent"] != node["point"]):
                        result.append(node["direction"])
                        node = node["parent"]
                    result.reverse()
                    fullPath.extend(result)
                    result = []
                    while(priorityQ.isEmpty() == False):
                        priorityQ.pop()
                    priorityQ.push({"point": nextStart, "parent": nextStart, "cost" : 0},0)
            node = priorityQ.pop()

        return fullPath
    else:
        start = state
        priorityQ.push({"point": start, "parent": start, "cost" : 0},0)
        node = priorityQ.pop()

        while(True):
            
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
    # Using if else to segerate the case of when we have only 1 end state and when we have 4 (Corner Problem)

    length = problem.getStartState() 
    tp = type(problem.getStartState()) # to check type of start state

    # In corner problem we are send starting point as well as all 4 corner as end goal state as dictionary combined

    # Format : ((starting point), {dict of 4 end state}) ---> In case of corner problem
    flag1 = 0
    if(len(length) == 2):
        try:
            length[1].asList()
        except:
            flag1 = 1


    if tp is str or (len(length) == 2 and type(length[1]) is not dict and flag1 == 1):
      
        visited = set() 
    
        result = []
        priorityQ = util.PriorityQueue()

        priorityQ.push({"point": problem.getStartState(), "parent": problem.getStartState(), "cost" : 0},0)
        node = priorityQ.pop()

        while(True):
            
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
    else:  

        fullPath = []
        cornerInPath = []
        cornerVisited = problem.getStartState()[1]
        flag = 0

      #  print("Here")

        # Using this to seperate code for input which have 4 corners as end goal or any number of random points as end goal
        # and converting random end goals to dictionary to reuse corner problem code only
        if(type(cornerVisited) is not dict):
            flag = 1
            cornerVisited2 = {}
            for corner in cornerVisited.asList():
                cornerVisited2[corner] = False

            cornerVisited = cornerVisited2
            cornerVisited2 = problem.getStartState()[1].asList()

        visited = set() #{start: True}
    
        result = []
        queue = util.PriorityQueue()

        queue.push({"point": problem.getStartState()[0], "parent": problem.getStartState()[0], "cost" : 0},0)
        node = queue.pop()

        # Running A* Till we reach all 4 corner points
        while(problem.isGoalState((node["point"],cornerVisited))[1] == False):
            if node["point"] not in visited:
                visited.add(node["point"]) 
                if True:
                    connected_elements = problem.getSuccessors((node["point"],length[1]))
                    for element in connected_elements:
                        # Depending on our problem type we have to assign our element so using ternary operator here
                        ele = element[0] if flag == 0 else element[0][0]
                        #print(ele)
                        if(ele not in visited):
                            queue.push({"point": ele, "parent": node, "direction": element[1], "cost" : node["cost"]+element[2]},heuristic((ele,length[1]),problem )+node["cost"]+element[2])

                # Creating a path from starting to a particular corner point and then starting A* algorithm 
                # Again considering that corner as Start till we cover all corners
                if(problem.isGoalState((node["point"],cornerVisited))[0] == True and node["point"] not in cornerInPath): 
                    cornerVisited[node["point"]] = True
                    cornerInPath.append(node["point"])
                    visited = set() # Reinitializing visited to restart algorithm again
                    nextStart = node["point"]
                    
                    # Creating path from start to corner
                    while(node["parent"] != node["point"]):
                        result.append(node["direction"])
                        node = node["parent"]
                    result.reverse()
                    fullPath.extend(result)
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
