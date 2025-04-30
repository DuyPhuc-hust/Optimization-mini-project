from collections import defaultdict

# Local Search-Based Harvest Plan

def harvest_plan_local_search(N, m, M, fields):
    # Step 1: Initialize assignments with a greedy approach
    fields = sorted(enumerate(fields, start=1), key=lambda x: (-x[1][0], x[1][2] - x[1][1]))
    daily_harvest = defaultdict(int)
    field_assignments = [-1] * (N + 1)

    for field_id, (d, s, e) in fields:
        for day in range(s, e + 1):
            if daily_harvest[day] + d <= M:
                daily_harvest[day] += d
                field_assignments[field_id] = day
                break

    # Step 2: Local search optimization to improve assignments
    def evaluate(day):
        return daily_harvest[day] >= m

    def reassign_field(field_id, d, s, e):
        for day in range(s, e + 1):
            if daily_harvest[day] + d <= M and evaluate(day):
                return day
        return -1

    for field_id, (d, s, e) in fields:
        current_day = field_assignments[field_id]
        if current_day == -1 or not evaluate(current_day):
            new_day = reassign_field(field_id, d, s, e)
            if new_day != -1 and new_day != current_day:
                if current_day != -1:
                    daily_harvest[current_day] -= d
                daily_harvest[new_day] += d
                field_assignments[field_id] = new_day

    # Step 3: Collect results for valid assignments
    result = [
        (field_id, day)
        for field_id, day in enumerate(field_assignments)
        if day > 0 and evaluate(day)
    ]

    # Output results
    print(len(result))
    for field_id, day in result:
        print(field_id, day)


# Input processing
N, m, M = map(int, input().split())
fields = [tuple(map(int, input().split())) for _ in range(N)]
harvest_plan_local_search(N, m, M, fields)
