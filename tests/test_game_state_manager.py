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
from entity import Entity
from unittest.mock import patch
from command_manager import CommandManager
from command import Command
import equipment


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
        self.command_manager = CommandManager()

    # Create Command Memento
    # Creates a basic command Memento for testing
    def create_command_memento(self):
        return Command.Memento(
            command_type="TestCommand",
            data={
                "entity_id": 1,
                "x": 5,
                "y": 10,
            },
        )

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
            "command_manager": {
                "undo_history": [],
                "redo_history": [],
            },
            "grid": None,
            "entities": [],
        }

    # Create Entity Memento For Testing
    # Creates a GameState with a spawned entity and returns its Memento
    # Params: entity_type - str - type of entity to spawn
    #         state_name - str/None - behavioral state to assign
    # Returns: GameState.Memento - Memento containing the entity
    def create_entity_memento(self, entity_type="goblin", state_name=None):
        game_state = GameState()
        game_state.create_grid(5, 5)

        # Spawn entity
        entity_id = game_state.spawn_entity(2, 2, entity_type)
        entity = game_state.get_entity_from_list(entity_id)

        # Assign a specific behavioral state when requested
        if state_name is not None:
            entity.restore_state_manager(
                Entity.StateManagerMemento(state_name=state_name), game_state
            )

        return game_state.create_memento(self.command_manager)

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
            command_manager_memento=CommandManager.Memento(
                undo_history=(),
                redo_history=(),
            ),
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
        self.assertEqual(save_data["command_manager"]["undo_history"], [])
        self.assertEqual(save_data["command_manager"]["redo_history"], [])
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

        self.manager.save_game(game_state, self.file_path, self.command_manager)

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

        self.manager.load_game(game_state, self.file_path, self.command_manager)

        restored_memento = game_state.create_memento(self.command_manager)

        self.assertEqual(restored_memento.turn_number, 1)
        self.assertEqual(restored_memento.entity_ids_issued, 1)
        self.assertFalse(restored_memento.map_created)
        self.assertIsInstance(
            restored_memento.command_manager_memento,
            CommandManager.Memento,
        )

    # Test that a new GameStateManager can be created
    def test_init_game_state_manager(self):
        self.assertIsNotNone(self.manager)

    # Test that the save directory is created during initialization
    def test_init_creates_save_directory(self):
        self.assertTrue(os.path.isdir("save_files"))

    # Test creating a filepath with a JSON extension
    def test_create_filepath_with_json_extension(self):
        filepath = self.manager.create_filepath("test_save.json")

        self.assertEqual(filepath, os.path.join("save_files", "test_save.json"))

    # Test adding a JSON extension when it is missing
    def test_create_filepath_without_json_extension(self):
        filepath = self.manager.create_filepath("test_save")

        self.assertEqual(filepath, os.path.join("save_files", "test_save.json"))

    # Test creating a filepath with a filename containing spaces
    def test_create_filepath_with_spaces(self):
        filepath = self.manager.create_filepath("my test save")

        self.assertEqual(filepath, os.path.join("save_files", "my test save.json"))

    # Test that creating a filepath does not create the save file itself
    def test_create_filepath_does_not_create_file(self):
        filepath = self.manager.create_filepath("test_save")

        self.assertFalse(os.path.exists(filepath))

    # Test that basic save data can be validated
    def test_validate_save_data(self):
        save_data = self.create_empty_save_data()

        self.assertIsNone(self.manager.validate_save_data(save_data))

    # Test that non-dictionary save data raises a ValueError
    def test_validate_non_dictionary_save_data(self):
        with self.assertRaises(ValueError):
            self.manager.validate_save_data([])

    # Success
    # Test deleting an existing save file
    def test_delete_save_removes_existing_file(self):
        # Create temporary save file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            filepath = temp_file.name

        # Mock file path creation
        with patch.object(self.manager, "create_filepath", return_value=filepath):
            # Delete save file
            self.manager.delete_save("test_save")

        # Test file no longer exists
        self.assertFalse(os.path.exists(filepath))

    # Failure
    # Test deleting a save file that does not exist
    def test_delete_save_with_missing_file_raises_error(self):
        # Mock file path creation
        with patch.object(
            self.manager, "create_filepath", return_value="missing_save.json"
        ):
            # Test FileNotFoundError
            with self.assertRaises(FileNotFoundError):
                self.manager.delete_save("missing_save")  # Success

    # Test deleting an existing save file
    def test_delete_save_removes_existing_file(self):
        # Create temporary save file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            filepath = temp_file.name

        # Mock file path creation
        with patch.object(self.manager, "create_filepath", return_value=filepath):
            # Delete save file
            self.manager.delete_save("test_save")

        # Test file no longer exists
        self.assertFalse(os.path.exists(filepath))

    # Failure
    # Test deleting a save file that does not exist
    def test_delete_save_with_missing_file_raises_error(self):
        # Mock file path creation
        with patch.object(
            self.manager, "create_filepath", return_value="missing_save.json"
        ):
            # Test FileNotFoundError
            with self.assertRaises(FileNotFoundError):
                self.manager.delete_save("missing_save")

    # Test Memento To Data - Goblin Defending
    # Checks that a Goblin's default behavioral state is serialized
    def test_memento_to_data_goblin_defending(self):
        memento = self.create_entity_memento("goblin")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"], {"state_name": "Defending"}
        )

    # Test Memento To Data - Goblin Attacking
    # Checks that an Attacking state is serialized
    def test_memento_to_data_goblin_attacking(self):
        memento = self.create_entity_memento("goblin", "Attacking")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"]["state_name"], "Attacking"
        )

    # Test Memento To Data - Goblin Fleeing
    # Checks that a Fleeing state is serialized
    def test_memento_to_data_goblin_fleeing(self):
        memento = self.create_entity_memento("goblin", "Fleeing")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"]["state_name"], "Fleeing"
        )

    # Test Memento To Data - Skeleton
    # Checks that Skeleton behavioral states are serialized
    def test_memento_to_data_skeleton(self):
        memento = self.create_entity_memento("skeleton", "Attacking")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"]["state_name"], "Attacking"
        )

    # Test Memento To Data - Warrior
    # Checks that player entities serialize with no behavioral state
    def test_memento_to_data_warrior(self):
        memento = self.create_entity_memento("warrior")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"], {"state_name": None}
        )

    # Test Memento To Data - Mage
    # Checks that wrapped Mage Mementos serialize without AI state
    def test_memento_to_data_mage(self):
        memento = self.create_entity_memento("mage")

        save_data = self.manager.memento_to_data(memento)

        self.assertEqual(
            save_data["entities"][0]["state_manager"], {"state_name": None}
        )

    # Test Memento To Data - JSON Serialization
    # Checks that behavioral state data can be serialized into JSON
    def test_memento_to_data_entity_json_serializable(self):
        memento = self.create_entity_memento("goblin", "Fleeing")

        save_data = self.manager.memento_to_data(memento)

        serialized_data = json.dumps(save_data)

        self.assertIsInstance(serialized_data, str)

        # Verify state is preserved after JSON conversion
        decoded_data = json.loads(serialized_data)

        self.assertEqual(
            decoded_data["entities"][0]["state_manager"]["state_name"], "Fleeing"
        )

    # Test Data To Memento - Defending
    # Checks that Defending state is reconstructed
    def test_data_to_memento_defending(self):
        memento = self.create_entity_memento("goblin")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        entity_memento = restored_memento.entity_mementos[0]

        self.assertIsInstance(entity_memento.state_manager, Entity.StateManagerMemento)
        self.assertEqual(entity_memento.state_manager.state_name, "Defending")

    # Test Data To Memento - Attacking
    # Checks that Attacking state is reconstructed
    def test_data_to_memento_attacking(self):
        memento = self.create_entity_memento("goblin", "Attacking")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertEqual(
            restored_memento.entity_mementos[0].state_manager.state_name, "Attacking"
        )

    # Test Data To Memento - Fleeing
    # Checks that Fleeing state is reconstructed
    def test_data_to_memento_fleeing(self):
        memento = self.create_entity_memento("goblin", "Fleeing")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertEqual(
            restored_memento.entity_mementos[0].state_manager.state_name, "Fleeing"
        )

    # Test Data To Memento - Skeleton
    # Checks that Skeleton state is reconstructed
    def test_data_to_memento_skeleton(self):
        memento = self.create_entity_memento("skeleton", "Attacking")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertEqual(
            restored_memento.entity_mementos[0].state_manager.state_name, "Attacking"
        )

    # Test Data To Memento - Warrior
    # Checks that Warriors restore with no behavioral state
    def test_data_to_memento_warrior(self):
        memento = self.create_entity_memento("warrior")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertIsNone(restored_memento.entity_mementos[0].state_manager.state_name)

    # Test Data To Memento - Mage
    # Checks that Mage Mementos preserve their wrapped Entity Memento
    def test_data_to_memento_mage(self):
        memento = self.create_entity_memento("mage")
        save_data = self.manager.memento_to_data(memento)

        restored_memento = self.manager.data_to_memento(save_data)

        mage_memento = restored_memento.entity_mementos[0]

        self.assertIsNone(mage_memento.entity_memento.state_manager.state_name)

    # Test Data To Memento - Missing Enemy State
    # Checks that older save files default enemies to Defending
    def test_data_to_memento_missing_enemy_state(self):
        memento = self.create_entity_memento("goblin")
        save_data = self.manager.memento_to_data(memento)

        # Simulate an older save file without state_manager
        del save_data["entities"][0]["state_manager"]

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertEqual(
            restored_memento.entity_mementos[0].state_manager.state_name, "Defending"
        )

    # Test Data To Memento - Missing Player State
    # Checks that older save files restore players without AI state
    def test_data_to_memento_missing_player_state(self):
        memento = self.create_entity_memento("warrior")
        save_data = self.manager.memento_to_data(memento)

        # Simulate an older save file without state_manager
        del save_data["entities"][0]["state_manager"]

        restored_memento = self.manager.data_to_memento(save_data)

        self.assertIsNone(restored_memento.entity_mementos[0].state_manager.state_name)

    # Test State Manager Memento Round Trip
    # Checks that a behavioral state survives serialization and reconstruction
    def test_state_manager_memento_round_trip(self):
        original_memento = self.create_entity_memento("goblin", "Fleeing")

        # Convert Memento to JSON data
        save_data = self.manager.memento_to_data(original_memento)

        # Simulate actual JSON serialization
        json_data = json.loads(json.dumps(save_data))

        # Convert JSON data back into Memento
        restored_memento = self.manager.data_to_memento(json_data)

        original_state = original_memento.entity_mementos[0].state_manager.state_name
        restored_state = restored_memento.entity_mementos[0].state_manager.state_name

        self.assertEqual(original_state, restored_state)
        self.assertEqual(restored_state, "Fleeing")

    # Test Multiple Entity State Managers Round Trip
    # Checks that each entity preserves its own behavioral state
    def test_multiple_entity_state_managers_round_trip(self):
        game_state = GameState()
        game_state.create_grid(5, 5)

        # Spawn different entity types
        goblin_id = game_state.spawn_entity(0, 0, "goblin")
        skeleton_id = game_state.spawn_entity(1, 1, "skeleton")
        warrior_id = game_state.spawn_entity(2, 2, "warrior")
        mage_id = game_state.spawn_entity(3, 3, "mage")

        # Assign enemy states
        goblin = game_state.get_entity_from_list(goblin_id)
        skeleton = game_state.get_entity_from_list(skeleton_id)

        goblin.restore_state_manager(
            Entity.StateManagerMemento("Attacking"), game_state
        )
        skeleton.restore_state_manager(
            Entity.StateManagerMemento("Fleeing"), game_state
        )

        # Create Memento and serialize
        original_memento = game_state.create_memento(self.command_manager)
        save_data = self.manager.memento_to_data(original_memento)

        # Simulate JSON save/load
        json_data = json.loads(json.dumps(save_data))
        restored_memento = self.manager.data_to_memento(json_data)

        # Extract states, handling Mage's wrapped Memento
        restored_states = []

        for entity_memento in restored_memento.entity_mementos:
            if hasattr(entity_memento, "entity_memento"):
                entity_memento = entity_memento.entity_memento

            restored_states.append(entity_memento.state_manager.state_name)

        self.assertEqual(restored_states, ["Attacking", "Fleeing", None, None])

    # Ogre Raging State Serialization
    def test_memento_to_data_ogre_raging(self):
        memento = self.create_entity_memento("ogre", "Raging")
        save_data = self.manager.memento_to_data(memento)
        self.assertEqual(
            save_data["entities"][0]["state_manager"]["state_name"], "Raging"
        )

    # Ogre Defending State Serialization
    def test_memento_to_data_ogre_defending(self):
        memento = self.create_entity_memento("ogre", "Defending")
        save_data = self.manager.memento_to_data(memento)
        self.assertEqual(
            save_data["entities"][0]["state_manager"]["state_name"], "Defending"
        )

    # Ogre Raging State Deserialization
    def test_data_to_memento_ogre_raging(self):
        memento = self.create_entity_memento("ogre", "Raging")
        save_data = self.manager.memento_to_data(memento)
        restored = self.manager.data_to_memento(save_data)
        self.assertEqual(restored.entity_mementos[0].state_manager.state_name, "Raging")

    # Ogre Raging State JSON Round Trip
    def test_ogre_raging_json_round_trip(self):
        memento = self.create_entity_memento("ogre", "Raging")
        data = json.loads(json.dumps(self.manager.memento_to_data(memento)))
        restored = self.manager.data_to_memento(data)
        self.assertEqual(restored.entity_mementos[0].state_manager.state_name, "Raging")

    # Ogre Missing State Defaults To Defending
    def test_data_to_memento_missing_ogre_state(self):
        memento = self.create_entity_memento("ogre", "Defending")
        data = self.manager.memento_to_data(memento)
        del data["entities"][0]["state_manager"]
        restored = self.manager.data_to_memento(data)
        self.assertEqual(
            restored.entity_mementos[0].state_manager.state_name, "Defending"
        )

    # Ogre Raging State Persists To File
    def test_save_load_ogre_raging(self):
        game_state = GameState()
        game_state.create_grid(5, 5)
        entity_id = game_state.spawn_entity(2, 2, "ogre")
        ogre = game_state.get_entity_from_list(entity_id)
        ogre.restore_state_manager(Entity.StateManagerMemento("Raging"), game_state)
        with patch.object(self.manager, "create_filepath", return_value=self.file_path):
            self.manager.save_game(game_state, "test_save", self.command_manager)
            restored_game = GameState()
            restored_commands = CommandManager()
            self.manager.load_game(restored_game, "test_save", restored_commands)
        restored_ogre = restored_game.get_entity_from_list(entity_id)
        self.assertEqual(restored_ogre.get_entity_state_name(), "Raging")

    # Convert Empty Command Manager Memento To Data
    # Checks that an empty CommandManager Memento converts correctly.
    # Params: None
    # Returns: None
    def test_command_manager_memento_to_data_empty(self):
        memento = CommandManager.Memento(
            undo_history=(),
            redo_history=(),
        )

        data = self.manager.command_manager_memento_to_data(memento)

        self.assertEqual(data["undo_history"], [])
        self.assertEqual(data["redo_history"], [])

    # Convert None Command Manager Memento To Data
    # Checks that None returns None.
    # Params: None
    # Returns: None
    def test_command_manager_memento_to_data_none(self):
        data = self.manager.command_manager_memento_to_data(None)

        self.assertIsNone(data)

    # Convert Command Manager Memento To Data
    # Checks that command histories are converted into lists of dictionaries.
    # Params: None
    # Returns: None
    def test_command_manager_memento_to_data(self):
        command_memento = self.create_command_memento()

        memento = CommandManager.Memento(
            undo_history=(command_memento,),
            redo_history=(command_memento,),
        )

        data = self.manager.command_manager_memento_to_data(memento)

        self.assertEqual(len(data["undo_history"]), 1)
        self.assertEqual(len(data["redo_history"]), 1)

        self.assertEqual(
            data["undo_history"][0]["command_type"],
            "TestCommand",
        )

        self.assertEqual(
            data["undo_history"][0]["data"]["entity_id"],
            1,
        )

    # Convert Command Memento To Data
    # Checks that a Command Memento converts into a dictionary.
    # Params: None
    # Returns: None
    def test_command_memento_to_data(self):
        memento = self.create_command_memento()

        data = self.manager.command_memento_to_data(memento)

        self.assertEqual(data["command_type"], "TestCommand")
        self.assertEqual(data["data"]["entity_id"], 1)
        self.assertEqual(data["data"]["x"], 5)
        self.assertEqual(data["data"]["y"], 10)

    # Convert Nested Command Data To Data
    # Checks that nested dictionaries, lists, and tuples are converted recursively.
    # Params: None
    # Returns: None
    def test_command_data_to_data_nested_collections(self):
        data = {
            "entity_id": 1,
            "position": (5, 10),
            "items": ["sword", "shield"],
            "nested": {
                "health": 100,
                "modifiers": ("attack", "defence"),
            },
        }

        converted_data = self.manager.command_data_to_data(data)

        self.assertEqual(converted_data["entity_id"], 1)
        self.assertEqual(converted_data["position"], [5, 10])
        self.assertEqual(converted_data["items"], ["sword", "shield"])
        self.assertEqual(
            converted_data["nested"]["modifiers"],
            ["attack", "defence"],
        )

    # Convert Nested Command Memento To Data
    # Checks that nested Command Mementos are converted recursively.
    # Params: None
    # Returns: None
    def test_command_data_to_data_nested_command_memento(self):
        command_memento = self.create_command_memento()

        data = {
            "old_command": command_memento,
        }

        converted_data = self.manager.command_data_to_data(data)

        self.assertEqual(
            converted_data["old_command"]["command_type"],
            "TestCommand",
        )

        self.assertEqual(
            converted_data["old_command"]["data"]["entity_id"],
            1,
        )

    # Convert Nested Command Manager Memento To Data
    # Checks that nested CommandManager Mementos are converted recursively.
    # Params: None
    # Returns: None
    def test_command_data_to_data_nested_command_manager_memento(self):
        command_memento = self.create_command_memento()

        command_manager_memento = CommandManager.Memento(
            undo_history=(command_memento,),
            redo_history=(),
        )

        converted_data = self.manager.command_data_to_data(
            {"manager": command_manager_memento}
        )

        self.assertEqual(
            converted_data["manager"]["undo_history"][0]["command_type"],
            "TestCommand",
        )

        self.assertEqual(
            converted_data["manager"]["redo_history"],
            [],
        )

    # Convert Unsupported Command Data
    # Checks that unsupported objects raise a TypeError.
    # Params: None
    # Returns: None
    def test_command_data_to_data_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.manager.command_data_to_data(object())

    # Convert Command Manager Memento To JSON
    # Checks that a CommandManager Memento can be serialized as JSON.
    # Params: None
    # Returns: None
    def test_command_manager_memento_to_data_json_serializable(self):
        command_memento = self.create_command_memento()

        memento = CommandManager.Memento(
            undo_history=(command_memento,),
            redo_history=(),
        )

        data = self.manager.command_manager_memento_to_data(memento)

        serialized_data = json.dumps(data)

        self.assertIsInstance(serialized_data, str)

    # Convert Data To Command Manager Memento
    # Checks that dictionary data converts back into a CommandManager Memento.
    # Params: None
    # Returns: None
    def test_data_to_command_manager_memento(self):
        command_data = {
            "command_type": "TestCommand",
            "data": {
                "entity_id": 1,
                "x": 5,
                "y": 10,
            },
        }

        manager_data = {
            "undo_history": [command_data],
            "redo_history": [],
        }

        memento = self.manager.data_to_command_manager_memento(manager_data)

        self.assertIsInstance(memento, CommandManager.Memento)
        self.assertEqual(len(memento.undo_history), 1)
        self.assertEqual(len(memento.redo_history), 0)
        self.assertEqual(memento.undo_history[0].command_type, "TestCommand")
        self.assertEqual(memento.undo_history[0].data["entity_id"], 1)

    # Convert None Data To Command Manager Memento
    # Checks that None returns None.
    # Params: None
    # Returns: None
    def test_data_to_command_manager_memento_none(self):
        memento = self.manager.data_to_command_manager_memento(None)

        self.assertIsNone(memento)

    # Convert Data To Command Memento
    # Checks that dictionary data converts back into a Command Memento.
    # Params: None
    # Returns: None
    def test_data_to_command_memento(self):
        command_data = {
            "command_type": "TestCommand",
            "data": {
                "entity_id": 1,
                "x": 5,
                "y": 10,
            },
        }

        memento = self.manager.data_to_command_memento(command_data)

        self.assertIsInstance(memento, Command.Memento)
        self.assertEqual(memento.command_type, "TestCommand")
        self.assertEqual(memento.data["entity_id"], 1)
        self.assertEqual(memento.data["x"], 5)
        self.assertEqual(memento.data["y"], 10)

    # Round Trip Command Manager Memento
    # Checks that a CommandManager Memento converts to data and back correctly.
    # Params: None
    # Returns: None
    def test_command_manager_memento_conversion_round_trip(self):
        original_command = self.create_command_memento()

        original_memento = CommandManager.Memento(
            undo_history=(original_command,),
            redo_history=(original_command,),
        )

        data = self.manager.command_manager_memento_to_data(original_memento)

        restored_memento = self.manager.data_to_command_manager_memento(data)

        self.assertEqual(
            restored_memento.undo_history[0].command_type,
            original_memento.undo_history[0].command_type,
        )

        self.assertEqual(
            restored_memento.undo_history[0].data,
            original_memento.undo_history[0].data,
        )

        self.assertEqual(
            restored_memento.redo_history[0].command_type,
            original_memento.redo_history[0].command_type,
        )

    # Test Equipment Memento Round Trip
    def test_equipment_memento_round_trip(self):
        original = equipment.EquipmentMemento(
            name="IronSword",
            slot="Weapon",
            rarity="Rare",
            rolled_effects=(("Attack", 6), ("Speed", 2)),
        )

        data = self.manager.equipment_memento_to_data(original)

        restored = self.manager.data_to_equipment_memento(data)

        self.assertEqual(original, restored)

    # Test Consumable Memento Round Trip
    def test_consumable_memento_round_trip(self):
        base = equipment.EquipmentMemento(
            name="TurtleMasterPotion",
            slot="Consumable",
            rarity="Common",
            rolled_effects=(),
        )

        original = equipment.ConsumableMemento(
            equipment_memento=base,
            instant_effects=(
                ("Flat_modifiers", (("Health", 10),)),
                ("Percent_modifiers", ()),
            ),
            over_time_effects=(
                ("Flat_modifiers", (("Attack", 3),)),
                ("Percent_modifiers", ()),
            ),
            duration=5,
        )

        data = self.manager.equipment_memento_to_data(original)

        restored = self.manager.data_to_equipment_memento(data)

        self.assertEqual(original, restored)

    # Test Equipment Memento JSON Serialization
    def test_equipment_memento_json_serializable(self):
        memento = equipment.EquipmentMemento(
            name="IronSword",
            slot="Weapon",
            rarity="Rare",
            rolled_effects=(("Attack", 6),),
        )

        data = self.manager.equipment_memento_to_data(memento)

        serialized = json.dumps(data)

        self.assertIsInstance(serialized, str)

    # Equipment and Consumable Serialization Helpers
    def create_item_memento(self, name="IronSword", rarity="Rare", rolled_effects=None):
        item = equipment.create_equipment(name)
        self.assertIsNotNone(item)
        original = item.create_memento()
        if rolled_effects is None:
            rolled_effects = (("Attack", 6), ("Speed", 2))
        base = equipment.EquipmentMemento(
            name=(
                original.name
                if isinstance(original, equipment.EquipmentMemento)
                else original.equipment_memento.name
            ),
            slot=item.slot,
            rarity=rarity,
            rolled_effects=tuple(rolled_effects),
        )
        if isinstance(original, equipment.ConsumableMemento):
            return equipment.ConsumableMemento(
                equipment_memento=base,
                instant_effects=original.instant_effects,
                over_time_effects=original.over_time_effects,
                duration=original.duration,
            )
        return base

    def assert_item_json_round_trip(self, original):
        data = self.manager.equipment_memento_to_data(original)
        restored = self.manager.data_to_equipment_memento(json.loads(json.dumps(data)))
        self.assertEqual(restored, original)
        return data

    # Equipment Memento Tests
    def test_equipment_memento_to_data_preserves_rarity_and_rolls(self):
        original = self.create_item_memento()
        data = self.manager.equipment_memento_to_data(original)
        self.assertEqual(data["name"], "IronSword")
        self.assertEqual(data["rarity"], "Rare")
        self.assertEqual(data["rolled_effects"], {"Attack": 6, "Speed": 2})
        self.assertEqual(data["item_type"], "Equipment")
        self.assertEqual(data["slot"], "Weapon")

    def test_equipment_memento_json_round_trip_with_multiple_rolls(self):
        self.assert_item_json_round_trip(self.create_item_memento())

    def test_equipment_memento_json_round_trip_empty_rolls(self):
        self.assert_item_json_round_trip(
            self.create_item_memento("LeatherTunic", "Common", ())
        )

    def test_equipment_memento_json_round_trip_negative_roll(self):
        self.assert_item_json_round_trip(
            self.create_item_memento("CursedDagger", "Epic", (("Defence", -5),))
        )

    def test_equipment_memento_to_data_none(self):
        self.assertIsNone(self.manager.equipment_memento_to_data(None))

    def test_data_to_equipment_memento_none(self):
        self.assertIsNone(self.manager.data_to_equipment_memento(None))

    def test_equipment_memento_to_data_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.manager.equipment_memento_to_data(object())

    def test_data_to_equipment_memento_rejects_unknown_item_type(self):
        data = self.manager.equipment_memento_to_data(self.create_item_memento())
        data["item_type"] = "Unknown"
        with self.assertRaises(ValueError):
            self.manager.data_to_equipment_memento(data)

    # Consumable Memento Tests
    def test_consumable_memento_to_data_preserves_effects(self):
        original = self.create_item_memento("TurtleMasterPotion", "Rare", ())
        data = self.manager.equipment_memento_to_data(original)
        self.assertEqual(data["item_type"], "Consumable")
        self.assertEqual(data["name"], "TurtleMasterPotion")
        self.assertEqual(data["rarity"], "Rare")
        self.assertEqual(data["slot"], "Consumable")
        self.assertEqual(data["duration"], 5)
        self.assertEqual(data["instant_effects"]["Percent_modifiers"]["Health"], "10")
        self.assertEqual(data["over_time_effects"]["Flat_modifiers"]["Speed"], "-3")
        self.assertEqual(
            data["over_time_effects"]["Percent_modifiers"]["Defence"], "20"
        )

    def test_consumable_memento_json_round_trip_with_timed_effects(self):
        self.assert_item_json_round_trip(
            self.create_item_memento("TurtleMasterPotion", "Rare", ())
        )

    def test_consumable_memento_json_round_trip_instant_only(self):
        self.assert_item_json_round_trip(
            self.create_item_memento("SmallHealthPotion", "Common", ())
        )

    def test_consumable_memento_json_round_trip_mana_potion(self):
        self.assert_item_json_round_trip(
            self.create_item_memento("ManaPotion", "Common", ())
        )

    def test_equipment_serialization_does_not_modify_original_memento(self):
        original = self.create_item_memento()
        before = original.rolled_effects
        data = self.manager.equipment_memento_to_data(original)
        data["rolled_effects"]["Attack"] = 999
        self.assertEqual(original.rolled_effects, before)

    def test_consumable_serialization_does_not_modify_original_memento(self):
        original = self.create_item_memento("TurtleMasterPotion", "Rare", ())
        data = self.manager.equipment_memento_to_data(original)
        data["instant_effects"]["Percent_modifiers"]["Health"] = "999"
        self.assertEqual(
            dict(dict(original.instant_effects)["Percent_modifiers"])["Health"],
            "10",
        )

    # Game State Item Integration Tests
    def test_memento_to_data_preserves_backpack_item_mementos(self):
        game_state = GameState()
        game_state.create_grid(5, 5)
        entity_id = game_state.spawn_entity(1, 1, "warrior")
        entity = game_state.get_entity_from_list(entity_id)
        entity.add_item_to_backpack(equipment.create_equipment("TurtleMasterPotion"))
        entity.add_item_to_backpack(equipment.create_equipment("IronSword"))
        save_data = self.manager.memento_to_data(
            game_state.create_memento(self.command_manager)
        )
        backpack = save_data["entities"][0]["backpack"]
        self.assertEqual(
            [item["name"] for item in backpack], ["TurtleMasterPotion", "IronSword"]
        )
        self.assertEqual(backpack[0]["duration"], 5)
        self.assertEqual(backpack[1]["slot"], "Weapon")

    def test_game_state_item_mementos_survive_json_round_trip(self):
        game_state = GameState()
        game_state.create_grid(5, 5)
        entity_id = game_state.spawn_entity(1, 1, "warrior")
        entity = game_state.get_entity_from_list(entity_id)
        entity.add_item_to_backpack(equipment.create_equipment("TurtleMasterPotion"))
        original = game_state.create_memento(self.command_manager)
        data = json.loads(json.dumps(self.manager.memento_to_data(original)))
        restored = self.manager.data_to_memento(data)
        self.assertEqual(
            restored.entity_mementos[0].backpack.items,
            original.entity_mementos[0].backpack.items,
        )


if __name__ == "__main__":
    unittest.main()
