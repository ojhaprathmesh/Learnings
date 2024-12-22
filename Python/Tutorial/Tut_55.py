class Employee:
    NoOfLeaves = 5

    def __init__(self, name, salary, depart):
        self.iname = name
        self.isalary = salary
        self.idepart = depart

    def printDetails(self):
        return f"Name Is {self.iname}, Salary Is {self.isalary} And Department Is {self.idepart}"


Shruti = Employee("Shruti", 40000, "Chemical")
Prathmesh = Employee("Prathmesh", 60000, "Computer Science")

# Shruti.name = "Shruti"
# Shruti.salary = 40000
# Shruti.depart = "Chemical"

# Prathmesh.name = "Prathmesh"
# Prathmesh.salary = 60000
# Prathmesh.depart = "Computer Science"

print(Prathmesh.printDetails())
print(Shruti.printDetails())
