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

# Trabalho de Fundamentos de inteligencia artificial
# Agentes de busca implementados
# Author: Felipe Lopes
# Date: 2019
#

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

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Busca em Profundidade
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
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action

    start = node(problem.getStartState(),'','')
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
                successor = node(vertex[0],path.path,vertex[1])
                frontier.push(successor)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

# Busca em Largura
def breadthFirstSearch(problem):
    from util import Queue

    frontier = Queue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action

    start = node(problem.getStartState(),'','')
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
                successor = node(vertex[0],path.path,vertex[1])
                frontier.push(successor)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

# Busca por custo uniforme
def uniformCostSearch(problem):
    from util import PriorityQueue
    import math

    frontier = PriorityQueue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, cost, action):
            self.path = path
            self.dad = dad
            self.action = action
            if dad == None:
                self.cost = cost
            else:
                self.cost = dad.cost + cost

    start = node(problem.getStartState(),None,0,'')
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
                successor = node(vertex[0],path,vertex[2],vertex[1])
                frontier.push(successor,successor.cost)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad.path:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

# Busca em A estrela
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    import math

    frontier = PriorityQueue()
    explored = []
    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            h = heuristic(path,problem.goal)
            if dad == None:
                self.g=0
            else:
                self.g = dad.g + heuristic(dad.path,path)
            self.cost = round(self.g + h,1)

    start = node(problem.getStartState(),None,'')
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
                successor = node(vertex[0],path,vertex[1])
                frontier.push(successor,successor.cost)
                if problem.isGoalState(successor.path):
                    while len(explored) > 0:
                        ant = explored.pop()
                        if ant.path == successor.dad.path:
                            actions.append(successor.action)
                            successor = ant
                    actions.reverse()
                    return actions

# Busca de subida de encosta
def hillClibingSearch(problem):
    from searchAgents import manhattanHeuristic

    actions = []

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            self.cost = manhattanHeuristic(path,problem.goal)

    current = node(problem.getStartState(),'','')
    antecessors = None
    smallneighbor = current
    while True:
        successors = problem.getSuccessors(current.path)
        for vertex in successors:
            successor = node(vertex[0], current.path, vertex[1])
            if successor.cost < smallneighbor.cost:
                smallneighbor = successor

        if smallneighbor.cost < current.cost:
            current = menor
            actions.append(current.action)
            if problem.isGoalState(current.path):
                return actions

        if antecessors == successors:
            print "Ficou preso em um maximo local!!!"
            return actions

        antecessors = successors

# Busca por tempera simulada
def simulatedAnnealingSearch(problem):
    from searchAgents import manhattanHeuristic
    import math
    import random

    class node:
        def __init__(self, path, dad, action):
            self.path = path
            self.dad = dad
            self.action = action
            self.cost = manhattanHeuristic(path,problem.goal)

    actions = []
    current = node(problem.getStartState(),'','')
    t = 1.0
    alfa = 1.5

    while True:

        successors = problem.getSuccessors(current.path)
        randomvalue = random.randint(0,len(successors)-1)
        successor = node(successors[randomvalue][0], current.path, successors[randomvalue][1])
        e = successor.cost - current.cost
        probability = math.exp(e/t)

        if e > 0:
            current = successor
            actions.append(current.action)
        else:
             if e < probability:
               current = successor
               actions.append(current.action)

        if problem.isGoalState(current.path):
            return actions

        t = t * alfa

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
hcl = hillClibingSearch
tps = simulatedAnnealingSearch
