import pygame      # Used for creating the window and event handling.
import render      # Used for importing the Renderer class and rotation matrix functions.
import algorithm
import numpy as np # Used for combining matrices with matrix dot product.
import time

# Main class handles the pygame window, the game loop, and all the event handling. 
class Main:
    def __init__(self):
        pygame.init()                                          # Initialise the pygame modules
        self.screen = pygame.display.set_mode((800, 600))      # Sets the width and height of the pygame window
        pygame.display.set_caption("Rubik's Cube Pathfinding") # Sets the title of the pygame window
        self.clock = pygame.time.Clock()                       # Used to control the frame rate of the window
        self.running = False                                   # Used to start and stop the pygame window
        self.renderer = render.Renderer(self.screen)           # Initialise the Renderer class from render.py and pass in self.screen so it can draw directly onto the pygame surface.

        # Used for the mouse drag state. 
        # self.drag becomes true when the left mouse button is pressed and false when it is released.
        # mouse_position stores where the mouse was on the previous frame so that we can calculate how far it moved on each MOUSEMOTION event.
        self.drag = False
        self.mouse_position = (0, 0)

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Checks if the user clicks the window's close button.
                    self.running = False      # Setting running to false to exit the while loop and into the pygame.quit().
    
                elif event.type == pygame.KEYDOWN: # Check for any keypress.
                    # Only allow these key presses if there is nothing being animated.
                    # If it was allowed the cubies would move around into each other overlapping and deform the cube.
                    # The start_animating_face() method takes in what face to be animated and the incremental angle for each frame.
                    # The incremental angle is the amount all the cubies are being moved in the direction of the rotation.
                    # A greater angle means each frame the distance moved is further giving the effect that it is moving faster.
                    # This is why scramble() method uses an angle of 9 instead of 3 so that the 10 consecutive moves finish faster.
                    if self.renderer.animating == False: 
                        if event.key == pygame.K_r or event.key == pygame.K_1:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("right", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("right", 3, "clockwise")
                        elif event.key == pygame.K_l or event.key == pygame.K_2:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("left", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("left", 3, "clockwise")
                        elif event.key == pygame.K_u or event.key == pygame.K_3:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("up", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("up", 3, "clockwise")
                        elif event.key == pygame.K_d or event.key == pygame.K_4:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("down", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("down", 3, "clockwise")
                        elif event.key == pygame.K_f or event.key == pygame.K_5:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("front", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("front", 3, "clockwise")
                        elif event.key == pygame.K_b or event.key == pygame.K_6:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.renderer.start_animating_face("back", 3, "anticlockwise")
                            else:
                                self.renderer.start_animating_face("back", 3, "clockwise")

                        # Clears out the statistics on the screen and scrambles the cube
                        elif event.key == pygame.K_s:
                            self.renderer.scramble()
                            self.renderer.stat = []

                        # Pressing space is used to solve the cube
                        elif event.key == pygame.K_SPACE:
                            if not self.renderer.choices:
                                # First clear out the statistics, indicate that the cube is solcing and record the time
                                self.renderer.stat = []
                                self.renderer.stat.append("Solving...")
                                self.renderer.draw_cube()
                                start_time = time.perf_counter()

                                # Makes an instance of MCTS passing in the current state of the cube
                                # An iteration budget and move_amount are set here to cap each phase
                                # There are different values for each of these depending if they are more difficult or not to reach
                                # Statistics about the amount of moves and time taken to solve for that phase are also shown onto the screen.
                                mcts = algorithm.MCTS(self.renderer.facelets)
                                cross_moves = mcts.main(algorithm.white_cross, 8, 3000, 20)
                                white_cross_time = time.perf_counter()
                                time_taken = white_cross_time - start_time
                                self.renderer.stat.append("White Cross took " + str(round(time_taken, 3)) + "s and " + str(len(cross_moves)) + " moves")
                                self.renderer.draw_cube()

                                mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                corner_moves  = mcts.main(algorithm.white_corners, 20, 4000, 40)
                                white_corner_time = time.perf_counter()
                                time_taken = white_corner_time - white_cross_time
                                self.renderer.stat.append("White Corner took " + str(round(time_taken, 3)) + "s and " + str(len(corner_moves)) + " moves")
                                self.renderer.draw_cube()

                                mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                second_layer_moves  = mcts.main(algorithm.second_layer, 28, 4000, 60)
                                second_layer_time = time.perf_counter()
                                time_taken = second_layer_time - white_corner_time
                                self.renderer.stat.append("Second Layer took " + str(round(time_taken, 3)) + "s and " + str(len(second_layer_moves)) + " moves")
                                self.renderer.draw_cube()

                                mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                yellow_cross_moves  = mcts.main(algorithm.yellow_cross, 32, 4000, 60)
                                yellow_cross_time = time.perf_counter()
                                time_taken = yellow_cross_time - second_layer_time
                                self.renderer.stat.append("Yellow Cross took " + str(round(time_taken, 3)) + "s and " + str(len(yellow_cross_moves)) + " moves")
                                self.renderer.draw_cube()

                                # These phases currently don't work currently
                                # This is because the specific sequence of moves needed like the Sune algorithm are way too long
                                # Meaning that the chance MCTS finds this sequences is incredibily low
                                # mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                # yellow_face_moves  = mcts.main(algorithm.yellow_face, 36, 4000, 60)
                                # mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                # yellow_edges_moves  = mcts.main(algorithm.yellow_edges, 40, 4000, 60)
                                # mcts = algorithm.MCTS(mcts.starting_node.facelets)
                                # yellow_corners_moves  = mcts.main(algorithm.yellow_corners, 48, 4000, 60)

                                moves = cross_moves + corner_moves + second_layer_moves + yellow_cross_moves #+ yellow_face_moves + yellow_edges_moves + yellow_corners_moves
                                self.renderer.stat.append("Total moves: " + str(len(moves)))
                                for move in moves:
                                    if move[1] == 1:
                                        self.renderer.choices.append((move[0], "clockwise"))
                                    else:
                                        self.renderer.choices.append((move[0], "anticlockwise"))
                                

                # Handles the cube rotation using mouse drag.
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    # Check if either the left or right mouse button is pressed down.
                    # Change the drag state to True and record the current mouse position as the starting point.
                    # Used for the MOUSEMOTION event as a reference to compare positions and find the distance in mouse movements.
                    self.drag = True
                    self.mouse_position = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Check if either the left or right mouse button is pressed up.
                    # Change the drag state to false so that it stops rotating the cube.
                    self.drag = False
                elif event.type == pygame.MOUSEMOTION:
                    # Only rotate the cube if the user is actively dragging.
                    if self.drag:
                        # Get the current x and y position of the mouse
                        x_current = pygame.mouse.get_pos()[0]
                        y_current = pygame.mouse.get_pos()[1]

                        # Find the difference between the current x and y from the starting x and y.
                        # x_difference is the horizontal distance so a positive x moves rightwards and vice versa.
                        # y_difference is the vertical distance but due to pygame's positive y value moving downwards, the vertical movement is inverted.
                        x_difference = x_current - self.mouse_position[0]
                        y_difference = y_current - self.mouse_position[1]

                        # Convert the differences in x and y into rotation angles.
                        # 0.005 is the sensitivity that scales everything down to smaller angle.
                        # y_difference controls the rotation of the x axis as rotating upon it moves it up and down.
                        # x_difference controls the rotation of the y axis as rotating upon it moves it left and right.
                        x_angle = 0.005 * y_difference
                        y_angle = 0.005 * x_difference

                        # Make 2 rotation matrices that account for the rotation from the mouse differences.
                        # Combine these two rotation matrices into one so that it can be directly multiplied in one go.
                        x_rotated = render.rotate_x(x_angle)
                        y_rotated = render.rotate_y(y_angle)
                        combined = np.dot(x_rotated, y_rotated)

                        # Multiply the combined rotation matrices into the render's already accumulated rotation.
                        self.renderer.rotation = np.dot(combined, self.renderer.rotation)
                        
                        # Make this mouse position the new starting point for the next iteration.
                        self.mouse_position = pygame.mouse.get_pos()

             # Sets the frame rate of the window to 60 frames per second.
            self.clock.tick(60)

            # Clears the screen, draws all the visible faces in order of their depth and then updates the display.
            # It's called every frame regardless if anything needs to be animated or not. 
            self.renderer.draw_cube() 
        pygame.quit()

# Only run when this specific file is the main program.
# Instantiate the Main class and call the run() method.
if __name__ == "__main__":
    main = Main()
    main.run()