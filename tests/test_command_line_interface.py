"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_command_line_interface.py
Purpose: Utilizes unittest to test all of the fron facing functions to insure there are no catastrohpic errors that make it into the game.
"""

# Imports
import unittest
from unittest.mock import patch
import io
from command_line_interface import CLI
from entity import Entity
from unittest.mock import MagicMock
from io import StringIO


class TestCLI(unittest.TestCase):

    # Repeated Test Functions

    # Create Test CLI
    # Create a CLI instance for testing
    # Returns: test_cli - CLI - CLI instance used for testing
    def create_test_cli(self):
        return CLI()

    # Create Test Map
    # Create a map for tests that require an initialized grid
    # Params: test_cli - CLI - CLI instance used for testing
    #           width - int - map width
    #           height - int - map height
    # Returns: None
    def create_test_map(self, test_cli, width=25, height=25):
        test_cli.process_command(f"init map {width} {height}")

    # Create Test Entity
    # Creates an entity through the public-facing CLI command
    # Params: test_cli - CLI - CLI instance used for testing
    #           entity_type - string - type of entity to spawn
    #           x/y - int - grid coordinates
    # Returns: None
    def create_test_entity(self, test_cli, entity_type="Warrior", x=1, y=1):
        test_cli.process_command(f"spawn {entity_type} {x} {y}")

    # Process Command Output
    # Process a command and capture its printed output
    # Params: test_cli - CLI - CLI instance used for testing
    #           command - string - command to process
    # Returns: output - string - printed output
    def process_command_and_get_output(self, test_cli, command):
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            test_cli.process_command(command)
        return mock_stdout.getvalue()

    # Capture Function Output
    # Call a function and capture its printed output
    # Params: function - callable - function to call
    # Returns: output - string - printed output
    def capture_function_output(self, function):
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            function()
        return mock_stdout.getvalue()

    # Reset Test Game State
    # Creates a fresh game state for tests that need one
    # Params: test_cli - CLI - CLI instance used for testing
    # Returns: None
    def reset_test_game_state(self, test_cli):
        test_cli.game_state = type(test_cli.game_state)()

    # Unknown Commands Start

    def test_unknown_command(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "not a command")
        # Check output
        self.assertEqual(output, "error: Unknown command!\n")

    def test_empty_command(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "   ")
        # Check output
        self.assertEqual(output, "error: Empty command!\n")

    def test_command_is_case_insensitive(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "InIt MaP 10 10")
        # Check output
        self.assertIn("map_initialized", output)
        self.assertTrue(test_cli.game_state.is_map_created())

    # Init Commands Start

    def test_init_map_incorrect_command_pieces(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "init cap 6 6")
        # Check output
        self.assertIn("map_init_failed", output)

    def test_init_map_incorrect_number_of_command_pieces(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "init map 6")
        # Check output
        self.assertIn("map_init_failed", output)

    def test_init_map_with_invalid_width_int(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "init map nope 10")
        self.assertIn("not valid integers", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_invalid_height_int(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "init map 10 nope")
        self.assertIn("not valid integers", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_width_bounds_higher_than_max(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map {50 + 1} 10")
        self.assertIn("exceed bound", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_height_bounds_higher_than_max(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map 10 {50 + 1}")
        self.assertIn("exceed bound", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_width_bounds_lower_than_min(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map {5 - 1} 10")
        self.assertIn("exceed bound", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_height_bounds_lower_than_min(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map 10 {5 - 1}")
        self.assertIn("exceed bound", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_min_bounds(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map {5} {5}")
        self.assertIn("map_initialized", output)
        self.assertTrue(test_cli.game_state.is_map_created())

    def test_init_map_with_max_bounds(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, f"init map {50} {50}")
        self.assertIn("map_initialized", output)
        self.assertTrue(test_cli.game_state.is_map_created())

    def test_init_map_success(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "init map 10 12")
        self.assertIn("width: 10 height: 12", output)
        self.assertTrue(test_cli.game_state.is_map_created())

    def test_init_map_with_map_created(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli, 10, 10)
        self.create_test_entity(test_cli, "Warrior", 2, 2)
        output = self.process_command_and_get_output(test_cli, "init map 6 6")
        self.assertIn("map_initialized", output)
        self.assertTrue(test_cli.game_state.is_map_created())
        self.assertFalse(test_cli.game_state.entities_exists())

    # Set Tile Commands Start

    def test_set_tile_incorrect_number_of_command_pieces(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "set tile 1 1")
        self.assertIn("set_tile_failed", output)

    def test_set_tile_with_wrong_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "set floor 1 1 Wall")
        self.assertIn("set_tile_failed", output)

    def test_set_tile_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "set tile 1 1 Wall")
        self.assertIn("Map does not exist", output)

    def test_set_tile_without_valid_x_int(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "set tile nope 1 Wall")
        self.assertIn("not valid integers", output)

    def test_set_tile_without_valid_y_int(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "set tile 1 nope Wall")
        self.assertIn("not valid integers", output)

    def test_set_tile_with_x_bounds_higher_than_grid_max(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, f"set tile {50} 1 Wall")
        self.assertIn("exceed current grid bounds", output)

    def test_set_tile_with_y_bounds_higher_than_grid_max(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, f"set tile 1 {50} Wall")
        self.assertIn("exceed current grid bounds", output)

    def test_set_tile_with_invalid_tile_type(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "set tile 1 1 Lava")
        self.assertIn("Tile type provided was invalid", output)

    def test_set_tile_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "set tile 2 3 Wall")
        self.assertIn("tile_set 2, 3 type: Wall", output)
        tile_info = test_cli.game_state.get_game_tile_info(2, 3)
        self.assertEqual(tile_info.tile_type.lower(), "wall")
        self.assertFalse(tile_info.passable)

    def test_set_tile_shallowwater_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(
            test_cli, "set tile 2 3 ShallowWater"
        )
        self.assertIn("type: ShallowWater", output)
        self.assertEqual(
            test_cli.game_state.get_game_tile_info(2, 3).tile_type.lower(),
            "shallowwater",
        )

    # Spawn Commands Start

    def test_spawn_entity_invalid_command_length(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "spawn Warrior 1")
        self.assertIn("spawn_failed", output)

    def test_spawn_entity_map_not_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "spawn Warrior 1 1")
        self.assertIn("Map does not exist", output)

    def test_spawn_entity_invalid_x_value(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "spawn Warrior nope 1")
        self.assertIn("not valid integers", output)

    def test_spawn_entity_invalid_y_value(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "spawn Warrior 1 nope")
        self.assertIn("not valid integers", output)

    def test_spawn_entity_invalid_type(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "spawn Dragon 1 1")
        self.assertIn("Invalid arguments", output)

    def test_spawn_entity_on_existing_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        output = self.process_command_and_get_output(test_cli, "spawn Goblin 1 1")
        self.assertIn("already present", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).e_type.capitalize(),
            "Warrior",
        )

    def test_spawn_entity_with_standard_entity_type(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "spawn Warrior 1 1")
        self.assertIn("Spawned warrior", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).e_type.capitalize(),
            "Warrior",
        )
        self.assertEqual(test_cli.game_state.get_entity_id_from_tile(1, 1), 1)

    def test_spawn_entity_with_mage_entity_type(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "spawn Mage 1 1")
        self.assertIn("Spawned mage", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).e_type, "mage"
        )

    def test_spawn_entity_increments_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 2)
        self.assertIsNotNone(test_cli.game_state.get_entity_info_from_list(1))
        self.assertIsNotNone(test_cli.game_state.get_entity_info_from_list(2))
        self.assertEqual(test_cli.game_state.get_entity_id_from_tile(2, 2), 2)

    def test_spawn_entity_position_out_of_bounds(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, f"spawn Warrior {50} 1")
        self.assertIn("exceed current grid bounds", output)

    def test_spawn_loot_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "spawn loot")
        self.assertIn("spawn_failed", output)

    def test_spawn_loot_without_map(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(
            test_cli, "spawn loot ironsword 1 1"
        )
        self.assertIn("Map does not exist", output)

    def test_spawn_loot_invalid_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(
            test_cli, "spawn loot fakeitem 1 1"
        )
        self.assertIn("Item name not found", output)

    def test_spawn_loot_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(
            test_cli, "spawn loot ironsword 1 1"
        )
        self.assertIn("spawn_loot ironsword at 1, 1", output)
        tile_info = test_cli.game_state.get_game_tile_info(1, 1)
        self.assertTrue(
            any(item.lower() == "ironsword" for item in tile_info.item_list)
        )

    # Inventory Commands Start

    def test_inventory_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "inventory")
        self.assertIn("inventory_failed", output)

    def test_inventory_with_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "inventory nope")
        self.assertIn("not valid integer", output)

    def test_inventory_with_no_player(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "inventory 1")
        self.assertIn("does not exist", output)

    def test_inventory_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "inventory 1")
        self.assertIn("Weapon:", output)
        self.assertIn("Armor:", output)
        self.assertIn("Accessory:", output)
        self.assertIn("Backpack Slots:", output)

    # Inspect Commands Start

    def test_inspect_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "inspect")
        self.assertIn("inspect_failed", output)

    def test_inspect_with_no_player(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "inspect 1")
        self.assertIn("No entities exist", output)

    def test_inspect_with_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "inspect nope")
        self.assertIn("not valid integer", output)

    def test_inspect_with_no_entity_matching_id_number(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "inspect 2")
        self.assertIn("Entity does not exist", output)

    def test_inspect_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "inspect 1")
        self.assertIn("Health:", output)
        self.assertIn("Attack:", output)
        self.assertIn("Defence:", output)

    # Tile Commands Start

    def test_tile_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "tile")
        self.assertIn("tile_failed", output)

    def test_tile_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "tile 1 1")
        self.assertIn("Map does not exist", output)

    def test_tile_with_invalid_x_value(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "tile nope 1")
        self.assertIn("not valid integers", output)

    def test_tile_with_invalid_y_value(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "tile 1 nope")
        self.assertIn("not valid integers", output)

    def test_tile_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "tile 1 1")
        self.assertIn("Coordinate: 1, 1", output)
        self.assertIn("Type: Floor", output)
        self.assertIn("Passable: True", output)
        self.assertIn("Occupants: None", output)

    def test_tile_with_entity_occupant(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "tile 1 1")
        self.assertIn("Occupants: 1", output)

    # Pickup Commands Start

    def test_pickup_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "pickup 1")
        self.assertIn("pickup_failed", output)

    def test_pickup_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "pickup 1 ironsword")
        self.assertIn("Map does not exist", output)

    def test_pickup_with_invalid_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "pickup 1 fakeitem")
        self.assertIn("Item name not found", output)

    def test_pickup_item_not_on_tile(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "pickup 1 ironsword")
        self.assertIn("Item not in tiles item list", output)

    def test_pickup_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("spawn loot ironsword 1 1")
        output = self.process_command_and_get_output(test_cli, "pickup 1 ironsword")
        self.assertIn("picked_up", output)
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertTrue(
            any(item.name.lower() == "ironsword" for item in entity_info.backpack)
        )
        tile_info = test_cli.game_state.get_game_tile_info(1, 1)
        self.assertFalse(
            any(item.lower() == "ironsword" for item in tile_info.item_list)
        )

    # Give Commands Start

    def test_give_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "give 1")
        self.assertIn("give_failed", output)

    def test_give_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "give 1 ironsword")
        self.assertIn("Map does not exist", output)

    def test_give_with_invalid_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "give 1 fakeitem")
        self.assertIn("Item name not found", output)

    def test_give_entity_does_not_exist(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "give 1 ironsword")
        self.assertIn("Entity does not exist", output)

    def test_give_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "give 1 ironsword")
        self.assertIn("added ironsword", output)
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertTrue(
            any(item.name.lower() == "ironsword" for item in entity_info.backpack)
        )

    # Drop Commands Start

    def test_drop_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "drop 1")
        self.assertIn("drop_failed", output)

    def test_drop_with_invalid_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "drop 1 fakeitem")
        self.assertIn("Item name not found", output)

    def test_drop_item_not_in_backpack(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "drop 1 ironsword")
        self.assertIn("Item not in backpack", output)

    def test_drop_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironsword")
        output = self.process_command_and_get_output(test_cli, "drop 1 ironsword")
        self.assertIn("dropped", output)
        self.assertFalse(
            any(
                item.lower() == "ironsword"
                for item in test_cli.game_state.get_entity_info_from_list(1).backpack
            )
        )
        self.assertTrue(
            any(
                item.lower() == "ironsword"
                for item in test_cli.game_state.get_game_tile_info(1, 1).item_list
            )
        )

    # Swap Commands Start

    def test_swap_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "swap 1 Weapon")
        self.assertIn("swap_failed", output)

    def test_swap_with_invalid_slot(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironsword")
        output = self.process_command_and_get_output(test_cli, "swap 1 Head ironsword")
        self.assertIn("slot not valid", output)

    def test_swap_item_not_in_backpack(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Weapon ironsword"
        )
        self.assertIn("Item not in backpack", output)

    def test_swap_with_incorrect_item_slot(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironchestplate")
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Weapon ironchestplate"
        )
        self.assertIn("Slot incorrect", output)

    def test_swap_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironsword")
        original_attack = test_cli.game_state.get_entity_info_from_list(1).attack
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Weapon ironsword"
        )
        # print(output)
        self.assertIn("swapped", output.lower())
        self.assertGreater(
            test_cli.game_state.get_entity_info_from_list(1).attack, original_attack
        )

    # Use Commands Start

    def test_use_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "use 1")
        self.assertIn("use_failed", output)

    def test_use_with_invalid_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "use 1 fakeitem")
        self.assertIn("Item name not found", output)

    def test_use_item_not_in_backpack(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(
            test_cli, "use 1 smallhealthpotion"
        )
        self.assertIn("Item not in backpack", output)

    def test_use_non_consumable_item(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironsword")
        output = self.process_command_and_get_output(test_cli, "use 1 ironsword")
        self.assertIn("not a consumable", output)

    def test_use_consumable_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        test_cli.process_command("give 1 smallhealthpotion")
        output = self.process_command_and_get_output(
            test_cli, "use 1 smallhealthpotion"
        )
        self.assertIn("used", output)

    # Move Commands Start

    def test_move_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "move 1 2")
        self.assertIn("move_failed", output)

    def test_move_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "move 1 2 2")
        self.assertIn("Map does not exist", output)

    def test_move_with_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "move nope 2 2")
        self.assertIn("Entity does not exist", output)

    def test_move_with_invalid_coordinates(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        output = self.process_command_and_get_output(test_cli, "move 1 nope 2")
        self.assertIn("not valid integers", output)

    def test_move_to_occupied_tile(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 2)
        output = self.process_command_and_get_output(test_cli, "move 1 2 2")
        self.assertIn("already present", output)

    def test_move_to_impassable_tile(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        test_cli.process_command("set tile 2 1 Wall")
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        self.assertIn("impassable", output)

    def test_move_out_of_range(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        output = self.process_command_and_get_output(test_cli, "move 1 20 20")
        self.assertIn("out of entity's range", output)

    def test_move_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        self.assertIn("moved 1 to 2, 1", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).position, [2, 1]
        )

    # Attack Commands Start

    def test_attack_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "attack 1")
        self.assertIn("attack_failed", output)

    def test_attack_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        self.assertIn("Map does not exist", output)

    def test_attack_with_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        output = self.process_command_and_get_output(test_cli, "attack nope 1")
        self.assertIn("not valid integers", output)

    def test_attack_with_missing_attacker(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        output = self.process_command_and_get_output(test_cli, "attack 5 2")
        self.assertIn("Attacking entity does not exist", output)

    def test_attack_with_missing_defender(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        self.assertIn("Defending entity does not exist", output)

    def test_attack_with_defender_out_of_range(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 10, 10)
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        self.assertIn("Defender is out of range", output)

    def test_attack_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        defender_before = test_cli.game_state.get_entity_info_from_list(2).health
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        self.assertIn("ok: attack", output)
        defender_after = test_cli.game_state.get_entity_info_from_list(2).health
        self.assertLess(defender_after, defender_before)

    # Cast Commands Start

    def test_cast_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "cast 1 2")
        self.assertIn("cast_failed", output)

    def test_cast_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        self.assertIn("Map does not exist", output)

    def test_cast_with_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        output = self.process_command_and_get_output(test_cli, "cast nope 1 Fireball")
        self.assertIn("cast_failed", output)

    def test_cast_with_invalid_spell(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        output = self.process_command_and_get_output(test_cli, "cast 1 2 FakeSpell")
        self.assertIn("Spell does not exist", output)

    def test_cast_with_non_mage_caster(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        self.assertIn("not a valid spellcaster", output)

    def test_cast_with_target_out_of_range(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 20, 20)
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        self.assertIn("outside of range", output)

    def test_cast_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        self.assertIn("ok: cast Fireball", output)

    # Tick Commands Start

    def test_tick_with_invalid_command(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "tick extra")
        self.assertIn("tick_failed", output)

    def test_tick_without_map_created(self):
        test_cli = self.create_test_cli()
        output = self.process_command_and_get_output(test_cli, "tick")
        self.assertIn("Map does not exist", output)

    def test_tick_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        output = self.process_command_and_get_output(test_cli, "tick")
        # Tick should advance the turn after processing entities.
        self.assertEqual(output, "ok: advanced to turn 2!\n")

    # Main Function Start

    @patch("builtins.input", side_effect=["quit"])
    def test_main_quits(self, mock_input):
        # Capture output
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            from main import main

            main()
        # Check output
        self.assertIn("Thank you for playing!", mock_stdout.getvalue())

    # Additional Validation Tests Start

    def test_init_map_with_negative_dimensions(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "init map -5 10")
        # Check output and state
        self.assertIn("map_init_failed", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_decimal_dimensions(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "init map 5.5 10")
        # Check output and state
        self.assertIn("map_init_failed", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_with_extra_arguments(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "init map 10 10 extra")
        # Check output
        self.assertIn("map_init_failed", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_init_map_resets_entity_ids_after_map_reset(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Create map and entity
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Reset map
        test_cli.process_command("init map 10 10")
        self.create_test_entity(test_cli, "Goblin", 2, 2)
        # Check ID reset
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertIsNotNone(entity_info)
        self.assertEqual(entity_info.e_type.lower(), "goblin")

    def test_set_tile_with_negative_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "set tile -1 0 Wall")
        # Check output
        self.assertIn("set_tile_failed", output)

    def test_set_tile_with_decimal_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "set tile 1.5 0 Wall")
        # Check output
        self.assertIn("set_tile_failed", output)

    def test_set_tile_preserves_entity_occupant(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 2, 2)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "set tile 2 2 ShallowWater"
        )
        # Check output and occupant
        self.assertIn("tile_set", output)
        tile_info = test_cli.game_state.get_game_tile_info(2, 2)
        self.assertIn(1, tile_info.occupants)

    def test_spawn_entity_with_decimal_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "spawn Warrior 1.5 1")
        # Check output
        self.assertIn("spawn_failed", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))

    def test_spawn_entity_with_negative_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "spawn Warrior -1 1")
        # Check output
        self.assertIn("spawn_failed", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))

    def test_spawn_entity_with_extra_arguments(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "spawn Warrior 1 1 extra"
        )
        # Check output
        self.assertIn("spawn_failed", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))

    def test_spawn_entity_does_not_increment_id_after_failure(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Attempt invalid spawn then valid spawn
        test_cli.process_command("spawn Dragon 1 1")
        test_cli.process_command("spawn Warrior 1 1")
        # Check ID
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertIsNotNone(entity_info)
        self.assertEqual(entity_info.id, 1)

    def test_spawn_loot_with_negative_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "spawn loot ironsword -1 1"
        )
        # Check output
        self.assertIn("spawn_failed", output)
        tile_info = test_cli.game_state.get_game_tile_info(0, 1)
        self.assertEqual(tile_info.item_list, ())

    def test_spawn_loot_with_decimal_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "spawn loot ironsword 1.5 1"
        )
        # Check output
        self.assertIn("not valid integers", output)

    def test_spawn_multiple_loot_on_same_tile(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Spawn multiple items
        test_cli.process_command("spawn loot ironsword 2 2")
        test_cli.process_command("spawn loot smallhealthpotion 2 2")
        # Check tile items
        tile_info = test_cli.game_state.get_game_tile_info(2, 2)
        item_names = [item.lower() for item in tile_info.item_list]
        self.assertIn("ironsword", item_names)
        self.assertIn("smallhealthpotion", item_names)

    def test_inventory_with_non_integer_entity_id(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "inventory nope")
        # Check output
        self.assertIn("not valid integer", output)

    def test_inventory_with_negative_entity_id(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "inventory -1")
        # Check output
        self.assertIn("does not exist", output)

    def test_inspect_with_non_integer_entity_id(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "inspect nope")
        # Check output
        self.assertIn("not valid integer", output)

    def test_inspect_with_negative_entity_id(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "inspect -1")
        # Check output
        self.assertIn("No entities exist", output)

    def test_tile_with_negative_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "tile -1 0")
        # Check output
        self.assertIn("exceed current grid bounds", output)

    def test_tile_with_decimal_coordinates(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "tile 1.5 0")
        # Check output
        self.assertIn("not valid integers", output)

    def test_pickup_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "pickup nope ironsword")
        # Check output
        self.assertIn("pickup_failed", output)

    def test_pickup_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "pickup 99 ironsword")
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_give_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "give nope ironsword")
        # Check output
        self.assertIn("give_failed", output)

    def test_give_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "give 99 ironsword")
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_drop_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "drop nope ironsword")
        # Check output
        self.assertIn("drop_failed", output)

    def test_drop_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "drop 99 ironsword")
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_swap_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "swap nope Weapon ironsword"
        )
        # Check output
        self.assertIn("swap_failed", output)

    def test_swap_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "swap 99 Weapon ironsword"
        )
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_use_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "use nope smallhealthpotion"
        )
        # Check output
        self.assertIn("use_failed", output)

    def test_use_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "use 99 smallhealthpotion"
        )
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_move_with_non_integer_entity_id_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "move nope 2 2")
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_move_with_nonexistent_entity_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "move 99 2 2")
        # Check output
        self.assertIn("Entity does not exist", output)

    def test_move_does_not_change_position_when_rejected(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Process command
        self.process_command_and_get_output(test_cli, "move 1 20 20")
        # Check position did not change
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.position, [1, 1])

    def test_move_updates_old_and_new_tile_occupants(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        # Check output and tile occupants
        self.assertIn("ok: moved", output)
        old_tile = test_cli.game_state.get_game_tile_info(1, 1)
        new_tile = test_cli.game_state.get_game_tile_info(2, 1)
        self.assertNotIn(1, old_tile.occupants)
        self.assertIn(1, new_tile.occupants)

    def test_move_rejected_by_occupied_tile_does_not_change_position(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        # Check output and position
        self.assertIn("already present", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).position, [1, 1]
        )

    def test_attack_with_non_integer_ids_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack nope 2")
        # Check output
        self.assertIn("attack_failed", output)

    def test_attack_does_not_damage_target_when_out_of_range(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 10, 10)
        # Get original health
        original_health = test_cli.game_state.get_entity_info_from_list(2).health
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        # Check output and health
        self.assertIn("out of range", output)
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(2).health, original_health
        )

    def test_attack_with_nonexistent_attacker_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 99 1")
        # Check output
        self.assertIn("attack_failed", output)

    def test_attack_with_nonexistent_defender_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 99")
        # Check output
        self.assertIn("attack_failed", output)

    def test_cast_with_non_integer_ids_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast nope 2 Fireball")
        # Check output
        self.assertIn("cast_failed", output)

    def test_cast_with_nonexistent_caster_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast 99 1 Fireball")
        # Check output
        self.assertIn("cast_failed", output)

    def test_cast_with_nonexistent_target_does_not_crash(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast 1 99 Fireball")
        # Check output
        self.assertIn("cast_failed", output)

    def test_tick_with_extra_arguments_does_not_advance_game(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Process invalid command
        output = self.process_command_and_get_output(test_cli, "tick extra")
        # Check output
        self.assertIn("tick_failed", output)

    def test_tick_with_entities_does_not_remove_living_entities(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Process command
        self.process_command_and_get_output(test_cli, "tick")
        # Check entity remains
        self.assertIsNotNone(test_cli.game_state.get_entity_info_from_list(1))

    def test_spawn_give_swap_and_inventory_command_interaction(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Give and equip weapon
        test_cli.process_command("give 1 ironsword")
        swap_output = self.process_command_and_get_output(
            test_cli, "swap 1 Weapon ironsword"
        )
        # Check output and observable attack stat change
        self.assertIn("swapped", swap_output)
        self.assertGreater(test_cli.game_state.get_entity_info_from_list(1).attack, 15)

    def test_spawn_loot_pickup_and_drop_command_interaction(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Spawn, pick up, then drop loot
        test_cli.process_command("spawn loot ironsword 1 1")
        pickup_output = self.process_command_and_get_output(
            test_cli, "pickup 1 ironsword"
        )
        drop_output = self.process_command_and_get_output(test_cli, "drop 1 ironsword")
        # Check item transitions
        self.assertIn("picked_up", pickup_output)
        self.assertIn("dropped", drop_output)
        tile_info = test_cli.game_state.get_game_tile_info(1, 1)
        self.assertIn("ironsword", [item.lower() for item in tile_info.item_list])
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertFalse(
            any(item.lower() == "ironsword" for item in entity_info.backpack)
        )

    def test_case_insensitive_equipment_commands(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Process commands using mixed casing
        test_cli.process_command("GIVE 1 IronSword")
        swap_output = self.process_command_and_get_output(
            test_cli, "SWAP 1 weapon IRONSWORD"
        )
        # Check output
        self.assertIn("swapped", swap_output)
        self.assertGreater(test_cli.game_state.get_entity_info_from_list(1).attack, 15)

    def test_command_with_whitespace_only_does_not_change_state(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, " \t  \n ")
        # Check output and state
        self.assertIn("Empty command", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    def test_unknown_command_does_not_change_state(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Process command
        output = self.process_command_and_get_output(test_cli, "teleport 1 2 3")
        # Check output and state
        self.assertIn("Unknown command", output)
        self.assertFalse(test_cli.game_state.is_map_created())

    # Additional Validation Tests End

    # Dead Entity Validation Tests Start

    # Create Dead Entity
    # Creates an entity and marks it as dead for commands that reject dead entities
    # Params: test_cli - CLI - CLI instance used for testing
    #           entity_type - string - type of entity to spawn
    #           x/y - int - grid coordinates
    # Returns: None
    def create_dead_entity(
        self, test_cli, entity_type="Warrior", x=1, y=1, entity_id=1
    ):
        self.create_test_entity(test_cli, entity_type, x, y)
        test_cli.game_state.get_entity_from_list(entity_id).handle_death()

    def test_dead_entity_blocked_inventory(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(test_cli, "inventory 1")
        # Check output
        self.assertIn("dead", output.lower())

    def test_dead_entity_blocked_inspect(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(test_cli, "inspect 1")
        # Check output
        self.assertIn("dead", output.lower())

    def test_dead_entity_blocked_pickup(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.game_state.get_entity_from_list(1).handle_death()
        test_cli.process_command("spawn loot ironsword 1 1")
        # Process command
        output = self.process_command_and_get_output(test_cli, "pickup 1 ironsword")
        # Check output
        self.assertIn("dead", output.lower())

    def test_dead_entity_blocked_drop(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironsword")
        test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(test_cli, "drop 1 ironsword")
        # Check output and unchanged backpack
        self.assertIn("dead", output.lower())
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertTrue(
            any(item.name.lower() == "ironsword" for item in entity_info.backpack)
        )

    def test_dead_entity_blocked_swap(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.reset_test_game_state(test_cli)
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironchestplate")
        test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Armor ironchestplate"
        )
        # Check output and unchanged inventory
        self.assertIn("dead", output.lower())
        self.assertEqual(test_cli.game_state.get_entity_info_from_list(1).defence, 10)
        # self.assertEqual(test_cli.game_state.get_entity_info_from_list(1).attack, 15)

    def test_dead_entity_blocked_use(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 smallhealthpotion")
        test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "use 1 smallhealthpotion"
        )
        # Check output and unchanged backpack
        self.assertIn("dead", output.lower())
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertTrue(
            any(
                item.name.lower() == "smallhealthpotion"
                for item in entity_info.backpack
            )
        )

    def test_dead_entity_blocked_move(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_dead_entity(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        # Check output and unchanged position
        self.assertIn("dead", output.lower())
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(1).position, [1, 1]
        )

    def test_dead_attacker_cannot_attack(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_dead_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Get defender health
        original_health = test_cli.game_state.get_entity_info_from_list(2).health
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        # Check output and unchanged health
        self.assertIn("dead", output.lower())
        self.assertEqual(
            test_cli.game_state.get_entity_info_from_list(2).health, original_health
        )

    def test_dead_defender_cannot_be_attacked(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_dead_entity(test_cli, "Goblin", 2, 1, entity_id=2)
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        # Check output
        self.assertIn("dead", output.lower())

    def test_dead_caster_cannot_cast(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)

        # Debug death status
        # Kill caster
        caster = test_cli.game_state.get_entity_from_list(1)
        caster.handle_death()

        # Debug death status
        print("Internal buffs:", caster._Entity__temp_buffs)
        print("Info buffs:", caster.get_info().temp_buffs)
        print(
            "Alive:",
            Entity.is_alive_from_info(test_cli.game_state.get_entity_info_from_list(1)),
        )

        # test_cli.game_state.get_entity_from_list(1).handle_death()
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        # Check output
        self.assertIn("dead", output.lower())

    def test_dead_target_cannot_be_cast_on(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_dead_entity(test_cli, "Goblin", 2, 1, entity_id=2)
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Fireball")
        # Check output
        self.assertIn("dead", output.lower())

    def test_backpack_full_rejects_additional_item(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        # Fill backpack to capacity
        items = [
            "ironsword",
            "curseddagger",
            "magestaff",
            "ironchestplate",
            "leathertunic",
            "scoutarmor",
            "ringofthesorcerer",
            "amuletofvitality",
        ]
        for item_name in items[: Entity.BACKPACK_SIZE]:
            test_cli.process_command(f"give 1 {item_name}")
        # Attempt to add another item
        output = self.process_command_and_get_output(test_cli, "give 1 ringofhaste")
        # Check output and backpack capacity
        self.assertIn("full", output.lower())
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertLessEqual(len(entity_info.backpack), Entity.BACKPACK_SIZE)

    def test_failed_pickup_preserves_tile_item(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("spawn loot ironsword 1 1")
        # Attempt pickup of an item not present on the tile
        output = self.process_command_and_get_output(
            test_cli, "pickup 1 ironchestplate"
        )
        # Check output and original loot
        self.assertIn("not in tiles item list", output.lower())
        tile_info = test_cli.game_state.get_game_tile_info(1, 1)
        self.assertIn("ironsword", [item.lower() for item in tile_info.item_list])

    def test_failed_swap_preserves_backpack_and_equipment(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironchestplate")
        # Attempt to equip armor in weapon slot
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Weapon ironchestplate"
        )
        # Check output and unchanged state
        self.assertIn("Slot incorrect", output)
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertTrue(
            any(item.name.lower() == "ironchestplate" for item in entity_info.backpack)
        )
        self.assertEqual(entity_info.defence, 10)

    # Dead Entity Validation Tests End

    # Expanded Inventory and Combat Coverage Start

    def test_give_item_case_insensitive(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        # Process command
        output = self.process_command_and_get_output(test_cli, "give 1 IronSword")
        # Check output and backpack
        self.assertIn("ironsword", output.lower())
        self.assertTrue(
            any(
                item.name.lower() == "ironsword"
                for item in test_cli.game_state.get_entity_info_from_list(1).backpack
            )
        )

    def test_pickup_item_case_insensitive(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("spawn loot ironsword 1 1")
        # Process command
        output = self.process_command_and_get_output(test_cli, "pickup 1 IRONSWORD")
        # Check output and backpack
        self.assertIn("picked_up", output)
        self.assertTrue(
            any(
                item.name.lower() == "ironsword"
                for item in test_cli.game_state.get_entity_info_from_list(1).backpack
            )
        )

    def test_swap_armor_success(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ironchestplate")
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Armor ironchestplate"
        )
        # Check output and inventory
        self.assertIn("swapped", output)
        self.assertGreater(test_cli.game_state.get_entity_info_from_list(1).defence, 10)

    def test_swap_accessory_success(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 ringofhaste")
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "swap 1 Accessory ringofhaste"
        )
        # Check output and inventory
        self.assertIn("swapped", output)
        self.assertGreater(test_cli.game_state.get_entity_info_from_list(1).speed, 5)

    def test_use_all_health_and_mana_potions(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Add each consumable to backpack
        potion_names = [
            "smallhealthpotion",
            "greaterhealthpotion",
            "superiorhealthpotion",
            "manapotion",
            "turtlemasterpotion",
        ]
        for item_name in potion_names:
            test_cli.process_command(f"give 1 {item_name}")
        # Use each potion and check it is consumed
        for item_name in potion_names:
            with self.subTest(item_name=item_name):
                output = self.process_command_and_get_output(
                    test_cli, f"use 1 {item_name}"
                )
                self.assertIn("used", output.lower())
                entity_info = test_cli.game_state.get_entity_info_from_list(1)
                self.assertFalse(
                    any(item.name.lower() == item_name for item in entity_info.backpack)
                )

    def test_use_item_keeps_unrelated_backpack_items(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)
        test_cli.process_command("give 1 smallhealthpotion")
        test_cli.process_command("give 1 ironsword")
        # Process command
        output = self.process_command_and_get_output(
            test_cli, "use 1 smallhealthpotion"
        )
        # Check output and remaining item
        self.assertIn("used", output.lower())
        entity_info = test_cli.game_state.get_entity_info_from_list(1)
        self.assertFalse(
            any(
                item.name.lower() == "smallhealthpotion"
                for item in entity_info.backpack
            )
        )
        self.assertTrue(
            any(item.name.lower() == "ironsword" for item in entity_info.backpack)
        )

    def test_use_item_from_another_entity_backpack_is_rejected(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Mage", 2, 1)
        test_cli.process_command("give 1 smallhealthpotion")
        # Try to use item from entity 2's backpack
        output = self.process_command_and_get_output(
            test_cli, "use 2 smallhealthpotion"
        )
        # Check output and item ownership
        self.assertIn("not in backpack", output.lower())
        self.assertTrue(
            any(
                item.name.lower() == "smallhealthpotion"
                for item in test_cli.game_state.get_entity_info_from_list(1).backpack
            )
        )

    def test_attack_melee_damage_reduces_health(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Get target health
        original_health = test_cli.game_state.get_entity_info_from_list(2).health
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        # Check output and health
        self.assertIn("ok: attack", output)
        self.assertLess(
            test_cli.game_state.get_entity_info_from_list(2).health, original_health
        )

    def test_attack_ranged_entity_can_attack_within_ranged_distance(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 3, 1)
        # Process command
        output = self.process_command_and_get_output(test_cli, "attack 1 2")
        # Check output
        self.assertIn("error: attack", output)

    def test_cast_heal_spell_success(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Warrior", 2, 1)
        # Lower target health before healing
        target = test_cli.game_state.get_entity_from_list(2)
        target.update_single_stat("Health", 20)
        test_cli.game_state.update_entity(2)
        # Process command
        output = self.process_command_and_get_output(test_cli, "cast 1 2 Heal")
        # Check output and target health
        self.assertIn("ok: cast Heal", output)
        self.assertGreater(test_cli.game_state.get_entity_info_from_list(2).health, 20)

    def test_cast_heal_does_not_exceed_max_health(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)
        self.create_test_entity(test_cli, "Warrior", 2, 1)
        # Set target health just below maximum
        target = test_cli.game_state.get_entity_from_list(2)
        target_info = target.get_info()
        target.update_single_stat("Health", target_info.max_health - 1)
        test_cli.game_state.update_entity(2)
        # Process command
        self.process_command_and_get_output(test_cli, "cast 1 2 Heal")
        # Check target health cap
        updated_info = test_cli.game_state.get_entity_info_from_list(2)
        self.assertLessEqual(updated_info.health, updated_info.max_health)

    def test_attack_then_heal_with_health_potion(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 1)
        # Add potion and take damage
        test_cli.process_command("give 1 smallhealthpotion")
        test_cli.process_command("attack 2 1")
        health_after_attack = test_cli.game_state.get_entity_info_from_list(1).health
        # Use potion
        output = self.process_command_and_get_output(
            test_cli, "use 1 smallhealthpotion"
        )
        # Check health and output
        self.assertIn("used", output.lower())
        self.assertGreaterEqual(
            test_cli.game_state.get_entity_info_from_list(1).health, health_after_attack
        )

    def test_spawn_all_supported_entity_types(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Spawn supported types at separate positions
        entity_types = ["Warrior", "Mage", "Skeleton", "Goblin"]
        for index, entity_type in enumerate(entity_types):
            with self.subTest(entity_type=entity_type):
                x = index + 1
                test_cli.process_command(f"spawn {entity_type} {x} 1")
                entity_info = test_cli.game_state.get_entity_info_from_list(index + 1)
                self.assertIsNotNone(entity_info)
                self.assertEqual(entity_info.e_type.lower(), entity_type.lower())

    def test_spawn_loot_does_not_affect_other_tiles(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Spawn loot on one tile
        test_cli.process_command("spawn loot ironsword 2 2")
        # Check target and unrelated tiles
        target_tile = test_cli.game_state.get_game_tile_info(2, 2)
        other_tile = test_cli.game_state.get_game_tile_info(3, 3)
        self.assertIn("ironsword", [item.lower() for item in target_tile.item_list])
        self.assertEqual(other_tile.item_list, ())

    def test_move_into_shallow_water_updates_entity_stats(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        test_cli.process_command("set tile 2 1 ShallowWater")
        # Get original speed and move onto shallow water
        original_speed = test_cli.game_state.get_entity_info_from_list(1).speed
        output = self.process_command_and_get_output(test_cli, "move 1 2 1")
        # Check output and speed modifier
        self.assertIn("ok: moved", output)
        self.assertLessEqual(
            test_cli.game_state.get_entity_info_from_list(1).speed, original_speed
        )

    def test_map_reset_clears_old_entities_and_occupants(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        # Reset map through the public command
        output = self.process_command_and_get_output(test_cli, "init map 10 10")
        # Check reset state
        self.assertIn("map_initialized", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))
        self.assertEqual(test_cli.game_state.get_game_tile_info(1, 1).occupants, ())

    # Expanded Inventory and Combat Coverage End

    def test_tick_removes_dead_entity_from_game(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_dead_entity(test_cli, "Warrior", 1, 1)
        # Process tick
        self.process_command_and_get_output(test_cli, "tick")
        self.process_command_and_get_output(test_cli, "tick")
        output = self.process_command_and_get_output(test_cli, "tick")
        # Check dead entity was removed from the entity list and tile
        self.assertIn("advanced to turn", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))
        self.assertEqual(test_cli.game_state.get_game_tile_info(1, 1).occupants, ())

    def test_tick_removes_multiple_dead_entities(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_dead_entity(test_cli, "Warrior", 1, 1)
        self.create_dead_entity(test_cli, "Goblin", 2, 1, entity_id=2)
        self.process_command_and_get_output(test_cli, "tick")
        self.process_command_and_get_output(test_cli, "tick")
        # Process tick
        output = self.process_command_and_get_output(test_cli, "tick")
        # Check all dead entities were removed
        self.assertIn("advanced to turn", output)
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(1))
        self.assertIsNone(test_cli.game_state.get_entity_info_from_list(2))
        self.assertEqual(test_cli.game_state.get_game_tile_info(1, 1).occupants, ())
        self.assertEqual(test_cli.game_state.get_game_tile_info(2, 1).occupants, ())

    # Initialization and Full Spawn Coverage Start

    def test_cli_initializes_with_fresh_game_state(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        # Check initial state
        self.assertFalse(test_cli.game_state.is_map_created())
        self.assertFalse(test_cli.game_state.entities_exists())

    def test_spawn_multiple_entities_have_expected_base_stats(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Expected base stats: health, attack, defence, speed
        expected_stats = {
            "Warrior": (120, 15, 10, 5),
            "Mage": (70, 8, 4, 5),
            "Skeleton": (60, 10, 8, 4),
            "Goblin": (45, 12, 3, 6),
        }
        # Spawn each entity type and check base stats
        for index, (entity_type, stats) in enumerate(expected_stats.items()):
            with self.subTest(entity_type=entity_type):
                test_cli.process_command(f"spawn {entity_type} {index + 1} 1")
                entity_info = test_cli.game_state.get_entity_info_from_list(index + 1)
                self.assertIsNotNone(entity_info)
                self.assertEqual(
                    (
                        entity_info.health,
                        entity_info.attack,
                        entity_info.defence,
                        entity_info.speed,
                    ),
                    stats,
                )

    def test_spawn_loot_on_multiple_tiles_keeps_items_separate(self):
        # Create test CLI
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        # Spawn loot on separate tiles
        test_cli.process_command("spawn loot ironsword 1 1")
        test_cli.process_command("spawn loot smallhealthpotion 2 2")
        # Check each tile contains only its own item
        first_tile = test_cli.game_state.get_game_tile_info(1, 1)
        second_tile = test_cli.game_state.get_game_tile_info(2, 2)
        self.assertEqual([item.lower() for item in first_tile.item_list], ["ironsword"])
        self.assertEqual(
            [item.lower() for item in second_tile.item_list], ["smallhealthpotion"]
        )

    # Initialization and Full Spawn Coverage End

    # Test saving a game with a valid filename
    def test_save_command_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        with patch("command_line_interface.GameStateManager.save_game") as mock_save:
            output = self.process_command_and_get_output(
                test_cli, "save test_save.json"
            )

        mock_save.assert_called_once_with(
            test_cli.game_state, "test_save.json", test_cli.command_manager
        )
        self.assertIn("ok: game saved to test_save.json", output)

    # Test saving when the game state is not initialized
    def test_save_command_inactive_game_state(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "save test_save.json")

        self.assertIn("error: save_failed", output)
        self.assertIn("Game State is not initialized", output)

    # Test saving with an invalid number of arguments
    def test_save_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "save")

        self.assertIn("error: save_failed - Invalid command!", output)

    # Test handling an error while saving
    def test_save_command_save_error(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        with patch(
            "command_line_interface.GameStateManager.save_game",
            side_effect=OSError("Unable to write file"),
        ):
            output = self.process_command_and_get_output(
                test_cli, "save test_save.json"
            )

        self.assertIn("error: save_failed", output)
        self.assertIn("Unable to write file", output)

    # Test loading a game with a valid filename
    def test_load_command_success(self):
        test_cli = self.create_test_cli()

        with patch("command_line_interface.GameStateManager.load_game") as mock_load:
            output = self.process_command_and_get_output(
                test_cli, "load test_save.json"
            )

        mock_load.assert_called_once_with(
            test_cli.game_state, "test_save.json", test_cli.command_manager
        )
        self.assertIn("ok: game loaded from test_save.json", output)

    # Test loading with an invalid number of arguments
    def test_load_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "load")

        self.assertIn("error: load_failed - Invalid command!", output)

    # Test handling an error while loading
    def test_load_command_load_error(self):
        test_cli = self.create_test_cli()

        with patch(
            "command_line_interface.GameStateManager.load_game",
            side_effect=ValueError("Invalid save data"),
        ):
            output = self.process_command_and_get_output(
                test_cli, "load test_save.json"
            )

        self.assertIn("error: load_failed", output)
        self.assertIn("Invalid save data", output)

    # Test displaying information about an active game state
    def test_state_info_command_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli)

        output = self.process_command_and_get_output(test_cli, "state-info")

        self.assertIn("ok: turn ", output)
        self.assertIn("entities: 1", output)
        self.assertIn("saved:", output)

    # Test displaying state information when the game is inactive
    def test_state_info_command_inactive_game_state(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "state-info")

        self.assertIn("error: state_info_failed", output)
        self.assertIn("Game State is not initialized", output)

    # Test handling an error while retrieving state information
    def test_state_info_command_error(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        with patch.object(
            test_cli.game_state,
            "get_game_state_info",
            side_effect=ValueError("Unable to retrieve state"),
        ):
            output = self.process_command_and_get_output(test_cli, "state-info")

        self.assertIn("error: state_info_failed", output)
        self.assertIn("Unable to retrieve state", output)

    # Test Undo Command With No Commands
    # Verify that undo fails when no commands have been executed
    # Returns: None
    def test_undo_command_no_commands(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "undo")

        self.assertIn("error: undo_failed - No commands to undo!", output)

    # Test Undo Command Invalid Arguments
    # Verify that undo rejects commands with extra arguments
    # Returns: None
    def test_undo_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "undo extra")

        self.assertIn("error: undo_failed - Invalid command!", output)

    # Test Undo Command Successfully Undoes Move
    # Verify that undo reverses the last successfully executed move
    # Returns: None
    def test_undo_command_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)

        # Execute a move command to create an undoable command
        move_output = self.process_command_and_get_output(test_cli, "move 1 2 1")

        # Ensure the move command succeeded before testing undo
        self.assertNotIn("error:", move_output.lower())

        # Undo the move
        output = self.process_command_and_get_output(test_cli, "undo")

        self.assertIn("ok: undone Move!", output)

    # Test Undo Command Only Accepts One Argument
    def test_undo_command_multiple_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "undo extra arguments")

        self.assertIn("error: undo_failed - Invalid command!", output)

        # Test Process Redo Command

    # Tests that the redo command redoes the last undone command
    def test_process_redo_command(self):
        test_cli = self.create_test_cli()

        # Add a command to the redo history
        command = MagicMock()
        command.get_name.return_value = "Move"
        test_cli.command_manager.redo_last_command = MagicMock(
            return_value=(True, command)
        )

        # Process redo command
        output = self.process_command_and_get_output(test_cli, "redo")

        # Verify the command was redone
        test_cli.command_manager.redo_last_command.assert_called_once()
        self.assertEqual(output.strip(), "ok: redone Move!")

    # Test Process Redo Command With Invalid Arguments
    # Tests that redo rejects commands with additional arguments
    def test_process_redo_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        # Process redo command with extra arguments
        output = self.process_command_and_get_output(test_cli, "redo extra")

        # Verify the error message
        self.assertEqual(output.strip(), "error: redo_failed - Invalid command!")

    # Test Process Redo Command With Empty History
    # Tests that redo reports an error when there are no commands to redo
    def test_process_redo_command_empty_history(self):
        test_cli = self.create_test_cli()

        # Simulate an empty redo history
        test_cli.command_manager.redo_last_command = MagicMock(
            return_value=(False, None)
        )

        # Process redo command
        output = self.process_command_and_get_output(test_cli, "redo")

        # Verify the error message
        test_cli.command_manager.redo_last_command.assert_called_once()
        self.assertEqual(output.strip(), "error: redo_failed - No commands to redo!")

    # Test History Command Success
    # Verify that the CLI executes the HistoryCommand
    # Returns: None
    def test_process_history_command(self):
        test_cli = CLI.__new__(CLI)
        test_cli.command_manager = MagicMock()

        with patch("command_line_interface.HistoryCommand") as mock_history_command:
            test_command = mock_history_command.return_value

            test_cli.process_history_command(["history"])

            mock_history_command.assert_called_once_with(test_cli.command_manager)
            test_cli.command_manager.execute_command.assert_called_once_with(
                test_command
            )

    # Test History Command Invalid Arguments
    # Verify that the CLI rejects additional arguments
    # Returns: None
    def test_process_history_command_invalid_arguments(self):
        test_cli = CLI.__new__(CLI)
        test_cli.command_manager = MagicMock()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_cli.process_history_command(["history", "extra"])

        output = mock_stdout.getvalue()

        self.assertEqual(output, "error: history_failed - Invalid command!\n")
        test_cli.command_manager.execute_command.assert_not_called()

    # Test History Command Error
    # Verify that the CLI handles errors raised while executing HistoryCommand
    # Returns: None
    def test_process_history_command_error(self):
        test_cli = CLI.__new__(CLI)
        test_cli.command_manager = MagicMock()
        test_cli.command_manager.execute_command.side_effect = ValueError("Test error")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_cli.process_history_command(["history"])

        output = mock_stdout.getvalue()

        self.assertEqual(output, "error: history_failed - Test error\n")

    # Test History Command Attribute Error
    # Verify that the CLI handles an AttributeError
    # Returns: None
    def test_process_history_command_attribute_error(self):
        test_cli = CLI.__new__(CLI)
        test_cli.command_manager = MagicMock()
        test_cli.command_manager.execute_command.side_effect = AttributeError(
            "Missing method"
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_cli.process_history_command(["history"])

        output = mock_stdout.getvalue()

        self.assertEqual(output, "error: history_failed - Missing method\n")

    # State Command Tests Start

    # Test State Command Invalid Arguments
    def test_state_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "state")

        self.assertIn("entity_state_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test State Command Extra Arguments
    def test_state_command_extra_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "state 1 extra")

        self.assertIn("entity_state_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test State Command Without Map
    def test_state_command_without_map(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("entity_state_failed", output)
        self.assertIn("Map does not exist", output)

    # Test State Command Invalid Entity ID
    def test_state_command_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "state 99")

        self.assertIn("Invalid entity ID", output)

    # Test State Command With Negative Entity ID
    def test_state_command_negative_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "state -1")

        self.assertIn("Invalid entity ID", output)

    # Test State Command With Player Entity
    # Player entities should not have behavioral states
    def test_state_command_player_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("entity_state_failed", output)
        self.assertIn("does not have a behavioral state", output)

    # Test State Command With Mage
    def test_state_command_mage_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("does not have a behavioral state", output)

    # Test State Command With Goblin
    def test_state_command_goblin_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("ok: entity 1 state: Defending!", output)

    # Test State Command With Skeleton
    def test_state_command_skeleton_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Skeleton", 1, 1)

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("ok: entity 1 state: Defending!", output)

    # Test State Command With Multiple Entities
    def test_state_command_multiple_entities(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)
        self.create_test_entity(test_cli, "Goblin", 2, 2)

        output = self.process_command_and_get_output(test_cli, "state 2")

        self.assertIn("ok: entity 2 state: Defending!", output)

    # Force State Command Tests Start

    # Test Force State Command Invalid Arguments
    def test_force_state_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "force  1")

        self.assertIn("force_state_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test Force State Command Extra Arguments
    def test_force_state_command_extra_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(
            test_cli, "force  1 Attacking extra"
        )

        self.assertIn("force_state_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test Force State Command Without Map
    def test_force_state_command_without_map(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "force  1 Attacking")

        self.assertIn("force_state_failed", output)
        self.assertIn("Map does not exist", output)

    # Test Force State Command Invalid Entity ID
    def test_force_state_command_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "force 99 Attacking")

        self.assertIn("force_state_failed", output)
        self.assertIn("Invalid entity ID", output)

    # Test Force State Command Negative Entity ID
    def test_force_state_command_negative_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "force  -1 Attacking")

        self.assertIn("Invalid entity ID", output)

    # Test Force State Command Invalid Behavioral State
    def test_force_state_command_invalid_state(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 Sleeping")

        self.assertIn("force_state_failed", output)
        self.assertIn("Invalid behavioral state", output)

    # Test Force State Command With Warrior
    def test_force_state_command_warrior_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 Attacking")

        self.assertIn("force_state_failed", output)
        self.assertIn("does not have a behavioral state", output)

    # Test Force State Command Attacking
    def test_force_state_command_attacking_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 Attacking")

        self.assertIn("ok: entity 1 transitioned to Attacking!", output)

        entity = test_cli.game_state.get_entity_from_list(1)
        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Test Force State Command Fleeing
    def test_force_state_command_fleeing_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 Fleeing")

        self.assertIn("ok: entity 1 transitioned to Fleeing!", output)

        entity = test_cli.game_state.get_entity_from_list(1)
        self.assertEqual(entity.get_entity_state_name(), "Fleeing")

    # Test Force State Command Defending
    def test_force_state_command_defending_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        self.process_command_and_get_output(test_cli, "force  1 Attacking")

        output = self.process_command_and_get_output(test_cli, "force  1 Defending")

        self.assertIn("ok: entity 1 transitioned to Defending!", output)

        entity = test_cli.game_state.get_entity_from_list(1)
        self.assertEqual(entity.get_entity_state_name(), "Defending")

    # Test Force State Command Case Insensitivity
    def test_force_state_command_lowercase_state(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 attacking")

        self.assertIn("transitioned to Attacking", output)

        entity = test_cli.game_state.get_entity_from_list(1)
        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Test Force State Command Skeleton
    def test_force_state_command_skeleton_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Skeleton", 1, 1)

        output = self.process_command_and_get_output(test_cli, "force  1 Fleeing")

        self.assertIn("transitioned to Fleeing", output)

        entity = test_cli.game_state.get_entity_from_list(1)
        self.assertEqual(entity.get_entity_state_name(), "Fleeing")

    # Test Force State Command Changes Only Target
    def test_force_state_command_only_changes_target(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)
        self.create_test_entity(test_cli, "Skeleton", 3, 3)

        self.process_command_and_get_output(test_cli, "force  1 Attacking")

        goblin = test_cli.game_state.get_entity_from_list(1)
        skeleton = test_cli.game_state.get_entity_from_list(2)

        self.assertEqual(goblin.get_entity_state_name(), "Attacking")
        self.assertEqual(skeleton.get_entity_state_name(), "Defending")

    # Test Force State Command And State Query
    def test_force_state_command_state_query_interaction(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        self.process_command_and_get_output(test_cli, "force  1 Fleeing")

        output = self.process_command_and_get_output(test_cli, "state 1")

        self.assertIn("state: Fleeing!", output)

    # Simulate Command Tests Start

    # Test Simulate Command Invalid Arguments
    def test_simulate_command_invalid_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "simulate")

        self.assertIn("simulate_ai_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test Simulate Command Extra Arguments
    def test_simulate_command_extra_arguments(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "simulate 1 extra")

        self.assertIn("simulate_ai_failed", output)
        self.assertIn("Invalid arguments", output)

    # Test Simulate Command Without Map
    def test_simulate_command_without_map(self):
        test_cli = self.create_test_cli()

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("simulate_ai_failed", output)
        self.assertIn("Map does not exist", output)

    # Test Simulate Command Invalid Entity ID
    def test_simulate_command_invalid_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "simulate 99")

        self.assertIn("Invalid entity ID", output)

    # Test Simulate Command Negative Entity ID
    def test_simulate_command_negative_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "simulate -1")

        self.assertIn("Invalid entity ID", output)

    # Test Simulate Command With Warrior
    def test_simulate_command_warrior_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 1, 1)

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("simulate_ai_failed", output)
        self.assertIn("does not have a behavioral state", output)

    # Test Simulate Command With Mage
    def test_simulate_command_mage_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Mage", 1, 1)

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("does not have a behavioral state", output)

    # Test Simulate Command With Goblin
    def test_simulate_command_goblin_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("ok: simulated for 1 command:", output)

    # Test Simulate Command With Skeleton
    def test_simulate_command_skeleton_success(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Skeleton", 1, 1)

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("ok: simulated for 1 command:", output)

    # Test Simulate Command With Nearby Player
    def test_simulate_command_with_nearby_player(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Warrior", 2, 1)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        output = self.process_command_and_get_output(test_cli, "simulate 2")

        self.assertIn("ok: simulated for 2 command:", output)

    # Test Simulate Command Only Targets Selected Entity
    def test_simulate_command_target_entity(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)
        self.create_test_entity(test_cli, "Skeleton", 5, 5)

        output = self.process_command_and_get_output(test_cli, "simulate 2")

        self.assertIn("ok: simulated for 2 command:", output)

    # Test Simulate Command After Force State
    def test_simulate_command_after_force_state(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        self.process_command_and_get_output(test_cli, "force  1 Attacking")

        output = self.process_command_and_get_output(test_cli, "simulate 1")

        self.assertIn("ok: simulated for 1 command:", output)

    # Test Simulate Command Executes AI Once
    def test_simulate_command_calls_entity_update(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)
        self.create_test_entity(test_cli, "Goblin", 1, 1)

        entity = test_cli.game_state.get_entity_from_list(1)

        with patch.object(
            entity, "update_entity_state", return_value="Defend"
        ) as mock_update:
            output = self.process_command_and_get_output(test_cli, "simulate 1")

        mock_update.assert_called_once()
        self.assertIn("command: Defend!", output)

    # Test State Command Non-Integer Entity ID
    def test_state_command_non_integer_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "state nope")

        self.assertIn("entity_state_failed", output)

    # Test Simulate Command Non-Integer Entity ID
    def test_simulate_command_non_integer_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "simulate nope")

        self.assertIn("simulate_ai_failed", output)

    # Test Force State Command Non-Integer Entity ID
    def test_force_state_command_non_integer_entity_id(self):
        test_cli = self.create_test_cli()
        self.create_test_map(test_cli)

        output = self.process_command_and_get_output(test_cli, "force  nope Attacking")

        self.assertIn("force_state_failed", output)


if __name__ == "__main__":
    unittest.main()
