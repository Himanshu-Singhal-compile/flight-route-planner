"""Time-constrained flight routes with three optimization objectives."""
from flight import Flight
from heap import Heap

class Planner:
    """Optimize routes with at least 20 minutes between connecting flights."""
    def __init__(self, flights: list[Flight]):
        self.data = {}
        self.flights = list(flights)
        ids = set()
        for flight in flights:
            if flight.flight_no in ids:
                raise ValueError('Flight IDs must be unique')
            if min(flight.fare, flight.departure_time, flight.start_city, flight.end_city) < 0 or flight.arrival_time < flight.departure_time:
                raise ValueError('Invalid flight times, cities, or fare')
            ids.add(flight.flight_no)
            self.data.setdefault(flight.start_city, []).append(flight)
        self.number_of_flights = len(flights)
        self.number_of_cities = len({c for f in flights for c in (f.start_city, f.end_city)})

    def _route(self, start_city, end_city, t1, t2, objective):
        if start_city == end_city or t1 > t2:
            return []
        heap = Heap(lambda a, b: a[0] < b[0])
        best, previous, settled = {}, {}, set()
        def priority(flight, legs, cost):
            if objective == 'earliest':
                return (legs, flight.arrival_time)
            if objective == 'cheapest':
                return (cost,)
            return (legs, cost)
        def offer(flight, legs, cost, parent):
            key = priority(flight, legs, cost)
            fid = flight.flight_no
            if fid not in best or key < best[fid]:
                best[fid] = key
                previous[fid] = parent
                heap.insert((key, flight, legs, cost))
        for flight in self.data.get(start_city, []):
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                offer(flight, 1, flight.fare, None)
        by_id = {f.flight_no: f for f in self.flights}
        while heap.data:
            key, flight, legs, cost = heap.extract()
            fid = flight.flight_no
            if fid in settled or key != best[fid]:
                continue
            settled.add(fid)
            if flight.end_city == end_city:
                route = []
                while fid is not None:
                    route.append(by_id[fid])
                    fid = previous[fid]
                return route[::-1]
            for onward in self.data.get(flight.end_city, []):
                if onward.departure_time >= flight.arrival_time + 20 and onward.arrival_time <= t2 and onward.flight_no not in settled:
                    offer(onward, legs + 1, cost + onward.fare, flight.flight_no)
        return []

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """Minimize flight count, then final arrival time."""
        return self._route(start_city, end_city, t1, t2, 'earliest')

    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """Preserve the original course interface spelling."""
        return self.least_flights_earliest_route(start_city, end_city, t1, t2)

    def cheapest_route(self, start_city, end_city, t1, t2):
        """Minimize total fare."""
        return self._route(start_city, end_city, t1, t2, 'cheapest')

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """Minimize flight count, then total fare."""
        return self._route(start_city, end_city, t1, t2, 'fewest-cheapest')
