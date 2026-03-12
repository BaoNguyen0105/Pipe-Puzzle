"""Blind search algorithms for the pipe-connecting puzzle game."""

from game import Map, Pipe, Direction, MapGenerator

def get_source(map:Map):
    """Find the source pipe in the map."""
    for pipe in map.to_list():
        if pipe.is_source():
            return pipe
    return None

def is_finished(map:Map):
    """Check if the puzzle is solved by verifying if every pipe is filled"""
    for pipe in map.to_list():
        if not pipe.is_filled():
            return False
    return True

def valid(pipe:Pipe, map:Map):
    openings=pipe.get_openings()
    x, y = pipe.get_position()
    adjacents=pipe.get_adjacent_pipes()
    width, height=map.get_map_size()
    if x==0 and Direction.LEFT in openings:
        return False
    if x==width-1 and Direction.RIGHT in openings:
        return False
    if y==0 and Direction.UP in openings:
        return False
    if y==height-1 and Direction.DOWN in openings:
        return False
    if pipe.is_sink():
        for dir,adjecent in adjacents.items():
            if adjecent.is_sink() and pipe.connected(adjecent, dir):
                return False
    # if Direction.UP in adjacents and not pipe.connected(adjacents[Direction.UP], Direction.UP):
    #     return False
    # if Direction.LEFT in adjacents and not pipe.connected(adjacents[Direction.LEFT], Direction.LEFT):
    #     return False
    return True



def is_edge_position(x,y, width, height):
    return x==0 or y==0 or x==width-1 or y==height-1


def is_corner_position(x,y, width, height):
    return is_edge_position(x, -1, width, height) and is_edge_position(-1, y, width, height)
        

def get_trivial_pipes(map:Map):
    """Trivial pipes are pipes with only one possible rotation, such as:
    Corner pipes in the corner
    Straight pipes on the edge
    T pipes on the edge
    """
    ret:list[Pipe]=[]
    for pipe in map.to_list():
        x, y =pipe.get_position()
        width, height = map.get_map_size()

        if is_corner_position(x,y,width, height) and pipe.is_corner():
            ret.append(pipe)
        elif is_edge_position(x,y,width, height) and pipe.is_straight():
            ret.append(pipe)
        elif is_edge_position(x,y,width, height) and pipe.is_t():
            ret.append(pipe)
    return ret

def rotate_trivial_pipes(map:Map, trivial_pipes:list[Pipe]):
    for pipe in trivial_pipes:
        while True:
            openings=pipe.get_openings()
            x, y = pipe.get_position()
            width, height=map.get_map_size()
            if x==0 and Direction.LEFT in openings:
                yield pipe.rotate()
                continue
            if x==width-1 and Direction.RIGHT in openings:
                yield pipe.rotate()
                continue
            if y==0 and Direction.UP in openings:
                yield pipe.rotate()
                continue
            if y==height-1 and Direction.DOWN in openings:
                yield pipe.rotate()
                continue

            break
    return


def dfs(map:Map):
    """Depth-First Search algorithm to solve the puzzle."""
    trivial_pipes=get_trivial_pipes(map)
    for _ in rotate_trivial_pipes(map, trivial_pipes):
        pass

    pipe_list = map.to_list()
    def recur(index=0):
        if index >= len(pipe_list):
            return
        pipe = pipe_list[index]
        if pipe in trivial_pipes:
            yield from recur(index+1)
            return
        for _ in range(4):
            if is_finished(map):
                return
            if valid(pipe, map):
                yield from recur(index+1)
            if is_finished(map):
                return
            yield pipe.rotate()
            
        
    yield from recur()

