
from turtle import distance
from model import Map, Field, Path, Walker


class PathFinder:
    def __init__(self):
        pass
        
    def find_all_paths(self, map, position):
        allPaths = []
        walker = Walker(map.start)
        self._search(map, walker, allPaths, {})
        return allPaths
        
    def _search(self, map, walker, allPaths, distances):
        if walker.get_position() == map.end:
            print("found path")
            return allPaths.append(walker.path.copy())
        
        candidates = map.get_neighbours(walker.get_position())
        currentLen = len(walker.path.fields)
        for candidate in candidates:
            if distances.get(candidate) is None or distances.get(candidate) > currentLen:
                if walker.can_walk(candidate) and not walker.has_walked(candidate):
                    walker.walk(candidate)
                    self._search(map, walker, allPaths, distances)
                    walker.step_back()
        
def manhatten(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

class BruteForcer:
    def __init__(self, map, start):
        self.stack = []
        ns = list(map.get_neighbours(start))
        self.stack.append(ns)
        self.bestPath = None
    
    def step(self, theMap, walker):
        while True:
            if len(self.stack) == 0:
                return
            candidates = self.stack[-1]
            if len(candidates) == 0:
                self.stack.pop()
                walker.step_back()
                return

            candidate = candidates.pop()
            
            if walker.can_walk(candidate) and not walker.has_walked(candidate):
                walker.walk(candidate)
                if walker.get_position() == theMap.end:
                    if self.bestPath == None or self.bestPath.get_length() > walker.path.get_length():
                        self.bestPath = walker.path.copy()
                        print("found path with length " + str(self.bestPath.get_length()))
                    walker.step_back()
                else:
                    ns = list(theMap.get_neighbours(candidate))
                    self.stack.append(ns)
                    return
                
                
class WalkerWithMemory1:
    def __init__(self, map, start):
        self.stack = []
        ns = list(map.get_neighbours(start))
        self.stack.append(ns)
        self.bestPath = None
        self.distance = dict();
    
    def step(self, theMap, walker):
        while True:
            if len(self.stack) == 0:
                return
            candidates = self.stack[-1]
            if len(candidates) == 0:
                self.stack.pop()
                walker.step_back()
                return

            candidate = candidates.pop()
            
            coord = (candidate.x, candidate.y)
            if walker.can_walk(candidate) and not walker.has_walked(candidate) and (self.distance.get(coord) is None or self.distance.get(coord) > walker.path.get_length()):
                #before we step on candiadte, we take note that we have been here with a given path length
                self.distance[coord] = walker.path.get_length()
                walker.walk(candidate)
                if walker.get_position() == theMap.end:
                    if self.bestPath == None or self.bestPath.get_length() > walker.path.get_length():
                        self.bestPath = walker.path.copy()
                        print("found path with length " + str(self.bestPath.get_length()))
                    walker.step_back()
                else:
                    ns = list(theMap.get_neighbours(candidate))
                    
                    
                    
                    self.stack.append(ns)
                    return
        
class OrientationWalker:
    def __init__(self, map, start):
        self.stack = []
        ns = list(map.get_neighbours(start))
        ns = sorted(ns, key=lambda n: manhatten(n.x, n.y, map.end.x, map.end.y))
        self.stack.append(ns)
 
        self.distance = dict();
        self.bestPath = None
    
    def step(self, theMap, walker):
        while True:
            if len(self.stack) == 0:
                return
            candidates = self.stack[-1]
            if len(candidates) == 0:
                self.stack.pop()
                walker.step_back()
                return

            candidate = candidates.pop()
            
            if self.bestPath is not None and self.bestPath.get_length() < walker.path.get_length():
                continue
            
            coordinates = (candidate.x, candidate.y)
            if walker.can_walk(candidate) and not walker.has_walked(candidate) and (self.distance.get(coordinates) is None or self.distance.get(coordinates) > walker.path.get_length()):
                self.distance[coordinates] = walker.path.get_length()
                walker.walk(candidate)
                if walker.get_position() == theMap.end:
                    if self.bestPath == None or self.bestPath.get_length() > walker.path.get_length():
                        self.bestPath = walker.path.copy()
                        print("found path with length " + str(self.bestPath.get_length()))
                    walker.step_back()
                else:
                    ns = list(theMap.get_neighbours(candidate))
                    # sort so the shortes distance will be the last item (because we use pop to get the next candidate)
                    ns = sorted(ns, key=lambda n: -1*manhatten(n.x, n.y, theMap.end.x, theMap.end.y))
                    for n in ns:
                        if walker.can_walk(n):
                            current_dist = self.distance.get((n.x, n.y))
                            if current_dist is None:
                                self.distance[(n.x, n.y)] = walker.path.get_length()+1
                            elif current_dist > walker.path.get_length()+1:
                                self.distance[(n.x, n.y)] = walker.path.get_length()+1
                    self.stack.append(ns)
                    return
        