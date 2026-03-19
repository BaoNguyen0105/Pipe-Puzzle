"""Heuristic search algorithms for the pipe-connecting puzzle game."""

import heapq
import itertools
from game import Map, PipeType, Direction

def get_state(game_map: Map) -> tuple:
    """Returns the current state as a tuple of pipe openings."""
    return tuple(pipe.get_openings() for pipe in game_map)

def apply_state(game_map: Map, state: tuple) -> None:
    """Applies the tuple state to the map and updates water flow."""
    for pipe, openings in zip(game_map, state):
        pipe._Pipe__openings = openings
    game_map._update_water_flow()

def get_heuristic(state: tuple, width: int, height: int) -> int:
    """
    SUPER FAST HEURISTIC: Counts the number of 'mismatches'.
    Purely mathematical algorithm, no water flow simulation needed.
    """
    mismatches = 0
    for i, openings in enumerate(state):
        x = i // height  # Map's __iter__ loop iterates x first, then y
        y = i % height

        # 1. Penalize if the pipe opens out of the map boundaries (Leaking to outside)
        if y == 0 and Direction.UP in openings: mismatches += 1
        if y == height - 1 and Direction.DOWN in openings: mismatches += 1
        if x == 0 and Direction.LEFT in openings: mismatches += 1
        if x == width - 1 and Direction.RIGHT in openings: mismatches += 1

        # 2. Check horizontal alignment with the right pipe (x + 1)
        if x < width - 1:
            right_openings = state[i + height]
            # If this pipe opens RIGHT, but the other doesn't open LEFT (and vice versa)
            if (Direction.RIGHT in openings) != (Direction.LEFT in right_openings):
                mismatches += 1
        
        # 3. Check vertical alignment with the bottom pipe (y + 1)
        if y < height - 1:
            down_openings = state[i + 1]
            # If this pipe opens DOWN, but the other doesn't open UP (and vice versa)
            if (Direction.DOWN in openings) != (Direction.UP in down_openings):
                mismatches += 1
                
    return mismatches

def is_goal(game_map: Map) -> bool:
    """Check the win condition: all SINKs are filled with water."""
    sinks = [pipe for pipe in game_map if pipe._get_type() == PipeType.SINK]
    return len(sinks) > 0 and all(pipe.is_filled() for pipe in sinks)

# Rotation lookup table to speed up the process (avoids calling class methods)
ROTATION_MAP = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP
}

def a_star(game_map: Map) -> None:
    """Optimized Weighted A* Algorithm for the Pipe Game."""
    
    if not hasattr(a_star, "solved"):
        a_star.solved = False
        a_star.solution_path = []

    # Pipe rotation animation once solved
    if a_star.solved:
        if a_star.solution_path:
            next_state = a_star.solution_path.pop(0)
            apply_state(game_map, next_state)
        return

    print("Solving with Optimized A* (Please wait)...")
    initial_state = get_state(game_map)
    width, height = game_map.get_map_size()
    
    counter = itertools.count() 
    
    # WEIGHT: Converts A* into Weighted A*
    # Increasing the heuristic weight makes the algorithm more greedy.
    WEIGHT = 2 
    
    initial_h = get_heuristic(initial_state, width, height)
    pq = [(initial_h * WEIGHT, 0, next(counter), initial_state, [])]
    visited = set()

    while pq:
        f, g, _, current_state, path = heapq.heappop(pq)

        if current_state in visited:
            continue
        visited.add(current_state)

        # LAZY EVALUATION
        current_h = get_heuristic(current_state, width, height)
        # Only update actual water simulation if the "leak" (current_h) is extremely low
        if current_h <= 2: 
            apply_state(game_map, current_state)
            if is_goal(game_map):
                print(f"Solved in {len(path)} moves!")
                a_star.solved = True
                a_star.solution_path = path + [current_state]
                apply_state(game_map, initial_state) 
                return

        # Generate next states (Neighbors)
        for i in range(len(current_state)):
            # STATIC ROTATION: Create a new tuple by replacing the i-th pipe's openings
            old_openings = current_state[i]
            new_openings = tuple(ROTATION_MAP[d] for d in old_openings)
            
            # Extremely fast tuple slicing and concatenation
            new_state = current_state[:i] + (new_openings,) + current_state[i+1:]
            
            if new_state not in visited:
                h = get_heuristic(new_state, width, height)
                # Evaluation formula f = g + W * h
                heapq.heappush(pq, (g + 1 + h * WEIGHT, g + 1, next(counter), new_state, path + [new_state]))

    print("No solution found.")
    a_star.solved = True
    apply_state(game_map, initial_state)