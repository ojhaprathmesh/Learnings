import math

# Input
Radius = int(input('Enter The Radius :- '))
Pi = math.pi
dPlace = int(input('Enter Decimal Places Required :- '))

# Main Processing
AreaC = round(Pi*(Radius**2), dPlace)

# Output
print(f'\nArea Of Circle Of Radius {Radius} units = {AreaC} units')