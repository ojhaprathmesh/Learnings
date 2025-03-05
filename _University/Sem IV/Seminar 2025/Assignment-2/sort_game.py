x = int(input())
N = int(input())
employees = []

for _ in range(N):
    name, salary = input().split()
    salary = int(salary)
    employees.append((name, salary))

filtered_employees = [employee for employee in employees if employee[1] >= x] # List containing tuple of employee info

sorted_employees = sorted(filtered_employees, key=lambda emp: (-emp[1], emp[0]))

for employee in sorted_employees:
    print(employee[0], employee[1])
