import heapq
from typing import Dict, List, Tuple, Set
import math

class AStarSearch:
    """
    A* Search algorithm for optimizing path resources.
    Finds the path with minimum total cost (distance/time/resources).
    """
    
    def __init__(self):
        self.nodes = {}  # Graph representation
        self.heuristics = {}  # Heuristic values (estimated cost to goal)
    
    def add_edge(self, from_node: str, to_node: str, cost: float):
        """Add bidirectional edge between nodes with given cost"""
        if from_node not in self.nodes:
            self.nodes[from_node] = []
        if to_node not in self.nodes:
            self.nodes[to_node] = []
        
        self.nodes[from_node].append((to_node, cost))
        self.nodes[to_node].append((from_node, cost))
    
    def set_heuristic(self, node: str, estimated_cost: float):
        """Set heuristic value (estimated cost from node to goal)"""
        self.heuristics[node] = estimated_cost
    
    def a_star_search(self, start: str, goal: str) -> Tuple[List[str], float, Dict]:
        """
        Execute A* search from start to goal.
        Returns: (path, total_cost, statistics)
        """
        
        # Priority queue: (f_score, counter, node, g_score, path)
        # f_score = g_score (actual cost) + h_score (heuristic)
        open_set = [(self.heuristics.get(start, 0), 0, start, 0, [start])]
        counter = 1  # For tie-breaking
        
        # Track best g_scores (actual cost from start)
        g_scores = {start: 0}
        
        # Track visited nodes with their best f_scores
        visited = {}
        
        # Statistics tracking
        stats = {
            'nodes_explored': 0,
            'open_set_size': 0,
            'max_open_set_size': 0
        }
        
        while open_set:
            # Get node with smallest f_score
            f_score, _, current, g_score, path = heapq.heappop(open_set)
            
            stats['nodes_explored'] += 1
            stats['open_set_size'] = len(open_set)
            stats['max_open_set_size'] = max(stats['max_open_set_size'], len(open_set))
            
            # Goal check
            if current == goal:
                return path, g_score, stats
            
            # Skip if we found a better path to this node already
            if current in visited and visited[current] < f_score:
                continue
            
            visited[current] = f_score
            
            # Explore neighbors
            for neighbor, edge_cost in self.nodes.get(current, []):
                tentative_g_score = g_score + edge_cost
                
                # If this is a better path to neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g_score
                    
                    # Calculate f_score = g_score + heuristic
                    h_score = self.heuristics.get(neighbor, 0)
                    f_score_new = tentative_g_score + h_score
                    
                    # Add to open set
                    new_path = path + [neighbor]
                    heapq.heappush(open_set, (f_score_new, counter, neighbor, 
                                              tentative_g_score, new_path))
                    counter += 1
        
        # No path found
        return [], float('inf'), stats
    
    def find_optimal_resource_path(self, start: str, goal: str, 
                                   resource_weights: Dict[str, float] = None):
        """
        Find path optimizing multiple resource constraints.
        Resources could be: distance, time, fuel, cost, etc.
        """
        # If resource weights are provided, adjust edge costs
        if resource_weights:
            original_costs = {}
            for node in self.nodes:
                for i, (neighbor, cost) in enumerate(self.nodes[node]):
                    key = f"{node}-{neighbor}"
                    if key not in original_costs:
                        original_costs[key] = cost
                        # Apply resource weight multiplier
                        weight = resource_weights.get('distance', 1.0)
                        self.nodes[node][i] = (neighbor, cost * weight)
        
        return self.a_star_search(start, goal)


# Example usage and demonstration
def demonstrate_astar():
    """Demonstrate A* search with a real-world example"""
    
    print("=" * 70)
    print("A* SEARCH PATH OPTIMIZATION DEMONSTRATION")
    print("=" * 70)
    
    # Create A* search instance
    astar = AStarSearch()
    
    # Create a graph of a city map (nodes represent locations)
    edges = [
        ("Home", "Market", 5), ("Home", "School", 8), ("Home", "Hospital", 10),
        ("Market", "School", 3), ("Market", "Park", 4), ("Market", "Hospital", 7),
        ("School", "Park", 6), ("School", "Mall", 9), ("School", "Hospital", 5),
        ("Park", "Mall", 4), ("Park", "Library", 3), ("Park", "Hospital", 8),
        ("Mall", "Library", 5), ("Mall", "Hospital", 6), ("Mall", "Office", 7),
        ("Library", "Office", 4), ("Library", "Hospital", 9), ("Library", "Museum", 3),
        ("Office", "Museum", 5), ("Office", "Hospital", 8), ("Office", "Airport", 10),
        ("Museum", "Airport", 6), ("Museum", "Hospital", 12), ("Hospital", "Airport", 15),
        ("Park", "Zoo", 7), ("Zoo", "Airport", 9),
    ]
    
    for from_node, to_node, cost in edges:
        astar.add_edge(from_node, to_node, cost)
    
    # Set heuristic values (straight-line distances or estimated costs to goal "Airport")
    heuristic_values = {
        "Home": 25, "Market": 22, "School": 20, "Park": 15, "Mall": 12,
        "Library": 10, "Hospital": 18, "Office": 8, "Museum": 6, "Zoo": 9,
        "Airport": 0  # Goal has heuristic 0
    }
    
    for node, h_val in heuristic_values.items():
        astar.set_heuristic(node, h_val)
    
    # Find optimal path from Home to Airport
    print("\n Scenario: Find optimal route from HOME to AIRPORT")
    print("-" * 70)
    
    path, total_cost, stats = astar.find_optimal_resource_path("Home", "Airport")
    
    print(f"\n OPTIMAL PATH FOUND:")
    print(f"   {' → '.join(path)}")
    print(f"\n TOTAL COST: {total_cost} units")
    print(f"\n SEARCH STATISTICS:")
    print(f"   - Nodes explored: {stats['nodes_explored']}")
    print(f"   - Max open set size: {stats['max_open_set_size']}")
    
    # Multi-resource optimization example
    print("\n" + "=" * 70)
    print("MULTI-RESOURCE OPTIMIZATION")
    print("-" * 70)
    print("Optimizing for: Distance (priority 1.0), Time (priority 1.5)")
    
    resource_weights = {'distance': 1.0, 'time': 1.5}
    path2, cost2, stats2 = astar.find_optimal_resource_path("Home", "Airport", 
                                                            resource_weights)
    
    print(f"\n OPTIMIZED PATH:")
    print(f"   {' → '.join(path2)}")
    print(f"   Weighted cost: {cost2}")
    
    return astar


# Run demonstration
if __name__ == "__main__":
    astar = demonstrate_astar()