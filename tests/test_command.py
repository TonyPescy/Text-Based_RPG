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
from command import Command, MoveCommand, SpawnCommand, SpawnLootCommand, AttackCommand


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

    # Test Move Command Redo
    # Verify that redo moves the entity to its original destination
    # Returns: None
    def test_move_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, 1, 5, 6)

        test_command.redo()

        test_game_state.move_entity.assert_called_once_with(1, 5, 6)

    # Test Move Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_move_command_get_name(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(2, 3)
        )

        test_command = MoveCommand(test_game_state, 1, 5, 6)

        self.assertEqual(test_command.get_name(), "Move")

    # Test Spawn Command Initialization
    # Verify that SpawnCommand stores the entity type and position
    # Returns: None
    def test_spawn_command_initialization(self):
        test_game_state = MagicMock()

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        self.assertEqual(test_command.get_name(), "Spawn")

    # Test Spawn Command Execute
    # Verify that executing the command spawns an entity at the specified position
    # Returns: None
    def test_spawn_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.spawn_entity.return_value = 10

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        test_command.execute()

        test_game_state.spawn_entity.assert_called_once_with(3, 4, "Warrior")

    # Test Spawn Command Undo
    # Verify that undo removes the spawned entity
    # Returns: None
    def test_spawn_command_undo(self):
        test_game_state = MagicMock()
        test_game_state.spawn_entity.return_value = 10

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        test_command.execute()
        test_command.undo()

        test_game_state.undo_spawn.assert_called_once_with(10)

    # Test Spawn Command Undo Before Execute
    # Verify that undo raises an error if the entity has not been spawned
    # Returns: None
    def test_spawn_command_undo_before_execute(self):
        test_game_state = MagicMock()

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        with self.assertRaisesRegex(ValueError, "Entity has not been spawned!"):
            test_command.undo()

        test_game_state.undo_spawn.assert_not_called()

    # Test Spawn Command Redo
    # Verify that redo spawns the entity at its original position
    # Returns: None
    def test_spawn_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.spawn_entity.return_value = 10

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        test_command.redo()

        test_game_state.spawn_entity.assert_called_once_with(3, 4, "Warrior")

    # Test Spawn Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_spawn_command_get_name(self):
        test_game_state = MagicMock()

        test_command = SpawnCommand(test_game_state, "Warrior", 3, 4)

        self.assertEqual(test_command.get_name(), "Spawn")

    # Test Spawn Loot Command Initialization
    def test_spawn_loot_command_initialization(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        self.assertEqual(test_command.get_name(), "Spawn Loot")

    # Test Spawn Loot Command Execute
    def test_spawn_loot_command_execute(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        test_command.execute()

        test_game_state.spawn_loot.assert_called_once_with(3, 4, "IronSword")

    # Test Spawn Loot Command Undo
    def test_spawn_loot_command_undo(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        test_command.undo()

        test_game_state.remove_item_from_tile.assert_called_once_with(3, 4, "IronSword")

    # Test Spawn Loot Command Execute And Undo
    def test_spawn_loot_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        test_command.execute()
        test_command.undo()

        test_game_state.spawn_loot.assert_called_once_with(3, 4, "IronSword")
        test_game_state.remove_item_from_tile.assert_called_once_with(3, 4, "IronSword")

    # Test Spawn Loot Command Redo
    def test_spawn_loot_command_redo(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        test_command.redo()

        test_game_state.spawn_loot.assert_called_once_with(3, 4, "IronSword")

    # Test Spawn Loot Command Get Name
    def test_spawn_loot_command_get_name(self):
        test_game_state = MagicMock()
        test_command = SpawnLootCommand(test_game_state, "IronSword", 3, 4)

        self.assertEqual(test_command.get_name(), "Spawn Loot")

    # Test Attack Command Initialization
    def test_attack_command_initialization(self):
        test_game_state = MagicMock()

        test_command = AttackCommand(test_game_state, "1", "2")

        self.assertEqual(test_command.get_name(), "Attack")
        self.assertIsNone(test_command.get_damage())

    # Test Attack Command Execute
    def test_attack_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.attack_entity.return_value = 15

        test_command = AttackCommand(test_game_state, "1", "2")
        test_command.execute()

        test_game_state.attack_entity.assert_called_once_with(1, 2)
        self.assertEqual(test_command.get_damage(), 15)

    # Test Attack Command Undo
    def test_attack_command_undo(self):
        test_game_state = MagicMock()
        test_game_state.attack_entity.return_value = 15

        test_command = AttackCommand(test_game_state, 1, 2)
        test_command.execute()
        test_command.undo()

        test_game_state.restore_entity_health.assert_called_once_with(2, 15)

    # Test Attack Command Undo Before Execute
    def test_attack_command_undo_before_execute(self):
        test_game_state = MagicMock()
        test_command = AttackCommand(test_game_state, 1, 2)

        with self.assertRaisesRegex(ValueError, "Attack has not been executed!"):
            test_command.undo()

        test_game_state.restore_entity_health.assert_not_called()

    # Test Attack Command Redo
    def test_attack_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.attack_entity.return_value = 15

        test_command = AttackCommand(test_game_state, 1, 2)
        test_command.execute()

        test_game_state.attack_entity.reset_mock()
        test_command.redo()

        test_game_state.attack_entity.assert_called_once_with(1, 2)

    # Test Attack Command Redo Before Execute
    def test_attack_command_redo_before_execute(self):
        test_game_state = MagicMock()
        test_command = AttackCommand(test_game_state, 1, 2)

        with self.assertRaisesRegex(ValueError, "Attack has not been executed!"):
            test_command.redo()

        test_game_state.attack_entity.assert_not_called()

    # Test Attack Command Get Name
    def test_attack_command_get_name(self):
        test_game_state = MagicMock()
        test_command = AttackCommand(test_game_state, 1, 2)

        self.assertEqual(test_command.get_name(), "Attack")

    # Test Attack Command Get Damage
    def test_attack_command_get_damage(self):
        test_game_state = MagicMock()
        test_game_state.attack_entity.return_value = 12

        test_command = AttackCommand(test_game_state, 1, 2)
        test_command.execute()

        self.assertEqual(test_command.get_damage(), 12)

    # Test Attack Command Execute And Undo
    def test_attack_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_game_state.attack_entity.return_value = 10

        test_command = AttackCommand(test_game_state, 1, 2)
        test_command.execute()
        test_command.undo()

        test_game_state.attack_entity.assert_called_once_with(1, 2)
        test_game_state.restore_entity_health.assert_called_once_with(2, 10)
        self.assertEqual(test_command.get_damage(), 10)

    # Test Attack Command Undo Removes Dead Status
    def test_attack_command_undo_removes_dead_status(self):
        game_state = MagicMock()
        entity = MagicMock()
        entity_info = MagicMock()

        entity_info.temp_buffs = ((("Name", "Dead"), ("Effects", []), ("Turns", 0)),)
        entity.get_info.return_value = entity_info
        game_state.get_entity_from_list.return_value = entity

        command = AttackCommand(game_state, 1, 2)
        command.execute()
        command.undo()

        entity.remove_temp_buffs.assert_called_once_with(["Dead"])
        game_state.restore_entity_health.assert_called_once_with(
            2, command.get_damage()
        )

    # Test Attack Command Undo Without Dead Status
    def test_attack_command_undo_without_dead_status(self):
        game_state = MagicMock()
        entity = MagicMock()
        entity_info = MagicMock()

        entity_info.temp_buffs = ()
        entity.get_info.return_value = entity_info
        game_state.get_entity_from_list.return_value = entity

        command = AttackCommand(game_state, 1, 2)
        command.execute()
        command.undo()

        entity.remove_temp_buffs.assert_not_called()
        game_state.restore_entity_health.assert_called_once_with(
            2, command.get_damage()
        )

    # Test Attack Command Undo Before Execute
    def test_attack_command_undo_before_execute(self):
        game_state = MagicMock()
        command = AttackCommand(game_state, 1, 2)

        with self.assertRaises(ValueError):
            command.undo()

        game_state.get_entity_from_list.assert_not_called()
        game_state.restore_entity_health.assert_not_called()


if __name__ == "__main__":
    unittest.main()
