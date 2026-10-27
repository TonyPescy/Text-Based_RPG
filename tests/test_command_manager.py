"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 26, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_command_manager.py
Purpose: Tests the Command manager methods and classes.
"""

# Imports
import unittest
from unittest.mock import MagicMock
from command_manager import CommandManager


# Test Command Manager
class TestCommandManager(unittest.TestCase):

    # Create Test Command Manager
    # Creates a CommandManager instance for testing
    # Returns: test_manager - CommandManager - instance used for testing
    def create_test_command_manager(self):
        return CommandManager()

    # Create Test Command
    # Creates a mock command for testing
    # Returns: test_command - Mock - command used for testing
    def create_test_command(self):
        return MagicMock()

    # Test Execute Command
    # Verify that executing a command calls its execute method
    # Returns: None
    def test_execute_command(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)

        test_command.execute.assert_called_once()
        test_command.undo.assert_not_called()
        test_command.redo.assert_not_called()

    # Test Undo Last Command
    # Verify that undo reverses the most recently executed command
    # Returns: None
    def test_undo_last_command(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)

        is_undone, command_undone = test_manager.undo_last_command()

        self.assertTrue(is_undone)
        self.assertIs(command_undone, test_command)
        test_command.undo.assert_called_once()

    # Test Undo With Empty History
    # Verify that undo returns False and None when history is empty
    # Returns: None
    def test_undo_empty_history(self):
        test_manager = self.create_test_command_manager()

        is_undone, command_undone = test_manager.undo_last_command()

        self.assertFalse(is_undone)
        self.assertIsNone(command_undone)

    # Test Undo Commands In Reverse Order
    # Verify that commands are undone in last-in, first-out order
    # Returns: None
    def test_undo_commands_in_reverse_order(self):
        test_manager = self.create_test_command_manager()
        first_command = self.create_test_command()
        second_command = self.create_test_command()

        test_manager.execute_command(first_command)
        test_manager.execute_command(second_command)

        is_undone, command_undone = test_manager.undo_last_command()

        self.assertTrue(is_undone)
        self.assertIs(command_undone, second_command)
        second_command.undo.assert_called_once()
        first_command.undo.assert_not_called()

        is_undone, command_undone = test_manager.undo_last_command()

        self.assertTrue(is_undone)
        self.assertIs(command_undone, first_command)
        first_command.undo.assert_called_once()

    # Test Redo Last Command
    # Verify that redo repeats the most recently undone command
    # Returns: None
    def test_redo_last_command(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)
        test_manager.undo_last_command()

        is_redone, command_redone = test_manager.redo_last_command()

        self.assertTrue(is_redone)
        self.assertIs(command_redone, test_command)
        test_command.redo.assert_called_once()

    # Test Redo With Empty History
    # Verify that redo returns False and None when no commands can be redone
    # Returns: None
    def test_redo_empty_history(self):
        test_manager = self.create_test_command_manager()

        is_redone, command_redone = test_manager.redo_last_command()

        self.assertFalse(is_redone)
        self.assertIsNone(command_redone)

    # Test Redo Commands In Reverse Order
    # Verify that multiple undone commands are redone in the correct order
    # Returns: None
    def test_redo_commands_in_order(self):
        test_manager = self.create_test_command_manager()
        first_command = self.create_test_command()
        second_command = self.create_test_command()

        test_manager.execute_command(first_command)
        test_manager.execute_command(second_command)

        test_manager.undo_last_command()
        test_manager.undo_last_command()

        is_redone, command_redone = test_manager.redo_last_command()

        self.assertTrue(is_redone)
        self.assertIs(command_redone, first_command)
        first_command.redo.assert_called_once()
        second_command.redo.assert_not_called()

        is_redone, command_redone = test_manager.redo_last_command()

        self.assertTrue(is_redone)
        self.assertIs(command_redone, second_command)
        second_command.redo.assert_called_once()

    # Test New Command Clears Redo History
    # Verify that executing a new command clears previously undone commands
    # Returns: None
    def test_new_command_clears_redo_history(self):
        test_manager = self.create_test_command_manager()
        first_command = self.create_test_command()
        second_command = self.create_test_command()

        test_manager.execute_command(first_command)
        test_manager.undo_last_command()

        # Execute a new command after undoing the first command
        test_manager.execute_command(second_command)

        is_redone, command_redone = test_manager.redo_last_command()

        self.assertFalse(is_redone)
        self.assertIsNone(command_redone)
        first_command.redo.assert_not_called()

    # Test Clear History
    # Verify that clearing history empties both undo and redo stacks
    # Returns: None
    def test_clear_history(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)
        test_manager.undo_last_command()

        test_manager.clear_history()

        is_undone, command_undone = test_manager.undo_last_command()
        is_redone, command_redone = test_manager.redo_last_command()

        self.assertFalse(is_undone)
        self.assertIsNone(command_undone)
        self.assertFalse(is_redone)
        self.assertIsNone(command_redone)

        test_command.undo.assert_called_once()
        test_command.redo.assert_not_called()

    # Test Failed Command Is Not Added To History
    # Verify that a command that raises an exception during execution
    # is not available to undo
    # Returns: None
    def test_failed_command_not_added_to_history(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_command.execute.side_effect = ValueError("Command failed!")

        with self.assertRaises(ValueError):
            test_manager.execute_command(test_command)

        test_command.execute.assert_called_once()

        is_undone, command_undone = test_manager.undo_last_command()

        self.assertFalse(is_undone)
        self.assertIsNone(command_undone)
        test_command.undo.assert_not_called()

    # Test Execute Multiple Commands
    # Verify that each command is executed exactly once
    # Returns: None
    def test_execute_multiple_commands(self):
        test_manager = self.create_test_command_manager()
        first_command = self.create_test_command()
        second_command = self.create_test_command()

        test_manager.execute_command(first_command)
        test_manager.execute_command(second_command)

        first_command.execute.assert_called_once()
        second_command.execute.assert_called_once()

    # Test Failed Undo Behavior
    # Verify that a failed undo does not lose the command from history
    # Returns: None
    def test_failed_undo(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)
        test_command.undo.side_effect = ValueError("Undo failed!")

        with self.assertRaises(ValueError):
            test_manager.undo_last_command()

        # The command should remain available in undo history
        test_command.undo.assert_called_once()

    # Test Failed Redo Behavior
    # Verify that a failed redo does not lose the command from redo history
    # Returns: None
    def test_failed_redo(self):
        test_manager = self.create_test_command_manager()
        test_command = self.create_test_command()

        test_manager.execute_command(test_command)
        test_manager.undo_last_command()
        test_command.redo.side_effect = ValueError("Redo failed!")

        with self.assertRaises(ValueError):
            test_manager.redo_last_command()

        # The command should remain available in redo history
        test_command.redo.assert_called_once()


if __name__ == "__main__":
    unittest.main()
