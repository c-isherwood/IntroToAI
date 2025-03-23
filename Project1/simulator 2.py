#!/bin/python3

import sys
import argparse
import os

class MazeEnvironment:
    def __init__(self, filename="maze.txt", position_file=".currpos"):
        self.filename = filename
        self.position_file = position_file
        self.load_maze()
        self.load_position_and_steps()
    def load_maze(self):
        self.maze = []
        with open(self.filename, "r") as f:
            for r, line in enumerate(f):
                row = []
                for c, char in enumerate(line.strip().split(',')):
                    if char == 'I':
                        self.initial_position = (r, c)
                        self.position = self.initial_position
                        row.append(0)  # Treat 'I' as open space (0)
                    elif char == 'G':
                        self.goal = (r, c)
                        row.append(0)  # Treat 'G' as open space (0)
                    else:
                        row.append(int(char))
                self.maze.append(row)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
    def load_position_and_steps(self):
        if os.path.exists(self.position_file):
            with open(self.position_file, "r") as f:
                data = f.read().strip().split(',')
                self.position = (int(data[0]), int(data[1]))
                self.steps = int(data[2]) if len(data) > 2 and data[2].isdigit() else 0
        else:
            self.reset_position_and_steps()
    def reset_position_and_steps(self):
        self.position = self.initial_position
        self.steps = 0
        sv = self.get_state_vector()
        self.write_state_vector(sv)
        self.save_position_and_steps()
    def save_position_and_steps(self):
        with open(self.position_file, "w") as f:
            f.write(f"{self.position[0]},{self.position[1]},{self.steps}\n")
    def display_cheat(self):
        for r in range(self.rows):
            row = " "
            for c in range(self.cols):
                if (r, c) == self.position:
                    if self.position == self.initial_position:
                        row += "A"
                    elif self.position == self.goal:
                        row += "G"
                    else:
                        row += "A"
                elif self.maze[r][c] == 1:
                    row += "X"
                else:
                    row += " "
            print(row)
        print()
    def write_state_vector(self,state_vector,filename="state_vector.txt"):
        with open(filename, "w") as file:
            if isinstance(state_vector, tuple) and state_vector[0] == "goal":
                file.write(f"goal,{state_vector[1]}\n")
            else:
                file.write(",".join(map(str, state_vector)) + "\n")
    def get_state_vector(self):
        r, c = self.position
        # Define the directions to correspond to top, topright, right, bottomright, bottom, bottomleft, left, topleft
        directions = [
            (-1, 0),    # Top
            (-1, 1),    # Topright
            (0, 1),     # Right
            (1, 1),     # Bottom right
            (1, 0),     # Bottom
            (1, -1),    # Bottom left
            (0, -1),    # Left
            (-1, -1)    # Topleft
        ]
        return [1 if (0 <= r+dr < self.rows and 0 <= c+dc < self.cols and self.maze[r+dr][c+dc] == 1) else 0 for dr, dc in directions]
    def move(self, action):
        if action not in ["up", "down", "left", "right", ""]:
            return "Invalid action"
        new_pos = self.position
        if action == "up":
            new_pos = (self.position[0] - 1, self.position[1])
        elif action == "down":
            new_pos = (self.position[0] + 1, self.position[1])
        elif action == "left":
            new_pos = (self.position[0], self.position[1] - 1)
        elif action == "right":
            new_pos = (self.position[0], self.position[1] + 1)
        elif action == "":
            self.reset_position_and_steps()
            return self.get_state_vector()
        if self.is_move_valid(new_pos):
            self.position = new_pos
            self.steps += 1
            self.save_position_and_steps()
        if self.position == self.goal:
            return "goal", self.steps
        return self.get_state_vector()
    def display_maze(self):
        r, c = self.position
        border_row = "?" * 5  # Because the core area is 3x3, the border will be 5 characters wide
        print(border_row)  # Top border
        for dr in [-1, 0, 1]:  # Row offset
            row = "?"
            for dc in [-1, 0, 1]:  # Column offset
                if dr == 0 and dc == 0:
                    if self.position == self.initial_position:
                        row += "I"
                    elif self.position == self.goal:
                        row += "G"
                    else:
                        row += "A"
                else:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.maze[nr][nc] == 1:
                            row += "X"
                        else:
                            row += " "
                    else:
                        row += " "
            row += "?"
            print(row)
        print(border_row)  # Top border
        print()
    def is_move_valid(self, position):
        r, c = position
        return 0 <= r < self.rows and 0 <= c < self.cols and self.maze[r][c] == 0

def main():
    parser = argparse.ArgumentParser(description="Maze Environment Command Line Interface")
    parser.add_argument("action", nargs='?', default="", help="Action to perform (up, down, left, right)")
    parser.add_argument("--cheat", action="store_true", help="Display the entire maze with the agent's current position")
    args = parser.parse_args()
    
    env = MazeEnvironment("maze.txt")
    state_vector = env.move(args.action)
    env.write_state_vector(state_vector)
    
    if args.cheat:
        env.display_cheat()
    else:
        env.display_maze()
    if isinstance(state_vector, tuple) and state_vector[0] == "goal":
        print("Congratulations! You have reached the goal in", state_vector[1], "steps!")
    else:
        print("State vector:", state_vector," steps:",env.steps)
if __name__ == "__main__":
    main()
