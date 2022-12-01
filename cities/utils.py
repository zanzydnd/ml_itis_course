import math
from typing import Tuple

EARTH_RADIUS = 6372795
from geopy.distance import geodesic


def count_distance(point_1: Tuple[float, float], point_2: Tuple[float, float]) -> float:
    return geodesic(point_1, point_2).km
    # return math.sqrt(
    #     (point_1[0] - point_2[0]) ** 2
    #     + (point_1[1] - point_2[1]) ** 2
    # )
