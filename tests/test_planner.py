"""Compare all objectives against exhaustive enumeration on small schedules."""
import random
import unittest
from flight import Flight
from planner import Planner

def enumerate_routes(flights, city, target, earliest, latest):
    routes = []
    for flight in flights:
        if (flight.start_city == city and flight.departure_time >= earliest
                and flight.arrival_time <= latest):
            if flight.end_city == target:
                routes.append([flight])
            else:
                for rest in enumerate_routes(flights, flight.end_city, target,
                                             flight.arrival_time + 20, latest):
                    routes.append([flight] + rest)
    return routes

class PlannerTests(unittest.TestCase):
    def test_random_schedules_against_exhaustive_search(self):
        rng = random.Random(42)
        for _ in range(200):
            flights = []
            for i in range(18):
                start, end = rng.sample(range(5), 2)
                departure = rng.randrange(0, 180)
                flights.append(Flight(i * 3, start, departure, end,
                                      departure + rng.randrange(1, 30), rng.randrange(0, 100)))
            planner = Planner(flights)
            routes = enumerate_routes(flights, 0, 4, 0, 220)
            objectives = [
                (planner.least_flights_earliest_route, lambda r: (len(r), r[-1].arrival_time)),
                (planner.cheapest_route, lambda r: (sum(f.fare for f in r),)),
                (planner.least_flights_cheapest_route, lambda r: (len(r), sum(f.fare for f in r))),
            ]
            for method, key in objectives:
                actual = method(0, 4, 0, 220)
                if routes:
                    self.assertEqual(key(actual), min(map(key, routes)))
                else:
                    self.assertEqual(actual, [])
            self.assertFalse(any(hasattr(f, 'previous_flight') for f in flights))

    def test_connection_boundary_and_empty_schedule(self):
        flights = [Flight(0, 0, 0, 1, 10, 5), Flight(1, 1, 29, 2, 40, 1),
                   Flight(2, 1, 30, 2, 40, 8)]
        p = Planner(flights)
        self.assertEqual([f.flight_no for f in p.cheapest_route(0, 2, 0, 40)], [0, 2])
        self.assertEqual(p.cheapest_route(0, 2, 0, 39), [])
        self.assertEqual(Planner([]).cheapest_route(0, 4, 0, 50), [])
        self.assertEqual(p.cheapest_route(0, 0, 0, 50), [])

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            Planner([Flight(0, 0, 0, 1, 10, 1), Flight(0, 1, 30, 2, 40, 1)])

if __name__ == '__main__':
    unittest.main()
