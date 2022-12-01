import functools
import random
from typing import Tuple, List

from cities.utils import count_distance

SELECTION_TYPE = ["TOURNEY", "ROULETTE_WHEEL"]
CROSSING_TYPE = [
    "ONE_POINT_RECOMBINATION",
    "TWO_POINT_RECOMBINATION",
    "ELEMENTWISE_RECOMBINATION",
    "ONE_ELEMENT_EXCHANGE"
]

import copy
import itertools
import math

#TODO добавить возвращение в исходную точку

class GeneticEngine:
    def __init__(self, cities_map: dict):
        self.cities_map = cities_map
        self.current_pop = []
        self.num_of_permutations = math.factorial(len(cities_map.keys()))
        self.percentage_of_survivors = 0.6
        self.count_in_gen = int(self.percentage_of_survivors * self.num_of_permutations)
        self.mutation_point = 60
        self.number_of_generations = 20

    def run(self) -> Tuple[int]:
        self.generate_first()

        for i in range(self.number_of_generations):
            self.crossing()
            self.selection()

            if self.count_distance_sum(self.current_pop[0]) == 0:
                return self.current_pop[0]

        return self.current_pop[0]

    def count_distance_sum(self, variant: Tuple[int]):
        i = 1
        previous_point = variant[0]
        distance = 0
        while i < len(variant):
            current_point = variant[i]
            distance += count_distance(
                point_1=self.cities_map[previous_point],
                point_2=self.cities_map[current_point]
            )
            previous_point = current_point
            i += 1
        return distance

    def generate_first(self):
        keys = copy.deepcopy(tuple(self.cities_map.keys()))
        self.current_pop = list(itertools.permutations(keys))[:self.count_in_gen]

    def selection(self):
        self.current_pop.sort(
            key=self.count_distance_sum
        )
        self.current_pop = self.current_pop[:self.count_in_gen]

    def _cross_two_parents(self, parent_1: Tuple[int], parent_2: Tuple[int]) -> Tuple[int]:
        # кроссовер
        parent_1_circle = list(copy.deepcopy(parent_1))
        parent_2_circle = list(copy.deepcopy(parent_2))
        child = []

        i = 0
        j = 0
        is_first_circle = True
        while len(child) != len(self.cities_map.keys()):
            if is_first_circle:
                val = parent_1_circle[i]
                while val in child:
                    i += 1
                    val = parent_1_circle[i]
            else:
                val = parent_2_circle[j]
                while val in child:
                    j += 1
                    val = parent_1_circle[j]
            child.append(val)

        return tuple(child)

    def crossing(self):
        # случайным образом выбираем count_in_gen пар
        pairs = []

        for i in range(self.count_in_gen):
            first_parent_index = random.randint(0, len(self.current_pop) - 1)
            second_parent_index = first_parent_index
            while second_parent_index == first_parent_index:
                second_parent_index = random.randint(0, len(self.current_pop) - 1)
            pairs.append(
                (
                    self.current_pop[first_parent_index],
                    self.current_pop[second_parent_index],
                )
            )

        self.current_pop += [
            self.mutation(self._cross_two_parents(*parents_tuple))
            for parents_tuple in pairs
        ]

    def mutation(self, child: Tuple[int]) -> Tuple[int]:
        if random.randint(0, 101) >= self.mutation_point: return child

        child = list(child)
        pos_1 = random.randint(0, len(child) - 1)
        pos_2 = random.randint(0, len(child) - 1)

        t = child[pos_1]
        child[pos_1] = child[pos_2]
        child[pos_2] = t

        return tuple(child)
