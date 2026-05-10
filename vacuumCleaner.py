import random
from enum import Enum
from typing import Dict, Tuple, List

class Location(Enum):
    """Possible locations in the environment"""
    A = "Room A"
    B = "Room B"
    C = "Room C"

class Action(Enum):
    """Possible actions the vacuum can take"""
    MOVE_LEFT = "Moving Left"
    MOVE_RIGHT = "Moving Right"
    SUCK = "Sucking dirt"
    IDLE = "Idle"

class VacuumEnvironment:
    """Environment containing rooms that can be dirty or clean"""
    
    def __init__(self, rooms: List[Location], initial_dirt: Dict[Location, bool]):
        """
        Initialize environment
        rooms: List of all rooms
        initial_dirt: Which rooms start dirty (True = dirty)
        """
        self.rooms = rooms
        self.dirt_status = initial_dirt.copy()
        self.total_dirt_collected = 0
        self.performance_score = 0
        
    def is_dirty(self, location: Location) -> bool:
        """Check if a specific room is dirty"""
        return self.dirt_status.get(location, False)
    
    def clean(self, location: Location) -> int:
        """Clean the specified room. Returns dirt collected (0 or 1)"""
        if self.dirt_status.get(location, False):
            self.dirt_status[location] = False
            self.total_dirt_collected += 1
            return 1
        return 0
    
    def all_clean(self) -> bool:
        """Check if all rooms are clean"""
        return not any(self.dirt_status.values())
    
    def get_performance(self) -> float:
        """Calculate current performance (percentage of dirt cleaned)"""
        if self.total_dirt_collected == 0:
            return 0.0
        return (self.total_dirt_collected / len(self.rooms)) * 100

class SimpleVacuumCleaner:
    """
    Simple reflex agent for vacuum cleaning.
    Implements a model-based reflex agent with state tracking.
    """
    
    def __init__(self, start_location: Location):
        """Initialize the vacuum cleaner"""
        self.current_location = start_location
        self.actions_taken = []
        self.total_moves = 0
        self.total_sucks = 0
        
        # Track visited rooms to optimize cleaning
        self.visited_rooms = set()
        self.cleaning_history = []
        
    def perceive(self, environment: VacuumEnvironment) -> Tuple[Location, bool]:
        """Sense current location and dirt status"""
        is_dirty = environment.is_dirty(self.current_location)
        return self.current_location, is_dirty
    
    def act(self, percept: Tuple[Location, bool], environment: VacuumEnvironment) -> Action:
        """
        Decide action based on percept (location, dirt status)
        Simple reflex logic:
        - If current room is dirty -> SUCK
        - Else -> MOVE to next room
        """
        location, is_dirty = percept
        action = None
        
        # Track visited rooms
        self.visited_rooms.add(location)
        
        # Reflex rule: Clean if dirty, otherwise move
        if is_dirty:
            action = Action.SUCK
            self.total_sucks += 1
        else:
            # Move to next room (simple deterministic movement)
            rooms = environment.rooms
            current_idx = rooms.index(location)
            
            # Move to next room cyclically
            next_idx = (current_idx + 1) % len(rooms)
            next_location = rooms[next_idx]
            
            # Determine direction
            if next_idx > current_idx:
                action = Action.MOVE_RIGHT
            elif next_idx < current_idx:
                action = Action.MOVE_LEFT
            else:
                action = Action.MOVE_RIGHT  # Default
            
            self.current_location = next_location
            self.total_moves += 1
        
        # Record action
        self.actions_taken.append(action)
        self.cleaning_history.append({
            'step': len(self.actions_taken),
            'location': location.value,
            'action': action.value,
            'dirty': is_dirty
        })
        
        return action
    
    def run(self, environment: VacuumEnvironment, max_steps: int = 100):
        """
        Run the vacuum cleaner agent in the environment
        max_steps: Maximum steps before stopping
        """
        print("=" * 80)
        print("VACUUM CLEANER AGENT SIMULATION")
        print("=" * 80)
        print(f"\nStarting location: {self.current_location.value}")
        print(f"Initial dirt: {[loc.value for loc, dirty in environment.dirt_status.items() if dirty]}")
        print("-" * 80)
        
        step = 0
        while step < max_steps and not environment.all_clean():
            # Perceive current state
            percept = self.perceive(environment)
            
            # Act based on percept
            action = self.act(percept, environment)
            
            # Execute action in environment
            if action == Action.SUCK:
                dirt_collected = environment.clean(percept[0])
                if dirt_collected > 0:
                    print(f"Step {step+1:3d}: {action.value} at {percept[0].value} ✓")
                else:
                    print(f"Step {step+1:3d}: {action.value} at {percept[0].value} - No dirt")
            else:
                print(f"Step {step+1:3d}: {action.value} → Now at {self.current_location.value}")
            
            step += 1
        
        # Simulation complete
        print("-" * 80)
        self.display_results(environment, step)
        
    def display_results(self, environment: VacuumEnvironment, steps_taken: int):
        """Display performance statistics"""
        print("\n" + "=" * 80)
        print("SIMULATION RESULTS")
        print("=" * 80)
        
        print(f"\n PERFORMANCE METRICS:")
        print(f"   • Total steps taken: {steps_taken}")
        print(f"   • Moves performed: {self.total_moves}")
        print(f"   • Suck actions: {self.total_sucks}")
        print(f"   • Rooms visited: {len(self.visited_rooms)}/{len(environment.rooms)}")
        print(f"   • Dirt collected: {environment.total_dirt_collected}/{len(environment.rooms)}")
        print(f"   • Performance score: {environment.get_performance():.1f}%")
        
        print(f"\n FINAL ROOM STATUS:")
        for room in environment.rooms:
            status = " DIRTY" if environment.is_dirty(room) else " CLEAN"
            print(f"   • {room.value}: {status}")
        
        print(f"\n Goal achieved: {'YES' if environment.all_clean() else 'NO'}")
        
        # Action summary
        print(f"\n ACTION SUMMARY:")
        from collections import Counter
        action_counts = Counter([a.value for a in self.actions_taken])
        for action, count in action_counts.items():
            print(f"   • {action}: {count} times")


# Run the simulation
def run_vacuum_simulation():
    """Execute vacuum cleaner demonstration"""
    
    # Define environment
    rooms = [Location.A, Location.B, Location.C]
    
    # Random initial dirt (or specify manually)
    initial_dirt = {
        Location.A: True,   # Room A starts dirty
        Location.B: True,   # Room B starts dirty
        Location.C: False   # Room C starts clean
    }
    
    # Create environment
    env = VacuumEnvironment(rooms, initial_dirt)
    
    # Create vacuum cleaner agent (start in Room A)
    vacuum = SimpleVacuumCleaner(Location.A)
    
    # Run simulation
    vacuum.run(env, max_steps=20)
    
    # Test with different starting conditions
    print("\n" + "=" * 80)
    print("ADDITIONAL TEST: DIFFERENT INITIAL CONDITIONS")
    print("=" * 80)
    
    # Test 2: All rooms dirty
    env2 = VacuumEnvironment(rooms, {Location.A: True, Location.B: True, Location.C: True})
    vacuum2 = SimpleVacuumCleaner(Location.C)  # Start in Room C
    print("\nTest Case: All rooms dirty, starting in Room C")
    vacuum2.run(env2, max_steps=15)


# Run the simulation
if __name__ == "__main__":
    run_vacuum_simulation()