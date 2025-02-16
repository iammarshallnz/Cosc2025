from dataclasses import dataclass
from typing import Dict, List, Tuple
import time

INFINITY = 16
TIMEOUT = 180  # 3 minutes
GARBAGE_COLLECTION = 120  # 2 minutes
UPDATE_INTERVAL = 30  # 30 seconds

@dataclass
class Route:
    destination: int
    next_hop: int
    metric: int
    last_update: float
    garbage_timer: float = 0

class RoutingTable:
    def __init__(self, router_id: int):
        self.router_id = router_id
        self.routes: Dict[int, Route] = {}
        
    def add_route(self, destination: int, next_hop: int, metric: int):
        if metric >= INFINITY:
            return
        
        self.routes[destination] = Route(
            destination=destination,
            next_hop=next_hop,
            metric=metric,
            last_update=time.time()
        )

    def get_routes(self) -> List[Route]:
        return list(self.routes.values())

    def update_route(self, destination: int, next_hop: int, metric: int) -> bool:
        """Returns True if route was updated"""
        current = self.routes.get(destination)
        
        if not current or current.next_hop == next_hop:
            self.add_route(destination, next_hop, metric)
            return True
            
        if metric < current.metric:
            self.add_route(destination, next_hop, metric)
            return True
            
        return False

    def check_timeouts(self):
        """Check for route timeouts and mark for garbage collection"""
        current_time = time.time()
        
        for route in list(self.routes.values()):
            if route.garbage_timer > 0:
                if current_time - route.garbage_timer > GARBAGE_COLLECTION:
                    del self.routes[route.destination]
            elif current_time - route.last_update > TIMEOUT:
                route.metric = INFINITY
                route.garbage_timer = current_time
