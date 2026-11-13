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
from unittest.mock import MagicMock, patch
from game_state_manager import GameStateManager
from command_manager import CommandManager, create_command_from_memento
from command import (
    Command,
    MoveCommand,
    SpawnCommand,
    SpawnLootCommand,
    AttackCommand,
    CastSpellCommand,
    SetTileCommand,
    PickupCommand,
    GiveItemCommand,
    DropItemCommand,
    SwapItemCommand,
    UseItemCommand,
    TickCommand,
    InitCommand,
    SaveCommand,
    LoadCommand,
    SimulateCommand,
    ForceStateCommand,
)


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

    def test_command_manager_initialization(self):
        test_command_manager = CommandManager()

        history_info = test_command_manager.get_history_info()

        self.assertEqual(history_info, (0, 0))

    def test_create_command_from_memento(self):
        game_state = object()

        command_types = [
            ("MoveCommand", MoveCommand),
            ("SpawnCommand", SpawnCommand),
            ("SpawnLootCommand", SpawnLootCommand),
            ("AttackCommand", AttackCommand),
            ("CastSpellCommand", CastSpellCommand),
            ("SetTileCommand", SetTileCommand),
            ("PickupCommand", PickupCommand),
            ("GiveItemCommand", GiveItemCommand),
            ("DropItemCommand", DropItemCommand),
            ("SwapItemCommand", SwapItemCommand),
            ("UseItemCommand", UseItemCommand),
            ("TickCommand", TickCommand),
            ("InitCommand", InitCommand),
            ("SaveCommand", SaveCommand),
            ("LoadCommand", LoadCommand),
            ("ForceStateCommand", ForceStateCommand),
            ("SimulateCommand", SimulateCommand),
        ]

        # Test each supported command type
        for command_type, command_class in command_types:
            with self.subTest(command_type=command_type):
                command_memento = Command.Memento(
                    command_type=command_type,
                    data={},
                )
                game_state_manager = GameStateManager()
                command_manager = CommandManager()
                # Mock restore so the test focuses on factory reconstruction
                with patch.object(
                    command_class, "restore", autospec=True
                ) as mock_restore:
                    command = create_command_from_memento(
                        command_memento, game_state, game_state_manager, command_manager
                    )

                    # Verify correct command object was created
                    self.assertIsInstance(command, command_class)

                    # Verify the command was restored
                    mock_restore.assert_called_once_with(
                        command,
                        command_memento,
                        game_state,
                        game_state_manager,
                        command_manager,
                    )

    # Test Create Command From Invalid Memento
    # Verifies that an unsupported command type raises an error
    # Params: None
    # Returns: None
    def test_create_command_from_invalid_memento(self):
        command_memento = Command.Memento(
            command_type="InvalidCommand",
            data={},
        )
        game_state_manager = GameStateManager()
        command_manager = CommandManager()
        with self.assertRaises(ValueError):
            create_command_from_memento(
                command_memento, object(), game_state_manager, command_manager
            )

    # Test Command Manager Restore
    # Verifies that undo and redo histories are reconstructed
    # Params: None
    # Returns: None
    def test_restore_command_history(self):
        game_state = object()
        manager = CommandManager()

        undo_memento = Command.Memento(
            command_type="MoveCommand",
            data={},
        )

        redo_memento = Command.Memento(
            command_type="AttackCommand",
            data={},
        )

        manager_memento = CommandManager.Memento(
            undo_history=(undo_memento,),
            redo_history=(redo_memento,),
        )

        undo_command = object()
        redo_command = object()

        # Mock the factory to verify the manager uses it for both histories
        with patch(
            "command_manager.create_command_from_memento",
            side_effect=[undo_command, redo_command],
        ) as mock_factory:
            game_state_manager = GameStateManager()
            command_manager = CommandManager()

            manager.restore(
                manager_memento, game_state, game_state_manager, command_manager
            )

            # Verify both commands were reconstructed
            self.assertEqual(mock_factory.call_count, 2)

            # Verify the commands were placed in the correct histories
            self.assertIs(
                manager._CommandManager__undo_history[0],
                undo_command,
            )

            self.assertIs(
                manager._CommandManager__redo_history[0],
                redo_command,
            )

            self.assertEqual(manager.get_history_info(), (1, 1))

    # Test Restore Invalid Memento
    # Verifies that an invalid manager memento raises a TypeError
    # Params: None
    # Returns: None
    def test_restore_invalid_memento(self):
        manager = CommandManager()

        with self.assertRaises(TypeError):
            manager.restore(object(), object())

    # Force State Command Factory Tests Start

    # Test Create Force State Command From Memento
    # Verify that the factory creates and restores a ForceStateCommand
    # Returns: None
    def test_create_force_state_command_from_memento(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        command_memento = Command.Memento(
            command_type="ForceStateCommand",
            data={
                "entity_id": 1,
                "state_name": "Attacking",
                "old_state": "Defending",
                "executed": True,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertIsInstance(command, ForceStateCommand)
        self.assertEqual(command.get_name(), "Force State")

        restored_memento = command.create_memento()

        self.assertEqual(restored_memento.command_type, "ForceStateCommand")
        self.assertEqual(restored_memento.data["entity_id"], 1)
        self.assertEqual(restored_memento.data["state_name"], "Attacking")
        self.assertEqual(restored_memento.data["old_state"], "Defending")
        self.assertTrue(restored_memento.data["executed"])

    # Test Create Force State Command With Fleeing State
    # Verify that the factory restores a different behavioral state
    # Returns: None
    def test_create_force_state_command_fleeing(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        command_memento = Command.Memento(
            command_type="ForceStateCommand",
            data={
                "entity_id": 2,
                "state_name": "Fleeing",
                "old_state": "Attacking",
                "executed": True,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertIsInstance(command, ForceStateCommand)

        restored_memento = command.create_memento()

        self.assertEqual(restored_memento.data["entity_id"], 2)
        self.assertEqual(restored_memento.data["state_name"], "Fleeing")
        self.assertEqual(restored_memento.data["old_state"], "Attacking")

    # Test Create Force State Command Before Execution
    # Verify that an unexecuted command is restored correctly
    # Returns: None
    def test_create_force_state_command_not_executed(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        command_memento = Command.Memento(
            command_type="ForceStateCommand",
            data={
                "entity_id": 1,
                "state_name": "Defending",
                "old_state": None,
                "executed": False,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertIsInstance(command, ForceStateCommand)

        restored_memento = command.create_memento()

        self.assertIsNone(restored_memento.data["old_state"])
        self.assertFalse(restored_memento.data["executed"])

    # Simulate Command Factory Tests Start

    # Test Create Simulate Command From Memento
    # Verify that the factory creates and restores a SimulateCommand
    # Returns: None
    def test_create_simulate_command_from_memento(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        old_state = {"turn_number": 3}

        command_memento = Command.Memento(
            command_type="SimulateCommand",
            data={
                "entity_id": 1,
                "old_state": old_state,
                "executed": True,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertIsInstance(command, SimulateCommand)
        self.assertEqual(command.get_name(), "Simulate")

        restored_memento = command.create_memento()

        self.assertEqual(restored_memento.command_type, "SimulateCommand")
        self.assertEqual(restored_memento.data["entity_id"], 1)
        self.assertEqual(restored_memento.data["old_state"], old_state)
        self.assertTrue(restored_memento.data["executed"])

    # Test Create Simulate Command Before Execution
    # Verify that a simulation without a previous snapshot is restored
    # Returns: None
    def test_create_simulate_command_not_executed(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        command_memento = Command.Memento(
            command_type="SimulateCommand",
            data={
                "entity_id": 2,
                "old_state": None,
                "executed": False,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertIsInstance(command, SimulateCommand)

        restored_memento = command.create_memento()

        self.assertEqual(restored_memento.data["entity_id"], 2)
        self.assertIsNone(restored_memento.data["old_state"])
        self.assertFalse(restored_memento.data["executed"])

    # Test Simulate Command Memento Deep Copy
    # Verify that changing the original snapshot does not affect
    # the snapshot stored by the restored command
    # Returns: None
    def test_create_simulate_command_memento_deepcopy(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        old_state = {"entities": [{"id": 1, "health": 100}]}

        command_memento = Command.Memento(
            command_type="SimulateCommand",
            data={
                "entity_id": 1,
                "old_state": old_state,
                "executed": True,
            },
        )

        command = create_command_from_memento(
            command_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        # Modify original snapshot after restoration
        old_state["entities"][0]["health"] = 25

        restored_memento = command.create_memento()

        # Restored command should retain the original health
        self.assertEqual(
            restored_memento.data["old_state"]["entities"][0]["health"],
            100,
        )

    # Test Restore History With AI Commands
    # Verify that ForceStateCommand and SimulateCommand are
    # reconstructed in the correct command history stacks
    # Returns: None
    def test_restore_history_with_ai_commands(self):
        game_state = MagicMock()
        game_state_manager = GameStateManager()
        command_manager = CommandManager()

        force_memento = Command.Memento(
            command_type="ForceStateCommand",
            data={
                "entity_id": 1,
                "state_name": "Attacking",
                "old_state": "Defending",
                "executed": True,
            },
        )

        simulate_memento = Command.Memento(
            command_type="SimulateCommand",
            data={
                "entity_id": 2,
                "old_state": None,
                "executed": False,
            },
        )

        manager_memento = CommandManager.Memento(
            undo_history=(force_memento,),
            redo_history=(simulate_memento,),
        )

        command_manager.restore(
            manager_memento,
            game_state,
            game_state_manager,
            command_manager,
        )

        self.assertEqual(command_manager.get_history_info(), (1, 1))

        undo_command = command_manager._CommandManager__undo_history[0]
        redo_command = command_manager._CommandManager__redo_history[0]

        self.assertIsInstance(undo_command, ForceStateCommand)
        self.assertIsInstance(redo_command, SimulateCommand)

        self.assertEqual(undo_command.get_name(), "Force State")
        self.assertEqual(redo_command.get_name(), "Simulate")


if __name__ == "__main__":
    unittest.main()
