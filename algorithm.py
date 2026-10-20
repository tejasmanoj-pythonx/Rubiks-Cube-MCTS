import math # Used for square root and log functions in UCB1
import random # Used to pick random moves in the simulation

# All Phases
# Each phase has a list of tuples that are made from (index, colour) of each facelet
# These tuples are what the cube would look like if that phase was solved 
white_cross = [(19, 2), (23, 2), (25, 2), (21, 2), (1, 0), (10, 1), (37, 4), (46, 5)]
white_corners = [(18, 2), (0, 0), (36, 4), (20, 2), (2, 0), (38, 4), (26, 2), (9, 1), (45, 5), (24, 2), (11, 1), (47, 5)]
second_layer = [(3, 0), (5, 0), (12, 1), (14, 1), (39, 4), (41, 4), (48, 5), (50, 5)]
yellow_cross = [(28, 3), (30, 3), (32, 3), (34, 3)]
yellow_face = [(27, 3), (29, 3), (33, 3),  (35, 3)]
yellow_edges = [(7, 0), (16, 1), (43, 4), (52, 5)]
yellow_corners = [(6, 0), (8, 0), (15, 1), (17, 1), (42, 4), (44, 4), (51, 5), (53, 5), ]

# scoring() uses this to know the order of the phases
phases = [white_cross, white_corners, second_layer, yellow_cross, yellow_face, yellow_edges, yellow_corners]


# Facelets class is a representation of the cube and is used to keep track of the 54 facelets.
# It must be representated like this instead of the Cubie in render.py so that MCTS can make changes faster without having to change the cube.
# Speed is incredibly important as MCTS is using hundreds of thousands of moves while looking for a solution.
class Facelets:
    def __init__(self):

        # This is the solved cube state
        self.facelets = [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 5
        ]

    # Makes a 90 degree turn of one face
    # A turn rotates the 9 facelets on the face itself and the 12 facelets that surround that face.
    def rotate_facelets(self, face):
        # Make sure that we have a copy of the list to swap old values with new ones
        old_facelets = self.facelets.copy()

        # start is the values of the first facelet in a face that is being turned around
        # surrounding_facelets is the four strips of facelets that are on the surrounding faces
        # It is in order so that strip 0 goes to 1, 1 goes to 2 and so on
        if face == "right":
            start = 0
            surrounding_facelets = [
                [26, 23, 20],
                [45, 48, 51],
                [35, 32, 29],
                [44, 41, 38]
            ]
        elif face == "left":
            start = 9
            surrounding_facelets = [
                [18, 21, 24],
                [36, 39, 42],
                [27, 30, 33],
                [53, 50, 47]
            ]
        elif face == "up":
            start = 18
            surrounding_facelets = [
                [47, 46, 45],
                [2, 1, 0],
                [38, 37, 36],
                [11, 10, 9]
            ]
        elif face == "down":
            start = 27
            surrounding_facelets = [
                [42, 43, 44],
                [6, 7, 8],
                [51, 52, 53],
                [15, 16, 17]
            ]
        elif face == "front":
            start = 36
            surrounding_facelets = [
                [24, 25, 26],
                [0, 3, 6],
                [29, 28, 27],
                [17, 14, 11]
            ]
        elif face == "back":
            start = 45
            surrounding_facelets = [
                [20, 19, 18],
                [9, 12, 15],
                [33, 34, 35],
                [8, 5, 2]
            ]

        # Rotates the 9 facelets on the face by 90 degrees clockwise
        self.facelets[start] = old_facelets[start+6]
        self.facelets[start+1] = old_facelets[start+3]
        self.facelets[start+2] = old_facelets[start]

        self.facelets[start+3] = old_facelets[start+7]
        self.facelets[start+4] = old_facelets[start+4]
        self.facelets[start+5] = old_facelets[start+1]

        self.facelets[start+6] = old_facelets[start+8]
        self.facelets[start+7] = old_facelets[start+5]
        self.facelets[start+8] = old_facelets[start+2]

        # Turn the surrounding strips in a circle
        # Each strip is taking the values of the strip before it
        self.facelets[surrounding_facelets[0][0]] = old_facelets[surrounding_facelets[3][0]]
        self.facelets[surrounding_facelets[0][1]] = old_facelets[surrounding_facelets[3][1]]
        self.facelets[surrounding_facelets[0][2]] = old_facelets[surrounding_facelets[3][2]]

        self.facelets[surrounding_facelets[1][0]] = old_facelets[surrounding_facelets[0][0]]
        self.facelets[surrounding_facelets[1][1]] = old_facelets[surrounding_facelets[0][1]]
        self.facelets[surrounding_facelets[1][2]] = old_facelets[surrounding_facelets[0][2]]

        self.facelets[surrounding_facelets[2][0]] = old_facelets[surrounding_facelets[1][0]]
        self.facelets[surrounding_facelets[2][1]] = old_facelets[surrounding_facelets[1][1]]
        self.facelets[surrounding_facelets[2][2]] = old_facelets[surrounding_facelets[1][2]]

        self.facelets[surrounding_facelets[3][0]] = old_facelets[surrounding_facelets[2][0]]
        self.facelets[surrounding_facelets[3][1]] = old_facelets[surrounding_facelets[2][1]]
        self.facelets[surrounding_facelets[3][2]] = old_facelets[surrounding_facelets[2][2]]

    # 3 90 degree clockwise turns make up an anticlockwise turn
    # This is done so that I don't have to rewrite the above code in the opposite direction
    def apply_move(self, face, direction):
        if direction == 1:
            turn = 1
        else:
            turn = 3
        for i in range(turn):
            self.rotate_facelets(face)

