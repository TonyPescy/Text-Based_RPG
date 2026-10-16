"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 21, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_grid.py
Purpose: Utilizes unittest to test all of the classes and methods in grid.py file
"""

"""
NOTE: These commands are written with the idea that they will only be called with
the correct typing or the expected correct parameters from the CLIs process command. 
As such this testing may lack certain cases such as handling when occupy is called 
with another unit on the same x,y of the grid. This is handled in the CLI, which is
why the CLI test file is far larger than any other test file. To avoid the extra redundant
code in this file as well as the grid.py, we will only be looking at cases that can
be tested without an entire refactor of all of the entire game logic.

TLDR: This will primarily test only success cases as any and all error handling of 
these functions are handled within the CLI prior to calling this function.
"""

# imports
import unittest
import domain_library as dl
from grid import Grid, Tile
import equipment


class TestGrid(unittest.TestCase):

    # Create Test Grid
    # Params: width/height - int - grid dimensions
    # Returns: Grid
    def create_test_grid(self, width=25, height=25):
        return Grid(width, height)

    # Reset Tile Item List
    # Params:   test_grid - Grid - current grid
    #           x/y - ints - grid position
    # Returns: None
    def reset_tile_item_list(self, test_grid, x=0, y=0):
        test_grid.clear_tile_item_list(x, y)

    # Add Test Item
    # Params:   test_grid - Grid - current grid
    #           x/y - ints - grid position
    #           item_name - string - item name
    # Returns: None
    def add_test_item(self, test_grid, x, y, item_name):
        test_grid.add_item_to_tile_item_list(x, y, item_name)

    # Get Test Tile Item
    # Gets item name from tile
    # Params:   test_grid - Grid - current grid
    #           x/y - ints - grid position
    #           item_index - int - item index
    # Returns: Item name present at position on grid
    def get_test_tile_item(self, test_grid, x=0, y=0, item_index=0):
        tile_info = test_grid.get_tile_info(x, y)
        return tile_info.item_list[item_index]

    # Assert Tile Defaults
    # Asserts common tile default stats
    # Params:   tile - Tile - current tile
    #           tile_type - string - current tiles type
    #           passable - bool - true if passable, false otherwise
    #           modifiers - dict - modifiers on tile
    # Returns: None
    def assert_tile_defaults(self, tile, tile_type, passable, modifiers):
        tile_info = tile.get_info()

        self.assertEqual(tile_info.tile_type, tile_type)
        self.assertEqual(tile_info.passable, passable)
        self.assertEqual(tile_info.occupants, ())
        self.assertDictEqual(dict(tile_info.modifiers), modifiers)
        self.assertEqual(tile_info.item_list, ())

    # test grid proper grid init
    def test_correct_grid_init_at_lower_bound(self):
        # Create grid
        test_grid = self.create_test_grid(5, 5)
        grid_info = test_grid.get_info()

        self.assertEqual(grid_info.width, 5)
        self.assertEqual(grid_info.height, 5)
        self.assertEqual(grid_info.grid[0][0].get_info().tile_type, "Floor")

    # test grid with too small init
    def test_grid_init_below_lower_bounds(self):
        # Create grid
        test_grid = Grid(1, 1)
        grid_info = test_grid.get_info()

        self.assertEqual(grid_info.width, 1)
        self.assertEqual(grid_info.height, 1)
        self.assertEqual(grid_info.grid, [])

    # test grid with too large init
    def test_grid_init_above_bounds(self):
        # Create grid
        test_grid = Grid(51, 51)
        grid_info = test_grid.get_info()

        self.assertEqual(grid_info.width, 51)
        self.assertEqual(grid_info.height, 51)
        self.assertEqual(grid_info.grid, [])

    # test grid proper grid init
    def test_correct_grid_init_at_higher_bound(self):
        # Create grid
        test_grid = Grid(50, 50)
        grid_info = test_grid.get_info()

        self.assertEqual(grid_info.width, 50)
        self.assertEqual(grid_info.height, 50)
        self.assertEqual(grid_info.grid[0][0].get_info().tile_type, "Floor")

    # test is_occupied success
    def test_is_occupied_success_with_occupant(self):
        # create grid
        test_grid = self.create_test_grid()
        # Add occupant
        test_grid.occupy(0, 0, 1)

        self.assertEqual(test_grid.is_occupied(0, 0), True)

    # test is_occupied x/y int fail
    def test_is_occupied_not_ints_provided(self):
        # create grid
        test_grid = self.create_test_grid()
        # Add occupant
        test_grid.occupy(0, 0, 1)

        self.assertEqual(test_grid.is_occupied(0, "sev"), None)

    # test is_occupied success without occupants
    def test_is_occupied_success_without_occupant(self):
        # create grid
        test_grid = self.create_test_grid()

        self.assertEqual(test_grid.is_occupied(0, 0), False)

    # test occupy success
    def test_occupy_success(self):
        # create grid
        test_grid = self.create_test_grid()
        # add occupant
        test_grid.occupy(0, 0, 0)

        self.assertEqual(test_grid.get_tile_info(0, 0).occupants, (0,))

    # test clear occupant (only 1) from grid position
    def test_clear_occupant_success(self):
        # create grid
        test_grid = self.create_test_grid()
        # add occupant
        test_grid.occupy(0, 0, 0)
        # Clear occupant
        test_grid.clear_occupant(0, 0, 0)

        self.assertEqual(test_grid.get_tile_info(0, 0).occupants, ())

    # test clear occupant (3) from grid position
    def test_clear_occupant_success_with_occupants(self):
        # create grid
        test_grid = self.create_test_grid()
        # add occupants
        test_grid.occupy(0, 0, 0)
        test_grid.occupy(0, 0, 1)
        test_grid.occupy(0, 0, 2)
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)

        self.assertEqual(test_grid.get_tile_info(0, 0).occupants, (0, 2))

    # test clear occupant (3) from grid position
    def test_clear_occupant_without_occupants(self):
        # create grid
        test_grid = self.create_test_grid()
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)

        self.assertEqual(test_grid.get_tile_info(0, 0).occupants, ())

    # test if tile on grid is passable - true due to floor at 0, 0
    def test_is_passable_true(self):
        # create grid
        test_grid = self.create_test_grid()

        self.assertEqual(test_grid.is_passable(0, 0), True)

    # test if tile on grid is passable - false due to wall at 0, 0
    def test_is_passable_false(self):
        # create grid
        test_grid = self.create_test_grid()
        # Set tile to wall
        test_grid.set_tile(0, 0, "wall")

        self.assertEqual(test_grid.is_passable(0, 0), False)

    # test to get stats of grid position
    def test_get_stats(self):
        # create grid
        test_grid = self.create_test_grid()
        # Add occupants
        test_grid.occupy(0, 0, 0)
        test_grid.occupy(0, 0, 1)
        test_grid.occupy(0, 0, 2)
        test_grid.occupy(0, 0, 3)
        test_grid.occupy(0, 0, 5)
        test_grid.occupy(0, 0, 4)
        test_grid.occupy(0, 0, 7)
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)
        # Get tile information
        tile_info = test_grid.get_tile_info(0, 0)

        self.assertEqual(tile_info.tile_type, "Floor")
        self.assertEqual(tile_info.passable, True)
        self.assertEqual(tile_info.occupants, (0, 2, 3, 5, 4, 7))

    # test to see if ints provided are within bounds - ints are within bounds
    def test_are_ints_within_bounds_true(self):
        self.assertEqual(Grid.within_bounds(25, 25), True)

    # test to see if ints provided are within bounds - ints are lower
    def test_are_ints_within_bounds_false_lower(self):
        self.assertEqual(Grid.within_bounds(4, 4), False)

    # test to see if ints provided are within bounds - ints are higher
    def test_are_ints_within_bounds_false_higher(self):
        self.assertEqual(Grid.within_bounds(51, 51), False)

    # test to see if ints provided are within bounds - ints are on lower boundary
    def test_are_ints_within_bounds_true_lower_boundary(self):
        self.assertEqual(Grid.within_bounds(5, 5), True)

    # test to see if ints provided are within bounds - ints are on higher boundary
    def test_are_ints_within_bounds_true_higher_boundary(self):
        self.assertEqual(Grid.within_bounds(50, 50), True)

    # test to see if ints provided are within grid bounds - ints are higher
    def test_valid_grid_position_false_higher(self):
        temp_grid = self.create_test_grid()

        self.assertEqual(
            Grid.is_valid_grid_position(temp_grid.get_info(), 25, 25),
            False,
        )

    # test to see if ints provided are within grid bounds - ints are on lower boundary
    def test_valid_grid_posiiton_true_lower_boundary(self):
        temp_grid = self.create_test_grid()

        self.assertEqual(
            Grid.is_valid_grid_position(temp_grid.get_info(), 0, 0),
            True,
        )

    # test to see if ints provided are within bounds - ints are on higher boundary
    def test_valid_grid_positions_true_higher_boundary(self):
        temp_grid = self.create_test_grid()

        self.assertEqual(
            Grid.is_valid_grid_position(temp_grid.get_info(), 24, 24),
            True,
        )

    # test to see if ints provided are within grid bounds - ints are lower
    def test_valid_grid_positions_false_lower(self):
        temp_grid = self.create_test_grid()

        self.assertEqual(
            Grid.is_valid_grid_position(temp_grid.get_info(), -1, -1),
            False,
        )

    # test to see if ints provided are within grid bounds - ints are valid
    def test_valid_grid_positions_true(self):
        temp_grid = self.create_test_grid()

        self.assertEqual(
            Grid.is_valid_grid_position(temp_grid.get_info(), 15, 15),
            True,
        )

    # Test set_tile success
    def test_set_tile_success(self):
        # create grid with entities and set tile
        temp_grid = self.create_test_grid()
        temp_grid.occupy(0, 0, 1)
        temp_grid.occupy(0, 0, 2)
        temp_grid.occupy(0, 0, 0)
        temp_grid.set_tile(0, 0, "shallowwater")
        tile_info = temp_grid.get_tile_info(0, 0)

        self.assertEqual(tile_info.tile_type, "ShallowWater")
        self.assertEqual(tile_info.passable, True)
        self.assertEqual(tile_info.occupants, (1, 2, 0))

    # test spawn entity
    def test_spawn_entity_success(self):
        # create grid
        temp_grid = self.create_test_grid()
        # Spawn entity directly on the grid
        # GameState is responsible for storing entities in its entity list
        temp_entity = temp_grid.spawn_entity(0, 0, "warrior", 1)
        # Get entity information
        entity_info = temp_entity.get_info()

        # check values
        self.assertEqual(entity_info.position, [0, 0])
        self.assertEqual(entity_info.id, 1)
        self.assertEqual(temp_grid.get_tile_info(0, 0).occupants, (1,))

    # Tests for Tile initialization
    def test_tile_init(self):
        tile = Tile(
            "floor",
            True,
            [],
            {"Speed": "-2"},
        )
        tile_info = tile.get_info()

        self.assertEqual(tile_info.tile_type, "floor")
        self.assertEqual(tile_info.passable, True)
        self.assertEqual(tile_info.occupants, ())
        self.assertDictEqual(dict(tile_info.modifiers), {"Speed": "-2"})

    # Tests for Tile initialization with no modifiers
    def test_tile_init_no_modifiers(self):
        tile = Tile(
            "floor",
            True,
            [],
        )
        tile_info = tile.get_info()

        self.assertEqual(tile_info.tile_type, "floor")
        self.assertEqual(tile_info.passable, True)
        self.assertEqual(tile_info.occupants, ())
        self.assertDictEqual(dict(tile_info.modifiers), {})

    # Tests for is_valid_tile with valid floor tile
    def test_is_valid_tile_floor(self):
        self.assertEqual(Tile.is_valid_tile("floor"), True)

    # Tests for is_valid_tile with valid wall tile
    def test_is_valid_tile_wall(self):
        self.assertEqual(Tile.is_valid_tile("wall"), True)

    # Tests for is_valid_tile with valid shallow water tile
    def test_is_valid_tile_shallow_water(self):
        self.assertEqual(Tile.is_valid_tile("shallowwater"), True)

    # Tests for create_tile with floor
    def test_create_tile_floor(self):
        tile = Tile.create_tile("floor")

        self.assert_tile_defaults(tile, "Floor", True, {})

    # Tests for create_tile with wall
    def test_create_tile_wall(self):
        tile = Tile.create_tile("wall")

        self.assert_tile_defaults(tile, "Wall", False, {})

    # Tests for create_tile with shallow water
    def test_create_tile_shallow_water(self):
        tile = Tile.create_tile("shallowwater")

        self.assert_tile_defaults(
            tile,
            "ShallowWater",
            True,
            {"Speed": "-2"},
        )

    # Tests for create_tile with forest
    def test_create_tile_forest(self):
        tile = Tile.create_tile("forest")

        self.assert_tile_defaults(
            tile,
            "Forest",
            True,
            {"Defence": "+5", "Speed": "-1"},
        )

    # Tests for create_tile with invalid tile type
    def test_create_tile_invalid(self):
        tile = Tile.create_tile("invalid")
        self.assertEqual(tile, None)

    # Test adding an item to a tile item list
    def test_add_item_to_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")

        # Check item was added
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ("IronSword",))

    # Test adding multiple items to a tile item list
    def test_add_multiple_items_to_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add items
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        temp_grid.add_item_to_tile_item_list(0, 0, "curseddagger")

        # Check items
        self.assertEqual(
            temp_grid.get_tile_info(0, 0).item_list,
            ("IronSword", "CursedDagger"),
        )

    # Test adding an item to a different tile
    def test_add_item_to_different_tile(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        self.reset_tile_item_list(temp_grid, 2, 3)
        # Add item to first tile
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        # Add item to second tile
        temp_grid.add_item_to_tile_item_list(2, 3, "magestaff")

        # Check first tile
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ("IronSword",))

        # Check second tile
        self.assertEqual(temp_grid.get_tile_info(2, 3).item_list, ("MageStaff",))

    # Test removing an item from a tile item list
    def test_remove_item_from_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        # Remove item
        temp_grid.remove_item_from_tile_item_list(0, 0, "ironsword")

        # Check item was removed
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ())

    # Test removing one item while another remains
    def test_remove_item_from_tile_item_list_with_multiple_items(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add items
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        temp_grid.add_item_to_tile_item_list(0, 0, "curseddagger")
        # Remove one item
        temp_grid.remove_item_from_tile_item_list(0, 0, "ironsword")

        # Check remaining item
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ("CursedDagger",))

    # Test removing an item using different capitalization
    def test_remove_item_case_insensitive(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        # Remove item using uppercase
        temp_grid.remove_item_from_tile_item_list(0, 0, "IRONSWORD")

        # Check item was removed
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ())

    # Test removing an item that does not exist
    def test_remove_nonexistent_item_from_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        # Try removing different item
        temp_grid.remove_item_from_tile_item_list(0, 0, "magestaff")

        # Original item should remain
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ("IronSword",))

    # Test setting a tile item list
    def test_set_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        item_list = [
            equipment.create_equipment("ironsword"),
            equipment.create_equipment("magestaff"),
        ]

        temp_grid.set_tile_item_list(0, 0, item_list)

        # Check item list
        self.assertEqual(
            temp_grid.get_tile_info(0, 0).item_list,
            ("IronSword", "MageStaff"),
        )

    # Test clearing a tile item list
    def test_clear_tile_item_list(self):
        temp_grid = self.create_test_grid(5, 5)
        # reset
        self.reset_tile_item_list(temp_grid, 0, 0)
        # Add items
        temp_grid.add_item_to_tile_item_list(0, 0, "ironsword")
        temp_grid.add_item_to_tile_item_list(0, 0, "magestaff")
        # Clear list
        temp_grid.clear_tile_item_list(0, 0)

        # Check list is empty
        self.assertEqual(temp_grid.get_tile_info(0, 0).item_list, ())

    # Test is_within_range - target is same position
    def test_is_within_range_same_position(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target is current position
        result = test_grid.is_within_range([5, 5], [5, 5], 0)

        self.assertEqual(result, True)

    # Test is_within_range - target is one tile away
    def test_is_within_range_one_tile(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target is within range
        result = test_grid.is_within_range([5, 5], [6, 5], 1)

        self.assertEqual(result, True)

    # Test is_within_range - target is exactly at range
    def test_is_within_range_exact_range(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target is exactly three tiles away
        result = test_grid.is_within_range([5, 5], [8, 5], 3)

        self.assertEqual(result, True)

    # Test is_within_range - target is outside range
    def test_is_within_range_outside_range(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target is farther than the provided range
        result = test_grid.is_within_range([5, 5], [8, 5], 2)

        self.assertEqual(result, False)

    # Test is_within_range - target is diagonal
    def test_is_within_range_diagonal(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Manhattan distance from (5, 5) to (7, 7) is 4
        result = test_grid.is_within_range([5, 5], [7, 7], 4)

        self.assertEqual(result, True)

    # Test is_within_range - diagonal target outside range
    def test_is_within_range_diagonal_outside_range(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Manhattan distance from (5, 5) to (7, 7) is 4
        result = test_grid.is_within_range([5, 5], [7, 7], 3)

        self.assertEqual(result, False)

    # Test is_within_range - zero range to another position
    def test_is_within_range_zero_range(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if another position is reachable with zero range
        result = test_grid.is_within_range([5, 5], [6, 5], 0)

        self.assertEqual(result, False)

    # Test is_within_range - shallow water is passable
    def test_is_within_range_shallow_water(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set target tile to shallow water
        test_grid.set_tile(6, 5, "shallowwater")
        # Check if shallow water can be reached
        result = test_grid.is_within_range([5, 5], [6, 5], 1)

        self.assertEqual(result, True)

    # Test is_within_range - wall blocks direct path
    def test_is_within_range_wall_blocks_path(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set wall between starting position and target
        test_grid.set_tile(6, 5, "wall")
        # Target requires going around the wall
        # Shortest path is 4 tiles
        result = test_grid.is_within_range([5, 5], [7, 5], 3)

        self.assertEqual(result, False)

    # Test is_within_range - path around wall is within range
    def test_is_within_range_path_around_wall(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set wall between starting position and target
        test_grid.set_tile(6, 5, "wall")
        # Target can be reached by going around the wall
        # Shortest path is 4 tiles
        result = test_grid.is_within_range([5, 5], [7, 5], 4)

        self.assertEqual(result, True)

    # Test is_within_range - target is an impassable wall
    def test_is_within_range_target_is_wall(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set target tile to wall
        test_grid.set_tile(6, 5, "wall")
        # Check if wall can be reached
        result = test_grid.is_within_range([5, 5], [6, 5], 1)

        self.assertEqual(result, False)

    # Test is_within_range - target at lower grid boundary
    def test_is_within_range_lower_boundary(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target at (0, 1) is within range
        result = test_grid.is_within_range([1, 1], [0, 1], 1)

        self.assertEqual(result, True)

    # Test is_within_range - target outside grid
    def test_is_within_range_outside_grid(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if target outside grid can be reached
        result = test_grid.is_within_range([1, 1], [-1, 1], 2)

        self.assertEqual(result, False)

    # Test is_within_range - string coordinates
    def test_is_within_range_string_coordinates(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Check if string coordinates are converted to integers
        result = test_grid.is_within_range(["5", "5"], ["6", "5"], 1)

        self.assertEqual(result, True)

    # Test manhattan_distance_calculator - horizontal distance
    def test_manhattan_distance_horizontal(self):
        # Check horizontal distance
        result = Grid.manhattan_distance_calculator(8, 5, 5, 5)

        self.assertEqual(result, 3)

    # Test manhattan_distance_calculator - vertical distance
    def test_manhattan_distance_vertical(self):
        # Check vertical distance
        result = Grid.manhattan_distance_calculator(5, 5, 9, 5)

        self.assertEqual(result, 4)

    # Test manhattan_distance_calculator - diagonal distance
    def test_manhattan_distance_diagonal(self):
        # Check diagonal distance
        result = Grid.manhattan_distance_calculator(7, 5, 8, 5)

        self.assertEqual(result, 5)

    # Test manhattan_distance_calculator - same position
    def test_manhattan_distance_same_position(self):
        # Check distance from position to itself
        result = Grid.manhattan_distance_calculator(5, 5, 5, 5)

        self.assertEqual(result, 0)

    # Test manhattan_distance_calculator - negative coordinates
    def test_manhattan_distance_negative_coordinates(self):
        # Check distance using negative coordinates
        result = Grid.manhattan_distance_calculator(2, -2, 3, -1)

        self.assertEqual(result, 8)

    # Test manhattan_distance_calculator - string coordinates
    def test_manhattan_distance_string_coordinates(self):
        # Check distance using string coordinates
        result = Grid.manhattan_distance_calculator("8", "5", "7", "5")

        self.assertEqual(result, 5)

    # Test get_neighbors - all four directions
    def test_get_neighbors_all_directions(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Get neighbors of center position
        result = test_grid.get_neighbors([5, 5])

        # Expected neighboring positions
        expected_neighbors = [
            [5, 4],
            [5, 6],
            [4, 5],
            [6, 5],
        ]

        # Check neighbors
        self.assertCountEqual(result, expected_neighbors)

    # Test get_neighbors - lower left corner
    def test_get_neighbors_lower_left_corner(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Get neighbors of lower left corner
        result = test_grid.get_neighbors([0, 0])

        # Expected valid neighbors
        expected_neighbors = [
            [0, 1],
            [1, 0],
        ]

        # Check neighbors
        self.assertCountEqual(result, expected_neighbors)

    # Test get_neighbors - upper right corner
    def test_get_neighbors_upper_right_corner(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Get neighbors of upper right corner
        result = test_grid.get_neighbors([24, 24])

        # Expected valid neighbors
        expected_neighbors = [
            [24, 23],
            [23, 24],
        ]

        # Check neighbors
        self.assertCountEqual(result, expected_neighbors)

    # Test get_neighbors - wall is excluded
    def test_get_neighbors_wall_excluded(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set one neighboring tile to wall
        test_grid.set_tile(6, 5, "wall")
        # Get neighbors
        result = test_grid.get_neighbors([5, 5])

        # Expected neighbors excluding wall
        expected_neighbors = [
            [5, 4],
            [5, 6],
            [4, 5],
        ]

        # Check neighbors
        self.assertCountEqual(result, expected_neighbors)

    # Test get_neighbors - shallow water is included
    def test_get_neighbors_shallow_water(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set one neighboring tile to shallow water
        test_grid.set_tile(6, 5, "shallowwater")
        # Get neighbors
        result = test_grid.get_neighbors([5, 5])

        # Check shallow water is included
        self.assertIn([6, 5], result)

    # Test get_neighbors - all neighboring tiles are walls
    def test_get_neighbors_surrounded_by_walls(self):
        # Create grid
        test_grid = self.create_test_grid()
        # Set all four neighboring tiles to walls
        test_grid.set_tile(5, 4, "wall")
        test_grid.set_tile(5, 6, "wall")
        test_grid.set_tile(4, 5, "wall")
        test_grid.set_tile(6, 5, "wall")
        # Get neighbors
        result = test_grid.get_neighbors([5, 5])

        # Check no valid neighbors remain
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
