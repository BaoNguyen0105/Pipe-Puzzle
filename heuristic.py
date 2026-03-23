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
    """Calculates mismatch score. Lower is better."""
    mismatches = 0
    for i, openings in enumerate(state):
        x = i // height
        y = i % height
        if y == 0 and Direction.UP in openings: mismatches += 1
        if y == height - 1 and Direction.DOWN in openings: mismatches += 1
        if x == 0 and Direction.LEFT in openings: mismatches += 1
        if x == width - 1 and Direction.RIGHT in openings: mismatches += 1
        if x < width - 1:
            right_openings = state[i + height]
            if (Direction.RIGHT in openings) != (Direction.LEFT in right_openings):
                mismatches += 1
        if y < height - 1:
            down_openings = state[i + 1]
            if (Direction.DOWN in openings) != (Direction.UP in down_openings):
                mismatches += 1
    return mismatches

def is_goal(game_map: Map) -> bool:
    """The goal is reached when ALL pipes on the map are filled with water."""
    return all(pipe.is_filled() for pipe in game_map)

ROTATION_MAP = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP
}

def a_star(game_map: Map):
    """
    A* Search implemented as a generator for step-by-step visualization.
    """
    width, height = game_map.get_map_size()
    initial_state = get_state(game_map)
    counter = itertools.count()
    WEIGHT = 2 
    
    pq = [(get_heuristic(initial_state, width, height) * WEIGHT, 0, next(counter), initial_state, [])]
    visited = {initial_state: 0}

    print("Searching...")

    while pq:
        f, g, _, current_state, path = heapq.heappop(pq)

        apply_state(game_map, current_state)

        yield 

        if get_heuristic(current_state, width, height) <= 2:
            if is_goal(game_map):
                print(f"Solution found in {len(path)} moves!")
                for state in path + [current_state]:
                    apply_state(game_map, state)
                    yield
                return

        for i in range(len(current_state)):
            rotated_openings = tuple(ROTATION_MAP[d] for d in current_state[i])
            neighbor_state = current_state[:i] + (rotated_openings,) + current_state[i+1:]
            
            new_g = g + 1
            if neighbor_state not in visited or new_g < visited[neighbor_state]:
                visited[neighbor_state] = new_g
                h = get_heuristic(neighbor_state, width, height)
                heapq.heappush(pq, (new_g + h * WEIGHT, new_g, next(counter), neighbor_state, path + [neighbor_state]))

    print("No solution exists.")