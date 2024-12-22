matrix = eval(input("Enter A Matrix In Form Of 2D-Array:- "))
transpose = []
for n in range(len(matrix[0])):
    temp = []
    for i in matrix:
        temp.append(i[n])
    transpose.append(temp)

print(transpose)
