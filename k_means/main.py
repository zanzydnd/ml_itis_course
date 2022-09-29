import itertools
import os
from math import sqrt
from typing import Tuple

import numpy as np
import matplotlib
from math import cos, sin, pi
import imageio

from k_means.colors import POINTS_COLOR

gif_name = 'movie'
n_frames = 10
bg_color = '#95A4AD'
marker_color = '#283F4E'
x_color = "#FF0000"
marker_size = 25

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



def find_center_of_gravity(points):
    if len(points) == 1:
        return points[0]

    if len(points) == 2:
        return (int(points[0][0]) + int(points[1][0])) / 2, (int(points[0][1]) + int(points[1][1])) / 2

    i = 0
    new_points = []
    while i < len(points):
        new_points.append(find_center_of_gravity(points[i:i + 2]))
        i += 2

    return find_center_of_gravity(new_points)


def distance_between_points(points):
    return int(sqrt((int(points[0][0]) - int(points[1][0])) ** 2 + (int(points[0][1]) - int(points[1][1])) ** 2))


def find_r_and_o(points) -> Tuple[int, Tuple[int, int]]:
    x_center, y_center = find_center_of_gravity(points)

    r = 0
    for point in points:
        distance = distance_between_points([(x_center, y_center), point])
        r = max(distance, r)

    return int(r + 2), (int(x_center), int(y_center))  # к радиусу добавляю 2, чтобы точка не лежала на окружности


def find_J_C(clusters_centers, clusters_points):
    # сумма квадратов расстояний от точек до до центроидов кластеров, к которым они относятся.
    sum = 0
    for i, cluster_center in enumerate(clusters_centers):
        for cluster_points in clusters_points:
            for cluster_point in cluster_points:
                sum += distance_between_points([cluster_point, cluster_center]) ** 2
    return sum


def generate_random_points():
    import random

    radius = 5
    rangeX = (10, 110)
    rangeY = (10, 110)
    qty = 20  # or however many points you want

    # Generate a set of all points within 200 of the origin, to be used as offsets later
    # There's probably a more efficient way to do this.
    deltas = set()
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x * x + y * y <= radius * radius:
                deltas.add((x, y))

    randPoints = []
    excluded = set()
    i = 0
    while i < qty:
        x = random.randrange(*rangeX)
        y = random.randrange(*rangeY)
        if (x, y) in excluded: continue
        randPoints.append((x, y))
        i += 1
        excluded.update((x + dx, y + dy) for (dx, dy) in deltas)
    return randPoints


def plot_helper():
    # plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    ax.set_facecolor(bg_color)

    plt.xlim(0, 140)
    plt.ylim(0, 140)

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
    ax.xaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


def main():
    # генерирует точки в прямоугольнике 0,0 1000,1000
    n = 20
    points = generate_random_points()

    k = 1
    J_C_array = []
    D_K = 100000000000

    filenames = []
    image_index = 0
    r, o = find_r_and_o(points)
    while k <= n:
        plot_helper()
        # находим точки к угольника вписанного в окружность
        clusters_centers = []
        if k == 1:
            clusters_centers.append(o)
        elif k == 2:
            clusters_centers.append((o[0] + r, o[1]))
            clusters_centers.append((o[0] - r, o[1]))
        else:
            for i in range(1, k + 1):
                alpha = 2.0 * float(i) * pi / k
                h_1 = r * cos(alpha) + o[0]
                h_2 = r * sin(alpha) + o[1]
                clusters_centers.append((int(h_1), int(h_2)))
        image_index += 1
        filename = f'images/frame_{image_index}.png'
        filenames.append(filename)
        plt.scatter(*zip(*points), c=marker_color, s=marker_size)
        plt.scatter(*zip(*clusters_centers), color=x_color, marker="x")
        plt.savefig(filename, dpi=96, facecolor=bg_color)
        plt.close()
        # создаем массив длиной к,points_in_cluster[i] - список точек, которые относятся к i-ому кластеру
        points_in_cluster = []
        for i in range(k):
            points_in_cluster.append([])
        while True:
            points_in_cluster = []
            for i in range(k):
                points_in_cluster.append([])
            plot_helper()
            plt.scatter(*zip(*clusters_centers), color=x_color, marker="x")

            # определяем к какому центру точка уйдет
            for point in points:
                distance_between_point_and_cluster_center = 10000000
                for i, cluster_center in enumerate(clusters_centers):
                    if distance_between_point_and_cluster_center > distance_between_points([point, cluster_center]):
                        distance_between_point_and_cluster_center = distance_between_points([point, cluster_center])
                        points_in_cluster[i].append(point)

            # рисуем точки - с цветами по кластеру
            image_index += 1
            filename = f'images/frame_{image_index}.png'
            filenames.append(filename)
            for i, cluster_points in enumerate(points_in_cluster):
                plt.scatter(*zip(*cluster_points), c=POINTS_COLOR[i])

            # высчитываем для каждого кластера - новый центр тяжести
            new_cluster_centers = []
            for i, cluster_center in enumerate(clusters_centers):
                new_cluster_centers.append(find_center_of_gravity(points_in_cluster[i]))

            flag_to_exit = True
            for i in range(len(new_cluster_centers)):
                flag_to_exit &= int(new_cluster_centers[i][0]) == int(clusters_centers[i][0]) and int(
                    new_cluster_centers[i][1]) == int(clusters_centers[i][1])
            plt.savefig(filename, dpi=96, facecolor=bg_color)
            plt.close()
            if flag_to_exit:
                break
            else:
                clusters_centers = new_cluster_centers

        image_end= image_index

        J_C_array.append(find_J_C(clusters_centers, points_in_cluster))

        if 2 < k < n:
            new_D_K = abs(J_C_array[k - 1 - 1] - J_C_array[k - 1]) / abs(
                J_C_array[k - 1 - 1 - 1] - J_C_array[k - 1 - 1])
            if D_K < new_D_K:
                # filenames = set(filenames)
                # for i in range(image_strt,image_end):
                #     filenames.remove(f"images/frame_{i}.png")
                #     os.remove(f"images/frame_{i}.png")
                break
            D_K = new_D_K

        k += 1
    actual_k = k - 1

    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('result.gif', images)
    for filename in set(filenames):
        os.remove(filename)


if __name__ == '__main__':
    main()
