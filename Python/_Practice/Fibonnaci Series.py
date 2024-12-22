def genSeries(num):
    seriesList = [0, 1]
    while len(seriesList) != num:
        seriesList.append(seriesList[-1] + seriesList[-2])

    return seriesList


print(genSeries(int(input("Enter A Number:-"))))
