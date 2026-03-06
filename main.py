from game import MapGenerator
from blind_search import bfs
from heuristic import a_star
from display import display_game

CURRENT_MAP = MapGenerator.default_map()
CURRENT_ALGORITHM = bfs

if __name__ == "__main__":
    display_game(CURRENT_MAP, CURRENT_ALGORITHM)
