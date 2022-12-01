import random as rnd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from math import sqrt


def generate_points(mean_x, mean_y, deviation_x, deviation_y):
    return rnd.gauss(mean_x, deviation_x), rnd.gauss(mean_y, deviation_y)


def distance_between_points(points):
    return sqrt(
        ((points[0][0] - points[1][0]) ** 2)
        + ((points[0][1] - points[1][1]) ** 2)
    )


def remove_n_max_edges(edges, N, points):
    to_remove = []

    while len(to_remove) != N:
        big = -1
        biggest_edge = None
        for edge in edges:
            if distance_between_points((points.get(edge[0]), points.get(edge[1]))) > big:
                big = distance_between_points((points.get(edge[0]), points.get(edge[1])))
                biggest_edge = edge

        edges.remove(biggest_edge)
        # edges.remove((biggest_edge[1], biggest_edge[0]))
        to_remove.append(biggest_edge)


if __name__ == '__main__':

    K = int(input("Enter k: "))

    points = {
        str(i): generate_points(mean_x=100, mean_y=100, deviation_x=50, deviation_y=50)
        for i in range(30)
    }

    visited_points = set()
    isolated_points = set(points.keys())
    min_distance = 10000000
    key_point_1 = None
    key_point_2 = None

    edges = set()

    for first_key, first_point in points.items():
        for second_key, second_point in points.items():
            if first_point == second_point:
                continue
            if distance_between_points((first_point, second_point)) < min_distance:
                min_distance = distance_between_points((first_point, second_point))
                key_point_1 = first_key
                key_point_2 = second_key

    visited_points.add(key_point_1)
    visited_points.add(key_point_2)
    isolated_points.remove(key_point_1)
    isolated_points.remove(key_point_2)

    edges.add((key_point_1, key_point_2))

    while isolated_points:
        dist = 1000000
        curr_key = None
        key_to = None
        for key_point in isolated_points:
            for key_point_visited in visited_points:
                point_1 = points.get(key_point)
                point_2 = points.get(key_point_visited)

                if dist > distance_between_points((point_2, point_1)):
                    curr_key = key_point
                    dist = distance_between_points((point_2, point_1))
                    key_to = key_point_visited

        visited_points.add(curr_key)
        isolated_points.remove(curr_key)
        edges.add((curr_key, key_to))

    for edge in edges:
        x_s = [points.get(edge[0])[0], points.get(edge[1])[0]]
        y_s = [points.get(edge[0])[1], points.get(edge[1])[1]]

        plt.plot(x_s, y_s, "ro-")

    plt.show()

    plt.clf()

    remove_n_max_edges(edges, K - 1, points)

    for point in points.values():
        plt.scatter(point[0], point[1])

    for edge in edges:
        x_s = [points.get(edge[0])[0], points.get(edge[1])[0]]
        y_s = [points.get(edge[0])[1], points.get(edge[1])[1]]

        plt.plot(x_s, y_s, "ro-")

    plt.show()
