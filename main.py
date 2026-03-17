from game import MapGenerator
from blind_search import dfs
from heuristic import a_star
from display import display_game
import time

CURRENT_MAP = MapGenerator.generate_solvable_map(10,10)
CURRENT_ALGORITHM = dfs
if __name__ == "__main__":

    display_game(CURRENT_MAP, CURRENT_ALGORITHM, fps=60)
