#  GRAPH SEARCH ALGORITHMS — Breadth-First Search & Depth-First Search
#  Both algorithms explore a graph to find a path from a START node to a GOAL node and print every step taken along the way.
#  Graph used (undirected):
#
#       A
#      / \
#     B   C
#    / \   \
#   D   E   F
#        \
#         G   ← GOAL
 
from collections import deque   # deque gives O(1) popleft(), used by BFS
 
 
# Graph definition (adjacency list) 
# Each key is a node; its value is an ordered list of neighbouring nodes.
# The order determines which neighbour is visited first.
 
GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "G"],
    "F": ["C"],
    "G": ["E"],        # G is the goal — still needs neighbours for completeness
}
 
START = "A"
GOAL  = "G"
 
#  BREADTH-FIRST SEARCH (BFS)
#
#  Strategy : explore all nodes at depth d before any node at depth d+1.
#  Data structure : QUEUE (FIFO) — the node added earliest is explored first.

#  Why a queue?
#    Nodes are enqueued in the order they are discovered.  Popping from the
#    front guarantees we always expand the shallowest un-visited node next,
#    which is what produces the SHORTEST PATH (fewest edges).

#  Time  complexity : O(V + E)   — V nodes, E edges
#  Space complexity : O(V)       — worst case every node sits in the queue

def bfs(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Perform Breadth-First Search on `graph` from `start` to `goal`.
 
    Each entry in the queue is a PATH (list of nodes) rather than a single
    node.  This lets us reconstruct the full route without a separate
    'parent' dictionary.
 
    Returns the path as a list of node names, or None if unreachable.
    """
 
    print("=" * 60)
    print("  BREADTH-FIRST SEARCH (BFS)")
    print("=" * 60)
    print(f"  Start : {start}  |  Goal : {goal}\n")
 
    # Initialise 
    queue   = deque([[start]])   # queue holds complete paths, seed with [start]
    visited = set()              # tracks nodes already expanded (not re-visited)
 
    step = 1   # step counter for readable output
 
    # Main loop
    while queue:
 
        # Dequeue the OLDEST (leftmost) path — FIFO order
        current_path = queue.popleft()
        current_node = current_path[-1]   # the node we are currently examining
 
        print(f"  Step {step:>2}: Dequeue  node '{current_node}'  |  "
              f"Path so far: {' → '.join(current_path)}")
 
        # Goal test 
        if current_node == goal:
            print(f"\n  ✔ Goal '{goal}' reached!\n")
            return current_path          # return the winning path immediately
 
        # Skip already-visited nodes 
        if current_node in visited:
            print(f"          └─ Already visited — skip.")
            step += 1
            continue
 
        visited.add(current_node)        # mark as visited AFTER the goal check
                                         # (so the goal itself is also marked)
 
        # Expand neighbours 
        neighbours = graph.get(current_node, [])
        unvisited  = [n for n in neighbours if n not in visited]
 
        print(f"          └─ Neighbours: {neighbours}  |  "
              f"Enqueuing unvisited: {unvisited}")
 
        for neighbour in unvisited:
            new_path = current_path + [neighbour]   # extend path by one hop
            queue.append(new_path)                  # enqueue at the BACK
 
        step += 1
 
    # Queue exhausted without finding the goal
    print(f"\n  ✘ Goal '{goal}' is NOT reachable from '{start}'.\n")
    return None
 
 
#  DEPTH-FIRST SEARCH (DFS)
#
#  Strategy : follow one branch as deep as possible before backtracking.
#  Data structure : STACK (LIFO) — the most-recently added node is tried first.
#
#  Why a stack?
#    Pushing neighbours onto a stack means the last neighbour added is popped
#    next, driving the search deeper along one branch before exploring others.
#    This does NOT guarantee the shortest path.

#  Time  complexity : O(V + E)
#  Space complexity : O(V)       — worst case the entire path is on the stack
 
def dfs(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Perform Depth-First Search on `graph` from `start` to `goal`.
 
    Uses an explicit stack of (node, path) tuples — iterative rather than
    recursive, so it works on arbitrarily deep graphs without hitting Python's
    default recursion limit (~1000).
 
    Returns the path as a list of node names, or None if unreachable.
    """
 
    print("=" * 60)
    print("  DEPTH-FIRST SEARCH (DFS)")
    print("=" * 60)
    print(f"  Start : {start}  |  Goal : {goal}\n")
 
    # Initialise 
    # Stack entries: (current_node, path_taken_to_reach_it)
    stack   = [(start, [start])]
    visited = set()
 
    step = 1
 
    # Main loop
    while stack:
 
        # Pop from the TOP of the stack — LIFO order (go deeper first)
        current_node, current_path = stack.pop()
 
        print(f"  Step {step:>2}: Pop      node '{current_node}'  |  "
              f"Path so far: {' → '.join(current_path)}")
 
        # Goal test 
        if current_node == goal:
            print(f"\n  ✔ Goal '{goal}' reached!\n")
            return current_path
 
        # Skip already-visited nodes 
        if current_node in visited:
            print(f"          └─ Already visited — skip.")
            step += 1
            continue
 
        visited.add(current_node)
 
        # Expand neighbours 
        neighbours = graph.get(current_node, [])
        unvisited  = [n for n in neighbours if n not in visited]
 
        # Push in REVERSE order so that the first neighbour in the list is
        # popped first (top of stack = leftmost neighbour = consistent order)
        push_order = list(reversed(unvisited))
 
        print(f"          └─ Neighbours: {neighbours}  |  "
              f"Pushing (reversed): {push_order}")
 
        for neighbour in push_order:
            new_path = current_path + [neighbour]
            stack.append((neighbour, new_path))   # push onto TOP of stack
 
        step += 1
 
    print(f"\n  ✘ Goal '{goal}' is NOT reachable from '{start}'.\n")
    return None
 
def print_result(algorithm: str, path: list[str] | None) -> None:
    print("-" * 60)
    if path:
        print(f"  {algorithm} final path  ({len(path) - 1} edge(s)):")
        print(f"    {' → '.join(path)}")
    else:
        print(f"  {algorithm}: no path found.")
    print("-" * 60)
    print()
 
#  MAIN
 
if __name__ == "__main__":
 
    # Run BFS 
    bfs_path = bfs(GRAPH, START, GOAL)
    print_result("BFS", bfs_path)
 
    # Run DFS 
    dfs_path = dfs(GRAPH, START, GOAL)
    print_result("DFS", dfs_path)
 
    # Side-by-side comparison
    print("=" * 60)
    print("  COMPARISON")
    print("=" * 60)
    print(f"  BFS path : {' → '.join(bfs_path) if bfs_path else 'None'}")
    print(f"  DFS path : {' → '.join(dfs_path) if dfs_path else 'None'}")
    print()
    print("  BFS always finds the SHORTEST path (fewest edges).")
    print("  DFS finds A path, but not necessarily the shortest.")
    print("=" * 60)
