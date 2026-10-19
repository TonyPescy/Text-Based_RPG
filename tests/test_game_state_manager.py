"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 19, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_game_state_manager.py
Purpose: Utilizes unittest to test all of the classes and methods in game_state_manager.py file
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

# Imports
from game_state_manager import GameStateManager
import os
import tempfile
from game_state import GameState
import json
import unittest


# Game state manager tests
class TestGameStateManager(unittest.TestCase):
    # Reused methods

    # Set Up Test
    # Creates a new GameStateManager and temporary directory for save files.
    # Params: None
    # Returns: None
    def setUp(self):
        self.manager = GameStateManager()
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_directory.name, "test_save.json")

    # Tear Down Test
    # Removes the temporary directory after each test.
    # Params: None
    # Returns: None
    def tearDown(self):
        self.temp_directory.cleanup()

    # Create Empty Save Data
    # Creates valid basic save data with no grid or entities.
    # Params: None
    # Returns: dict - Save data
    def create_empty_save_data(self):
        return {
            "game_state": {
                "turn_number": 1,
                "entity_ids_issued": 1,
                "map_created": False,
            },
            "grid": None,
            "entities": [],
        }

    # Create Empty Game State Memento
    # Creates a Memento representing a new game state.
    # Params: None
    # Returns: GameState.Memento - Empty game state snapshot
    def create_empty_memento(self):
        return GameState.Memento(
            grid_memento=None,
            entity_mementos=(),
            entity_ids_issued=1,
            map_created=False,
            turn_number=1,
            is_saved=True,
        )

    # Initialization Tests

    # Initialize Game State Manager
    # Checks that a new GameStateManager can be created.
    # Params: None
    # Returns: None
    def test_init_game_state_manager(self):
        self.assertIsNotNone(self.manager)

    # Validation Tests

    # Validate Save Data
    # Checks that basic save data can be validated.
    # Params: None
    # Returns: None
    def test_validate_save_data(self):
        save_data = self.create_empty_save_data()

        self.assertIsNone(self.manager.validate_save_data(save_data))

    # Validate Non-Dictionary Save Data
    # Checks that non-dictionary save data raises a ValueError.
    # Params: None
    # Returns: None
    def test_validate_non_dictionary_save_data(self):
        with self.assertRaises(ValueError):
            self.manager.validate_save_data([])

    # Memento Conversion Tests

    # Convert Memento To Data
    # Checks that a GameState Memento converts to JSON-compatible data.
    # Params: None
    # Returns: None
    def test_memento_to_data(self):
        memento = self.create_empty_memento()

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(save_data["game_state"]["turn_number"], 1)
        self.assertEqual(save_data["game_state"]["entity_ids_issued"], 1)
        self.assertFalse(save_data["game_state"]["map_created"])
        self.assertIsNone(save_data["grid"])
        self.assertEqual(save_data["entities"], [])

    # Convert Data To Memento
    # Checks that basic save data converts back into a GameState Memento.
    # Params: None
    # Returns: None
    def test_data_to_memento(self):
        save_data = self.create_empty_save_data()

        memento = self.manager.data_to_memento(save_data)

        self.assertIsInstance(memento, GameState.Memento)
        self.assertEqual(memento.turn_number, 1)
        self.assertEqual(memento.entity_ids_issued, 1)
        self.assertFalse(memento.map_created)
        self.assertIsNone(memento.grid_memento)
        self.assertEqual(memento.entity_mementos, ())

    # Convert Memento To JSON-Compatible Data
    # Checks that converted save data can be serialized as JSON.
    # Params: None
    # Returns: None
    def test_memento_to_data_is_json_serializable(self):
        memento = self.create_empty_memento()

        save_data = self.manager.memento_to_data(memento)

        # JSON serialization should not raise an exception.
        serialized_data = json.dumps(save_data)

        self.assertIsInstance(serialized_data, str)

    # Round-Trip Empty Memento
    # Checks that converting a Memento to data and back preserves its state.
    # Params: None
    # Returns: None
    def test_memento_conversion_round_trip(self):
        original_memento = self.create_empty_memento()

        save_data = self.manager.memento_to_data(original_memento)
        restored_memento = self.manager.data_to_memento(save_data)

        self.assertEqual(restored_memento.turn_number, original_memento.turn_number)
        self.assertEqual(
            restored_memento.entity_ids_issued, original_memento.entity_ids_issued
        )
        self.assertEqual(restored_memento.map_created, original_memento.map_created)
        self.assertEqual(
            restored_memento.entity_mementos, original_memento.entity_mementos
        )

    # File Operation Tests

    # Write Save File
    # Checks that save data can be written to a JSON file.
    # Params: None
    # Returns: None
    def test_write_save_file(self):
        save_data = self.create_empty_save_data()

        self.manager.write_save_file(save_data, self.file_path)

        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r", encoding="utf-8") as save_file:
            loaded_data = json.load(save_file)

        self.assertEqual(loaded_data, save_data)

    # Read Save File
    # Checks that save data can be read from a JSON file.
    # Params: None
    # Returns: None
    def test_read_save_file(self):
        save_data = self.create_empty_save_data()

        with open(self.file_path, "w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file)

        loaded_data = self.manager.read_save_file(self.file_path)

        self.assertEqual(loaded_data, save_data)

    # Read Missing Save File
    # Checks that reading a missing file raises FileNotFoundError.
    # Params: None
    # Returns: None
    def test_read_missing_save_file(self):
        with self.assertRaises(FileNotFoundError):
            self.manager.read_save_file(
                os.path.join(self.temp_directory.name, "missing.json")
            )

    # Read Invalid JSON File
    # Checks that invalid JSON raises a ValueError.
    # Params: None
    # Returns: None
    def test_read_invalid_json_file(self):
        with open(self.file_path, "w", encoding="utf-8") as save_file:
            save_file.write("{ invalid json")

        with self.assertRaises(ValueError):
            self.manager.read_save_file(self.file_path)

    # Save Game Integration
    # Checks that save_game writes the current GameState to a file.
    # Params: None
    # Returns: None
    def test_save_game(self):
        game_state = GameState()

        self.manager.save_game(game_state, self.file_path)

        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)

        self.assertIn("game_state", save_data)
        self.assertIn("grid", save_data)
        self.assertIn("entities", save_data)

    # Load Game Integration
    # Checks that load_game restores a saved GameState.
    # Params: None
    # Returns: None
    def test_load_game(self):
        game_state = GameState()
        save_data = self.create_empty_save_data()

        with open(self.file_path, "w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file)

        self.manager.load_game(game_state, self.file_path)

        restored_memento = game_state.create_memento()

        self.assertEqual(restored_memento.turn_number, 1)
        self.assertEqual(restored_memento.entity_ids_issued, 1)
        self.assertFalse(restored_memento.map_created)


if __name__ == "main":
    unittest.main()
