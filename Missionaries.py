from collections import deque

def is_valid(m_left, c_left, m_right, c_right, num_missionaries, num_cannibals):
    # Check boundaries
    if m_left < 0 or c_left < 0 or m_right < 0 or c_right < 0:
        return False
    if m_left > num_missionaries or c_left > num_cannibals or m_right > num_missionaries or c_right > num_cannibals:
        return False

    # Check if cannibals outnumber missionaries on left bank
    if m_left > 0 and c_left > m_left:
        return False

    # Check if cannibals outnumber missionaries on right bank
    if m_right > 0 and c_right > m_right:
        return False

    return True

def solve_missionaries_and_cannibals(num_m, num_c, boat_capacity):
    # State representation: (M_left, C_left, Boat_position, M_right, C_right)
    # Boat_position: 1 for Left bank, 0 for Right bank
    initial_state = (num_m, num_c, 1, 0, 0)
    goal_state = (0, 0, 0, num_m, num_c)

    queue = deque([(initial_state, [])])
    visited = set([initial_state])

    # Generate possible boat moves based on capacity
    possible_moves = []
    for m in range(boat_capacity + 1):
        for c in range(boat_capacity + 1):
            if 1 <= m + c <= boat_capacity:
                possible_moves.append((m, c))

    while queue:
        (m_l, c_l, boat, m_r, c_r), path = queue.popleft()
        current_path = path + [(m_l, c_l, boat, m_r, c_r)]

        # Goal check
        if (m_l, c_l, boat, m_r, c_r) == goal_state:
            print(f"\nGoal state reached in {len(current_path) - 1} moves!")
            print("\nStep-by-step Solution:")
            print("Format: [Left Bank: M, C | Boat Side | Right Bank: M, C]")
            print("-" * 55)
            for step, state in enumerate(current_path):
                boat_side = "Left " if state[2] == 1 else "Right"
                print(f"Step {step}: Left: ({state[0]}M, {state[1]}C) | Boat: {boat_side} | Right: ({state[3]}M, {state[4]}C)")
            return True

        for m_move, c_move in possible_moves:
            if boat == 1:  # Move from Left to Right
                new_m_l, new_c_l = m_l - m_move, c_l - c_move
                new_m_r, new_c_r = m_r + m_move, c_r + c_move
                new_boat = 0
            else:  # Move from Right to Left
                new_m_l, new_c_l = m_l + m_move, c_l + c_move
                new_m_r, new_c_r = m_r - m_move, c_r - c_move
                new_boat = 1

            next_state = (new_m_l, new_c_l, new_boat, new_m_r, new_c_r)

            if is_valid(new_m_l, new_c_l, new_m_r, new_c_r, num_m, num_c) and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, current_path))

    print("\nNo valid solution exists for the given configuration!")
    return False

if __name__ == "__main__":
    print("--- MISSIONARIES AND CANNIBALS SOLVER (BFS) ---")
    try:
        num_missionaries = int(input("Enter number of Missionaries: "))
        num_cannibals = int(input("Enter number of Cannibals: "))
        boat_cap = int(input("Enter boat capacity (standard is 2): "))

        if num_cannibals > num_missionaries and num_missionaries > 0:
            print("\nInitial configuration invalid: Cannibals outnumber Missionaries on the starting bank!")
        else:
            solve_missionaries_and_cannibals(num_missionaries, num_cannibals, boat_cap)
    except ValueError:
        print("Please enter valid integer inputs.")