# A node is one state of the cube in the MCTS tree
# It holds its state, the move that the parent made to get to it, the parent, its own children and values that help MCTS make decision
class Node:
    def __init__(self, facelets, move, parent):
        self.facelets = facelets # The cube state at this node
        self.move = move         # The move applied from the parent to get here
        self.parent = parent     # The node that this node was made from
        self.children = []       # Nodes that this node made

        self.visits = 0          # How many time this node has been visited in through backpropagation 
        self.score = 0           # Total of all the simulation scores that have gone through this node

        # These are all the options a node has to move in
        # Each turn is a tuple made from a face and a direction, 1 for clockwise and -1 for anticlockwise
        # First 12 turns are single turns in both directions
        # Last 8 turns are common algorithms like the righty and left algorithms to give MCTS a little bit of help
        self.moves = [
            (("right", 1),),
            (("right", -1),),
            (("left", 1),),
            (("left", -1),),
            (("up", 1),),
            (("up", -1),),
            (("down", 1),),
            (("down", -1),),
            (("front", 1),),
            (("front", -1),),
            (("back", 1),),
            (("back", -1),),

            (("right", 1), ("down", 1), ("right", -1), ("down", -1)),
            (("right", -1), ("down", -1), ("right", 1), ("down", 1)),
            (("left", 1), ("down", 1), ("left", -1), ("down", -1)),
            (("left", -1), ("down", -1), ("left", 1), ("down", 1)),
            (("front", 1), ("down", 1), ("front", -1), ("down", -1)),
            (("front", -1), ("down", -1), ("front", 1), ("down", 1)),
            (("back", 1), ("down", 1), ("back", -1), ("down", -1)),
            (("back", -1), ("down", -1), ("back", 1), ("down", 1))
        ]

        # Moves for a node that haven't been tested out yet
        # expand() uses this to choose unused moves
        self.not_tried_moves = self.moves.copy()

        # Single turns can be undone if they the opposite direction of the same turn is used immediately after
        # To prevent this we remove it
        if move != None and len(move) == 1:
            self.not_tried_moves.remove(((move[0][0], move[0][1] * -1),))


    def make_child(self, move):
        # Copies the facelets so that the child's state is seperate to the parent's
        facelet = Facelets()
        facelet.facelets = self.facelets.facelets.copy()

        # Apply each move
        # A single turn would only loop once and an algorithm would loop 4 times
        for turn in move:
            facelet.apply_move(turn[0], turn[1])
        child = Node(facelet, move, self)
        self.children.append(child)

        # Now that this moved has a child, we don't need to test it again
        self.not_tried_moves.remove(move)

        return child

