"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 26, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_command.py
Purpose: Tests the Command methods and classes.
"""

# Imports
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock
from command import Command, MoveCommand


# Test Command
class TestCommand(unittest.TestCase):

    # Test Abstract Command
    # Verify that Command cannot be instantiated directly
    # Returns: None
    def test_command_is_abstract(self):
        with self.assertRaises(TypeError):
            Command()

    # Test Move Command Initialization
    # Verify that MoveCommand stores the entity and destination
    # Returns: None
    def test_move_command_initialization(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, 1, 5, 6)

        self.assertEqual(test_command.get_name(), "Move")

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Move Command With Invalid Entity
    # Verify that MoveCommand raises an error if the entity does not exist
    # Returns: None
    def test_move_command_invalid_entity(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = None

        with self.assertRaises(ValueError):
            MoveCommand(test_game_state, 999, 5, 6)

    # Test Move Command Execute
    # Verify that executing the command moves the entity to its destination
    # Returns: None
    def test_move_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, "1", "5", "6")

        test_command.execute()

        test_game_state.move_entity.assert_called_once_with(1, 5, 6)

    # Test Move Command Undo
    # Verify that undo moves the entity back to its original position
    # Returns: None
    def test_move_command_undo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, 1, 5, 6)

        test_command.undo()

        test_game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test Move Command Execute And Undo
    # Verify that executing and undoing a command calls move_entity
    # with the destination and then the original position
    # Returns: None
    def test_move_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, 1, 5, 6)

        test_command.execute()
        test_command.undo()

        self.assertEqual(
            test_game_state.move_entity.call_args_list,
            [unittest.mock.call(1, 5, 6), unittest.mock.call(1, 2, 3)],
        )


if __name__ == "__main__":
    unittest.main()
