"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 23, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: dungeon_floor.py
Purpose: Houses all functions necessary for proper dungeon floor functionality.
"""

# Imports
from dataclasses import dataclass
from grid import Grid


# Immutable dataclass for dungeon floor
@dataclass(frozen=True)
class DungeonFloorInfo:
    floor_number: int
    width: int
    height: int
    entrance: tuple | None
    exit: tuple | None


# Dungeon Floor Class
class DungeonFloor:
    # Memento for Dungeon Floor
    @dataclass(frozen=True)
    class Memento:
        floor_number: int
        grid_memento: Grid.Memento
        entrance: tuple | None
        exit: tuple | None

    # init
    # Initialize a dungeon floor with its own grid
    # Params:   floor_number - int
    #           width, height - ints
    #           grid - Grid for floor > Created by dungeon generator
    # Returns: None
    def __init__(self, floor_number, width=None, height=None, grid=None):
        # Ensure valid ints for floor number
        if (
            not isinstance(floor_number, int)
            or isinstance(floor_number, bool)
            or floor_number < 1
        ):
            raise ValueError("Floor number must be a positive integer")

        # Ensure valid ints for grid dimensions
        if grid is None:
            if (
                not isinstance(width, int)
                or not isinstance(height, int)
                or not Grid.within_bounds(width, height)
            ):
                raise ValueError("Invalid dungeon floor dimensions")
            # Create grid with valid dimensions
            grid = Grid(width, height)

        # Ensure valid grid - if provided
        elif not isinstance(grid, Grid):
            raise TypeError("grid must be a Grid")

        grid_info = grid.get_info()
        # Ensure valid grid dimensions
        if not Grid.within_bounds(grid_info.width, grid_info.height):
            raise ValueError("Invalid grid dimensions")
        # Assign variables
        self.__floor_number = floor_number
        self.__grid = grid
        self.__entrance = None
        self.__exit = None

    # Get Grid
    # Return the floor's grid for existing grid operations
    # Params: None
    # Return: grid - Grid - floor's current grid
    def get_grid(self):
        return self.__grid

    # Get Info
    # Return read-only floor information
    # Params: None
    # Returns: DungeonFloorInfo
    def get_info(self):
        grid_info = self.__grid.get_info()
        return DungeonFloorInfo(
            floor_number=self.__floor_number,
            width=grid_info.width,
            height=grid_info.height,
            entrance=self.__entrance,
            exit=self.__exit,
        )

    # Validate Position
    # Validate a passable coordinate on this floor
    # Params:   position - tuple/list - coordinates on grid
    # Return: x,y - tuple - Valid position
    def __validate_position(self, position):
        # Ensure only 2 vals given
        if not isinstance(position, (tuple, list)) or len(position) != 2:
            raise ValueError("Position must contain x and y")

        x, y = position
        # Ensure position is made of ints
        if any(not isinstance(v, int) or isinstance(v, bool) for v in (x, y)):
            raise ValueError("Position coordinates must be integers")
        # Ensure position is a valid grid position
        elif not Grid.is_valid_grid_position(self.__grid.get_info(), x, y):
            raise ValueError("Position is outside the grid")
        # Ensure position is passable
        elif not self.__grid.is_passable(x, y):
            raise ValueError("Position must be passable")

        return (x, y)

    # Set Entrance
    # Sets the entrance position
    # Params: x,y - ints - Grid position of entrance stairs
    # Returns: None
    def set_entrance(self, x, y):
        # Validate position
        position = self.__validate_position((x, y))
        # Ensure player doesn't spawn on the exit
        if position == self.__exit:
            raise ValueError("Entrance and exit must be different")

        self.__entrance = position

    # Set Exit
    # Set the exit position
    # Params: x,y - ints - Grid position of exit stairs
    # Returns: None
    def set_exit(self, x, y):
        # Validate position
        position = self.__validate_position((x, y))
        # Ensure player doesn't spawn on the exit
        if position == self.__entrance:
            raise ValueError("Entrance and exit must be different")

        self.__exit = position

    # Create memento
    # Create memento snapshot the floor and its grid
    # Params: None
    # Returns: Dungeon Floor Memento
    def create_memento(self):
        return DungeonFloor.Memento(
            floor_number=self.__floor_number,
            grid_memento=self.__grid.create_memento(),
            entrance=self.__entrance,
            exit=self.__exit,
        )

    # Restore
    # Restore a saved floor and its grid
    # Params: memento - Dungeon Floor Memento
    # Returns: None
    def restore(self, memento):
        # Ensure saved memento is correct type
        if not isinstance(memento, DungeonFloor.Memento):
            raise TypeError("Invalid DungeonFloor Memento")
        # Ensure valid int for saved floor number
        if not isinstance(memento.floor_number, int) or memento.floor_number < 1:
            raise ValueError("Invalid saved floor number")
        # Ensure valid grid memento for saved grid
        if not isinstance(memento.grid_memento, Grid.Memento):
            raise TypeError("Invalid saved Grid Memento")

        # Restores grid
        restored_grid = Grid(memento.grid_memento.width, memento.grid_memento.height)
        restored_grid.restore(memento.grid_memento)

        # Validate coordinates against the restored grid before changing this floor
        previous_grid = self.__grid
        self.__grid = restored_grid

        try:
            entrance = (
                self.__validate_position(memento.entrance)
                if memento.entrance is not None
                else None
            )
            exit_position = (
                self.__validate_position(memento.exit)
                if memento.exit is not None
                else None
            )
            if entrance is not None and entrance == exit_position:
                raise ValueError("Entrance and exit must be different")

        except Exception:
            self.__grid = previous_grid
            raise
        # Restores rest of Dungeon Floor info
        self.__floor_number = memento.floor_number
        self.__entrance = entrance
        self.__exit = exit_position
