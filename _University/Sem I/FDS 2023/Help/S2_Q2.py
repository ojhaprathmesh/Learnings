point = eval(input("Enter a 2D point (x,y): "))
x, y = point

if 0 in point:
    if x == 0 and y == 0:
        print("Point lies on origin!")
    elif point[1] == 0:  # Checking y = 0
        print("Point lies on x-axis")
    else:
        print("Point lies on y-axis")

else:
    if x * y > 0:
        if x > 0:
            print("Point lies in first quadrant")
        else:
            print("Point lies in third quadrant")
    if x * y < 0:
        if x < 0:
            print("Point lies in second quadrant")
        else:
            print("Point lies in fourth quadrant")
