## sources
## https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
## https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
## https://www.baeldung.com/java-monte-carlo-tree-search

try:
    import BasicPlayers
except ModuleNotFoundError:
    import DotsAndBoxes.BasicPlayers as BasicPlayers
import time
import random
import math

class MonteCarloPlayer(BasicPlayers.RandomPlayer):
    def __init__(self, playerIndex, colour="red", timeLimit=2, c=1.4142):
        """
        Override for Monte Carlo Player.
        Args:
            playerIndex(int): player index in game
            colour(str): Colour for the UI to render. Defaults to Red
            timeLimit(int/float): Time limit in seconds for moves
        """
        self.index = playerIndex
        self.colour = colour
        self.timeLimit = timeLimit
        self.c = c

    def chooseMove(self, game):
        """
        Monte Carlo choose move
        """
        move = self.monteCarlo(game)
        if game.is_legal_move(move):
            return move
        else:
            return self.randomMove(game)

        # main function for the Monte Carlo Tree Search
    def monteCarlo(self, game):
        """
        Main function for monte carlo tree search. Sets up the tree search and
        then loops until time is up, randomly playing games.
        Args:
            game(Game): Game state to made move for.
        Retuns:
            move
        """
        root = MonteCarloNode(self.index, game, (0,0,0), "Root", self.c)
        root.makeChildren()
        current = root.chooseChild()
        #print("Starting Monte Carlo Method.")
        no_trials = 0
        startTime = time.time()
        timeTaken = time.time() - startTime
        # While we haven't exceeded the time limit
        """
        while timeTaken <= self.timeLimit:
            if current.game.is_finished() or current.n == 0:
                # the rollout method also handles the backpropagation step.
                current.rollout()
                # after rollout reset to root.
                current = root
                no_trials += 1
                # recalculating here saves a little bit of time.
                timeTaken = time.time() - startTime
            # the next node is the best child of the current node.
            current = current.chooseChild()
            # that's it that's the algorithm
        """
        while time.time() - startTime <= self.timeLimit:
            if current.children:
                current = current.chooseChild()
            else:
                current.rollout()
                current.makeChildren()
                current = root
            no_trials += 1


        bestChild = root.chooseChild()
        bestMove = root.chooseChild().move
        #print("Child chosen. {} trials performed".format(no_trials))
        #root.print_node()
        #print("Chosen move {}".format(bestMove))
        #print("Monte Carlo returning move {}".format(bestMove))
        return bestMove

    def __str__(self):
        return "{}_monty".format(self.index)

class MonteCarloNode:
    def __init__(self, playerIndex, game, move, name, c=1.4142, parent=None):
        """
        Initialise a node for the Monte Carlo Tree search with a gamestate, the
        move made to reach this game state and its parent node.
        Args:
            playerIndex: Index that the Monte Carlo player has
            game(Game): Gamestate this node represents
            move(3-Tuple[int]): Move made to get to this node
            name(str): debug parameter
            c(float): exploration parameter.
            parent(MonteCarloNode): Parent of this node. None for root node.
        """
        self.playerIndex = playerIndex
        self.parent = parent
        self.move = move
        self.game = game
        self.name = name
        self.t = 0.0
        self.n = 0.0
        # c is the exploration coefficient - how likely the player is to explore new paths.
        # sqrt(2) ~~ 1.4142
        self.c = c
        self.children = []

    def chooseChild(self):
        """
        Choose the best child node based on UCB values.
        """
        if not self.children:
            self.makeChildren()
        bestValue = 0
        # This picks the first node by default
        bestNode = self.children[0]
        for node in self.children:
            ucb = node.ucb()
            if ucb > bestValue:
                bestValue = ucb
                bestNode = node

        return bestNode

    def ucb(self):
        """
        Calculate Upper Confidence Bound for node.
        To calculate UCB, an exploitation and exploration parameter are calculated
        exploitation is the average win rate at this node
        exploration is a factor of how many times this node has already been chosen
        c is the exploration coefficient. Altering this value will change the rate of
        exploration.
        Returns:
            float: Upper Confidence Bound for node.
        """
        if self.n == 0:
            return 1000000
        if self.parent is None:
            return -1
        exploitation = self.t/self.n
        exploration =  self.c*math.sqrt(math.log(self.parent.n)/self.n)
        return exploitation + exploration

    def makeChildren(self):
        """
        Create child nodes for this node. Each move that can be made will spawn
        a new child node.
        """
        moves = self.game.get_all_legal_moves()
        for i, m in enumerate(moves):
            newName = self.name+"-"+str(i)
            # Make new node with player index, new game state, move made, new name and parent.
            self.children.append(MonteCarloNode(self.playerIndex, self.makeMove(m), m, newName, self.c, self))
        #self.children = [MonteCarloNode(self.playerIndex, self.makeMove(m), m, self) for m in moves]

    def rollout(self):
        """
        Rollout will take the state and play random moves until the game is finished.
        The end state will then be evaluated and backpropagated.
        """
        copyGame = self.game.get_copy()
        moves = copyGame.get_all_legal_moves()
        random.shuffle(moves)
        for move in moves:
            copyGame.take_turn(move)
        if copyGame.winner() == self.playerIndex:
            eval = 10
        else:
            eval = 0
        # we then call our own backpropagate method to send the values up the tree
        self.backpropagate(eval)

    def backpropagate(self, eval):
        """
        Backpropagate method to send values all the way back to the root of the tree.
        Also recalculate ucb for each node on the way.
        """
        self.n += 1
        self.t += eval
        if self.parent is not None:
            self.parent.backpropagate(eval)

    def makeMove(self, move):
        """
        Takes a move, copies self.game and makes the move in the copy.
        Args:
            move(Tuple[int]): Move to make
        Returns:
            Game: Deep copy of self.game with move made
        """
        copyGame = self.game.get_copy()
        copyGame.take_turn(move)
        return copyGame

    def print_node(self):
        """
        Prints the node and all of its children.
        """
        print("Node {} - Move {} - Score {}".format(self.name, self.move, self.ucb()))
        #self.game.print_grid()
        for child in self.children:
            print("  Child {} - Move {} - Score {}".format(child.name, child.move, child.ucb()))

    def __str__(self):
        returnStr = "Node {} - Move {} - Score {} - visits {} - wr {}\n".format(self.name, self.move, self.ucb(), self.n, self.t)
        if self.children:
            childStr = ""
            for child in self.children:
                childStr += "  Child {} - Move {} - Score {} - visits {} - wr {}\n".format(child.name, child.move, child.ucb(), child.n, child.t)
        else:
            childStr = "  Node has no children.\n"
        return returnStr + childStr
