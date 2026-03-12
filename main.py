from game import MapGenerator
from blind_search import dfs
from heuristic import a_star
from display import display_game
import time

CURRENT_MAP = MapGenerator.default_map_3()
CURRENT_ALGORITHM = dfs

if __name__ == "__main__":
    display_game(CURRENT_MAP, CURRENT_ALGORITHM, fps=10)
