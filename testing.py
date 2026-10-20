# This file is just a testing file used for the data provided in the Learning Journal

import algorithm
import time

moves = [
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

for trial in range(5):
    facelets = algorithm.Facelets()

    for i in range(30):
        face = algorithm.random.choice(moves)
        facelets.apply_move(face[0], face[1])

    start_time = time.perf_counter()

    mcts = algorithm.MCTS(facelets)
    cross_moves = mcts.main(algorithm.white_cross, 8, 3000, 20)

    mcts = algorithm.MCTS(mcts.starting_node.facelets)
    corner_moves  = mcts.main(algorithm.white_corners, 20, 4000, 40)

    mcts = algorithm.MCTS(mcts.starting_node.facelets)
    second_layer_moves  = mcts.main(algorithm.second_layer, 28, 4000, 60)

    mcts = algorithm.MCTS(mcts.starting_node.facelets)
    yellow_cross_moves  = mcts.main(algorithm.yellow_cross, 32, 4000, 60)

    end_time = time.perf_counter()

    total_time = round(end_time - start_time, 3)
    total_moves = len(cross_moves) + len(corner_moves) + len(second_layer_moves) + len(yellow_cross_moves)

    score = mcts.scoring(mcts.starting_node.facelets, algorithm.yellow_cross)

    if score == 32:
        result = "solved"
    else:
        result = "not solved"

    print("trial " + str(trial+1) + " moves " + str(total_moves) + " time " + str(total_time) + " result " + result)