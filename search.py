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
    from util import Stack

    frontier = Stack()
    explored = []
    actions = []

    class node:
        def __init__(self, path, cost, dad, action):
            self.path = path
            self.cost = cost
            self.dad = dad
            self.action = action

    start = node(problem.getStartState(),0,'','')
    frontier.push(start)

    while frontier.isEmpty() == False:
        path = frontier.pop()
        successors = problem.getSuccessors(path.path)
        explored.append(path)
        for vertex in successors:
            achou = False
            for path_ex in explored:
                if vertex[0] == path_ex.path:
                    achou = True
            if achou == False:
                successor = node(vertex[0],vertex[2],path.path,vertex[1])
                frontier.push(successor)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    frontier = Queue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, cost, dad, action):
            self.path = path
            self.cost = cost
            self.dad = dad
            self.action = action

    start = node(problem.getStartState(),0,'','')
    frontier.push(start)

    while frontier.isEmpty() == False:
        path = frontier.pop()
        successors = problem.getSuccessors(path.path)
        explored.append(path)

        for vertex in successors:
            achou = False
            for path_ex in explored:
                if vertex[0] == path_ex.path:
                    achou = True

            if achou == False:
                successor = node(vertex[0],vertex[2],path.path,vertex[1])
                frontier.push(successor)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import euclideanHeuristic
    import math

    frontier = PriorityQueue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            self.cost = round(euclideanHeuristic(problem.getStartState(),path),1)

    start = node(problem.getStartState(),'','')
    frontier.push(start,start.cost)

    while frontier.isEmpty() == False:
        path = frontier.pop()
        successors = problem.getSuccessors(path.path)
        explored.append(path)
        for vertex in successors:
            achou = False
            for path_ex in explored:
                if vertex[0] == path_ex.path:
                    achou = True

            if achou == False:
                successor = node(vertex[0],path.path,vertex[1])
                frontier.push(successor,successor.cost)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import euclideanHeuristic
    import math

    frontier = PriorityQueue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            h = euclideanHeuristic(path,problem.goal)
            g = euclideanHeuristic(problem.getStartState(),path)
            self.cost = round(g + h,1)

    start = node(problem.getStartState(),'','')
    frontier.push(start,start.cost)

    while frontier.isEmpty() == False:
        path = frontier.pop()
        successors = problem.getSuccessors(path.path)
        explored.append(path)
        for vertex in successors:
            achou = False
            for path_ex in explored:
                if vertex[0] == path_ex.path:
                    achou = True

            if achou == False:
                successor = node(vertex[0],path.path,vertex[1])
                frontier.push(successor,successor.cost)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

def hillClibing(problem):
    from util import PriorityQueue
    from util import euclideanHeuristic
    import math

    frontier = PriorityQueue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            self.cost = round(euclideanHeuristic(path,problem.goal),1)

    start = node(problem.getStartState(),'','')
    frontier.push(start,start.cost)

    while frontier.isEmpty() == False:
        path = frontier.pop()
        successors = problem.getSuccessors(path.path)
        explored.append(path)
        for vertex in successors:
            achou = False
            for path_ex in explored:
                if vertex[0] == path_ex.path:
                    achou = True

            if achou == False:
                successor = node(vertex[0],path.path,vertex[1])
                frontier.push(successor,successor.cost)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
hcl = hillClibing
