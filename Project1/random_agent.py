import random
import subprocess

def send_command_and_read_result(command):
    subprocess.run(["python3", "simulator.py", command], check=True)

    with open("state_vector.txt", "r") as file:
        result = file.read().strip().split(',')
    return result

index_to_direction = {
    0: "up",
    2: "right",
    4: "down",
    6: "left"
}


# Given a state vector, return a list of directions where the agent can move
def get_valid_moves(state_vector):
    return [index_to_direction[i] for i in index_to_direction if state_vector[i] == '0']

def random_agent():
    # Reset maze
    state_vector = send_command_and_read_result("")  # Initial state after reset

    while True:
        if state_vector[0] == "goal":
            print(f"Goal reached in {state_vector[1]} steps!")
            break

        valid_moves = get_valid_moves(state_vector)

        if not valid_moves:
            print("No valid moves")
            break

        move = random.choice(valid_moves)
        print(f"🚶 Moving: {move}")

        state_vector = send_command_and_read_result(move)

        if state_vector[0] == "goal":
            print(f"Goal reached in {state_vector[1]} steps!")
            break

# Start the agent
if __name__ == "__main__":
    random_agent()
