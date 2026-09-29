"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: grid.py
Purpose: Houses all functions necessary for proper grid/tile handling and logic in the game
"""

# imports
import heapq
import domain_library as dl
import entity
from enum import Enum


# Grid class with all methods needed for manipulating the grid
class Grid:
    # Constants
    MIN_BOUNDS = 5
    MAX_BOUNDS = 50

    # Initialize Grid with height, width
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []  # To be filed with Tiles

        if dl.are_valid_ints(width, height) and Grid.within_bounds(width, height):
            # Generate grid based on height and width and fill with OPEN spaces
            for col in range(int(width)):  # for each col based on width of grid
                temp_col = []

                # For each row in that column
                for row in range(int(height)):
                    # Each cell is initialized with an empty space
                    temp_col.append(Tile("Floor", True, []))

                # After row was completed add row to grid
                self.grid.append(temp_col)

    # Is Occupied Start
    # Checks grid location at given x,y to see if it is occupied
    # Params: x,y - int - grid position to check
    # Returns: Bool - if grid tile is occupied T/F
    def is_occupied(self, x, y):
        # typing fix
        try:
            x = int(x)
            y = int(y)
        except:
            print(
                f"error: Grid.is_occupied_failed - x ({x}) and/or y ({y}) is/are not integer(s)!"
            )
            return None

        if len(self.grid[x][y].occupants) == 0:  # empty list of occupants
            return False
        else:
            return True

    # Is Occupied End

    # Occupy Start
    # Sets grid location to given entity's ID, marking it as occupied
    # only called after tile is known to be unoccupied and x,y are cleaned valid ints
    # Params: x,y - int - grid position to occupy
    #       e_ID - int - entity ID value
    # Return: None
    def occupy(self, x, y, e_ID):
        self.grid[x][y].occupants.append(e_ID)

    # Occupy End

    # Clear Occupant Start
    # Removes occupant from grid location at given x,y
    # x,y are cleaned valid ints
    # Params: x,y - int - tile position to clear occupant from
    #       e_ID - int - id number of occupant to remove at given tile
    # Return: None
    def clear_occupant(self, x, y, e_ID):
        # functionality with multiple occupants
        for occupant in self.grid[x][y].occupants:
            if occupant == e_ID:
                self.grid[x][y].occupants.remove(occupant)

    # Clear Occupant End

    # Is Passable Start
    # Sets grid location at given x,y to open
    # x,y are cleaned valid ints
    # Params: x,y - int - grid position to clear
    # Returns: Bool - if tile is passable
    def is_passable(self, x, y):
        return self.grid[x][y].passable

    # Is Passable End

    # Get Stats Start
    # Gets all relevant stats of the tile at designated position and returns them
    # Params: x,y - int - position of tile
    # Returns tuple - Contains all stats needed for Command Line Interface commands
    #       (int x coord, int y coord, str t_type, bool passable, list occupants)
    def get_stats(self, x, y):
        stat_tuple = (
            x,
            y,
            self.grid[x][y].t_type,
            self.grid[x][y].passable,
            self.grid[x][y].occupants,
        )
        return stat_tuple

    # Get Stats End

    # Within Bounds start
    # checks to see if width and height are within bounds - only runs if they are valid ints
    # Params: width/height - ints
    # Returns: bool
    def within_bounds(width, height):
        if (
            Grid.MIN_BOUNDS <= int(width) <= Grid.MAX_BOUNDS
            and Grid.MIN_BOUNDS <= int(height) <= Grid.MAX_BOUNDS
        ):
            return True
        else:
            return False

    # Is Valid Grid Position
    # checks to see if x and y are valid in current grid
    # Params: x/y - ints - grid positon
    # Returns: Bool
    def is_valid_grid_position(self, x, y):
        if int(self.width) > int(x) >= 0 and int(self.height) > int(y) >= 0:
            return True
        else:
            return False

    # Set Tile Start
    # Sets tile at given grid position
    # Params: x/y - ints - grid position
    #       tile_type - string - Type of tile to set
    # Return: None
    def set_tile(self, x, y, tile_type):
        # Create tile to be placed
        temp_tile = Tile.create_tile(tile_type)
        # Stop if the tile type was invalid
        if temp_tile is None:
            return
        # cast to int
        x = int(x)
        y = int(y)
        # update temp_tile to have correct occupants
        for occupant in self.grid[x][y].occupants:
            temp_tile.occupants.append(occupant)
        # set tile on grid
        self.grid[x][y] = temp_tile

    # Spawn Entity start
    # Spawns entity at given grid position
    # Params: x/y - ints - grid position
    #       entity_type - string - Type of entity to spawn
    # Returns: new_entity - Entity - spawned in entity
    def spawn_entity(self, x, y, entity_type, entity_ids_issued):
        # typing fix
        x = int(x)
        y = int(y)
        # spawn/get entity
        new_entity = entity.create_entity(entity_type, x, y, entity_ids_issued)

        # occupy position on map
        self.occupy(x, y, new_entity.id)

        # return updated grid
        return new_entity

    # Reset Grid start
    # resets grid to prevent any errors during testing
    # Params: None
    # Return: None
    def reset_grid():
        # reset grid stats
        Grid.width = 0
        Grid.height = 0
        Grid.grid = []
        # return grid to CLI
        return Grid.grid

    # Add Item To Tile List Start
    # Adds the provided item to the current grids
    # Params: x,y - ints - grid position of tile
    #         item_name - string - Name of item to be added
    # Returns: None
    def add_item_to_tile_item_list(self, x, y, item_name):
        # fetch/create item
        if item_name.lower() in dl.EQUIPMENT_TYPES:
            item = dl.EQUIPMENT_TYPES.get(item_name.lower())()
        else:
            return
        # Append to list
        self.grid[int(x)][int(y)].item_list.append(item)

    # Remove Item From Tile List Start
    # Removes the provided item from the current grids
    # Params: x,y - ints - grid position of tile
    #         item_name - string - Name of item to be removed
    # Returns: None
    def remove_item_from_tile_item_list(self, x, y, item_name):
        # Get item name
        if isinstance(item_name, type):
            item_name = item_name.__name__

        elif hasattr(item_name, "name"):
            item_name = item_name.name

        # Find and remove item
        for item in self.grid[x][y].item_list:

            # Get item name
            if isinstance(item, type):
                tile_item_name = item.__name__

            elif hasattr(item, "name"):
                tile_item_name = item.name

            elif isinstance(item, str):
                tile_item_name = item

            else:
                continue

            # Compare item names
            if tile_item_name.lower() == item_name.lower():
                self.grid[x][y].item_list.remove(item)
                return

    # Set Tile Item List Start
    # Adds the provided item list to the current grids
    # Intended use is for map creation - not player actions
    # Params: x,y - ints - grid position of tile
    #         item_list - list - list of items to add
    # Returns: None
    def set_tile_item_list(self, x, y, item_list):
        for item in item_list:
            self.grid[x][y].item_list.append(item)

    # Clear Tile Item List Start
    # Clears the current grid positions item list
    # Intended use is for map creation and testing - not player actions
    # Params: x,y - ints - grid position of tile
    # Returns: None
    def clear_tile_item_list(self, x, y):
        self.grid[x][y].item_list.clear()

    # Is Within Range
    # Returns bool based on if provided tile location is within the range of the entity
    # All variables are cleaned prior to passing into this function
    # Params:   entity_ordered_pair - list - [x, y] current gird position of entity
    #           target_ordered_pair - list - [x, y] target gird position
    #           range - int - entity mvoement speed or weapon range
    #           current_grid - grid - CLI current game grid
    # Returns:  bool - true if target is within range of entity
    def is_within_range(self, entity_ordered_pair, target_ordered_pair, range):
        # Assign x's and y's
        start_x = int(entity_ordered_pair[0])
        start_y = int(entity_ordered_pair[1])
        target_x = int(target_ordered_pair[0])
        target_y = int(target_ordered_pair[1])

        # Priority Queue for A* - (estimated cost, distance, x, y)
        open_tile_list = []
        # Start at intial position
        heapq.heappush(
            open_tile_list,
            (
                Grid.manhattan_distance_calculator(
                    target_x, start_x, target_y, start_y
                ),
                0,
                start_x,
                start_y,
            ),
        )

        # Keep track of shortest ditances to each tile
        distances = {}
        distances[(start_x, start_y)] = 0

        # While there are open tiles remaining
        while open_tile_list:
            # Get "cheapest" tile
            _, distance, x, y = heapq.heappop(open_tile_list)

            # Skip over old paths
            if distance != distances.get((x, y)):
                continue

            # Target found
            if int(x) == target_x and int(y) == target_y:
                # Check distance against range
                if distance <= range:
                    return True
                else:  # Not within range
                    return False

            # Skip over tiles outside of range
            if distance >= range:
                continue  # Skips checking neighbors when at ranges limit

            # Get neighbor tiles
            neighbors = self.get_neighbors([x, y])

            # Check each neighbor tile
            for next_tile in neighbors:
                # Set next x and y
                next_x = next_tile[0]
                next_y = next_tile[1]

                # Count each step - Speed effects of tiles only happen when started on them
                new_distance = distance + 1

                # Only keep the shortest distance
                if new_distance < distances.get((next_x, next_y), float("inf")):

                    distances[(next_x, next_y)] = new_distance

                    # A* priority - (distance traveled + Manhattan distance)
                    priority = new_distance + Grid.manhattan_distance_calculator(
                        next_x, next_y, target_x, target_y
                    )
                    # Push neighbor tile to priority queue
                    heapq.heappush(
                        open_tile_list,
                        (priority, new_distance, next_x, next_y),
                    )

        # No path within range
        return False

    # Manhattan Distance Calculator
    # Calculates the manhattan distance using formula
    # Params:   x,y - ints - intial x and y coordinates
    #           x2,y2 - ints - target x and y coordinates
    # Returns: manhattan_distance - int
    def manhattan_distance_calculator(x2, x, y2, y):
        try:
            x2 = int(x2)
            x = int(x)
            y2 = int(y2)
            y = int(y)
        except:
            return  # never will happen as the x's and y's are pulled from grid positions
        return abs(x2 - x) + abs(y2 - y)

    # Get Neighbors
    # Gets all valid neighboring positions
    # Params: ordered_pair - list - [x, y] current position
    # Returns: list - Valid neighboring positions
    def get_neighbors(self, ordered_pair):

        # Store valid neighbors
        neighbors = []

        # Get current x and y coordinates
        x = ordered_pair[0]
        y = ordered_pair[1]

        # Check each cardinal direction
        for dir in Direction:

            # Get direction moves
            direction_x = dir.value[0]
            direction_y = dir.value[1]

            # Calculate neighbor
            next_x = x + direction_x
            next_y = y + direction_y

            # Create ordered pair for neighbor
            next_position = [next_x, next_y]

            # Check valid grid position and passable tile
            if self.is_valid_grid_position(next_x, next_y) and self.is_passable(
                next_x, next_y
            ):
                neighbors.append(next_position)

        return neighbors


# Create Tile class because the grid will be made up of Tiles
class Tile:
    # Tile Type Enum
    class TileType(Enum):
        FLOOR = "Floor"
        WALL = "Wall"
        SHALLOW_WATER = "ShallowWater"
        FOREST = "Forest"

    # Initialize Tile with t_type, passable, occupant
    def __init__(self, t_type, passable, occupants, modifiers=None, item_list=None):
        self.t_type = t_type
        self.passable = passable
        self.occupants = occupants

        if modifiers is None:
            modifiers = {}

        if item_list is None:
            item_list = []

        self.modifiers = modifiers
        self.item_list = item_list

    # Is Valid Tile Start
    # Checks to see input is a valid tile type
    # Params: tile_type - string - tile name
    # Returns: Bool
    def is_valid_tile(tile_type):
        # Check if the provided tile type is a string
        if isinstance(tile_type, str):

            # Check against each valid TileType Enum value
            for valid_type in Tile.TileType:
                if tile_type.lower() == valid_type.value.lower():
                    return True

        # Invalid tile type
        return False

    # Create Tile Start
    # Creates an empty tile based on the tile type and returns it - Tiles occupied later
    # WITH MORE TILES WILL LEAD TO CYCLOMATIC COMPLEXITY - split into different tile creators + factory?
    # Params: t_type - TileType - Type of tile to create
    # Returns: Tile - Tile based on tile type provided
    # Create Tile Start
    def create_tile(t_type):

        # Convert string to enum - prevents no tiles being placed error
        if isinstance(t_type, str):
            for valid_type in Tile.TileType:
                if t_type.lower() == valid_type.value.lower():
                    t_type = valid_type
                    break

        # Match case for each type of tile
        match t_type:

            # Floor tile
            case Tile.TileType.FLOOR:
                # create and return floor tile
                return Tile(t_type.value, True, [])

            # Wall tile
            case Tile.TileType.WALL:
                # create and return Wall tile
                return Tile(t_type.value, False, [])

            # ShallowWater tile
            case Tile.TileType.SHALLOW_WATER:
                # create and return ShallowWater tile
                return Tile(
                    t_type.value,
                    True,
                    [],
                    {"Speed": "-2"},
                )

            # Forest Tile
            case Tile.TileType.FOREST:
                # create and return Forest tile
                return Tile(
                    t_type.value,
                    True,
                    [],
                    {"Defence": "+5", "Speed": "-1"},
                )

            # Invalid tile type
            case _:
                return None


# Direction Enum - used within A* pathfinding for manhattan distance calcs
class Direction(Enum):

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
