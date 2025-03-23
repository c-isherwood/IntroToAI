import subprocess

# Direction helpers
MOVE_DELTAS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
INDEX_TO_DIR = {0: "up", 2: "right", 4: "down", 6: "left"}
REVERSE_MOVE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

def send_command_and_read_result(command):
    subprocess.run(["python3", "simulator.py", command], check=True)
    with open("state_vector.txt", "r") as f:
        return f.read().strip().split(',')

def get_valid_moves(state_vector):
    return [INDEX_TO_DIR[i] for i in INDEX_TO_DIR if state_vector[i] == '0']

def dfs_agent():
    visited = set()
    current_pos = (0, 0)
    visited.add(current_pos)
    path_stack = []   # Tracks path history for backtracking

    # Initial state read
    state_vector = send_command_and_read_result("")

    while True:
        if state_vector[0] == "goal":
            print(f"Goal reached in {state_vector[1]} steps!")
            return

        valid_moves = get_valid_moves(state_vector)
        moved = False

        for move in valid_moves:
            # Determine new position if we move in this direction
            dx, dy = MOVE_DELTAS[move]
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if next_pos not in visited:
                # Try the move
                state_vector = send_command_and_read_result(move)

                # Confirm if we reached the goal
                if state_vector[0] == "goal":
                    print(f"Goal reached in {state_vector[1]} steps!")
                    return

                visited.add(next_pos)
                path_stack.append(REVERSE_MOVE[move])
                current_pos = next_pos
                moved = True
                break

        if not moved:
            if not path_stack:
                print("No more paths to backtrack. Goal not found.")
                return
            # Backtrack
            back = path_stack.pop()
            dx, dy = MOVE_DELTAS[back]
            current_pos = (current_pos[0] + dx, current_pos[1] + dy)
            state_vector = send_command_and_read_result(back)

# Run the agent
if __name__ == "__main__":
    dfs_agent()
