import subprocess
from collections import deque

# Direction helpers
MOVE_DELTAS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
INDEX_TO_DIR = {0: "up", 2: "right", 4: "down", 6: "left"}

def send_command_and_read_result(command):
    subprocess.run(["python3", "simulator.py", command], check=True)
    with open("state_vector.txt", "r") as f:
        return f.read().strip().split(',')

def get_valid_moves(state_vector):
    return [INDEX_TO_DIR[i] for i in INDEX_TO_DIR if state_vector[i] == '0']

def bfs_agent():
    # Reset maze to initial position
    send_command_and_read_result("")

    visited = set()
    queue = deque()
    
    start_pos = (0, 0)
    queue.append((start_pos, []))  # position, path so far
    visited.add(start_pos)

    while queue:
        pos, path = queue.popleft()

        # Replay path to reach this position
        send_command_and_read_result("")  # reset
        for move in path:
            result = send_command_and_read_result(move)
            if result[0] == "goal":
                print(f"Goal reached in {result[1]} steps!")
                return

        # Check if already at goal
        state_vector = send_command_and_read_result(path[-1] if path else "")
        if state_vector[0] == "goal":
            print(f"Goal reached in {state_vector[1]} steps!")
            return

        for move in get_valid_moves(state_vector):
            dx, dy = MOVE_DELTAS[move]
            next_pos = (pos[0] + dx, pos[1] + dy)

            if next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [move]))

    print("Goal not found.")

if __name__ == "__main__":
    bfs_agent()
