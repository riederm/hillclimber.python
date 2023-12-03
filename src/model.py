import sys

class Field:
    # Field class represents a single field on the map
    def __init__(self, x, y, elevation):
        # Initialize the field's position and elevation
        self.x = x
        self.y = y
        self.elevation = elevation

    def __repr__(self):
        # Return a string representation of the field
        return f'Field(x={self.x}, y={self.y}, elevation={self.elevation})'

    def __eq__(self, other):
        # Return True if the fields are equal, False otherwise
        return self.x == other.x and self.y == other.y and self.elevation == other.elevation

class Map:
    # Map class represents a 2D map of fields
    def __init__(self):
        # Initialize an empty list of fields
        self.fields = {}
        self.height = 0
        self.width = 0
        self.start = None
        self.end = None

    def set_start(self, x, y):
        # Set the start field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        if self.start:
            raise Exception("Multiple starting points detected!")
        self.start = self.get_field(x, y)

    def set_end(self, x, y):
        # Set the end field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        if self.end:
            raise Exception("Multiple ending points detected!")
        self.end = self.get_field(x, y)

    def add_field(self, x, y, elevation):
        # Add a new field to the map with given x, y coordinates and elevation
        f = Field(x, y, elevation)
        self.fields[(x,y)] = f
        self.height = max(self.height, y+1)
        self.width = max(self.width, x+1)
        return f

    def get_field(self, x, y):
        # Get the field at given x, y coordinates
        if (x,y) in self.fields:
            return self.fields[(x,y)]
        else:
            return Field(x, y, sys.maxsize)

    def get_neighbours(self, field):
        # Get a list of available neighbouring fields (N, S, W, E) of the given field
        # if they are not on the map, they are not available
        return (
            self.get_field(field.x+0,field.y-1), #N
            self.get_field(field.x+0,field.y+1), #S
            self.get_field(field.x-1,field.y-0), #W
            self.get_field(field.x+1,field.y-0)  #E
        )

    @staticmethod
    def from_string(map_string):
        map = Map()
        # Static method to create a Map object from a multiline string
        for y, line in enumerate(map_string.splitlines()):
            for x, char in enumerate(line):
                match  char:
                    case 'S':
                        map.add_field(x, y, 0)
                        map.set_start(x, y)
                    case 'E':
                        map.add_field(x, y, 25)
                        map.set_end(x, y)
                    case _:
                        if (char.isalpha() and char.islower()):
                            map.add_field(x, y, ord(char)-ord('a'))
                        else:
                            raise Exception(f"Invalid cell detected at {(x, y)}!")

        return map

class Walker:
    # Walker class represents a walker with a position on the map
    def __init__(self, position):
        # Initialize the walker's position
        self.path = Path()
        self.path.add_step(position)
        
    def walk(self, field):
        # Move the walker to the given field
        self.path.add_step(field)
        
    def step_back(self):
        # Move the walker back to the previous field
        self.path.remove_last_step()
        
    def get_position(self):
        # Return the walker's current position
        return self.path.get_last_step()
    
    def has_walked(self, field):
        # Return True if the walker has walked on the given field, False otherwise
        return self.path.field_visited(field)
    
    def can_walk(self, field):
        # Return True if the walker can walk to the given field, False otherwise
        return field.elevation - self.get_position().elevation <= 1

class Path:
    # Path class represents a sequence of fields forming a path on the map
    def __init__(self):
        # Initialize an empty list of fields
        self.fields = []
        self.fieldSet = set()

    def add_step(self, field):
        # Add a new step to the path
        self.fields.append(field)
        self.fieldSet.add((field.x, field.y))

    def remove_last_step(self):
        # Remove the last step from the path
        if self.fields:
            f = self.fields.pop()
            self.fieldSet.remove((f.x, f.y))
            
    def get_length(self):
        # returns the number of steps in this path
        return len(self.fields)
    
    def field_visited(self, field):
        return (field.x, field.y) in self.fieldSet
    
    def get_last_step(self):
        return self.fields[-1]

    def copy(self):
        # returns a copy of this path
        p = Path()
        p.fields = self.fields.copy()
        p.fieldSet = self.fieldSet.copy()
        return p
    
    def __repr__(self):
        # Return a string representation of the path
        return f'Path({self.fields})'
