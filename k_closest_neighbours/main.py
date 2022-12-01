import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris

import matplotlib.pyplot as plt

proections = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
plt.rcParams["figure.figsize"] = [15.00, 15.00]
points_before_normalization = iris.get('data')
fig, axs = plt.subplots(3, 2)

i = 0
j = 0
for proection in proections:
    for array_ in points_before_normalization:
        axs[i, j].plot(array_[proection[0]], array_[proection[1]], marker="o")
    if i == 2:
        if j < 1:
            j += 1
        else:
            i = 0
    else:
        i += 1

plt.show()


def normalize(column):
    # sum = 0

    # for item in column:
    #   sum += item

    # sum /= len(column)

    # s = 0
    # for item in column:
    #   s += (item - sum) ** 2
    # s /= len(column) - 1
    # import math
    # s = math.sqrt(s)
    # return [((item - sum) / s) for item in column]
    x_min = 1000000000
    x_max = -10000000000
    for x in column:
        if x_min > x:
            x_min = x
        if x_max < x:
            x_min = x
    return [((item - x_min) / (x_max - x_min)) for item in column]


normalized = [[0] * len(points_before_normalization[0]) for i in range(len(points_before_normalization))]
row_max = len(points_before_normalization)
column_max = len(points_before_normalization[0])

j = 0

while j < column_max:
    column = []
    i = 0
    while i < row_max:
        column.append(points_before_normalization[i][j])
        i += 1
    normalized_column = normalize(column)
    # print(normalized_column)

    normalized_i = 0

    while normalized_i < row_max:
        normalized[normalized_i][j] = float(normalized_column[normalized_i])
        normalized_i += 1
    j += 1

plt.clf()

fig, axs = plt.subplots(3, 2)

i = 0
j = 0
for proection in proections:
    for array_ in normalized:
        axs[i, j].plot(array_[proection[0]], array_[proection[1]], marker="o")
    if i == 2:
        if j < 1:
            j += 1
        else:
            i = 0
    else:
        i += 1

plt.show()

import math


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)
