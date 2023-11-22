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

    def set_start(self, x, y):
        # Set the start field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        self.start = self.get_field(x, y)

    def set_end(self, x, y):
        # Set the end field at given x, y coordinates
        # dont forget to make sure that this field was added to the map prior
        # to calling this method (otherwise you will get a KeyError)
        self.end = self.get_field(x, y)

    def add_field(self, x, y, elevation):
        # Add a new field to the map with given x, y coordinates and elevation
        self.fields[(x,y)] = Field(x, y, elevation)

    def get_field(self, x, y):
        # Get the field at given x, y coordinates
        return self.fields[(x,y)]

    def get_neighbours(self, field):
        # Get a list of available neighbouring fields (N, S, W, E) of the given field
        # if they are not on the map, they are not available
        pass

    @staticmethod
    def from_string(map_string):
        # Static method to create a Map object from a multiline string
        pass

class Walker:
    # Walker class represents a walker with a position on the map
    def __init__(self, position):
        # Initialize the walker's position
        self.position = position


class Path:
    # Path class represents a sequence of fields forming a path on the map
    def __init__(self):
        # Initialize an empty list of fields
        self.fields = []

    def add_step(self, field):
        # Add a new step to the path
        self.fields.append(field)

    def remove_last_step(self):
        # Remove the last step from the path
        if self.fields:
            self.fields.pop()


multilinestring = """\
abc
def
ghi"""

print(multilinestring)