class Employee:
    NoOfLeaves = 5

harry = Employee()
meera = Employee()

harry.name = "Harry"
harry.salary = 12000
harry.role = "Technician"

meera.name = "Meera"
meera.salary = 15000
meera.role = "Developer"

print(harry.role, meera.role) # Instance Variable
print(harry.NoOfLeaves, meera.NoOfLeaves) # Class Variable

print(meera.__dict__, Employee.NoOfLeaves)
Employee.NoOfLeaves = 8 # This Updates Class Variable
meera.NoOfLeaves = 8 # This Creates A New Instance Variable For The Object
print(meera.__dict__, Employee.NoOfLeaves)
