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
from grid import Grid, Tile
import command_line_interface as cli
import domain_library as dl


class TestEquipment(unittest.TestCase):

    # test grid proper grid init
    def test_correct_grid_init_at_lower_bound(self):
        # Create grid
        test_grid = Grid(5, 5)

        self.assertEqual(test_grid.width, 5)
        self.assertEqual(test_grid.height, 5)
        self.assertEqual(test_grid.grid[0][0].t_type, "Floor")

    # test grid with too small init
    def test_grid_init_below_lower_bounds(self):
        # Create grid
        test_grid = Grid(1, 1)

        self.assertEqual(test_grid.width, 1)
        self.assertEqual(test_grid.height, 1)
        self.assertEqual(test_grid.grid, [])

    # test grid with too large init
    def test_grid_init_above_bounds(self):
        # Create grid
        test_grid = Grid(51, 51)

        self.assertEqual(test_grid.width, 51)
        self.assertEqual(test_grid.height, 51)
        self.assertEqual(test_grid.grid, [])

    # test grid proper grid init
    def test_correct_grid_init_at_higher_bound(self):
        # Create grid
        test_grid = Grid(50, 50)

        self.assertEqual(test_grid.width, 50)
        self.assertEqual(test_grid.height, 50)
        self.assertEqual(test_grid.grid[0][0].t_type, "Floor")

    # test is_occupied success
    def test_is_occupied_success_with_occupant(self):
        # create grid
        test_grid = Grid(25, 25)
        # Add occupant  - LIST
        test_grid.grid[0][0].occupants = [1]
        self.assertEqual(test_grid.is_occupied(0, 0), True)

    # test is_occupied x/y int fail
    def test_is_occupied_not_ints_provided(self):
        # create grid
        test_grid = Grid(25, 25)
        # Add occupant  - LIST
        test_grid.grid[0][0].occupants = [1]
        self.assertEqual(test_grid.is_occupied(0, "sev"), None)

    # test is_occupied success without occupants
    def test_is_occupied_success_without_occupant(self):
        # create grid
        test_grid = Grid(25, 25)
        # Add occupant  - LIST
        test_grid.grid[0][0].occupants = []
        self.assertEqual(test_grid.is_occupied(0, 0), False)

    # test occupy success
    def test_occupy_success(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = []
        # add occupants
        test_grid.occupy(0, 0, 0)
        self.assertEqual(test_grid.grid[0][0].occupants[0], 0)

    # test occupy failure due to ints not being strings
    def test_occupy_int_typing_fail(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = []
        # add occupants
        test_grid.occupy(0, "sev", 0)
        self.assertEqual(test_grid.grid[0][0].occupants, [])

    # test clear occupant (only 1) from grid position
    def test_clear_occupant_success(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = []
        # add occupants
        test_grid.occupy(0, 0, 0)
        # Clear occupant
        test_grid.clear_occupant(0, 0, 0)
        self.assertEqual(test_grid.grid[0][0].occupants, [])

    # test clear occupant (3) from grid position
    def test_clear_occupant_success_with_occupants(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = []
        # add occupants
        test_grid.occupy(0, 0, 0)
        test_grid.occupy(0, 0, 1)
        test_grid.occupy(0, 0, 2)
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)
        self.assertEqual(test_grid.grid[0][0].occupants, [0, 2])

    # test clear occupant (3) from grid position
    def test_clear_occupant_without_occupants(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = []
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)
        self.assertEqual(test_grid.grid[0][0].occupants, [])

    # test if tile on grid is passable - true due to floor at 0, 0
    def test_is_passable_true(self):
        # create grid
        test_grid = Grid(25, 25)
        # Clear occupant
        test_grid.grid[0][0].passable = True
        self.assertEqual(test_grid.is_passable(0, 0), True)

    # test if tile on grid is passable - false due to wall at 0, 0
    def test_is_passable_false(self):
        # create grid
        test_grid = Grid(25, 25)
        # Clear occupant
        test_grid.grid[0][0].passable = False
        self.assertEqual(test_grid.is_passable(0, 0), False)

    # test to get stats of grid position
    def test_get_stats(self):
        # create grid
        test_grid = Grid(25, 25)
        # Reset occupants  - LIST
        test_grid.grid[0][0].occupants = [0, 1, 2, 3, 5, 4, 7]
        # Clear occupant
        test_grid.clear_occupant(0, 0, 1)
        self.assertEqual(
            test_grid.get_stats(0, 0), (0, 0, "Floor", True, [0, 2, 3, 5, 4, 7])
        )

    # test to see if ints provided are within bounds - ints are within bouns
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
        temp_grid = Grid(25, 25)
        self.assertEqual(temp_grid.is_valid_grid_position(25, 25), False)

    # test to see if ints provided are within grid bounds - ints are on lower boundary
    def test_valid_grid_posiiton_true_lower_boundary(self):
        temp_grid = Grid(25, 25)
        self.assertEqual(temp_grid.is_valid_grid_position(0, 0), True)

    # test to see if ints provided are within bounds - ints are on higher boundary
    def test_valid_grid_positions_true_higher_boundary(self):
        temp_grid = Grid(25, 25)
        self.assertEqual(temp_grid.is_valid_grid_position(24, 24), True)

    # test to see if ints provided are within grid bounds - ints are lower
    def test_valid_grid_positions_false_lower(self):
        temp_grid = Grid(25, 25)
        self.assertEqual(temp_grid.is_valid_grid_position(-1, -1), False)

    # test to see if ints provided are within bounds - ints are vlid
    def test_valid_grid_positions_true(self):
        temp_grid = Grid(25, 25)
        self.assertEqual(temp_grid.is_valid_grid_position(15, 15), True)

    # Test set_tile success
    def test_set_tile_success(self):
        # create grid with entities and set tile
        temp_grid = Grid(25, 25)
        temp_grid.occupy(0, 0, 1)
        temp_grid.occupy(0, 0, 2)
        temp_grid.occupy(0, 0, 0)
        temp_grid.set_tile(0, 0, "shallowwater")
        stats = temp_grid.get_stats(0, 0)
        self.assertEqual(stats[0], 0)
        self.assertEqual(stats[1], 0)
        self.assertEqual(stats[2], "ShallowWater")
        self.assertEqual(stats[3], True)
        self.assertEqual(stats[4], [1, 2, 0])

    # test spawn entity
    def test_spawn_entity_success(self):
        # create grid
        temp_grid = Grid(25, 25)
        # reset
        cli.entity_list = []
        cli.entity_ids_issued = 0
        # spawn entity
        temp_entity = temp_grid.spawn_entity(0, 0, "warrior", cli.entity_ids_issued)
        # check values
        self.assertEqual(temp_entity.position, [0, 0])
        self.assertEqual(temp_grid.grid[0][0].occupants, [temp_entity.id])

    # Tests for Tile initialization
    def test_tile_init(self):
        tile = Tile(
            "floor",
            True,
            [],
            {"Speed": "-2"},
        )

        self.assertEqual(tile.t_type, "floor")
        self.assertEqual(tile.passable, True)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(
            tile.modifiers,
            {"Speed": "-2"},
        )

    # Tests for Tile initialization with no modifiers
    def test_tile_init_no_modifiers(self):
        tile = Tile(
            "floor",
            True,
            [],
        )

        self.assertEqual(tile.t_type, "floor")
        self.assertEqual(tile.passable, True)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(tile.modifiers, {})

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

        self.assertEqual(tile.t_type, "Floor")
        self.assertEqual(tile.passable, True)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(tile.modifiers, {})

    # Tests for create_tile with wall
    def test_create_tile_wall(self):
        tile = Tile.create_tile("wall")

        self.assertEqual(tile.t_type, "Wall")
        self.assertEqual(tile.passable, False)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(tile.modifiers, {})

    # Tests for create_tile with shallow water
    def test_create_tile_shallow_water(self):
        tile = Tile.create_tile("shallowwater")

        self.assertEqual(tile.t_type, "ShallowWater")
        self.assertEqual(tile.passable, True)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(
            tile.modifiers,
            {"Speed": "-2"},
        )

    # Tests for create_tile with shallow water
    def test_create_tile_forest(self):
        tile = Tile.create_tile("forest")

        self.assertEqual(tile.t_type, "Forest")
        self.assertEqual(tile.passable, True)
        self.assertEqual(tile.occupants, [])
        self.assertDictEqual(
            tile.modifiers,
            {"Defence": "+5", "Speed": "-1"},
        )

    # Tests for create_tile with invalid tile type
    def test_create_tile_invalid(self):
        tile = Tile.create_tile("invalid")
        self.assertEqual(tile, None)

    # Test adding an item to a tile item list
    def test_add_item_to_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Check item was added
        self.assertEqual(
            len(temp_grid.grid[0][0].item_list),
            1,
        )

        self.assertEqual(
            temp_grid.grid[0][0].item_list[0].name,
            "IronSword",
        )

    # Test adding multiple items to a tile item list
    def test_add_multiple_items_to_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add items
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "curseddagger",
        )

        # Check items
        self.assertEqual(
            len(temp_grid.grid[0][0].item_list),
            2,
        )

        self.assertEqual(
            temp_grid.grid[0][0].item_list[0].name,
            "IronSword",
        )

        self.assertEqual(
            temp_grid.grid[0][0].item_list[1].name,
            "CursedDagger",
        )

    # Test adding an item to a different tile
    def test_add_item_to_different_tile(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        temp_grid.clear_tile_item_list(2, 3)
        # Add item to first tile
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )
        # Add item to second tile
        temp_grid.add_item_to_tile_item_list(
            2,
            3,
            "magestaff",
        )
        # Check first tile
        self.assertEqual(
            len(temp_grid.grid[0][0].item_list),
            1,
        )
        self.assertEqual(
            temp_grid.grid[0][0].item_list[0].name,
            "IronSword",
        )

        # Check second tile
        self.assertEqual(
            len(temp_grid.grid[2][3].item_list),
            1,
        )

        self.assertEqual(
            temp_grid.grid[2][3].item_list[0].name,
            "MageStaff",
        )

    # Test removing an item from a tile item list
    def test_remove_item_from_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Remove item
        temp_grid.remove_item_from_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Check item was removed
        self.assertEqual(
            temp_grid.grid[0][0].item_list,
            [],
        )

    # Test removing one item while another remains
    def test_remove_item_from_tile_item_list_with_multiple_items(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add items
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "curseddagger",
        )

        # Remove one item
        temp_grid.remove_item_from_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Check remaining item
        self.assertEqual(
            len(temp_grid.grid[0][0].item_list),
            1,
        )

        self.assertEqual(
            temp_grid.grid[0][0].item_list[0].name,
            "CursedDagger",
        )

    # Test removing an item using different capitalization
    def test_remove_item_case_insensitive(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Remove item using uppercase
        temp_grid.remove_item_from_tile_item_list(
            0,
            0,
            "IRONSWORD",
        )

        # Check item was removed
        self.assertEqual(
            temp_grid.grid[0][0].item_list,
            [],
        )

    # Test removing an item that does not exist
    def test_remove_nonexistent_item_from_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add item
        temp_grid.add_item_to_tile_item_list(
            0,
            0,
            "ironsword",
        )

        # Try removing different item
        temp_grid.remove_item_from_tile_item_list(
            0,
            0,
            "magestaff",
        )

        # Original item should remain
        self.assertEqual(
            len(temp_grid.grid[0][0].item_list),
            1,
        )

        self.assertEqual(
            temp_grid.grid[0][0].item_list[0].name,
            "IronSword",
        )

    # Test setting a tile item list
    def test_set_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        item_list = [
            dl.EQUIPMENT_TYPES["ironsword"],
            dl.EQUIPMENT_TYPES["magestaff"],
        ]

        temp_grid.set_tile_item_list(
            0,
            0,
            item_list,
        )

        # Check item list
        self.assertEqual(
            temp_grid.grid[0][0].item_list,
            item_list,
        )

    # Test clearing a tile item list
    def test_clear_tile_item_list(self):
        temp_grid = Grid(5, 5)
        # reset
        temp_grid.clear_tile_item_list(0, 0)
        # Add items directly
        temp_grid.grid[0][0].item_list = [
            dl.EQUIPMENT_TYPES["ironsword"],
            dl.EQUIPMENT_TYPES["magestaff"],
        ]

        # Clear list
        temp_grid.clear_tile_item_list(
            0,
            0,
        )

        # Check list is empty
        self.assertEqual(
            temp_grid.grid[0][0].item_list,
            [],
        )
