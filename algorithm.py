import math
import random

white_cross = [(19, 2), (23, 2), (25, 2), (21, 2), (1, 0), (10, 1), (37, 4), (46, 5)]
white_corners = [(18, 2), (0, 0), (36, 4), (20, 2), (2, 0), (38, 4), (26, 2), (9, 1), (45, 5), (24, 2), (11, 1), (47, 5)]
second_layer = [(3, 0), (5, 0), (12, 1), (14, 1), (39, 4), (41, 4), (48, 5), (50, 5)]
yellow_cross = [(28, 3), (30, 3), (32, 3), (34, 3)]
yellow_face = [(27, 3), (29, 3), (33, 3),  (35, 3)]
yellow_edges = [(7, 0), (16, 1), (43, 4), (52, 5)]
yellow_corners = [(6, 0), (8, 0), (15, 1), (17, 1), (42, 4), (44, 4), (51, 5), (53, 5), ]

phases = [white_cross, white_corners, second_layer, yellow_cross, yellow_face, yellow_edges, yellow_corners]

class Facelets:
    def __init__(self):
        self.facelets = [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 5
        ]

    def rotate_facelets(self, face):
        old_facelets = self.facelets.copy()

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

        self.facelets[start] = old_facelets[start+6]
        self.facelets[start+1] = old_facelets[start+3]
        self.facelets[start+2] = old_facelets[start]

        self.facelets[start+3] = old_facelets[start+7]
        self.facelets[start+4] = old_facelets[start+4]
        self.facelets[start+5] = old_facelets[start+1]

        self.facelets[start+6] = old_facelets[start+8]
        self.facelets[start+7] = old_facelets[start+5]
        self.facelets[start+8] = old_facelets[start+2]

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

    def apply_move(self, face, direction):
        if direction == 1:
            turn = 1
        else:
            turn = 3
        for i in range(turn):
            self.rotate_facelets(face)

class Node:
    def __init__(self, facelets, move, parent):
        self.facelets = facelets
        self.move = move
        self.parent = parent
        self.children = []

        self.visits = 0
        self.score = 0

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

        self.not_tried_moves = self.moves.copy()

        if move != None and len(move) == 1:
            self.not_tried_moves.remove(((move[0][0], move[0][1] * -1),))


    def make_child(self, move):
        facelet = Facelets()
        facelet.facelets = self.facelets.facelets.copy()

        for turn in move:
            facelet.apply_move(turn[0], turn[1])
        child = Node(facelet, move, self)
        self.children.append(child)
        self.not_tried_moves.remove(move)

        return child

class MCTS:
    def __init__(self, facelets):
        starting_facelets = Facelets()
        starting_facelets.facelets = facelets.facelets.copy()
        self.starting_node = Node(starting_facelets, None, None)

    def selection(self):
        current_node = self.starting_node

        while not current_node.not_tried_moves and current_node.children:
            current_best_child = None
            current_best_value = -1

            for child in current_node.children:

                ucb1 = ((child.score / child.visits) / self.goal_score)+ (0.25 * math.sqrt(math.log(current_node.visits) / child.visits))

                if ucb1 > current_best_value:
                    current_best_child = child
                    current_best_value = ucb1

            current_node = current_best_child

        return current_node

    def expand(self, node):
        if node.not_tried_moves:
            move = node.not_tried_moves[0]
        else:
            return

        child = node.make_child(move)

        return child

    def simulation(self, node, goal):
        facelets = Facelets()
        facelets.facelets = node.facelets.facelets.copy()

        best_current_score = self.scoring(facelets, goal)

        for i in range(10):
            number = random.randint(0, 11)
            move = node.moves[number]

            for turn in move:
                facelets.apply_move(turn[0], turn[1])

            score = self.scoring(facelets, goal)

            if score > best_current_score:
                best_current_score = score

        return best_current_score

    def backpropagation(self, node, score):
        current_node = node

        while current_node:
            current_node.visits += 1
            current_node.score += score

            current_node = current_node.parent

    def scoring(self, facelets, goal):
        score = 0

        index = phases.index(goal)
        if index != 0:
            phase_before = index - 1
            score += self.scoring(facelets, phases[phase_before])

        for index, colour in goal:
            if facelets.facelets[index] == colour:
                score += 1

        return score

    def main(self, goal, goal_score, iterations, move_amount):
        moves = []
        self.goal_score = goal_score

        for i in range(move_amount):

            score = self.scoring(self.starting_node.facelets, goal)

            if score == goal_score:
                break

            best_node = None
            best_node_score = score
                
            for i in range(iterations):
                
                node = self.selection()
                node = self.expand(node)
                score = self.simulation(node, goal)
                self.backpropagation(node, score)

                node_score = self.scoring(node.facelets, goal)
                if node_score > best_node_score:
                    best_node = node
                    best_node_score = node_score

            if best_node is not None:
                path = []
                current_node = best_node

                while current_node.parent is not None:
                    path.append(current_node.move)
                    current_node = current_node.parent

                path.reverse()
                for move in path:
                    moves += move

                print(len(moves), best_node_score)

                best_node.parent = None
                self.starting_node = best_node

            else:
                current_best_child = None
                most_visits = -1

                for child in self.starting_node.children:
                    if child.visits > most_visits:
                        current_best_child = child
                        most_visits = child.visits

                moves += current_best_child.move
                print(len(moves), self.scoring(current_best_child.facelets, goal))

                current_best_child.parent = None
                self.starting_node = current_best_child
        print(phases.index(goal))
        return moves