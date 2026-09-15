import unittest
from unittest.mock import patch
import io
from command_line_interface import CLI
from domain_library import Entity, Grid, BASE_INVENTORY, Equipment


class TestCML(unittest.TestCase):

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
            "ok: tile_set 0, 0 type: wall!\n",
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
            "ok: tile_set 24, 24 type: wall!\n",
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
            "ok: tile_set 24, 24 type: wall!\n",
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
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip this command is too long"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: equip_failed - Invalid arguments!\n",
        )

    def test_equip_with_correct_equipment_and_invalid_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
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
            "error: equip_failed - Invalid arguments!\n",
        )

    def test_equip_with_correct_slot_and_invalid_equipment(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
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
            "error: equip_failed - Invalid arguments!\n",
        )

    def test_equip_invalid_equipment_and_no_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
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
            "error: equip_failed - Invalid arguments!\n",
        )

    def test_equip_with_no_player_entity_created(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
        command = "equip IronSWORD weapon"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: equip_failed - Player entity does not exist!\n",
        )

    def test_equip_with_valid_weapon_but_incorrect_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip IronSWORD armor"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: equip_failed - Slot provided does not match items slot!\n",
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
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip ironsword weapon"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Valid items: None, IronSword, CursedDagger, MageStaff, IronChestplate, "
            "LeatherTunic, ScoutArmor, RingOfTheSorcerer, AmuletOfVitality, RingOfHaste\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: Equipped IronSword to Weapon!\n",
        )

    # success
    def test_equip_with_valid_weapon_and_no_provided_slot(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "equip ironsword"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "Valid items: None, IronSword, CursedDagger, MageStaff, IronChestplate, "
            "LeatherTunic, ScoutArmor, RingOfTheSorcerer, AmuletOfVitality, RingOfHaste\n"
            "Valid slots: Weapon, Armor, Accessory\n"
            "ok: Equipped IronSword to Weapon!\n",
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
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory display"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            "error: inventory_failed - Too many command arguemnts!\n",
        )

    def test_inventory_with_no_player(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # Create Map
        test_cli.process_command("init map 25 25")
        # clear out entity list
        Entity.reset_entity_list()
        command = "inventory"
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
        Entity.reset_entity_list()
        # create entity to be "player"
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory"
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        test_cli.process_command("spawn warrior 10 10")
        command = "inventory"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            # Display inventory of entity
            "Weapon: None\n" "Armor: None\n" "Accessory: None\n",
        )

    # Success
    def test_inventory_success_with_equips(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # Change all slots
        test_cli.process_command("equip scoutarmor")
        test_cli.process_command("equip amuletofvitality accessory")
        test_cli.process_command("equip ironsword")
        command = "inventory"
        # Process command
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        # Get print output to comapre
        output = mock_stdout.getvalue()
        # check output
        self.assertEqual(
            output,
            # Display inventory of entity
            "Weapon: IronSword\n" "Armor: ScoutArmor\n" "Accessory: AmuletOfVitality\n",
        )

    # Inspect Cases
    def test_inspect_with_invalid_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # Change all slots
        test_cli.process_command("equip ironchestplate")
        test_cli.process_command("equip amuletofvitality accessory")
        test_cli.process_command("equip ironsword")
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn mage 10 10")
        # Change all slots
        test_cli.process_command("equip ironchestplate")
        test_cli.process_command("equip ringofthesorcerer accessory")
        test_cli.process_command("equip magestaff")
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
            "Active_modifiers: 5\n",
        )

    # success with warrior custom inventory + stat changes (both % and flat, also -)
    def test_inspect_success_with_warrior_with_mage_specific_items(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # Change all slots
        test_cli.process_command("equip ironchestplate")
        test_cli.process_command("equip ringofthesorcerer accessory")
        test_cli.process_command("equip magestaff")
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
            "Active_modifiers: 3\n",
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # set tile at 10, 10
        test_cli.set_tile(10, 10, "shallowwater")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # Change all slots
        test_cli.process_command("equip ironchestplate")
        test_cli.process_command("equip ringofvitality accessory")
        test_cli.process_command("equip ironsword")
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
            "Attack: 27\n"
            "Defence: 25\n"
            "Speed: 1\n"
            "Active_modifiers: 3\n",
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
        Entity.reset_entity_list()
        # Create Map
        test_cli.process_command("init map 25 25")
        # spawn warrior
        test_cli.process_command("spawn warrior 10 10")
        # set tile at 10, 10
        test_cli.set_tile(10, 10, "shallowwater")
        # Change all slots
        test_cli.process_command("equip ironchestplate")
        test_cli.process_command("equip ringofvitality accessory")
        test_cli.process_command("equip ironsword")
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
            "Attack: 27\n"
            "Defence: 25\n"
            "Speed: 1\n"
            "Active_modifiers: 3\n",
        )

    # tile cases
    def test_tile_with_invalid_command(self):
        # Create test CLI
        test_cli = CLI()
        # Clear out grid
        test_cli.grid = Grid.reset_grid()
        # clear out entity list
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        Entity.reset_entity_list()
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
        test_cli.set_tile(0, 0, "wall")
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
        test_cli.set_tile(24, 24, "wall")
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
        test_cli.set_tile(10, 10, "shallowwater")
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
        test_cli.set_tile(10, 10, "shallowwater")
        # spawn entity
        test_cli.spawn("warrior", 10, 10)
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


if __name__ == "__main__":
    unittest.main()
