from sklearn.neighbors import KNeighborsClassifier

# Given data
x = [2, 5, 8, 4, 3, 9, 14, 8, 10, 12, 13, 14]
y = [21, 19, 18, 17, 16, 25, 29, 22, 21, 21, 23, 25]
classes = [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]

# New point A(9, 20)
new_point = [[9, 20]]

# KNN for K=1
knn_1 = KNeighborsClassifier(n_neighbors=1)
knn_1.fit(list(zip(x, y)), classes)
prediction_1 = knn_1.predict(new_point)

# KNN for K=3
knn_3 = KNeighborsClassifier(n_neighbors=3)
knn_3.fit(list(zip(x, y)), classes)
prediction_3 = knn_3.predict(new_point)

print(f"For K=1, Predicted class for point A(9, 20): {prediction_1[0]}")
print(f"For K=3, Predicted class for point A(9, 20): {prediction_3[0]}")
