white_cross = [(19, 2), (23, 2), (25, 2), (21, 2), (1, 0), (10, 1), (37, 4), (46, 5)]
white_corners = [(18, 2), (20, 2), (26, 2), (24, 2), (0, 0), (2, 0), (9, 1), (11, 1), (36, 4), (38, 4), (45, 5), (47, 5)]
second_layer = [(3, 0), (5, 0), (12, 1), (14, 1), (39, 4), (41, 4), (48, 5), (50, 5)]
everything_else = [(6, 0), (7, 0), (8, 0), (15, 1), (16, 1), (17, 1), (42, 4), (43, 4), (44, 4), (51, 5), (52, 5), (53, 5), (27, 3), (28, 3), (29, 3), (30, 3), (32, 3), (33, 3), (34, 3), (35, 3)]

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

        self.not_tried_moves = [
            ("right", 1),
            ("right", -1),
            ("left", 1),
            ("left", -1),
            ("up", 1),
            ("up", -1),
            ("down", 1),
            ("down", -1),
            ("front", 1),
            ("front", -1),
            ("back", 1),
            ("back", -1)
        ]

    def make_child(self, move):
        facelet = Facelets()
        facelet.facelets = self.facelets.facelets.copy()

        facelet.apply_move(move[0], move[1])
        child = Node(facelet, move, self)
        self.children.append(child)
        self.not_tried_moves.remove(move)

        return child
