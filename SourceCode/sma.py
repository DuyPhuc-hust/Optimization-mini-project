#PYTHON 
import random
from collections import defaultdict

# Enhanced Simulated Annealing with Strict Constraints
def harvest_plan_simulated_annealing(N, m, M, fields):
    # Step 1: Initial Heuristic Solution
    def initial_solution():
        sorted_fields = sorted(enumerate(fields, start=1), key=lambda x: (-x[1][0], x[1][2] - x[1][1]))
        daily_harvest = defaultdict(int)
        assignments = [-1] * (N + 1)

        for field_id, (d, s, e) in sorted_fields:
            for day in range(s, e + 1):
                if daily_harvest[day] + d <= M:
                    daily_harvest[day] += d
                    assignments[field_id] = day
                    break
        return assignments, daily_harvest

    # Step 2: Evaluate Solution
    def evaluate(daily_harvest):
        valid_days = [day for day in daily_harvest if m <= daily_harvest[day] <= M]
        total_product = sum(daily_harvest[day] for day in valid_days)
        return total_product

    # Step 3: Generate Neighbor Solution
    def neighbor_solution(assignments, daily_harvest):
        new_assignments = assignments[:]
        new_daily_harvest = daily_harvest.copy()

        # Randomly pick a field to modify
        field_id = random.randint(1, N)
        current_day = new_assignments[field_id]
        d, s, e = fields[field_id - 1]

        # Remove the field from its current day
        if current_day != -1:
            new_daily_harvest[current_day] -= d

        # Reassign to a new day or skip harvesting
        valid_days = [-1] + [day for day in range(s, e + 1) if new_daily_harvest[day] + d <= M]
        new_day = random.choice(valid_days)
        if new_day != -1:
            new_daily_harvest[new_day] += d
        new_assignments[field_id] = new_day

        return new_assignments, new_daily_harvest

    # Step 4: Validate Solution
    def is_valid_solution(daily_harvest):
        for day, harvest in daily_harvest.items():
            if harvest > M or (0 < harvest < m):
                return False
        return True

    # Step 5: Simulated Annealing
    def simulated_annealing():
        assignments, daily_harvest = initial_solution()
        current_value = evaluate(daily_harvest)
        best_assignments = assignments[:]
        best_value = current_value

        temperature = 100
        cooling_rate = 0.99
        iterations = 1000

        for _ in range(iterations):
            new_assignments, new_daily_harvest = neighbor_solution(assignments, daily_harvest)
            if not is_valid_solution(new_daily_harvest):
                continue  # Skip invalid solutions

            new_value = evaluate(new_daily_harvest)
            delta = new_value - current_value

            # Accept new solution based on SA acceptance criteria
            if delta > 0 or random.uniform(0, 1) < (2.71828 ** (delta / temperature)):
                assignments, daily_harvest = new_assignments, new_daily_harvest
                current_value = new_value

                # Update best solution
                if current_value > best_value:
                    best_assignments = assignments[:]
                    best_value = current_value

            # Decrease temperature
            temperature *= cooling_rate

        return best_assignments, best_value

    # Step 6: Output the Best Solution
    best_assignments, _ = simulated_annealing()
    valid_assignments = [(field_id, day) for field_id, day in enumerate(best_assignments) if day != -1]

    print(len(valid_assignments))
    for field_id, day in sorted(valid_assignments):
        print(field_id, day)


# Input processing
N, m, M = map(int, input().split())
fields = [tuple(map(int, input().split())) for _ in range(N)]
harvest_plan_simulated_annealing(N, m, M, fields)
