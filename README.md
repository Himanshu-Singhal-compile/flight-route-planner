# Flight Route Planner

A dependency-free Python route planner for scheduled flights, with three optimization policies and a minimum connection-time constraint.

[![CI](https://github.com/Himanshu-Singhal-compile/flight-route-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/Himanshu-Singhal-compile/flight-route-planner/actions/workflows/ci.yml)


## Route policies

| Method | Primary goal | Tie breaker |
| --- | --- | --- |
| `least_flights_earliest_route` | Fewest flights | Earliest final arrival |
| `cheapest_route` | Lowest total fare | Any optimal route |
| `least_flights_cheapest_route` | Fewest flights | Lowest total fare |

All routes depart at or after `t1`, arrive at or before `t2`, and allow at least 20 minutes between connections. Empty results mean no feasible route, or no travel is needed. The original misspelled `least_flights_ealiest_route` remains as a compatibility alias.

## Quick start

Python 3.10 or newer; no third-party runtime dependencies.

```sh
git clone https://github.com/Himanshu-Singhal-compile/flight-route-planner.git
cd flight-route-planner
python main.py
python -m unittest discover -s tests -v
```

The sample prints `Task 1 PASSED`, `Task 2 PASSED`, and `Task 3 PASSED`.

```python
from flight import Flight
from planner import Planner

flights = [
    Flight(10, 0, 0, 1, 30, 50),
    Flight(20, 1, 50, 2, 80, 70),
    Flight(30, 0, 10, 2, 90, 150),
]
planner = Planner(flights)
route = planner.cheapest_route(0, 2, 0, 100)
print([f.flight_no for f in route])  # [10, 20]
print(sum(f.fare for f in route))   # 120
```

## Architecture

Cities map to outgoing flights. Each query explores flight states with a custom binary min-heap. Labels store the appropriate cost or lexicographic objective; predecessor IDs reconstruct the itinerary. Query state is local, allowing repeated calls without modifying `Flight` objects. For F flights and E feasible connections, the implementation uses approximately O((F + E) log(F + E)) time and O(F + E) worst-case space including queued candidates.

Flight IDs must be unique; sparse IDs are supported. Cities, fares, and departure times are non-negative integers; arrival must not precede departure. Time is an abstract minute count, without time zones, calendars, airports, or real airline integrations. Equal-optimal routes have no guaranteed ordering.

## Validation

Regression tests compare all three policies against exhaustive route enumeration on 200 seeded random schedules, plus connection boundaries, empty schedules, and invalid IDs. The sample schedule is also checked. Packaging corrects the original arrival/fare tie breaking and removes shared predecessor mutation.

| Path | Purpose |
| --- | --- |
| `planner.py` | Route optimization and reconstruction |
| `flight.py` | Flight record |
| `heap.py` | Custom comparison-based binary heap |
| `myQueue.py` | Original linked queue, retained as a data-structure example |
| `main.py` | Demonstration schedule |
| `tests/` | Exhaustive-oracle regression tests |


