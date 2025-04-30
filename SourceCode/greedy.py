# Read the number of fields, minimum yield (m), and maximum yield (M) per day
N, m, M = map(int, input().split())
quantity_fields = [(0, 0)] * N  # Store yield and the end day for each field
s_days, e_days = [], []  # Lists to track start and end days for each field

# Determine the maximum day needed based on the input
max_day = 0
for i in range(N):
    d_i, s_i, e_i = map(int, input().split())
    # Ensure s_days and e_days are large enough to include current start and end days
    while len(s_days) <= max(s_i, e_i + 1):
        s_days.append([])
        e_days.append([])
    # Add the field index to the respective start and end day lists
    s_days[s_i].append(i)
    e_days[e_i + 1].append(i)
    # Store the yield and end day for the field
    quantity_fields[i] = (d_i, e_i)
    # Update the maximum day
    max_day = max(max_day, e_i + 1)

# Initialize variables for tracking current fields and harvesting results
cur_fields = {}  # Active fields available for harvest
ans, cur_quantity = 0, 0  # Total yield harvested and current yield for the day
day_harvest = [-1] * N  # Array to store the day each field is harvested

# Loop through each day up to the maximum day
for i in range(1, max_day + 1):
    cur_quantity = 0  # Reset current yield for the day
    # Add fields starting on the current day to the active fields
    for field in s_days[i]:
        cur_quantity += quantity_fields[field][0]
        cur_fields[field] = quantity_fields[field]
    # Remove fields that are no longer valid (end day passed)
    for field in e_days[i]:
        if day_harvest[field] == -1:  # Only remove if not yet harvested
            cur_quantity -= quantity_fields[field][0]
            cur_fields.pop(field)
    # Adjust current yield if it exceeds the maximum daily limit (M)
    while cur_quantity > M:
        # Select the field with the furthest end day to remove
        field = max(cur_fields, key=lambda x: cur_fields[x][1])
        if quantity_fields[field][1] == i:  # Stop if field must be harvested today
            break
        cur_quantity -= cur_fields[field][0]  # Reduce current yield
        s_days[i + 1].append(field)  # Postpone field to the next day
        cur_fields.pop(field)  # Remove the field from active fields
    # If the current yield is within the valid range [m, M], harvest
    if cur_quantity >= m:
        ans += min(M, cur_quantity)  # Add harvested yield to total
        for field in cur_fields:
            day_harvest[field] = i  # Record the harvest day for each field
        cur_quantity = 0  # Reset yield after harvesting
        cur_fields = {}  # Clear active fields

# Print the total number of fields and their respective harvest days
print(N)
for i in range(N):
    print(i + 1, day_harvest[i])
