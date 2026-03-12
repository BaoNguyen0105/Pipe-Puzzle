"""Display module for the pipe-connecting puzzle game.
This module handles the rendering of the game board and the user interface."""

from game import Pipe, Map, MapGenerator, Direction, PipeType
import pygame
from typing import Callable

GRID_SIZE = 128  # Size of each grid cell in pixels


PIPE_ASSETS = {
    'straight-nofill': "assets/straight-nofill.png",
    'corner-nofill': "assets/corner-nofill.png",
    't-nofill': "assets/t-nofill.png",
    'cross-nofill': "assets/cross-nofill.png",
    'sink-nofill': "assets/sink-nofill.png",
    'straight-fill': "assets/straight-fill.png",
    'corner-fill': "assets/corner-fill.png",
    't-fill': "assets/t-fill.png",
    'cross-fill': "assets/cross-fill.png",
    'sink-fill': "assets/sink-fill.png",
    'source': "assets/source.png"
}

def load_assets():
    """Load all necessary assets for the game."""
    loaded_assets = {}
    for key, path in PIPE_ASSETS.items():
        image= pygame.image.load(path).convert_alpha()
        image=pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        loaded_assets[key] = image
    return loaded_assets

def draw_pipe(screen:pygame.Surface, pipe:Pipe, loaded_assets:dict):
    """Draw a pipe on the screen at the specified grid coordinates."""
    if len(pipe.get_openings()) == 4:
        image= loaded_assets['cross-fill'] if pipe.is_filled() else loaded_assets['cross-nofill']

    elif len(pipe.get_openings()) == 3:
        image= loaded_assets['t-fill'] if pipe.is_filled() else loaded_assets['t-nofill']
        if Direction.LEFT not in pipe.get_openings():
            image=pygame.transform.rotate(image, -90)
        elif Direction.UP not in pipe.get_openings():
            image=pygame.transform.rotate(image, -180)
        elif Direction.RIGHT not in pipe.get_openings():
            image=pygame.transform.rotate(image, -270)
    
    elif len(pipe.get_openings()) == 2:
        if Direction.UP in pipe.get_openings() and Direction.RIGHT in pipe.get_openings():
            image= loaded_assets['corner-fill'] if pipe.is_filled() else loaded_assets['corner-nofill']
        elif Direction.RIGHT in pipe.get_openings() and Direction.DOWN in pipe.get_openings():
            image= loaded_assets['corner-fill'] if pipe.is_filled() else loaded_assets['corner-nofill']
            image=pygame.transform.rotate(image, -90)
        elif Direction.DOWN in pipe.get_openings() and Direction.LEFT in pipe.get_openings():
            image= loaded_assets['corner-fill'] if pipe.is_filled() else loaded_assets['corner-nofill']
            image=pygame.transform.rotate(image, -180)
        elif Direction.LEFT in pipe.get_openings() and Direction.UP in pipe.get_openings():
            image= loaded_assets['corner-fill'] if pipe.is_filled() else loaded_assets['corner-nofill']
            image=pygame.transform.rotate(image, -270)
        elif Direction.LEFT in pipe.get_openings() and Direction.RIGHT in pipe.get_openings():
            image= loaded_assets['straight-fill'] if pipe.is_filled() else loaded_assets['straight-nofill']
        elif Direction.UP in pipe.get_openings() and Direction.DOWN in pipe.get_openings():
            image= loaded_assets['straight-fill'] if pipe.is_filled() else loaded_assets['straight-nofill']
            image=pygame.transform.rotate(image, -90)

    elif len(pipe.get_openings()) == 1:
        image= loaded_assets['sink-fill'] if pipe.is_filled() else loaded_assets['sink-nofill']
        if Direction.DOWN in pipe.get_openings():
            image=pygame.transform.rotate(image, -90)
        elif Direction.LEFT in pipe.get_openings():
            image=pygame.transform.rotate(image, -180)
        elif Direction.UP in pipe.get_openings():
            image=pygame.transform.rotate(image, -270)
    x,y = pipe.get_position()
    x,y = x*GRID_SIZE, y*GRID_SIZE
    image_rect=image.get_rect()
    image_rect.center=(x+GRID_SIZE//2, y+GRID_SIZE//2)
    screen.blit(image, image_rect)
    if pipe.get_type() == PipeType.SOURCE:
        source_image = loaded_assets['source']
        source_image_rect = source_image.get_rect()
        source_image_rect.center = image_rect.center
        screen.blit(source_image, source_image_rect)

def display_game(map:Map, update:Callable[[Map],None]=None, fps:float=5):
    """Display the game board and user interface using Pygame.

    @param map: The Map object representing the game board
    @param update: An optional callback function that takes the Map object as an argument and updates the game state. This function will be called once per frame.
    *If none is provided, the game will update in response to user interactions (i.e. rotating pipes).*
    @param fps: The frames per second for the game loop (default is 5)
    """
    #TODO: Implement the display function to render the game board and handle user interactions.
    map_width, map_height = map.get_map_size()
    screen_width, screen_height = map_width * GRID_SIZE, map_height * GRID_SIZE

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pipe-Connecting Puzzle Game")
    clock = pygame.time.Clock()
    loaded_assets = load_assets()

    running = True
    algorithm=None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and update is None:
                mouse_x, mouse_y = event.pos 
                grid_x = mouse_x // GRID_SIZE
                grid_y = mouse_y // GRID_SIZE
                map.rotate_pipe(grid_x, grid_y)

        screen.fill((255, 255, 255))  # Clear the screen with white background
        # Draw the grid lines
        for x in range(0, screen_width, GRID_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, screen_height))
        for y in range(0, screen_height, GRID_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (screen_width, y))

        for pipe in map.to_list():
            draw_pipe(screen, pipe, loaded_assets)

        
        if update and not algorithm:
            algorithm=update(map)
    
        if algorithm:
            try:
                next(algorithm)
            except StopIteration:
                pass

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    map = MapGenerator.default_map()
    display_game(map,fps=60)
    
