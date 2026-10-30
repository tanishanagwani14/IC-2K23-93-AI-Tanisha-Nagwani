from collections import deque

def solve_water_jug(jug1_cap, jug2_cap, target):
    # Base check
    if target > max(jug1_cap, jug2_cap):
        print("\nTarget cannot be greater than the maximum jug capacity!")
        return False

    # Queue stores: (jug1_level, jug2_level, path_taken)
    queue = deque([(0, 0, [])])
    visited = set([(0, 0)])

    while queue:
        j1, j2, path = queue.popleft()
        current_path = path + [(j1, j2)]

        # Goal state reached
        if j1 == target or j2 == target:
            print(f"\nTarget achieved in {len(current_path) - 1} steps!")
            print("\nStep-by-step Solution (Jug 1, Jug 2):")
            for step, (amt1, amt2) in enumerate(current_path):
                print(f"Step {step}: ({amt1}, {amt2})")
            return True

        # 6 Possible operations
        possible_states = [
            (jug1_cap, j2),  # Fill Jug 1
            (j1, jug2_cap),  # Fill Jug 2
            (0, j2),         # Empty Jug 1
            (j1, 0),         # Empty Jug 2
            # Pour Jug 1 -> Jug 2
            (j1 - min(j1, jug2_cap - j2), j2 + min(j1, jug2_cap - j2)),
            # Pour Jug 2 -> Jug 1
            (j1 + min(j2, jug1_cap - j1), j2 - min(j2, jug1_cap - j1))
        ]

        for state in possible_states:
            if state not in visited:
                visited.add(state)
                queue.append((state[0], state[1], current_path))

    print("\nNo solution exists for the given jug capacities and target!")
    return False

if __name__ == "__main__":
    print("--- WATER JUG PROBLEM SOLVER ---")
    try:
        j1_capacity = int(input("Enter capacity of Jug 1: "))
        j2_capacity = int(input("Enter capacity of Jug 2: "))
        target_amount = int(input("Enter target amount to measure: "))

        solve_water_jug(j1_capacity, j2_capacity, target_amount)
    except ValueError:
        print("Please enter valid integer values.")