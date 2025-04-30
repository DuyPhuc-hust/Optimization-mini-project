from ortools.sat.python import cp_model

def read_input():
    N, m, M = list(map(int, input().split()))
    harvest_plans = []
    for i in range(N):
        harvest_plans.append(list(map(int, input().split())))

    max_days = 0
    for i in range(N):
        max_days = max(max_days, harvest_plans[i][2])

    return N, m, M, harvest_plans, max_days

def harvest_planning(N, m, M, harvest_plans, MD):
    model = cp_model.CpModel()

    # Variables
    # Thửa thứ i được thu hoạch vào ngày j hay không
    x = {}
    for i in range(N):
        for j in range(MD):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    harvest_today = {}
    for j in range(MD):
        harvest_today[j] = model.NewBoolVar(f'harvest_today_{j}')

    # Constraints
    # Mỗi thửa chỉ được thu hoạch một ngày
    for i in range(N):
        model.Add(sum(x[i, j] for j in range(MD)) <= 1)

    # Ngày thu hoạch của thửa i phải nằm trong khoảng [s, e]
    for i in range(N):
        _, s_i, e_i = harvest_plans[i]
        s_i, e_i = s_i - 1, e_i - 1
        model.Add(sum(x[i, j] for j in range(MD) if j < s_i or j > e_i ) == 0)

    # Lượng thu hoạch mỗi ngày phải nằm trong khoảng [m, M]
    for j in range(MD):
        # Nếu có ít nhất một thửa được thu hoạch vào ngày j
        model.Add(sum(x[i, j] for i in range(N)) >= 1).OnlyEnforceIf(harvest_today[j])
        # Nếu không có thửa nào được thu hoạch vào ngày j
        model.Add(sum(x[i, j] for i in range(N)) == 0).OnlyEnforceIf(harvest_today[j].Not())

        amount = sum(harvest_plans[i][0] * x[i, j] for i in range(N))
        model.Add(amount >= m).OnlyEnforceIf(harvest_today[j])
        model.Add(amount <= M).OnlyEnforceIf(harvest_today[j])

    # Objective function
    model.Maximize(sum(harvest_plans[i][0] * x[i, j] for i in range(N) for j in range(MD)))

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Print the number of fields harvested, then print on each line "i, j" if field i is harvested on day j
        print(sum(solver.Value(x[i, j]) for i in range(N) for j in range(MD)))

        for i in range(N):
            for j in range(MD):
                if solver.Value(x[i, j]) == 1:
                    print(i + 1, j + 1)
    else:
        print('NO_SOLUTION')

if __name__ == "__main__":
    N, m, M, harvest_plans, max_days = read_input()
    harvest_planning(N, m, M, harvest_plans, max_days)
