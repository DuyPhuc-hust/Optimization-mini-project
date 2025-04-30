from ortools.linear_solver import pywraplp

def solve_harvesting_problem(N, m, M, fields):
    # Tạo solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver.")
        return
    MD = 0
    for i in range(N):
        MD = max(MD, fields[i][2])

    # Biến quyết định
    x = {}  # x[i, j] = 1 nếu thửa ruộng i được thu hoạch vào ngày j
    y = {}  # y[j] = 1 nếu nhà máy hoạt động vào ngày j

    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    for j in range(1, MD + 1):
        y[j] = solver.BoolVar(f'y[{j}]')

    # Ràng buộc 1: Mỗi thửa ruộng chỉ được thu hoạch một ngày hoặc không thu hoạch
    for i in range(N):
        solver.Add(sum(x[i, j] for j in range(fields[i][1], fields[i][2] + 1)) <= 1)

    # Ràng buộc 2: Tổng sản phẩm thu hoạch mỗi ngày không vượt quá khả năng xử lý của nhà máy
    
    for j in range(1, MD + 1):
        solver.Add(sum(fields[i][0] * x[i, j] for i in range(N) if fields[i][1] <= j <= fields[i][2]) <= M * y[j])

    # Ràng buộc 3: Nếu nhà máy hoạt động ngày j, thì ít nhất một thửa ruộng được thu hoạch
    
    for j in range(1, MD + 1):
        solver.Add(sum(x[i, j] for i in range(N) if fields[i][1] <= j <= fields[i][2]) <= y[j] * N)

    for j in range(1, MD + 1):
        solver.Add(sum(x[i, j] for i in range(N) if fields[i][1] <= j <= fields[i][2]) >= y[j])
    # Ràng buộc 4: Nhà máy chỉ hoạt động nếu tổng sản phẩm thu hoạch không ít hơn m
    
    total_harvested = sum(fields[i][0] * x[i, j] for i in range(N) for j in range(fields[i][1], fields[i][2] + 1))
    solver.Add(total_harvested >= m)

    # Hàm mục tiêu: Tối đa hóa tổng sản phẩm thu hoạch
    solver.Maximize(total_harvested)

    # Giải bài toán
    status = solver.Solve()

    # Xuất kết quả
    if status == pywraplp.Solver.OPTIMAL:
        harvested_fields = []
        for i in range(N):
            for j in range(fields[i][1], fields[i][2] + 1):
                if x[i, j].solution_value() > 0:
                    harvested_fields.append((i + 1, j))

        print(len(harvested_fields))
        for field in harvested_fields:
            print(field[0], field[1])
    else:
        print("No optimal solution found.")

# Đọc input
def main():
    N, m, M = map(int, input().split())
    fields = []
    for _ in range(N):
        fields.append(list(map(int, input().split())))
    solve_harvesting_problem(N, m, M, fields)

if __name__ == '__main__':
    main()
