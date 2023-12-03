
import pytest
import sys
from src.model import Map, Field, Path 
from src.PathFinder import RecursivePathFinder

def test_create_a_minimal_complex_twoline_map_from_string():
    # GIVEN a multiline string
    map_string = """\
SaE
"""
    # WHEN creating a map from the string
    world = Map.from_string(map_string)
    world.end.elevation = 0
    
    pathfinder = RecursivePathFinder()
    allPaths = pathfinder.find_all_paths(world, world.start)
    print(allPaths)
    print(1)
