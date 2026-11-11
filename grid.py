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
from copy import deepcopy
import heapq
import domain_library as dl
import equipment
import entity
from enum import Enum
from dataclasses import dataclass


# Data Classes
# Data class created for Tile
@dataclass(frozen=True)
class TileInfo:
    tile_type: str
    passable: bool
    occupants: tuple
    modifiers: tuple
    item_list: tuple


# Dataclass created for Grid
@dataclass(frozen=True)
class GridInfo:
    width: int
    height: int
    grid: tuple


# Grid class with all methods needed for manipulating the grid
class Grid:
    # Constants
    __MIN_BOUNDS = 5
    __MAX_BOUNDS = 50

    # Initialize Grid with height, width
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__grid = []  # To be filed with Tiles

        if dl.are_valid_ints(width, height) and Grid.within_bounds(width, height):
            # Generate grid based on height and width and fill with OPEN spaces
            for col in range(int(width)):  # for each col based on width of grid
                temp_col = []

                # For each row in that column
                for row in range(int(height)):
                    # Each cell is initialized with an empty space
                    temp_col.append(Tile("Floor", True, []))

                # After row was completed add row to grid
                self.__grid.append(temp_col)

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

        # Get tile info at position
        tile_info = self.__grid[x][y].get_info()

        if len(tile_info.occupants) == 0:  # empty list of occupants
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
        self.__grid[x][y].occupy_tile(e_ID)

    # Occupy End

    # Clear Occupant Start
    # Removes occupant from grid location at given x,y
    # x,y are cleaned valid ints
    # Params: x,y - int - tile position to clear occupant from
    #       e_ID - int - id number of occupant to remove at given tile
    # Return: None
    def clear_occupant(self, x, y, e_ID):
        self.__grid[x][y].remove_occupant(e_ID)

    # Clear Occupant End

    # Is Passable Start
    # Sets grid location at given x,y to open
    # x,y are cleaned valid ints
    # Params: x,y - int - grid position to clear
    # Returns: Bool - if tile is passable
    def is_passable(self, x, y):
        tile_info = self.__grid[x][y].get_info()
        return tile_info.passable

    # Is Passable End

    # Within Bounds start
    # checks to see if width and height are within bounds - only runs if they are valid ints
    # Params: width/height - ints
    # Returns: bool
    def within_bounds(width, height):
        if (
            Grid.__MIN_BOUNDS <= int(width) <= Grid.__MAX_BOUNDS
            and Grid.__MIN_BOUNDS <= int(height) <= Grid.__MAX_BOUNDS
        ):
            return True
        else:
            return False

    # Is Valid Grid Position
    # checks to see if x and y are valid in current grid
    # Params: x/y - ints - grid positon
    # Returns: Bool
    def is_valid_grid_position(grid_info, x, y):
        if int(grid_info.width) > int(x) >= 0 and int(grid_info.height) > int(y) >= 0:
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
        # Get old tile info to preserve occupants
        old_tile_info = self.__grid[x][y].get_info()
        # update temp_tile to have correct occupants
        for occupant in old_tile_info.occupants:
            temp_tile.occupy_tile(occupant)
        # set tile on grid
        self.__grid[x][y] = temp_tile

    # Spawn Entity start
    # Spawns entity at given grid position
    # Params: x/y - ints - grid position
    #       entity_type - string - Type of entity to spawn
    # Returns: new_entity - Entity - spawned in entity
    def spawn_entity(self, x, y, entity_type, entity_ids_issued):
        # typing fix
        x = int(x)
        y = int(y)
        # spawn/get entity - immutabble copy of entity is returned to game state for updating
        new_entity = entity.create_entity(entity_type, x, y, entity_ids_issued)

        # occupy position on map
        self.occupy(x, y, entity_ids_issued)

        # return updated grid
        return new_entity

    # Add Item To Tile List Start
    # Adds the provided item to the current grids
    # Params: x,y - ints - grid position of tile
    #         item_name - string - Name of item to be added
    # Returns: None
    def add_item_to_tile_item_list(self, x, y, item_name):
        # fetch/create item
        item = equipment.create_equipment(item_name.lower())

        # Return if item is invalid
        if item is None:
            return

        # Append to list
        self.__grid[int(x)][int(y)].add_item(item)

    # Remove Item From Tile List Start
    # Removes the provided item from the current grids
    # Params: x,y - ints - grid position of tile
    #         item_name - string - Name of item to be removed
    # Returns: Item removed
    def remove_item_from_tile_item_list(self, x, y, item_name):
        return self.__grid[x][y].remove_item(item_name)

    # Set Tile Item List Start
    # Adds the provided item list to the current grids
    # Intended use is for map creation - not player actions
    # Params: x,y - ints - grid position of tile
    #         item_list - list - list of items to add
    # Returns: None
    def set_tile_item_list(self, x, y, item_list):
        for item in item_list:
            self.__grid[x][y].add_item(item)

    # Clear Tile Item List Start
    # Clears the current grid positions item list
    # Intended use is for map creation and testing - not player actions
    # Params: x,y - ints - grid position of tile
    # Returns: None
    def clear_tile_item_list(self, x, y):
        self.__grid[x][y].clear_item_list()

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

        range = int(range)

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
    @staticmethod
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

            grid_info = self.get_info()

            # Check valid grid position and passable tile
            if Grid.is_valid_grid_position(
                grid_info, next_x, next_y
            ) and self.is_passable(next_x, next_y):
                neighbors.append(next_position)

        return neighbors

    # Get Tile Info
    # Gets TileInfo at specific position
    # Params: x,y - ints - grid position of tile
    # Returns: TileInfo - all info about the current tile
    def get_tile_info(self, x, y):
        return self.__grid[x][y].get_info()

    # Get Info
    # Gets Grid obj info
    # Params: None
    # Returns: GridInfo - all info about the current Grid obj
    def get_info(self):
        return GridInfo(width=self.__width, height=self.__height, grid=self.__grid)

    # Memento class stores the Grid's state
    @dataclass(frozen=True)
    class Memento:
        width: int
        height: int
        tiles: tuple

    # Create Memento
    # Create a memento Grid and all its Tiles
    # Params: None
    # Returns: memento - Memento - memento containing grid info and all tile mementos
    def create_memento(self):
        tile_mementos = []

        # Save each column and its Tiles
        for col in self.__grid:
            temp_col = []

            for tile in col:
                temp_col.append(tile.create_memento())

            # Store each column as a tuple
            tile_mementos.append(tuple(temp_col))

        return Grid.Memento(
            width=self.__width,
            height=self.__height,
            tiles=tuple(tile_mementos),
        )

    # Restore
    # Restores grid and tiles based on Memento
    # Params: memento - Memento - Memento will all grid info and tile mementos
    # Returns: None
    def restore(self, memento):
        if not isinstance(memento, Grid.Memento):
            raise TypeError("Invalid Grid Memento")

        # Rebuild the grid from the saved Tile Mementos
        restored_grid = []

        for col in memento.tiles:
            temp_col = []

            for tile_memento in col:
                tile = Tile(
                    tile_memento.t_type,
                    tile_memento.passable,
                    list(tile_memento.occupants),
                    deepcopy(tile_memento.modifiers),
                    list(tile_memento.item_list),
                )

                temp_col.append(tile)

            restored_grid.append(temp_col)

        # Update the Grid's private state
        self.__width = memento.width
        self.__height = memento.height
        self.__grid = restored_grid

    # Get Path Distance
    # Finds the shortest reachable distance between two positions using A*
    # Params: start_position - list - starting [x, y] coordinates
    #         target_position - list - target [x, y] coordinates
    # Returns: distance - int/None - shortest path distance or None if unreachable
    def get_path_distance(self, start_position, target_position):
        # Get starting coordinates
        start_x = int(start_position[0])
        start_y = int(start_position[1])

        # Get target coordinates
        target_x = int(target_position[0])
        target_y = int(target_position[1])

        # Get grid information
        grid_info = self.get_info()

        # Validate starting and target positions
        if not Grid.is_valid_grid_position(
            grid_info, start_x, start_y
        ) or not Grid.is_valid_grid_position(grid_info, target_x, target_y):
            return None

        # Check target passability
        if not self.is_passable(target_x, target_y):
            return None

        # Initialize priority queue
        open_tile_list = []

        # Add starting position
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

        # Store shortest known distances
        distances = {(start_x, start_y): 0}

        # Search for shortest path
        while open_tile_list:
            _, distance, x, y = heapq.heappop(open_tile_list)

            # Skip outdated paths
            if distance != distances.get((x, y)):
                continue

            # Target reached
            if x == target_x and y == target_y:
                return distance

            # Get valid neighbors (excludes walls)
            neighbors = self.get_neighbors([x, y])

            for next_x, next_y in neighbors:
                # Ignore occupied tiles except the target
                if (next_x, next_y) != (target_x, target_y):
                    if self.is_occupied(next_x, next_y):
                        continue

                # Calculate new distance
                new_distance = distance + 1

                # Skip longer paths
                if new_distance >= distances.get((next_x, next_y), float("inf")):
                    continue

                # Update shortest distance
                distances[(next_x, next_y)] = new_distance

                # Calculate A* priority
                priority = new_distance + Grid.manhattan_distance_calculator(
                    target_x, next_x, target_y, next_y
                )

                # Add neighbor to queue
                heapq.heappush(
                    open_tile_list,
                    (priority, new_distance, next_x, next_y),
                )

        # No valid path exists
        return None


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
        self.__t_type = t_type
        self.__passable = passable
        self.__occupants = occupants

        if modifiers is None:
            modifiers = {}

        if item_list is None:
            item_list = []

        self.__modifiers = modifiers
        self.__item_list = item_list

    # Get Info
    # Gets immutable info on tile
    # Params: None
    # Returns: TileInfo - all info about the current tile
    def get_info(self):
        return TileInfo(
            tile_type=self.__t_type,
            passable=self.__passable,
            occupants=tuple(self.__occupants),
            modifiers=tuple(self.__modifiers.items()),  # Items() for key-value pairs
            item_list=tuple(item.get_info().name for item in self.__item_list),
        )

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

    # Get Item From List
    # Gets the item from the tiles item list
    # Params: item_name - string - item name
    # Return: item - item instance - matchning item in list
    def get_item_from_list(self, item_name):
        for item in self.__item_list:
            if item.name.lower() == item_name.lower():
                return item
            else:
                continue
        return None

    # Remove Item
    # Removes and returns the matching item instance
    # Params: item_name - string - name of item to remove
    # Returns: item instance or None
    def remove_item(self, item_name):
        for item in self.__item_list:
            item_info = item.get_info()
            if item_info.name.lower() == item_name.lower():
                self.__item_list.remove(item)
                return item_info

        return None

    # Add Item
    # Adds item to the tiles item list
    # Params: item - Item - item instance to add
    # Returns: None
    def add_item(self, item):
        self.__item_list.append(item)

    # Clear Item List
    # Clears the tiles item list
    # Params: None
    # Returns: None
    def clear_item_list(self):
        self.__item_list.clear()

    # Occupy Tile
    # Adds entity id to the tile to be occupied
    # Params: entity_id - int - id of entity to occupy tile
    # Returns: None
    def occupy_tile(self, entity_id):
        self.__occupants.append(entity_id)

    # Remove Occupant
    # Removes entity id from the tile to be unoccupied
    # Params: entity_id - int - id of entity to unoccupy tile
    # Returns: None
    def remove_occupant(self, entity_id):
        if entity_id in self.__occupants:
            self.__occupants.remove(entity_id)

    # Memento class for Tile's state
    @dataclass(frozen=True)
    class Memento:
        t_type: str
        passable: bool
        occupants: object
        modifiers: object
        item_list: object

    # Create Momento
    # Create a tiles state memento
    # Params: None
    # Returns: memento - Memento - tile info from save
    def create_memento(self):
        return Tile.Memento(
            t_type=deepcopy(self.__t_type),
            passable=self.__passable,
            occupants=deepcopy(self.__occupants),
            modifiers=deepcopy(self.__modifiers),
            item_list=deepcopy(self.__item_list),
        )

    # Restore
    # Restore a tiles state from memento
    # Params: memento - Memento - tile info from save
    # Returns: None
    def restore(self, memento):
        if not isinstance(memento, Tile.Memento):
            raise TypeError("Invalid Tile Memento")

        self.__t_type = deepcopy(memento.t_type)
        self.__passable = memento.passable
        self.__occupants = list(memento.occupants)
        self.__modifiers = deepcopy(memento.modifiers)
        self.__item_list = list(memento.item_list)


# Direction Enum - used within A* pathfinding for manhattan distance calcs
class Direction(Enum):

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
