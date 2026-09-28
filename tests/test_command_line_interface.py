"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_cml.py
Purpose: Utilizes unittest to test all of the fron facing functions to insure there are no catastrohpic errors that make it into the game.
"""

# Imports
import unittest
from unittest.mock import patch
import io
from command_line_interface import CLI
from grid import Grid
import domain_library as dl
from entity import Entity


class TestCLI(unittest.TestCase):

    # Unknown Commands Start
    def test_unknown_command(self):
        # Create test CLI
        test_cli = CLI()
        command = "Not a command"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: Unknown command!\n")

    # Init Commands Start
    def test_init_map_incorrect_command_pieces(self):
        # Create test CLI
        test_cli = CLI()
        command = "init cap 6 6"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: map_init_failed due to invalid arguments.\n")

    def test_init_map_incorrect_number_of_command_pieces(self):
        # Create test CLI
        test_cli = CLI()
        command = "init cap 6"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: map_init_failed due to invalid arguments.\n")

    def test_init_map_with_map_created(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create map
        test_cli.process_command("init map 10 10")
        command = "init map 6 6"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: map_init_failed - Map is already created!\n")

    def test_init_map_with_invalid_width_int(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map dozen 6"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height are not valid integers!\n",
        )

    def test_init_map_with_invalid_height_int(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 12 dozen"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height are not valid integers!\n",
        )

    def test_init_map_with_both_bounds_higher_than_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 60 60"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_width_bounds_higher_than_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 60 30"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_height_bounds_higher_than_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 30 51"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_both_bounds_lower_than_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 4 4"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_width_bounds_lower_than_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 4 30"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_height_bounds_lower_than_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 30 4"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_width_bounds_lower_than_min_and_height_higher_than_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 4 51"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_height_bounds_lower_than_min_and_width_higher_than_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 51 4"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: map_init_failed - Width and height exceed bound minimum and maximum!\n",
        )

    def test_init_map_with_max_bounds(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 50 50"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: map_initialized width: 50 height: 50!\n",
        )

    def test_init_map_with_min_bounds(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 5 5"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: map_initialized width: 5 height: 5!\n",
        )

    # Success for init map
    def test_init_map_success(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "init map 30 30"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: map_initialized width: 30 height: 30!\n",
        )

    # Set Cases
    def test_set_tile_incorrect_number_of_command_pieces(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "set tile 6 6"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: set_tile_failed - Invalid arguments!\n")

    def test_set_tile_with_wrong_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "set type 10 10 floor"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(output, "error: set_tile_failed - Invalid arguments!\n")

    def test_set_tile_without_map_created(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "set tile 10 10 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_set_failed - Map does not exist!\n",
        )

    def test_set_tile_without_valid_x_int(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile dozen 10 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y are not valid integers!\n",
        )

    def test_set_tile_without_valid_y_int(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 10 dozen wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y are not valid integers!\n",
        )

    def test_set_tile_with_x_bounds_higher_than_grid_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 26 10 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_set_tile_with_y_bounds_higher_than_grid_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 20 26 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_set_tile_with_y_bounds_lower_than_grid_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 20 -1 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_set_tile_with_x_bounds_lower_than_grid_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile -1 20 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - x and y exceed current grid bounds!\n",
        )

    # zero indexed so 25x25 = 0-24
    def test_set_tile_with_x_y_on_lower_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 0 0 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: tile_set 0, 0 type: Wall!\n",
        )

    # zero indexed so 25x25 = 0-24
    def test_set_tile_with_x_y_on_higher_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 24 24 wall"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: tile_set 24, 24 type: Wall!\n",
        )

    def test_set_tile_with_invalid_tile_type(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set tile 24 24 NOTATYPE"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: set_tile_failed - Tile type provided was invalid!\n",
        )

    def test_set_tile_success(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "set TILE 24 24 WalL"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: tile_set 24, 24 type: Wall!\n",
        )

    # Spawn cases
    def test_spawn_entity_invalid_command_length(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "spawn"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid arguments!\n",
        )

    def test_spawn_entity_invalid_command_arguments(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn NOTENTITYTYPE 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid arguments!\n",
        )

    def test_spawn_entity_map_not_created(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        command = "spawn warrior 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - Map does not exist!\n",
        )

    def test_spawn_entity_invalid_x_value(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior nineT 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    def test_spawn_entity_invalid_y_value(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 nineT"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    def test_spawn_entity_y_position_higher_than_height(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 25"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    def test_spawn_entity_y_position_lower_than_height(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 -1"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    # Entity will be generated and will be 0 as it is the first one created
    def test_spawn_entity_y_position_on_min_height_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned warrior at 10, 0. id: 0!\n",
        )

    # Entity will be generated and will be 0 as it is the first one created
    def test_spawn_entity_y_position_on_max_height_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 24"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned warrior at 10, 24. id: 0!\n",
        )

    def test_spawn_entity_x_position_higher_than_width(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 25 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    def test_spawn_entity_x_position_lower_than_width(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior -1 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    # Entity will be generated and will be 0 as it is the first one created
    def test_spawn_entity_x_position_on_min_width_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 0 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned warrior at 0, 10. id: 0!\n",
        )

    # Entity will be generated and will be 0 as it is the first one created
    def test_spawn_entity_x_position_on_max_width_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 24 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned warrior at 24, 10. id: 0!\n",
        )

    def test_spawn_entity_on_existing_entity(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior at 10 10
        test_cli.process_command("spawn warrior 10 10")
        command = "spawn goblin 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: spawn_failed - Entity is already present at (10, 10)!\n",
        )

    def test_spawn_entity_with_mage_entity_type(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        test_cli.entity_list.clear()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn mage 10 10"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned mage at 10, 10. id: 0!\n",
        )
        # other checks

        entity = test_cli.entity_list[0]

        # Check that Health and Mana are tracked
        self.assertEqual(entity.mana, entity.max_mana)
        self.assertEqual(entity.health, entity.max_health)

    # Standard = types that do not require inheritance (warrior, goblin, skeleton, etc)
    def test_spawn_entity_with_standard_entity_type(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "spawn warrior 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned warrior at 10, 10. id: 0!\n",
        )
        # other check
        entity = test_cli.entity_list[0]

        # Check that only Health is tracked
        self.assertEqual(entity.health, entity.max_health)

    # Only sends back the last entity spawned id: 3 (0, 1, 2, X)
    def test_spawn_all_entities(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")

        # Create entities
        test_cli.process_command("spawn warrior 10 11")
        test_cli.process_command("spawn mage 11 10")
        test_cli.process_command("spawn goblin 11 11")
        command = "spawn skeleton 12 12"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned skeleton at 12, 12. id: 3!\n",
        )

    def test_spawn_multiple_entities_max_stats(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn warrior
        test_cli.process_command("spawn warrior 10 10")

        # Spawn mage
        test_cli.process_command("spawn mage 11 10")

        # Get spawned entities
        warrior = test_cli.entity_list[0]
        mage = test_cli.entity_list[1]

        # Check that the entities have different IDs
        self.assertNotEqual(warrior.id, mage.id)

        # Check warrior max stats
        self.assertEqual(warrior.max_health, 120)

        # Check mage max stats
        self.assertEqual(mage.max_health, 70)
        self.assertEqual(mage.max_mana, 100)

    def test_spawn_increments_entity_id(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn first entity
        test_cli.process_command("spawn warrior 10 10")

        # Spawn second entity
        test_cli.process_command("spawn mage 11 10")

        # Check that entity IDs are assigned correctly
        self.assertEqual(test_cli.entity_list[0].id, 0)
        self.assertEqual(test_cli.entity_list[1].id, 1)

        # Check that the next ID has been incremented
        self.assertEqual(test_cli.entity_ids_issued, 2)

    # Only sends back the last entity spawned id: 8 (0, 1, 2, 3, 4, 5, 6, X)
    def test_spawn_multiple_of_all_entities(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # create entities
        test_cli.process_command("spawn warrior 10 11")
        test_cli.process_command("spawn warrior 11 10")
        test_cli.process_command("spawn goblin 11 11")
        test_cli.process_command("spawn goblin 12 12")
        test_cli.process_command("spawn mage 12 11")
        test_cli.process_command("spawn mage 11 12")
        test_cli.process_command("spawn skeleton 13 12")
        command = "spawn skeleton 12 13"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "ok: Spawned skeleton at 12, 13. id: 7!\n",
        )

    # Equip Cases
    def test_equip_with_incomplete_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "swap this command is too long"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: swap_failed - Invalid command!\n",
        )

    def test_equip_with_correct_equipment_and_invalid_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip ironsword primary"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: Unknown command!\n",
        )

    def test_equip_with_correct_slot_and_invalid_equipment(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip MoonDaggerThatDoesNotExist weapon"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: Unknown command!\n",
        )

    def test_equip_invalid_equipment_and_no_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip MoonDaggerThatDoesNotExist"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: Unknown command!\n",
        )

    def test_equip_with_no_player_entity_created(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        command = "swap 0 weapon IronSWORD"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: swap_failed - Entity does not exist!\n",
        )

    def test_equip_with_valid_weapon_but_incorrect_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        command = "swap 0 armor IronSWORD"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: swap_failed - Slot inccorect for item type!\n",
        )

    # success
    def test_equip_with_valid_weapon_and_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        command = "swap 0 weapon ironsword"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # print(f"FAILED OUTPUT: {output}")
        # check output
        self.assertEqual(
            output,
            "Valid items: ironsword, curseddagger, magestaff, ironchestplate, leathertunic, scoutarmor, ringofthesorcerer, amuletofvitality, ringofhaste, none_wep, none_armor, none_acc, smallhealthpotion, greaterhealthpotion, superiorhealthpotion, manapotion, turtlemasterpotion\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: swapped Weapon with backpack item!\n",
        )

    # inventory cases
    def test_inventory_with_invalid_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory display please!"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inventory_failed - Invalid command!\n",
        )

    def test_inventory_with_no_player(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        command = "inventory 99"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inventory_failed - Player entity does not exist!\n",
        )

    def test_inventory_with_no_map(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory 99"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inventory_failed - Player entity does not exist!\n",
        )

    # Success
    def test_inventory_success(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            # Display inventory of entity
            "Weapon: None\n"
            "Armor: None\n"
            "Accessory: None\n"
            "Backpack Slots:\n"
            "1. Empty\n"
            "2. Empty\n"
            "3. Empty\n"
            "4. Empty\n"
            "5. Empty\n",
        )

    # Success
    def test_inventory_success_with_equips(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        test_cli.process_command("spawn warrior 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("scoutarmor"))
        entity.add_item_to_backpack(dl.create_equipment("amuletofvitality"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        # Change all slots
        test_cli.process_command("swap 0 armor scoutarmor")
        test_cli.process_command("swap 0 accessory amuletofvitality")
        test_cli.process_command("swap 0 weapon ironsword")
        command = "inventory 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            # Display inventory of entity
            "Weapon: IronSword\n"
            "Armor: ScoutArmor\n"
            "Accessory: AmuletOfVitality\n"
            "Backpack Slots:\n"
            "1. ScoutArmor\n"
            "2. AmuletOfVitality\n"
            "3. IronSword\n"
            "4. Empty\n"
            "5. Empty\n",
        )
        # Check that entity max Health equals current Health -  didnt lose hp
        self.assertEqual(
            entity.max_health,
            entity.health,
        )

    # Success
    def test_inventory_success_with_equips_mage(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # clear out entity list
        test_cli.reset_entity_list()

        # Create Map
        test_cli.process_command("init map 25 25")

        # spawn mage
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        test_cli.process_command("spawn mage 10 10")

        # backpack fix
        entity = test_cli.entity_list[0]

        entity.add_item_to_backpack(dl.create_equipment("scoutarmor"))
        entity.add_item_to_backpack(dl.create_equipment("ringofthesorcerer"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))

        # Change all slots
        test_cli.process_command("swap 0 armor scoutarmor")
        test_cli.process_command("swap 0 accessory ringofthesorcerer")
        test_cli.process_command("swap 0 weapon ironsword")

        command = "inventory 0"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # check output
        self.assertEqual(
            output,
            # Display inventory of entity
            "Weapon: IronSword\n"
            "Armor: ScoutArmor\n"
            "Accessory: RingOfTheSorcerer\n"
            "Backpack Slots:\n"
            "1. ScoutArmor\n"
            "2. RingOfTheSorcerer\n"
            "3. IronSword\n"
            "4. Empty\n"
            "5. Empty\n",
        )

        # Check that entity max Health equals current Health
        self.assertEqual(
            entity.max_health,
            entity.health,
        )

        # Check that entity max Mana equals current Mana
        self.assertEqual(
            entity.max_mana,
            entity.mana,
        )

    # Inspect Cases
    def test_inspect_with_invalid_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        command = "inspect nothing really"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - Invalid arguments!\n",
        )

    def test_inspect_with_invalid_command_less_than_2_pieces(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        command = "inspect"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - Invalid arguments!\n",
        )

    def test_inspect_with_no_player(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - No entities exist yet!\n",
        )

    def test_inspect_with_no_map(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - No entities exist yet!\n",
        )

    def test_inspect_with_invalid_entity_id(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        command = "inspect zip"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - Entity id is not valid integer!\n",
        )

    def test_inspect_with_no_entity_matching_id_number(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        command = "inspect 100"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inspect_failed - Entity does not exist!\n",
        )

    # success
    def test_inspect_success(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Warrior\n"
            "Position: [10, 10]\n"
            "Health: 120\n"
            "Attack: 15\n"
            "Defence: 10\n"
            "Speed: 5\n"
            "Active_modifiers: 0\n",
        )

    # success with mage custom inventory + stat changes (both % and flat)
    def test_inspect_success_with_mage(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        # spawn warrior
        test_cli.process_command("spawn mage 10 10")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Mage\n"
            "Position: [10, 10]\n"
            "Health: 70\n"
            "Mana: 100\n"
            "Attack: 8\n"
            "Defence: 4\n"
            "Speed: 5\n"
            "Active_modifiers: 0\n",
        )

    # success with custom inventory + stat changes (both % and flat, also -)
    def test_inspect_success_with_custom_inventory(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironchestplate"))
        entity.add_item_to_backpack(dl.create_equipment("amuletofvitality"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        # Change all slots
        test_cli.process_command("swap 0 armor ironchestplate")
        test_cli.process_command("swap 0 accessory amuletofvitality")
        test_cli.process_command("swap 0 weapon ironsword")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Warrior\n"
            "Position: [10, 10]\n"
            "Health: 132.0\n"
            "Attack: 27\n"
            "Defence: 28\n"
            "Speed: 3\n"
            "Active_modifiers: 4\n",
        )

    # success with mage custom inventory + stat changes (both % and flat, also -)
    def test_inspect_success_with_mage_with_custom_inventory(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        # spawn warrior
        test_cli.process_command("spawn mage 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironchestplate"))
        entity.add_item_to_backpack(dl.create_equipment("ringofthesorcerer"))
        entity.add_item_to_backpack(dl.create_equipment("magestaff"))
        # Change all slots
        test_cli.process_command("swap 0 armor ironchestplate")
        test_cli.process_command("swap 0 accessory ringofthesorcerer")
        test_cli.process_command("swap 0 weapon magestaff")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Mage\n"
            "Position: [10, 10]\n"
            "Health: 70\n"
            "Mana: 115.0\n"
            "Attack: 8\n"
            "Defence: 19\n"
            "Speed: 3\n"
            "Active_modifiers: 4\n",
        )

    # success with warrior custom inventory + stat changes (both % and flat, also -)
    def test_inspect_success_with_warrior_with_mage_specific_items(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # Reset
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironchestplate"))
        entity.add_item_to_backpack(dl.create_equipment("amuletofvitality"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        # Change all slots
        test_cli.process_command("swap 0 armor ironchestplate")
        test_cli.process_command("swap 0 accessory ringofthesorcerer")
        test_cli.process_command("swap 0 weapon magestaff")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Warrior\n"
            "Position: [10, 10]\n"
            "Health: 120\n"
            "Attack: 15\n"
            "Defence: 25\n"
            "Speed: 3\n"
            "Active_modifiers: 2\n",
        )

    # success with warrior custom inventory + stat changes including tile modifiers
    def test_inspect_success_with_warrior_with_tile_with_modifiers_placed_before_entity(
        self,
    ):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile at 10, 10
        test_cli.grid.set_tile(10, 10, "shallowwater")
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironchestplate"))
        entity.add_item_to_backpack(dl.create_equipment("amuletofvitality"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        # Change all slots
        test_cli.process_command("swap 0 armor ironchestplate")
        test_cli.process_command("swap 0 accessory amuletofvitality")
        test_cli.process_command("swap 0 weapon ironsword")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Warrior\n"
            "Position: [10, 10]\n"
            "Health: 132.0\n"
            "Attack: 27\n"
            "Defence: 28\n"
            "Speed: 1\n"
            "Active_modifiers: 4\n",
        )

    # success with warrior custom inventory + stat changes including tile modifiers
    def test_inspect_success_with_warrior_with_tile_with_modifiers_placed_after_entity(
        self,
    ):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # set tile at 10, 10
        test_cli.grid.set_tile(10, 10, "shallowwater")
        # backpack fix
        entity = test_cli.entity_list[0]
        entity.add_item_to_backpack(dl.create_equipment("ironchestplate"))
        entity.add_item_to_backpack(dl.create_equipment("amuletofvitality"))
        entity.add_item_to_backpack(dl.create_equipment("ironsword"))
        # Change all slots
        test_cli.process_command("swap 0 armor ironchestplate")
        test_cli.process_command("swap 0 accessory amuletofvitality")
        test_cli.process_command("swap 0 weapon ironsword")
        command = "inspect 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Id: 0\n"
            "Type: Warrior\n"
            "Position: [10, 10]\n"
            "Health: 132.0\n"
            "Attack: 27\n"
            "Defence: 28\n"
            "Speed: 1\n"
            "Active_modifiers: 4\n",
        )

    # tile cases
    def test_tile_with_invalid_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        command = "tile nothing really lol"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - Invalid command!\n",
        )

    def test_tile_with_short_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        test_cli.reset_entity_list()
        command = "tile"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - Invalid command!\n",
        )

    def test_tile_with_invalid_x_value(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        test_cli.reset_entity_list()
        command = "tile nineT 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y are not valid integers!\n",
        )

    def test_tile_with_invalid_y_value(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "tile 10 fortyy"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y are not valid integers!\n",
        )

    def test_tile_without_map(self):
        # Create test CLI
        test_cli = CLI()
        test_cli.grid = Grid.reset_grid()
        command = "tile 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - Map does not exist!\n",
        )

    # FIX THESE

    def test_tile_with_x_bounds_higher_than_grid_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "tile 26 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_tile_with_y_bounds_higher_than_grid_max(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "tile 10 26"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_tile_with_y_bounds_lower_than_grid_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "tile 10 -1"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y exceed current grid bounds!\n",
        )

    def test_tile_with_x_bounds_lower_than_grid_min(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        command = "tile -1 20"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: tile_failed - x and y exceed current grid bounds!\n",
        )

    # zero indexed so 25x25 = 0-24 - Success
    def test_tile_with_x_y_on_lower_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile to wall
        test_cli.grid.set_tile(0, 0, "wall")
        command = "tile 0 0"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Coordinate: 0, 0\n" "Type: Wall\n" "Passable: False\n" "Occupants: None\n",
        )

    # zero indexed so 25x25 = 0-24 - Success
    def test_tile_with_x_y_on_higher_boundary(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile to wall
        test_cli.grid.set_tile(24, 24, "wall")
        command = "tile 24 24"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Coordinate: 24, 24\n"
            "Type: Wall\n"
            "Passable: False\n"
            "Occupants: None\n",
        )

    # success
    def test_tile_success(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile to wall
        test_cli.grid.set_tile(10, 10, "shallowwater")
        command = "tile 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Coordinate: 10, 10\n"
            "Type: ShallowWater\n"
            "Passable: True\n"
            "Occupants: None\n",
        )

    # success with occupant
    def test_tile_success_with_occupant(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile to wall
        test_cli.grid.set_tile(10, 10, "shallowwater")
        # spawn entity
        test_cli.process_command("spawn warrior 10 10")
        command = "tile 10 10"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Coordinate: 10, 10\n"
            "Type: ShallowWater\n"
            "Passable: True\n"
            "Occupants: 0\n",
        )

    # Test invalid command with too few arguments
    def test_pickup_item_invalid_command_too_few_arguments(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "0"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Invalid command!\n",
        )

    # Test invalid command with too many arguments
    def test_pickup_item_invalid_command_too_many_arguments(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "0", "IronSword", "extra"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Invalid command!\n",
        )

    # Test pickup when map does not exist
    def test_pickup_item_no_map(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "0", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Map does not exist!\n",
        )

    # Test pickup with an invalid entity ID
    def test_pickup_item_invalid_entity_id(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "-1", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Entity does not exist!\n",
        )

    # Test pickup with an entity ID that does not exist
    def test_pickup_item_nonexistent_entity(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "9999", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Entity does not exist!\n",
        )

    # Test pickup with an invalid item name
    def test_pickup_item_invalid_item_name(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", "0", "NotAnItem"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Item name not found!\n",
        )

    # Test pickup with different item name capitalization
    def test_pickup_item_case_insensitive(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = "ironsword"
        item_class = dl.EQUIPMENT_TYPES[item_name]

        # Place item class on entity's tile
        test_cli.grid.grid[10][10].item_list.append(item_class)

        # Add existing item to backpack
        entity.backpack.append("Existing Item")

        # Process command using uppercase item name
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(
                ["pickup", str(entity.id), item_name.upper()]
            )

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: picked_up IronSword into backpack!\n")

        # Check item was added to backpack
        self.assertTrue(
            any(
                backpack_item.name.lower() == "ironsword"
                for backpack_item in entity.backpack
                if hasattr(backpack_item, "name")
            )
        )
        # Check item was removed from tile
        self.assertNotIn(
            item_class,
            test_cli.grid.grid[10][10].item_list,
        )

    # Test pickup when backpack is full
    def test_pickup_item_backpack_full(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.create_equipment(item_name.lower())

        # Fill backpack to maximum capacity
        entity.backpack = [
            dl.create_equipment("ironsword"),
            dl.create_equipment("leathertunic"),
            dl.create_equipment("manapotion"),
            dl.create_equipment("turtlemasterpotion"),
            dl.create_equipment("ringofhaste"),
        ]

        # Place item on entity's tile
        test_cli.grid.grid[10][10].item_list.append(item)

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Backpack if full!\n",
        )

        # Check item was not removed from tile
        self.assertIn(
            item,
            test_cli.grid.grid[10][10].item_list,
        )

    # Test pickup when item is not on the entity's tile
    def test_pickup_item_not_on_tile(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.EQUIPMENT_TYPES[item_name]

        # Process command without placing item on tile
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Item not in tiles item list!\n",
        )

        # Check backpack remains empty
        self.assertEqual(entity.backpack, [])

    # Test item on a different tile
    def test_pickup_item_on_different_tile(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.EQUIPMENT_TYPES[item_name]

        # Place item on a different tile
        test_cli.grid.grid[11][10].item_list.append(item)

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: pickup_failed - Item not in tiles item list!\n",
        )

        # Check item was not added to backpack
        self.assertNotIn(item, entity.backpack)

    # Test pickup while backpack already contains an item
    def test_pickup_item_with_existing_backpack_items(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.EQUIPMENT_TYPES[item_name]

        # Add existing item to backpack
        entity.backpack.append("Existing Item")

        # Place item on entity's tile
        test_cli.grid.grid[10][10].item_list.append(item)

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: picked_up IronSword into backpack!\n")

        # Check existing item remains
        self.assertIn("Existing Item", entity.backpack)

        # Check new item was added
        self.assertTrue(
            any(
                backpack_item.name.lower() == item_name.lower()
                for backpack_item in entity.backpack
                if hasattr(backpack_item, "name")
            )
        )

    # Test that picking up one item preserves other tile items
    def test_pickup_item_preserves_other_tile_items(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get two different valid items
        item_names = list(dl.EQUIPMENT_TYPES.keys())

        item_name = item_names[0]
        other_item_name = item_names[1]

        item = dl.EQUIPMENT_TYPES[item_name]
        other_item = dl.EQUIPMENT_TYPES[other_item_name]

        # Place both items on entity's tile
        test_cli.grid.grid[10][10].item_list.append(item)
        test_cli.grid.grid[10][10].item_list.append(other_item)

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_pickup_item_command(["pickup", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: picked_up IronSword into backpack!\n")

        # Check picked-up item was removed
        self.assertNotIn(
            item,
            test_cli.grid.grid[10][10].item_list,
        )

        # Check other item remains
        self.assertIn(
            other_item,
            test_cli.grid.grid[10][10].item_list,
        )

    # Test successful item give
    def test_give_item_success(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.create_equipment(item_name)

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            f"ok: added {item.name} to {entity.id}'s backpack!\n",
        )

        # Check item was added to backpack
        self.assertTrue(
            any(
                temp_item.name.lower() == item.name.lower()
                for temp_item in entity.backpack
            )
        )

    # Test invalid command with too few arguments
    def test_give_item_invalid_command_too_few_arguments(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", "0"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Invalid command!\n",
        )

    # Test invalid command with too many arguments
    def test_give_item_invalid_command_too_many_arguments(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", "0", "IronSword", "extra"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Invalid command!\n",
        )

    # Test give when map does not exist
    def test_give_item_no_map(self):

        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", "0", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Map does not exist!\n",
        )

    # Test give with an invalid entity ID
    def test_give_item_invalid_entity_id(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", "-1", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Entity does not exist!\n",
        )

    # Test give with an entity ID that does not exist
    def test_give_item_nonexistent_entity(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", "9999", "IronSword"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Entity does not exist!\n",
        )

    # Test give with an invalid item name
    def test_give_item_invalid_item_name(self):

        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", str(entity.id), "NotAnItem"])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Item name not found!\n",
        )

    # Test give with different item name capitalization
    def test_give_item_case_insensitive(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.create_equipment(item_name)

        # Process command using uppercase item name
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(
                ["give", str(entity.id), item_name.upper()]
            )

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            f"ok: added {item.name} to {entity.id}'s backpack!\n",
        )

        # Check item was added to backpack
        self.assertTrue(
            any(
                temp_item.name.lower() == item.name.lower()
                for temp_item in entity.backpack
            )
        )

    # Test give when backpack is full
    def test_give_item_backpack_full(self):

        # Create test CLI
        test_cli = CLI()

        # Clear out grid
        test_cli.grid = Grid.reset_grid()

        # Clear out entity list
        test_cli.entity_list.clear()

        # Create map
        test_cli.process_command("init map 25 25")

        # Spawn entity
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Get valid item
        item_name = next(iter(dl.EQUIPMENT_TYPES))
        item = dl.EQUIPMENT_TYPES[item_name]

        # Fill backpack to maximum capacity
        entity.backpack = [item for _ in range(Entity.BACKPACK_SIZE)]

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_give_item_command(["give", str(entity.id), item_name])

        # Get print output
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: give_failed - Backpack if full!\n",
        )

        # Check backpack size remains unchanged
        self.assertEqual(
            len(entity.backpack),
            Entity.BACKPACK_SIZE,
        )

    # Test Process Drop Item Command - Successful Drop
    def test_process_drop_item_command_success(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Give entity an item
        test_cli.process_command(f"give {entity.id} IronSword")

        # Drop item
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", str(entity.id), "IronSword"])
            output = fake_out.getvalue()

        # Check item was added to tile
        self.assertIn(
            dl.EQUIPMENT_TYPES["ironsword"]().name,
            test_cli.grid.grid[10][10].item_list[0].name,
        )

        # Check item was removed from backpack
        self.assertFalse(any(item.name == "IronSword" for item in entity.backpack))

        # Check no error was printed
        self.assertEqual(output, "ok: dropped IronSword onto tile!\n")

    # Test Process Drop Item Command - Invalid Command (Too Few Pieces)
    def test_process_drop_item_command_too_few_pieces(self):

        # Create CLI
        test_cli = CLI()

        # Run command with too few pieces
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", "1"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: drop_failed - Invalid command!\n")

    # Test Process Drop Item Command - Invalid Command (Too Many Pieces)
    def test_process_drop_item_command_too_many_pieces(self):

        # Create CLI
        test_cli = CLI()

        # Run command with too many pieces
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", "1", "IronSword", "extra"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: drop_failed - Invalid command!\n")

    # Test Process Drop Item Command - Map Does Not Exist
    def test_process_drop_item_command_no_map(self):

        # Create CLI
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        # Run command without creating a map
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", "1", "IronSword"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: drop_failed - Map does not exist!\n")

    # Test Process Drop Item Command - Entity Does Not Exist
    def test_process_drop_item_command_entity_not_found(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")

        # Run command with invalid entity ID
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", "999", "IronSword"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: drop_failed - Entity does not exist!\n")

    # Test Process Drop Item Command - Invalid Item Name
    def test_process_drop_item_command_invalid_item(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Run command with invalid item name
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", str(entity.id), "InvalidItem"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: drop_failed - Item name not found!\n")

    # Test Process Drop Item Command - Case-Insensitive Item Name
    def test_process_drop_item_command_case_insensitive(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Give entity an item
        test_cli.process_command(f"give {entity.id} IronSword")

        # Drop item using lowercase name
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", str(entity.id), "ironsword"])
            output = fake_out.getvalue()

        # Check item was added to tile
        self.assertIn(
            dl.EQUIPMENT_TYPES["ironsword"]().name,
            test_cli.grid.grid[10][10].item_list[0].name,
        )

        # Check item was removed from backpack
        self.assertFalse(any(item.name == "IronSword" for item in entity.backpack))

        # Check no error was printed
        self.assertEqual(output, "ok: dropped IronSword onto tile!\n")

    # Test Process Drop Item Command - Item Not In Backpack
    def test_process_drop_item_command_item_not_in_backpack(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Run command without giving the entity the item
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_drop_item_command(["drop", str(entity.id), "IronSword"])
            output = fake_out.getvalue()

        # Check item was not added to the tile
        self.assertNotIn("IronSword", test_cli.grid.grid[10][10].item_list)
        self.assertEqual(output, "error: drop_failed - Item not in backpack!\n")

    # Test Process Swap Item Command - Successful Weapon Swap
    def test_process_swap_item_command_success_weapon(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]
        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Give entity a weapon
        test_cli.process_command(f"give {entity.id} IronSword")

        # Swap weapon
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Weapon", "IronSword"]
            )
            output = fake_out.getvalue()

        # Check weapon was equipped
        self.assertEqual(
            entity.inventory[0].name, dl.create_equipment("ironsword").name
        )

        # Check success message
        # check output
        self.assertEqual(
            output,
            "Valid items: ironsword, curseddagger, magestaff, ironchestplate, leathertunic, scoutarmor, ringofthesorcerer, amuletofvitality, ringofhaste, none_wep, none_armor, none_acc, smallhealthpotion, greaterhealthpotion, superiorhealthpotion, manapotion, turtlemasterpotion\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: swapped Weapon with backpack item!\n",
        )

    # Test Process Swap Item Command - Successful Armor Swap
    def test_process_swap_item_command_success_armor(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]
        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Give entity armor
        test_cli.process_command(f"give {entity.id} IronChestplate")

        # Swap armor
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Armor", "IronChestplate"]
            )
            output = fake_out.getvalue()

        # Check armor was equipped
        self.assertEqual(
            entity.inventory[1].name, dl.create_equipment("ironchestplate").name
        )

        # Check success message
        self.assertEqual(
            output,
            "Valid items: ironsword, curseddagger, magestaff, ironchestplate, leathertunic, scoutarmor, ringofthesorcerer, amuletofvitality, ringofhaste, none_wep, none_armor, none_acc, smallhealthpotion, greaterhealthpotion, superiorhealthpotion, manapotion, turtlemasterpotion\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: swapped Armor with backpack item!\n",
        )

    # Test Process Swap Item Command - Successful Accessory Swap
    def test_process_swap_item_command_success_accessory(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]
        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Give entity accessory
        test_cli.process_command(f"give {entity.id} RingOfHaste")

        # Swap accessory
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Accessory", "RingOfHaste"]
            )
            output = fake_out.getvalue()

        # Check accessory was equipped
        self.assertEqual(
            entity.inventory[2].name, dl.create_equipment("ringofhaste").name
        )

        # Check success message
        # check output
        self.assertEqual(
            output,
            "Valid items: ironsword, curseddagger, magestaff, ironchestplate, leathertunic, scoutarmor, ringofthesorcerer, amuletofvitality, ringofhaste, none_wep, none_armor, none_acc, smallhealthpotion, greaterhealthpotion, superiorhealthpotion, manapotion, turtlemasterpotion\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: swapped Accessory with backpack item!\n",
        )

    # Test Process Swap Item Command - Invalid Command (Too Few Pieces)
    def test_process_swap_item_command_too_few_pieces(self):

        # Create CLI
        test_cli = CLI()

        # Run command with too few pieces
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(["swap", "1", "Weapon"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Invalid command!\n")

    # Test Process Swap Item Command - Invalid Command (Too Many Pieces)
    def test_process_swap_item_command_too_many_pieces(self):

        # Create CLI
        test_cli = CLI()

        # Run command with too many pieces
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", "1", "Weapon", "IronSword", "extra"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Invalid command!\n")

    # Test Process Swap Item Command - Map Does Not Exist
    def test_process_swap_item_command_no_map(self):

        # Create CLI
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        # Run command without creating a map
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(["swap", "1", "Weapon", "IronSword"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Map does not exist!\n")

    # Test Process Swap Item Command - Entity Does Not Exist
    def test_process_swap_item_command_entity_not_found(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")

        # Run command with invalid entity ID
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(["swap", "999", "Weapon", "IronSword"])
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Entity does not exist!\n")

    # Test Process Swap Item Command - Invalid Item Name
    def test_process_swap_item_command_invalid_item(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Run command with invalid item name
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Weapon", "InvalidItem"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Item name not found!\n")

    # Test Process Swap Item Command - Invalid Slot
    def test_process_swap_item_command_invalid_slot(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Run command with invalid slot
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Helmet", "IronSword"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(
            output, "error: swap_failed - Item slot not valid inventory slot!\n"
        )

    # Test Process Swap Item Command - Incorrect Slot For Item
    def test_process_swap_item_command_incorrect_item_slot(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Try to equip armor in weapon slot
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Weapon", "IronChestplate"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output, "error: swap_failed - Slot inccorect for item type!\n")

    # Test Process Swap Item Command - Case-Insensitive Slot And Item
    def test_process_swap_item_command_case_insensitive(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]
        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Give entity a weapon
        test_cli.process_command(f"give {entity.id} IronSword")

        # Swap using lowercase slot and item name
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "weapon", "ironsword"]
            )
            output = fake_out.getvalue()

        # Check weapon was equipped
        self.assertEqual(
            entity.inventory[0].name, dl.create_equipment("ironsword").name
        )

        # check output
        self.assertEqual(
            output,
            "Valid items: ironsword, curseddagger, magestaff, ironchestplate, leathertunic, scoutarmor, ringofthesorcerer, amuletofvitality, ringofhaste, none_wep, none_armor, none_acc, smallhealthpotion, greaterhealthpotion, superiorhealthpotion, manapotion, turtlemasterpotion\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: swapped Weapon with backpack item!\n",
        )

    # Test Process Swap Item Command - Consumable Item
    def test_process_swap_item_command_consumable(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Attempt to equip a consumable item
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Consumable", "smallhealthpotion"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(
            output, "error: swap_failed - Item slot not valid inventory slot!\n"
        )

        # Check consumable was not equipped
        self.assertNotIn(dl.EQUIPMENT_TYPES["smallhealthpotion"], entity.inventory)

    # Test Process Swap Item Command - Check Stats After Swapping Armor
    def test_process_swap_item_command_armor_stats(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]
        entity.backpack = []

        # Get armor items
        iron_chestplate = dl.create_equipment("ironchestplate")
        leather_tunic = dl.create_equipment("leathertunic")

        entity.inventory[1] = leather_tunic
        entity.backpack.append(leather_tunic)
        entity.backpack.append(iron_chestplate)

        # get stats
        entity.update_stats(test_cli)

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Before swap
        self.assertEqual(entity.defence, 15)
        self.assertEqual(entity.speed, 5)

        # Swap
        test_cli.process_command(f"swap {str(entity.id)} armor ironchestplate")

        # After swap
        self.assertEqual(entity.inventory[1].name, iron_chestplate.name)
        self.assertEqual(entity.defence, 25)
        self.assertEqual(entity.speed, 3)

    # Test Process Swap Item Command - Item Not In Backpack
    def test_process_swap_item_command_item_not_in_backpack(self):

        # Create CLI and initialize map
        test_cli = CLI()
        Grid.reset_grid()
        test_cli.entity_list.clear()

        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")

        # Get spawned entity
        entity = test_cli.entity_list[0]

        entity.inventory = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

        # Ensure item is not in backpack
        entity.backpack = []

        # Attempt to swap to IronChestplate
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            test_cli.process_swap_item_command(
                ["swap", str(entity.id), "Armor", "IronChestplate"]
            )
            output = fake_out.getvalue()

        # Check error message
        self.assertEqual(output.strip(), "error: swap_failed - Item not in backpack!")

        # Check armor was not equipped
        self.assertNotEqual(entity.inventory[1], dl.EQUIPMENT_TYPES["ironchestplate"])

    # Test CLI initialization
    def test_cli_init(self):

        # Create test CLI
        test_cli = CLI()

        # Check grid is initialized to None
        self.assertIsNone(test_cli.grid)

        # Check entity list is initialized empty
        self.assertEqual(test_cli.entity_list, [])

        # Check entity IDs issued is initialized to 0
        self.assertEqual(test_cli.entity_ids_issued, 0)

        # Check map created is initialized to False
        self.assertFalse(test_cli.map_created)

    # Use Commands Start

    # Test an incorrect number of command pieces
    def test_use_item_incorrect_number_of_command_pieces(self):
        # Create test CLI
        test_cli = CLI()

        command = "use 0"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Invalid command!\n",
        )

    # Test too many command pieces
    def test_use_item_too_many_command_pieces(self):
        # Create test CLI
        test_cli = CLI()

        command = "use 0 SmallHealthPotion extra"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Invalid command!\n",
        )

    # Test using an entity that does not exist
    def test_use_item_entity_does_not_exist(self):
        # Create test CLI
        test_cli = CLI()

        command = "use 999 SmallHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Entity does not exist!\n",
        )

    # Test using an invalid item name
    def test_use_item_invalid_item_name(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        command = "use 0 NotARealItem"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Item name not found!\n",
        )

    # Test using a valid item that is not in the entity's backpack
    def test_use_item_not_in_backpack(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        command = "use 0 SmallHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Item not in backpack!\n",
        )

    # Test using an item that is not a consumable
    def test_use_item_not_a_consumable(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]

        # Add a weapon to the backpack
        item = dl.EQUIPMENT_TYPES["ironsword"]()
        entity.backpack.append(item)

        command = "use 0 IronSword"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Item is not a consumable!\n",
        )

        # Check that the weapon remains in the backpack
        self.assertIn(item, entity.backpack)

    # Test using a Small Health Potion
    def test_use_small_health_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]

        # Lower health so the potion has an effect
        entity.health = 50

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["smallhealthpotion"]()
        entity.backpack.append(item)

        command = "use 0 SmallHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used SmallHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 70)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test using a Greater Health Potion
    def test_use_greater_health_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 50

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["greaterhealthpotion"]()
        entity.backpack.append(item)

        command = "use 0 GreaterHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used GreaterHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 100)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test using a Superior Health Potion
    def test_use_superior_health_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 10

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["superiorhealthpotion"]()
        entity.backpack.append(item)

        command = "use 0 SuperiorHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used SuperiorHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 110)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test using a Superior Health Potion with overflow
    def test_use_superior_health_potion_overflow(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 30

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["superiorhealthpotion"]()
        entity.backpack.append(item)

        command = "use 0 SuperiorHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used SuperiorHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 120)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)
        # Check for max health cap
        self.assertEqual(entity.max_health, entity.health)

    # Test using a Mana Potion
    def test_use_mana_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and Mage
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Mage 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.mana = 25

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["manapotion"]()
        entity.backpack.append(item)

        command = "use 0 ManaPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used ManaPotion!\n")

        # Check potion effect
        self.assertEqual(entity.mana, 75)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test using a Mana Potion with overflow
    def test_use_mana_potion_overlfow(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and Mage
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Mage 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.mana = 51

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["manapotion"]()
        entity.backpack.append(item)

        command = "use 0 ManaPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used ManaPotion!\n")

        # Check potion effect
        self.assertEqual(entity.mana, 100)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)
        # Check mana cap
        self.assertEqual(entity.max_mana, entity.mana)

    # Test using a Turtle Master Potion
    def test_use_turtle_master_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and Warrior
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 50

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()
        entity.backpack.append(item)

        command = "use 0 TurtleMasterPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used TurtleMasterPotion!\n")

        # Check instant health effect
        self.assertEqual(entity.health, 55)

        # Check that temporary buffs were added
        self.assertGreater(len(entity.temp_buffs), 0)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test that item names are case-insensitive
    def test_use_item_name_case_insensitive(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 50

        # Add potion to backpack
        item = dl.EQUIPMENT_TYPES["smallhealthpotion"]()
        entity.backpack.append(item)

        # Use potion with lowercase name
        command = "use 0 smallhealthpotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used SmallHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 70)

        # Check that potion was removed
        self.assertNotIn(item, entity.backpack)

    # Test that using one item does not remove other items
    def test_use_item_keeps_other_backpack_items(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and entity
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")

        # Get entity
        entity = test_cli.entity_list[0]
        entity.health = 50

        # Add two potions to backpack
        potion_to_use = dl.EQUIPMENT_TYPES["smallhealthpotion"]()
        other_potion = dl.EQUIPMENT_TYPES["greaterhealthpotion"]()

        entity.backpack.append(potion_to_use)
        entity.backpack.append(other_potion)

        command = "use 0 SmallHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(output, "ok: used SmallHealthPotion!\n")

        # Check potion effect
        self.assertEqual(entity.health, 70)

        # Check used potion was removed
        self.assertNotIn(potion_to_use, entity.backpack)

        # Check other potion remains
        self.assertIn(other_potion, entity.backpack)

    # Test that an item belonging to another entity cannot be used
    def test_use_item_from_another_entity_backpack(self):
        # Create test CLI
        test_cli = CLI()

        # Create map and two entities
        test_cli.process_command("init map 10 10")
        test_cli.process_command("spawn Warrior 1 1")
        test_cli.process_command("spawn Warrior 2 2")

        # Get entities
        entity_1 = test_cli.entity_list[0]
        entity_2 = test_cli.entity_list[1]

        entity_1.health = 50

        # Add potion only to the second entity
        item = dl.EQUIPMENT_TYPES["smallhealthpotion"]()
        entity_2.backpack.append(item)

        command = f"use {entity_1.id} SmallHealthPotion"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: use_failed - Item not in backpack!\n",
        )

        # Check first entity's health was not changed
        self.assertEqual(entity_1.health, 50)

        # Check second entity still has the potion
        self.assertIn(item, entity_2.backpack)

    # Spawn Loot Commands Start

    # Test an incorrect number of command pieces
    def test_spawn_loot_incorrect_number_of_command_pieces(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 2"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid arguments!\n",
        )

    # Test too many command pieces
    def test_spawn_loot_too_many_command_pieces(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 2 3 extra"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid arguments!\n",
        )

    # Test an incorrect command type
    def test_spawn_loot_incorrect_command_type(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn item IronSword 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid arguments!\n",
        )

    # Test spawning loot when a map does not exist
    def test_spawn_loot_map_does_not_exist(self):
        # Create test CLI
        test_cli = CLI()

        command = "spawn loot IronSword 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Map does not exist!\n",
        )

    # Test an invalid x coordinate
    def test_spawn_loot_invalid_x_coordinate(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword abc 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    # Test an invalid y coordinate
    def test_spawn_loot_invalid_y_coordinate(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 2 abc"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    # Test coordinates outside the grid
    def test_spawn_loot_coordinates_outside_grid(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 100 100"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    # Test a negative coordinate
    def test_spawn_loot_negative_coordinates(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword -1 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    # Test an invalid item name
    def test_spawn_loot_invalid_item_name(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot NotARealItem 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Item name not found!\n",
        )

    # Test successfully spawning an Iron Sword
    def test_spawn_loot_iron_sword(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot ironsword at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item was created
        self.assertEqual(
            tile.item_list[0].name,
            dl.EQUIPMENT_TYPES["ironsword"]().name,
        )

    # Test successfully spawning a health potion
    def test_spawn_loot_health_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot SmallHealthPotion 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot smallhealthpotion at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item was created
        self.assertEqual(
            tile.item_list[0].name,
            dl.EQUIPMENT_TYPES["smallhealthpotion"]().name,
        )

    # Test that item names are case-insensitive
    def test_spawn_loot_item_name_case_insensitive(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot ironsword 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot ironsword at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item was created
        self.assertEqual(
            tile.item_list[0].name,
            dl.EQUIPMENT_TYPES["ironsword"]().name,
        )

    # Test that multiple items can be spawned on the same tile
    def test_spawn_multiple_loot_on_same_tile(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Spawn first item
        test_cli.process_command("spawn loot IronSword 2 3")

        # Spawn second item
        command = "spawn loot SmallHealthPotion 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot smallhealthpotion at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that both items were added
        self.assertEqual(len(tile.item_list), 2)

        # Check that the correct items were created
        self.assertEqual(
            tile.item_list[0].name,
            dl.EQUIPMENT_TYPES["ironsword"]().name,
        )

        self.assertEqual(
            tile.item_list[1].name,
            dl.EQUIPMENT_TYPES["smallhealthpotion"]().name,
        )

    # Test that spawning loot does not affect another tile
    def test_spawn_loot_does_not_affect_other_tile(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        command = "spawn loot IronSword 2 3"

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot ironsword at 2, 3!\n",
        )

        # Get tiles
        target_tile = test_cli.grid.grid[2][3]
        other_tile = test_cli.grid.grid[3][2]

        # Check that loot was added to the target tile
        self.assertEqual(len(target_tile.item_list), 1)

        # Check that the other tile remains empty
        self.assertEqual(len(other_tile.item_list), 0)

    # Spawn Entity For CLI Tests Start

    # Test spawning an entity when a map does not exist
    def test_spawn_entity_no_map(self):
        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, 3, "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Map does not exist!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

    # Test spawning an entity with an invalid x coordinate
    def test_spawn_entity_invalid_x(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli("abc", 3, "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

    # Test spawning an entity with an invalid y coordinate
    def test_spawn_entity_invalid_y(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, "abc", "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

    # Test spawning an entity outside the grid
    def test_spawn_entity_outside_grid(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(100, 100, "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

    # Test spawning an entity at a negative coordinate
    def test_spawn_entity_negative_coordinates(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(-1, 3, "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

    # Test spawning an entity at an occupied location
    def test_spawn_entity_occupied_location(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Spawn first entity
        test_cli.spawn_entity_for_cli(2, 3, "Warrior")

        # Attempt to spawn another entity at the same location
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, 3, "Mage")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Entity is already present at (2, 3)!\n",
        )

        # Check that only one entity exists
        self.assertEqual(len(test_cli.entity_list), 1)

        # Check that the entity ID was not incremented again
        self.assertEqual(test_cli.entity_ids_issued, 1)

    # Test spawning an invalid entity type
    def test_spawn_entity_invalid_type(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, 3, "Dragon")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Invalid entity type!\n",
        )

        # Check that no entity was created
        self.assertEqual(len(test_cli.entity_list), 0)

        # Check that the entity ID was not incremented
        self.assertEqual(test_cli.entity_ids_issued, 0)

    # Test successfully spawning a Warrior
    def test_spawn_entity_warrior(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, 3, "Warrior")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: Spawned Warrior at 2, 3. id: 0!\n",
        )

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Check entity details
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type.lower(), "warrior")

        # Check max health
        self.assertEqual(entity.max_health, entity.health)

        # Check temporary buffs
        self.assertEqual(entity.temp_buffs, [])

        # Check entity ID counter
        self.assertEqual(test_cli.entity_ids_issued, 1)

        # Check entity was added to entity list
        self.assertEqual(len(test_cli.entity_list), 1)

        # Check grid location
        self.assertTrue(Grid.is_occupied(test_cli.grid, 2, 3))

    # Test successfully spawning a Mage
    def test_spawn_entity_mage(self):
        # Create test CLI
        test_cli = CLI()
        test_cli.reset_entity_list()
        test_cli.reset_id_issuer_tracker()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(2, 3, "Mage")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: Spawned Mage at 2, 3. id: 0!\n",
        )

        # Get spawned entity
        entity = test_cli.entity_list[0]

        # Check entity details
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type.lower(), "mage")

        # Check max health and mana
        self.assertEqual(entity.max_health, entity.health)
        self.assertEqual(entity.max_mana, entity.mana)

        # Check temporary buffs
        self.assertEqual(entity.temp_buffs, [])

        # Check entity ID counter
        self.assertEqual(test_cli.entity_ids_issued, 1)

        # Check entity was added to entity list
        self.assertEqual(len(test_cli.entity_list), 1)

        # Check grid location
        self.assertTrue(Grid.is_occupied(test_cli.grid, 2, 3))

    # Test that entity IDs increment when spawning multiple entities
    def test_spawn_multiple_entities(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Spawn first entity
        test_cli.spawn_entity_for_cli(2, 3, "Warrior")

        # Spawn second entity
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_entity_for_cli(4, 5, "Mage")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: Spawned Mage at 4, 5. id: 1!\n",
        )

        # Check entity count
        self.assertEqual(len(test_cli.entity_list), 2)

        # Check entity IDs
        self.assertEqual(test_cli.entity_list[0].id, 0)
        self.assertEqual(test_cli.entity_list[1].id, 1)

        # Check entity ID counter
        self.assertEqual(test_cli.entity_ids_issued, 2)

        # Check both grid locations
        self.assertTrue(Grid.is_occupied(test_cli.grid, 2, 3))
        self.assertTrue(Grid.is_occupied(test_cli.grid, 4, 5))

    # Spawn Loot For CLI Tests Start

    # Test spawning loot when a map does not exist
    def test_spawn_loot_for_cli_no_map(self):
        # Create test CLI
        test_cli = CLI()

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Map does not exist!\n",
        )

    # Test spawning loot with an invalid x coordinate
    def test_spawn_loot_for_cli_invalid_x(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", "abc", 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    # Test spawning loot with an invalid y coordinate
    def test_spawn_loot_for_cli_invalid_y(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", 2, "abc")

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y are not valid integers!\n",
        )

    # Test spawning loot outside the grid
    def test_spawn_loot_for_cli_outside_grid(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", 100, 100)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - x and y exceed current grid bounds!\n",
        )

    # Test spawning loot with an invalid item name
    def test_spawn_loot_for_cli_invalid_item(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("NotARealItem", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "error: spawn_failed - Item name not found!\n",
        )

    # Test successfully spawning an Iron Sword
    def test_spawn_loot_for_cli_iron_sword(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot IronSword at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item class was created
        self.assertIsInstance(
            tile.item_list[0],
            dl.EQUIPMENT_TYPES["ironsword"],
        )

    # Test successfully spawning a health potion
    def test_spawn_loot_for_cli_health_potion(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("SmallHealthPotion", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot SmallHealthPotion at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item class was created
        self.assertIsInstance(
            tile.item_list[0],
            dl.EQUIPMENT_TYPES["smallhealthpotion"],
        )

    # Test that item names are case-insensitive
    def test_spawn_loot_for_cli_case_insensitive(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("ironsword", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot ironsword at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that loot was added
        self.assertEqual(len(tile.item_list), 1)

        # Check that the correct item class was created
        self.assertIsInstance(
            tile.item_list[0],
            dl.EQUIPMENT_TYPES["ironsword"],
        )

    # Test that multiple items can be spawned on the same tile
    def test_spawn_multiple_loot_for_cli(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Spawn first item
        test_cli.spawn_loot_for_cli("IronSword", 2, 3)

        # Spawn second item
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("SmallHealthPotion", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot SmallHealthPotion at 2, 3!\n",
        )

        # Get tile
        tile = test_cli.grid.grid[2][3]

        # Check that both items were added
        self.assertEqual(len(tile.item_list), 2)

        # Check item classes
        self.assertIsInstance(
            tile.item_list[0],
            dl.EQUIPMENT_TYPES["ironsword"],
        )

        self.assertIsInstance(
            tile.item_list[1],
            dl.EQUIPMENT_TYPES["smallhealthpotion"],
        )

    # Test that spawning loot does not affect another tile
    def test_spawn_loot_for_cli_does_not_affect_other_tile(self):
        # Create test CLI
        test_cli = CLI()

        # Create map
        test_cli.process_command("init map 10 10")

        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.spawn_loot_for_cli("IronSword", 2, 3)

        # Get print output to compare
        output = mock_stdout.getvalue()

        # Check output
        self.assertEqual(
            output,
            "ok: spawn_loot IronSword at 2, 3!\n",
        )

        # Get tiles
        target_tile = test_cli.grid.grid[2][3]
        other_tile = test_cli.grid.grid[3][2]

        # Check target tile
        self.assertEqual(len(target_tile.item_list), 1)

        # Check other tile
        self.assertEqual(len(other_tile.item_list), 0)


if __name__ == "__main__":
    unittest.main()
