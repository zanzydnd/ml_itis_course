from cities.constructor_html import construct_html
from cities.engine import GeneticEngine

# TODO добавить карты
if __name__ == '__main__':
    # n = int(input("Введите кол-во городов"))

    cities = {
        1: (55.75, 37.62),
        2: (24.47, 54.37),
        3: (25.7743, -80.1937),
        4: (78.5, 82.4),
        5: (1.5, 91.0),
        6: (51.1, 23.0),
        # 7: (41.7, 64.6),
    }
    g_engine = GeneticEngine(
        cities_map=cities
    )
    result = g_engine.run()
    construct_html(cities, result)
