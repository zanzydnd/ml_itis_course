import random
import matplotlib
import matplotlib.pyplot as plt

from math import sqrt
from itertools import cycle


def generate_points(mean_x, mean_y, deviation_x, deviation_y):
    return random.gauss(mean_x, deviation_x), random.gauss(mean_y, deviation_y)


def distance_between_points(points):
    return sqrt( (points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2 )


def U(e, x, points) -> list:
    result = []
    for i in points:
        distance = distance_between_points((x, i))
        if distance < e:
            result.append(i)
    return result


def main():
    e = 60  # размер окрестности
    m = 5  # кол-во точек в окрестности

    a = 0

    # points = [
    #     generate_points(mean_x=100, mean_y=100, deviation_x=50, deviation_y=50)
    #     for i in range(100)
    # ]

    # points = [(64, 150), (84, 112), (106, 90), (154, 64), (192, 62), (220, 82), (244, 92), (271, 111), (275, 137),
    #           (286, 161), (56, 178), (80, 156), (101, 131), (123, 104), (155, 94), (191, 100), (242, 70), (231, 114),
    #           (272, 95), (261, 131), (299, 136), (308, 124), (128, 78), (47, 128), (47, 159), (137, 186), (166, 228),
    #           (171, 250), (194, 272), (221, 287), (253, 292), (308, 293), (332, 280), (385, 256), (398, 237),
    #           (413, 205), (435, 166), (447, 137), (422, 126), (400, 154), (389, 183), (374, 214), (358, 235),
    #           (321, 250), (274, 263), (249, 263), (208, 230), (192, 204), (182, 174), (147, 205), (136, 246),
    #           (147, 255), (182, 282), (204, 298), (252, 316), (312, 321), (349, 313), (393, 288), (417, 259),
    #           (434, 222), (443, 187), (463, 174)]
    points = [(126, 63), (101, 100), (80, 160), (88, 208), (89, 282), (88, 362), (94, 406), (149, 377), (147, 304), (147, 235), (146, 152), (160, 103), (174, 142), (169, 184), (170, 241), (169, 293), (185, 376), (178, 422), (116, 353), (124, 194), (273, 69), (277, 112), (260, 150), (265, 185), (270, 235), (265, 295), (281, 351), (285, 416), (321, 404), (316, 366), (306, 304), (309, 254), (309, 207), (327, 161), (318, 108), (306, 66), (425, 66), (418, 135), (411, 183), (413, 243), (414, 285), (407, 333), (411, 385), (443, 387), (455, 330), (441, 252), (457, 207), (453, 149), (455, 90), (455, 56), (439, 102), (431, 162), (431, 193), (426, 236), (427, 281), (438, 323), (419, 379), (425, 389), (422, 349), (451, 275), (441, 222), (297, 145), (284, 195), (288, 237), (292, 282), (288, 313), (303, 356), (293, 395), (274, 268), (280, 344), (303, 187), (114, 247), (131, 270), (144, 215), (124, 219), (98, 240), (96, 281), (146, 267), (136, 221), (123, 166), (101, 185), (152, 184), (104, 283), (74, 239), (107, 287), (118, 335), (89, 336), (91, 315), (151, 340), (131, 373), (108, 133), (134, 130), (94, 260), (113, 193)]

    visited = set()
    clustered = set()

    NOIZY = 0
    clusters = {NOIZY: []}

    for x in points:
        if x in visited:
            continue
        visited.add(x)
        U_x = U(e, x, points)
        if len(U_x) < m:
            clusters[NOIZY].append(x)
        else:
            # создание нового кластера
            a += 1

            if a not in clusters:
                clusters[a] = []
            clusters[a].append(x)
            clustered.add(x)

            while U_x:
                x_ = U_x.pop()
                if x_ not in visited:
                    visited.add(x_)
                    U_x_ = U(e, x, points)
                    if len(U_x_) > m:
                        U_x.extend(U_x_)

                if x_ not in clustered:
                    clustered.add(x_)
                    clusters[a].append(x_)
                    if x_ in clusters[NOIZY]:
                        clusters[NOIZY].remove(x_)

    print(clusters.keys())

    for c, points in zip(cycle('bgrcmykgrcmykgrcmykgrcmykgrcmykgrcmyk'), clusters.values()):
        X = [p[0] for p in points]
        Y = [p[1] for p in points]
        plt.scatter(X, Y, c=c)

    plt.show()


if __name__ == '__main__':
    main()