# Monte Carlo Tree Search
# Keeps building a tree that uses random simulations to figure out what moves look the best
# Every iteration has 4 steps to it: selection, expansion, simulation and backpropagation
class MCTS:
    def __init__(self, facelets):
        # Instantiate a Facelets class but replace the facelets with the actual state passed from the main file
        starting_facelets = Facelets()
        starting_facelets.facelets = facelets.facelets.copy()

        # The starting node has no move or parent
        self.starting_node = Node(starting_facelets, None, None)

    # Starts from the root and keeps going downwards until it finds the best node with untried moves
    def selection(self):
        current_node = self.starting_node

        # Only keep moving down if every move from this node has been tested and has children that it can choose from
        while not current_node.not_tried_moves and current_node.children:

            # We don't know anything about the best child right now so we give them default stats
            # The value can never be a negative value which is why its set to -1 at the start
            current_best_child = None
            current_best_value = -1

            for child in current_node.children:

                # UCB1 formula decides which child is the most promising
                # First part is the exploitation that that takes the child's average score divided by the goal_score to give back a value between 0 and 1
                # The reason it needs to be between 0 and 1 is so that its balanced with the exploration part
                # The second is the exploration which also less visited children to be given a chance
                # 0.1 is a constant that has been tested and the results for that are in the learning journal
                ucb1 = ((child.score / child.visits) / self.goal_score)+ (0.1 * math.sqrt(math.log(current_node.visits) / child.visits))

                # If the score for the child is better than the current one than replace the information
                if ucb1 > current_best_value:
                    current_best_child = child
                    current_best_value = ucb1

            current_node = current_best_child

        return current_node

    # Adds one child to a node using the next untried move
    def expand(self, node):
        # Moves are done in the order they are in the list
        # If there are none left than there is nothing to expand
        if node.not_tried_moves:
            move = node.not_tried_moves[0]
        else:
            return

        # Make the new child with the move
        child = node.make_child(move)

        return child

    # Plays 10 random moves for a node and returns the best score that it saw along the way
    # Goal is the phase that it is currently being scored against
    def simulation(self, node, goal):
        facelets = Facelets()
        facelets.facelets = node.facelets.facelets.copy()

        # Grab the current score the state is already at as we don't want to go down from here
        best_current_score = self.scoring(facelets, goal)

        for i in range(10):
            # Only pick from the 12 single moves and the algorithms worsen the result and change the state too much
            number = random.randint(0, 11)
            move = node.moves[number]

            # Apply the single turn
            for turn in move:
                facelets.apply_move(turn[0], turn[1])

            # Keep the highest score we see along the way instead of just the score at the end
            # This is so that we are rewarding a node that is working towards a better state even if it starts to lose a lot later on
            score = self.scoring(facelets, goal)
            if score > best_current_score:
                best_current_score = score

        return best_current_score

    # Sends the score from the simulation back through all the parents
    def backpropagation(self, node, score):
        current_node = node

        # The starting node has a parent of None so it will stop then
        while current_node:
            current_node.visits += 1
            current_node.score += score

            current_node = current_node.parent

    # Gives a score based on how many facelets match the goal
    def scoring(self, facelets, goal):
        score = 0

        # This is done so that the algorithm is rewarded for not breaking the previous phases
        index = phases.index(goal)                                # Find the index of the current phase
        if index != 0:                                            # Check if we are at the white cross as it doesn't have any phases behind it
            phase_before = index - 1                              # Go to the phase before it
            score += self.scoring(facelets, phases[phase_before]) # Repeat the loop by recursively scoring until it reaches the white cross

        # Reward 1 point for every matching facelet
        for index, colour in goal:
            if facelets.facelets[index] == colour:
                score += 1

        return score

    # Combines the four MCTS steps for every iteration
    # move_amount is the most amount of times it will try to commit before giving up
    def main(self, goal, goal_score, iterations, move_amount):
        moves = []
        self.goal_score = goal_score

        # Each loop is searching for the an iteration amount of times and then it will commit one move and then that node will become the new root
        for i in range(move_amount):

            # Check how close we are to the goal
            # Once the cube reaches the goal we can break out as no more moves would be needed
            score = self.scoring(self.starting_node.facelets, goal)
            if score == goal_score:
                break

            # Stores the best node that is found during the search
            # This is the minimum we want to beat so that we are only improving
            best_node = None
            best_node_score = score

            # Set a budget so that we don't go for too long    
            for i in range(iterations):

                # Follow the four main steps of MCTS
                node = self.selection()
                node = self.expand(node)
                score = self.simulation(node, goal)
                self.backpropagation(node, score)

                # Check how well that node did compared to the goal
                # Replace it if it is the best we have seen so far
                node_score = self.scoring(node.facelets, goal)
                if node_score > best_node_score:
                    best_node = node
                    best_node_score = node_score

            # If we did find a node with a better score then store the moves that it takes to go from the current root to that node
            if best_node is not None:
                path = []
                current_node = best_node

                # Keep following the branches of parent until we reach the root
                while current_node.parent is not None:
                    path.append(current_node.move)
                    current_node = current_node.parent

                # Since we went from the bottom to the top, the actual path is in reverse
                # Add this path into our move list
                path.reverse()
                for move in path:
                    moves += move

                # Remove that link from the best to its old parent
                # This is so that the best node is now the new root
                best_node.parent = None
                self.starting_node = best_node

            # If we never found anything better then instead find the child that was visted the most
            else:
                current_best_child = None
                most_visits = -1

                # Replace the child if it has more visits that what we have currently seen
                for child in self.starting_node.children:
                    if child.visits > most_visits:
                        current_best_child = child
                        most_visits = child.visits

                # Add their move to our list
                moves += current_best_child.move

                # Make this child the new root and remove their parent
                current_best_child.parent = None
                self.starting_node = current_best_child
        return moves