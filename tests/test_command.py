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
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
from entity import Entity
from io import StringIO
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
    InspectCommand,
    InventoryCommand,
    TileCommand,
    StateInfoCommand,
    HistoryCommand,
    UndoCommand,
    RedoCommand,
)


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

    # Test Cast Spell Command Execute
    def test_cast_spell_command_execute(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target.get_info.return_value.health = 70

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, "1", "2", "Fireball")
        test_command.execute()

        test_game_state.cast_spell.assert_called_once_with(1, 2, "Fireball")
        self.assertEqual(
            test_command.get_spell_result(),
            "Dealt 15 damage to 2!",
        )

    # Test Cast Spell Command Undo
    def test_cast_spell_command_undo(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target.get_info.return_value.health = 70
        target.get_info.return_value.temp_buffs = ()

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()
        test_command.undo()

        test_game_state.undo_cast.assert_called_once_with(1, 2, "Fireball", 100, 70)

    # Test Cast Spell Command Undo Before Execute
    def test_cast_spell_command_undo_before_execute(self):
        test_game_state = MagicMock()
        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")

        with self.assertRaisesRegex(ValueError, "Spell has not been cast!"):
            test_command.undo()

        test_game_state.get_entity_from_list.assert_not_called()
        test_game_state.undo_cast.assert_not_called()

    # Test Cast Spell Command Redo
    def test_cast_spell_command_redo(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target.get_info.return_value.health = 70

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()

        test_game_state.cast_spell.reset_mock()
        test_command.redo()

        test_game_state.cast_spell.assert_called_once_with(1, 2, "Fireball")

    # Test Cast Spell Command Redo Before Execute
    def test_cast_spell_command_redo_before_execute(self):
        test_game_state = MagicMock()
        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")

        with self.assertRaisesRegex(ValueError, "Spell has not been cast!"):
            test_command.redo()

        test_game_state.cast_spell.assert_not_called()

    # Test Cast Spell Command Get Name
    def test_cast_spell_command_get_name(self):
        test_game_state = MagicMock()
        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")

        self.assertEqual(test_command.get_name(), "Cast")

    # Test Cast Spell Command Get Spell Result
    def test_cast_spell_command_get_spell_result(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target.get_info.return_value.health = 70

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()

        self.assertEqual(
            test_command.get_spell_result(),
            "Dealt 15 damage to 2!",
        )

    # Test Cast Spell Command Execute And Undo
    def test_cast_spell_command_execute_and_undo(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 80
        target.get_info.return_value.health = 50
        target.get_info.return_value.temp_buffs = ()

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()
        test_command.undo()

        test_game_state.cast_spell.assert_called_once_with(1, 2, "Fireball")
        test_game_state.undo_cast.assert_called_once_with(1, 2, "Fireball", 80, 50)

    # Test Cast Spell Command Undo Removes Dead Status
    def test_cast_spell_command_undo_removes_dead_status(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target_info = MagicMock()
        target_info.health = 0
        target_info.temp_buffs = ((("Name", "Dead"), ("Effects", []), ("Turns", 0)),)
        target.get_info.return_value = target_info

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Target died!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()
        test_command.undo()

        target.remove_temp_buffs.assert_called_once_with(["Dead"])
        test_game_state.undo_cast.assert_called_once_with(1, 2, "Fireball", 100, 0)

    # Test Cast Spell Command Undo Without Dead Status
    def test_cast_spell_command_undo_without_dead_status(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target_info = MagicMock()
        target_info.health = 50
        target_info.temp_buffs = ()
        target.get_info.return_value = target_info

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Dealt 15 damage to 2!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Fireball")
        test_command.execute()
        test_command.undo()

        target.remove_temp_buffs.assert_not_called()
        test_game_state.undo_cast.assert_called_once_with(1, 2, "Fireball", 100, 50)

    # Test Cast Spell Command Undo Removes Spell Effect
    def test_cast_spell_command_undo_removes_spell_effect(self):
        test_game_state = MagicMock()
        caster = MagicMock()
        target = MagicMock()

        caster.get_info.return_value.mana = 100
        target_info = MagicMock()
        target_info.health = 50
        target_info.temp_buffs = (
            (
                ("Name", "Frostbolt"),
                ("Effects", []),
                ("Turns", 1),
            ),
        )
        target.get_info.return_value = target_info

        test_game_state.get_entity_from_list.side_effect = lambda entity_id: (
            caster if entity_id == 1 else target
        )
        test_game_state.cast_spell.return_value = "Applied Frostbolt effect!"

        test_command = CastSpellCommand(test_game_state, 1, 2, "Frostbolt")
        test_command.execute()
        test_command.undo()

        target.remove_temp_buffs.assert_called_once_with(["Frostbolt"])
        test_game_state.undo_cast.assert_called_once_with(1, 2, "Frostbolt", 100, 50)

    # Success
    def test_set_tile_command_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as unoccupied
        game_state.is_grid_tile_occupied.return_value = False

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Execute command
        command.execute()

        # Check original tile was retrieved
        game_state.get_game_tile_info.assert_called_once_with(1, 2)

        # Check new tile was set
        game_state.set_game_grid_tile.assert_called_once_with(1, 2, "ShallowWater")

        # Check entity was not updated
        game_state.update_entity.assert_not_called()

    # Success
    def test_set_tile_command_execute_updates_occupied_tile(self):
        # Create mock game state
        game_state = MagicMock()

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as occupied
        game_state.is_grid_tile_occupied.return_value = True
        game_state.get_entity_id_from_tile.return_value = 1

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Execute command
        command.execute()

        # Check tile was set
        game_state.set_game_grid_tile.assert_called_once_with(1, 2, "ShallowWater")

        # Check entity was updated
        game_state.update_entity.assert_called_once_with(1)

    # Success
    def test_set_tile_command_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as unoccupied
        game_state.is_grid_tile_occupied.return_value = False

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Execute command
        command.execute()

        # Reset mock call history
        game_state.set_game_grid_tile.reset_mock()

        # Undo command
        command.undo()

        # Check original tile was restored
        game_state.set_game_grid_tile.assert_called_once_with(1, 2, "Floor")

    # Failure
    def test_set_tile_command_undo_before_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Check undo raises an error
        with self.assertRaisesRegex(ValueError, "Tile has not been set!"):
            command.undo()

        # Check tile was not changed
        game_state.set_game_grid_tile.assert_not_called()

    # Success
    def test_set_tile_command_redo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as unoccupied
        game_state.is_grid_tile_occupied.return_value = False

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Execute command
        command.execute()

        # Undo command
        command.undo()

        # Reset mock call history
        game_state.set_game_grid_tile.reset_mock()

        # Redo command
        command.redo()

        # Check tile was set again
        game_state.set_game_grid_tile.assert_called_once_with(1, 2, "ShallowWater")

    # Failure
    def test_set_tile_command_redo_before_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as unoccupied
        game_state.is_grid_tile_occupied.return_value = False

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Execute command
        command.execute()

        # Check redo raises an error
        with self.assertRaisesRegex(ValueError, "Tile has already been set!"):
            command.redo()

    # Success
    def test_set_tile_command_get_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = SetTileCommand(game_state, 1, 2, "ShallowWater")

        # Check command name
        self.assertEqual(command.get_name(), "Set")

    # Success
    def test_set_tile_command_converts_coordinates_to_integers(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command with string coordinates
        command = SetTileCommand(game_state, "1", "2", "ShallowWater")

        # Create original tile info
        old_tile = MagicMock()
        old_tile.tile_type = "Floor"
        game_state.get_game_tile_info.return_value = old_tile

        # Set tile as unoccupied
        game_state.is_grid_tile_occupied.return_value = False

        # Execute command
        command.execute()

        # Check coordinates were converted to integers
        game_state.set_game_grid_tile.assert_called_once_with(1, 2, "ShallowWater")

    # Success
    def test_pickup_command_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check tile item was removed
        game_state.remove_item_from_tile.assert_called_once_with(
            1, 2, "SmallHealthPotion"
        )

        # Check item was added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Failure
    def test_pickup_command_execute_item_not_on_tile(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info without the requested item
        tile_info = MagicMock()
        tile_info.item_list = ["IronSword"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Check execute raises an error
        with self.assertRaisesRegex(ValueError, "Item not found on tile!"):
            command.execute()

        # Check item was not removed
        game_state.remove_item_from_tile.assert_not_called()

        # Check item was not added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_not_called()

    # Failure
    def test_pickup_command_execute_item_removal_fails(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Simulate failed item removal
        game_state.remove_item_from_tile.return_value = None

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Check execute raises an error
        with self.assertRaisesRegex(ValueError, "Item could not be removed from tile!"):
            command.execute()

        # Check item was not added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_not_called()

    # Success
    def test_pickup_command_execute_case_insensitive_item_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command with different capitalization
        command = PickupCommand(game_state, 1, "smallhealthpotion")

        # Execute command
        command.execute()

        # Check actual tile item was removed
        game_state.remove_item_from_tile.assert_called_once_with(
            1, 2, "SmallHealthPotion"
        )

        # Check item was added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_pickup_command_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Reset mock call history
        game_state.set_game_grid_tile.reset_mock()

        # Undo command
        command.undo()

        # Check item was removed from backpack
        game_state.remove_item_from_backpack.assert_called_once_with(
            1, "SmallHealthPotion"
        )

        # Check item was returned to original tile
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

    # Failure
    def test_pickup_command_undo_before_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Check undo raises an error
        with self.assertRaisesRegex(ValueError, "Item has not been picked up!"):
            command.undo()

        # Check item was not returned to tile
        game_state.add_item_to_tile.assert_not_called()

        # Check item was not removed from backpack
        game_state.remove_item_from_backpack.assert_not_called()

    # Success
    def test_pickup_command_redo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Undo command
        command.undo()

        # Reset mock call history
        game_state.add_item_to_backpack_based_on_info.reset_mock()
        game_state.remove_item_from_tile.reset_mock()

        # Redo command
        command.redo()

        # Check item was removed from tile again
        game_state.remove_item_from_tile.assert_called_once_with(
            1, 2, "SmallHealthPotion"
        )

        # Check item was added to backpack again
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Failure
    def test_pickup_command_redo_before_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check redo raises an error
        with self.assertRaisesRegex(ValueError, "Item has already been picked up!"):
            command.redo()

    # Success
    def test_pickup_command_get_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = PickupCommand(game_state, 1, "SmallHealthPotion")

        # Check command name
        self.assertEqual(command.get_name(), "Pickup")

    # Success
    def test_pickup_command_converts_entity_id_to_integer(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create tile info
        tile_info = MagicMock()
        tile_info.item_list = ["SmallHealthPotion"]
        game_state.get_game_tile_info.return_value = tile_info

        # Create removed item
        removed_item = MagicMock()
        removed_item.name = "SmallHealthPotion"
        game_state.remove_item_from_tile.return_value = removed_item

        # Create command with string entity ID
        command = PickupCommand(game_state, "1", "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check entity ID was converted to integer
        game_state.get_entity_info_from_list.assert_called_with(1)

        # Check item was added to correct backpack
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_give_item_command_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check item was added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_give_item_command_execute_converts_entity_id_to_integer(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command with string entity ID
        command = GiveItemCommand(game_state, "1", "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check item was added using integer entity ID
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_give_item_command_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Undo command
        command.undo()

        # Check item was removed from backpack
        game_state.remove_item_from_backpack.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Failure
    def test_give_item_command_undo_before_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Check undo raises an error
        with self.assertRaisesRegex(ValueError, "Item has not been given!"):
            command.undo()

        # Check item was not removed from backpack
        game_state.remove_item_from_backpack.assert_not_called()

    # Success
    def test_give_item_command_redo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Undo command
        command.undo()

        # Reset mock call history
        game_state.add_item_to_backpack_based_on_info.reset_mock()

        # Redo command
        command.redo()

        # Check item was added again
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Failure
    def test_give_item_command_redo_before_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check redo raises an error
        with self.assertRaisesRegex(ValueError, "Item has already been given!"):
            command.redo()

        # Check item was only added once
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_give_item_command_get_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = GiveItemCommand(game_state, 1, "SmallHealthPotion")

        # Check command name
        self.assertEqual(command.get_name(), "Give")

    # Success
    def test_drop_item_command_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check item was added to tile
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

        # Check item was removed from backpack
        game_state.remove_item_from_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

        # Check inventory was updated
        game_state.update_inventory_based_on_info.assert_called_once_with(1)

        # Check entity was updated
        game_state.update_entity.assert_called_once_with(1)

    # Failure
    def test_drop_item_command_execute_item_not_in_backpack(self):
        # Create mock game state
        game_state = MagicMock()

        # Create entity info without the requested item
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = ()
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Check execute raises an error
        with self.assertRaisesRegex(ValueError, "Item not found in backpack!"):
            command.execute()

        # Check item was not added to tile
        game_state.add_item_to_tile.assert_not_called()

        # Check item was not removed from backpack
        game_state.remove_item_from_backpack_based_on_info.assert_not_called()

    # Success
    def test_drop_item_command_execute_case_insensitive_item_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command with different capitalization
        command = DropItemCommand(game_state, 1, "smallhealthpotion")

        # Execute command
        command.execute()

        # Check actual item name was used
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

        # Check item was removed from backpack
        game_state.remove_item_from_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Success
    def test_drop_item_command_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Reset mock call history
        game_state.remove_item_from_tile.reset_mock()
        game_state.add_item_to_backpack_based_on_info.reset_mock()

        # Undo command
        command.undo()

        # Check item was removed from tile
        game_state.remove_item_from_tile.assert_called_once_with(
            1, 2, "SmallHealthPotion"
        )

        # Check item was returned to backpack
        game_state.add_item_to_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

        # Check inventory and entity were updated
        self.assertEqual(game_state.update_inventory_based_on_info.call_count, 2)
        self.assertEqual(game_state.update_entity.call_count, 2)

    # Failure
    def test_drop_item_command_undo_before_execute(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Check undo raises an error
        with self.assertRaisesRegex(ValueError, "Item has not been dropped!"):
            command.undo()

        # Check item was not removed from tile
        game_state.remove_item_from_tile.assert_not_called()

        # Check item was not added to backpack
        game_state.add_item_to_backpack_based_on_info.assert_not_called()

    # Success
    def test_drop_item_command_redo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Undo command
        command.undo()

        # Reset mock call history
        game_state.add_item_to_tile.reset_mock()
        game_state.remove_item_from_backpack_based_on_info.reset_mock()

        # Redo command
        command.redo()

        # Check item was added to tile again
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

        # Check item was removed from backpack again
        game_state.remove_item_from_backpack_based_on_info.assert_called_once_with(
            1, "SmallHealthPotion"
        )

    # Failure
    def test_drop_item_command_redo_before_undo(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check redo raises an error
        with self.assertRaisesRegex(ValueError, "Item has already been dropped!"):
            command.redo()

        # Check item was only dropped once
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

    # Success
    def test_drop_item_command_get_name(self):
        # Create mock game state
        game_state = MagicMock()

        # Create command
        command = DropItemCommand(game_state, 1, "SmallHealthPotion")

        # Check command name
        self.assertEqual(command.get_name(), "Drop")

    # Success
    def test_drop_item_command_converts_entity_id_to_integer(self):
        # Create mock game state
        game_state = MagicMock()

        # Create item info
        item_info = MagicMock()
        item_info.name = "SmallHealthPotion"

        # Create entity info
        entity_info = MagicMock()
        entity_info.position = (1, 2)
        entity_info.backpack = (item_info,)
        game_state.get_entity_info_from_list.return_value = entity_info

        # Create command with string entity ID
        command = DropItemCommand(game_state, "1", "SmallHealthPotion")

        # Execute command
        command.execute()

        # Check entity ID was converted to integer
        game_state.get_entity_info_from_list.assert_called_with(1)

        # Check correct entity was updated
        game_state.update_entity.assert_called_once_with(1)

    # Success
    def test_swap_item_command_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create backpack item
        backpack_item = MagicMock()
        backpack_item.name = "Iron Sword"
        backpack_item.slot = "Weapon"

        # Create previously equipped item
        old_item = MagicMock()
        old_item.name = "None"
        old_item.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = [backpack_item]

        # Mock GameState methods
        test_game_state.get_entity_info_from_list.return_value = entity_info
        test_game_state.get_equipped_item_info.return_value = old_item

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Execute Command
        test_command.execute()

        # Verify results
        test_game_state.get_entity_info_from_list.assert_called_once_with(1)
        test_game_state.get_equipped_item_info.assert_called_once_with(1, "Weapon")
        test_game_state.equip_item_based_on_info.assert_called_once_with(
            1, "Iron Sword", "Weapon"
        )
        test_game_state.update_entity.assert_called_once_with(1)

    # Success
    def test_swap_item_command_converts_entity_id_to_integer(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, "1", "Weapon", "Iron Sword")

        # Verify entity ID conversion
        self.assertEqual(test_command._SwapItemCommand__entity_id, 1)

    # Failure
    def test_swap_item_command_execute_item_not_in_backpack(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = []

        # Mock GameState method
        test_game_state.get_entity_info_from_list.return_value = entity_info

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item not found in backpack!"):
            test_command.execute()

        # Verify item was not equipped
        test_game_state.equip_item_based_on_info.assert_not_called()
        test_game_state.update_entity.assert_not_called()

    # Success
    def test_swap_item_command_execute_finds_item_case_insensitive(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create backpack item
        backpack_item = MagicMock()
        backpack_item.name = "Iron Sword"
        backpack_item.slot = "Weapon"

        # Create previously equipped item
        old_item = MagicMock()
        old_item.name = "None"
        old_item.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = [backpack_item]

        # Mock GameState methods
        test_game_state.get_entity_info_from_list.return_value = entity_info
        test_game_state.get_equipped_item_info.return_value = old_item

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "iron sword")

        # Execute Command
        test_command.execute()

        # Verify matching item was equipped
        test_game_state.equip_item_based_on_info.assert_called_once_with(
            1, "Iron Sword", "Weapon"
        )

    # Success
    def test_swap_item_command_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create backpack item
        backpack_item = MagicMock()
        backpack_item.name = "Iron Sword"
        backpack_item.slot = "Weapon"

        # Create previously equipped item
        old_item = MagicMock()
        old_item.name = "None"
        old_item.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = [backpack_item]

        # Mock GameState methods
        test_game_state.get_entity_info_from_list.return_value = entity_info
        test_game_state.get_equipped_item_info.return_value = old_item

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Execute Command
        test_command.execute()

        # Reset method call history
        test_game_state.equip_item_based_on_info.reset_mock()
        test_game_state.update_entity.reset_mock()

        # Undo Command
        test_command.undo()

        # Verify previous item was restored
        test_game_state.equip_item_based_on_info.assert_called_once_with(
            1, "None", "Weapon"
        )
        test_game_state.update_entity.assert_called_once_with(1)

    # Failure
    def test_swap_item_command_undo_before_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item has not been swapped!"):
            test_command.undo()

    # Success
    def test_swap_item_command_redo_after_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create backpack item
        backpack_item = MagicMock()
        backpack_item.name = "Iron Sword"
        backpack_item.slot = "Weapon"

        # Create previously equipped item
        old_item = MagicMock()
        old_item.name = "None"
        old_item.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = [backpack_item]

        # Mock GameState methods
        test_game_state.get_entity_info_from_list.return_value = entity_info
        test_game_state.get_equipped_item_info.return_value = old_item

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Reset call history
        test_game_state.equip_item_based_on_info.reset_mock()
        test_game_state.update_entity.reset_mock()

        # Redo Command
        test_command.redo()

        # Verify item was equipped again
        test_game_state.equip_item_based_on_info.assert_called_once_with(
            1, "Iron Sword", "Weapon"
        )
        test_game_state.update_entity.assert_called_once_with(1)

    # Failure
    def test_swap_item_command_redo_before_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create backpack item
        backpack_item = MagicMock()
        backpack_item.name = "Iron Sword"
        backpack_item.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.backpack = [backpack_item]

        # Mock GameState method
        test_game_state.get_entity_info_from_list.return_value = entity_info

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item has already been swapped!"):
            test_command.redo()

    # Success
    def test_swap_item_command_get_name(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Swap Item Command
        test_command = SwapItemCommand(test_game_state, 1, "Weapon", "Iron Sword")

        # Verify command name
        self.assertEqual(test_command.get_name(), "Swap")

    # Success
    def test_use_item_command_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Execute Command
        test_command.execute()

        # Verify results
        test_game_state.create_memento.assert_called_once_with()
        test_game_state.use_consumable.assert_called_once_with(1, "Small Health Potion")

    # Success
    def test_use_item_command_converts_entity_id_to_integer(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, "1", "Small Health Potion")

        # Verify entity ID conversion
        self.assertEqual(test_command._UseItemCommand__entity_id, 1)

    # Success
    def test_use_item_command_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Execute Command
        test_command.execute()

        # Reset restore method call history
        test_game_state.restore_memento.reset_mock()

        # Undo Command
        test_command.undo()

        # Verify state was restored
        test_game_state.restore_memento.assert_called_once_with(old_state)

    # Failure
    def test_use_item_command_undo_before_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item has not been used!"):
            test_command.undo()

        # Verify state was not restored
        test_game_state.restore_memento.assert_not_called()

    # Success
    def test_use_item_command_redo_after_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Reset method call history
        test_game_state.create_memento.reset_mock()
        test_game_state.use_consumable.reset_mock()

        # Redo Command
        test_command.redo()

        # Verify command was executed again
        test_game_state.create_memento.assert_called_once_with()
        test_game_state.use_consumable.assert_called_once_with(1, "Small Health Potion")

    # Failure
    def test_use_item_command_redo_before_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item has already been used!"):
            test_command.redo()

        # Verify consumable was not used a second time
        test_game_state.use_consumable.assert_called_once_with(1, "Small Health Potion")

    # Success
    def test_use_item_command_get_name(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(test_game_state, 1, "Small Health Potion")

        # Verify command name
        self.assertEqual(test_command.get_name(), "Use")

    # Success
    def test_tick_command_execute_with_entities(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Mock entity updates
        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Verify entity updates
        test_game_state.create_memento.assert_called_once_with()
        test_game_state.entities_exists.assert_called_once_with()
        test_game_state.process_tick_for_all_entities.assert_called_once_with()

        # Verify game state updates
        test_game_state.mark_as_unsaved.assert_called_once_with()
        test_game_state.advance_turn.assert_called_once_with()

    # Success
    def test_tick_command_execute_without_entities(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entity existence
        test_game_state.entities_exists.return_value = False

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Verify entities were not updated
        test_game_state.process_tick_for_all_entities.assert_not_called()
        test_game_state.remove_entity_from_game.assert_not_called()

        # Verify turn still advances
        test_game_state.mark_as_unsaved.assert_called_once_with()
        test_game_state.advance_turn.assert_called_once_with()

    # Success
    def test_tick_command_execute_removes_entities(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entities to remove
        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = [1, 2, 3]

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Verify entities were removed
        test_game_state.remove_entity_from_game.assert_any_call(1)
        test_game_state.remove_entity_from_game.assert_any_call(2)
        test_game_state.remove_entity_from_game.assert_any_call(3)
        self.assertEqual(test_game_state.remove_entity_from_game.call_count, 3)

        # Verify turn advances
        test_game_state.advance_turn.assert_called_once_with()

    # Success
    def test_tick_command_execute_with_no_entities_to_remove(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entity updates
        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Verify no entities were removed
        test_game_state.remove_entity_from_game.assert_not_called()

        # Verify turn advances
        test_game_state.advance_turn.assert_called_once_with()

    # Success
    def test_tick_command_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Mock entity updates
        test_game_state.entities_exists.return_value = False

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Reset restore method call history
        test_game_state.restore_memento.reset_mock()

        # Undo Command
        test_command.undo()

        # Verify game state was restored
        test_game_state.restore_memento.assert_called_once_with(old_state)

    # Failure
    def test_tick_command_undo_before_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Tick has not been executed!"):
            test_command.undo()

        # Verify state was not restored
        test_game_state.restore_memento.assert_not_called()

    # Success
    def test_tick_command_redo_after_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entity updates
        test_game_state.entities_exists.return_value = False

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Reset call history
        test_game_state.create_memento.reset_mock()
        test_game_state.advance_turn.reset_mock()
        test_game_state.mark_as_unsaved.reset_mock()

        # Redo Command
        test_command.redo()

        # Verify tick was executed again
        test_game_state.create_memento.assert_called_once_with()
        test_game_state.advance_turn.assert_called_once_with()
        test_game_state.mark_as_unsaved.assert_called_once_with()

    # Failure
    def test_tick_command_redo_before_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entity updates
        test_game_state.entities_exists.return_value = False

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Execute Command
        test_command.execute()

        # Reset advance turn call history
        test_game_state.advance_turn.reset_mock()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Tick has already been executed!"):
            test_command.redo()

        # Verify turn did not advance again
        test_game_state.advance_turn.assert_not_called()

    # Success
    def test_tick_command_get_name(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Tick Command
        test_command = TickCommand(test_game_state)

        # Verify command name
        self.assertEqual(test_command.get_name(), "Tick")

    # Set Up
    # Creates a mock GameState and InitMapCommand for testing
    # Params: None
    # Returns: None
    def setUp(self):
        # Create mock game state
        self.game_state = MagicMock()

        # Mock map does not exist
        self.game_state.is_map_created.return_value = False

        # Create command
        self.command = InitCommand(self.game_state, 25, 25)

    # Execute Tests

    # Success
    # Test initializing a map when one does not already exist
    def test_execute_creates_map_when_map_does_not_exist(self):
        # Execute command
        self.command.execute()

        # Test grid was created
        self.game_state.create_grid.assert_called_once_with(25, 25)

        # Test map was checked
        self.game_state.is_map_created.assert_called_once()

        # Test map was not reset
        self.game_state.reset_map.assert_not_called()

    # Success
    # Test resetting an existing map before creating a new map
    def test_execute_resets_existing_map_before_creating_new_map(self):
        # Mock map already exists
        self.game_state.is_map_created.return_value = True

        # Execute command
        self.command.execute()

        # Test map was reset
        self.game_state.reset_map.assert_called_once()

        # Test new grid was created
        self.game_state.create_grid.assert_called_once_with(25, 25)

    # Success
    # Test creating a map with string dimensions
    def test_execute_converts_dimensions_to_integers(self):
        # Create command with string dimensions
        command = InitCommand(self.game_state, "10", "15")

        # Execute command
        command.execute()

        # Test grid was created with integer dimensions
        self.game_state.create_grid.assert_called_once_with(10, 15)

    # Undo Tests

    # Success
    # Test undoing map initialization restores previous game state
    def test_undo_restores_previous_game_state(self):
        # Execute command
        self.command.execute()

        # Undo command
        self.command.undo()

        # Test previous state was restored
        self.game_state.restore_memento.assert_called_once_with(
            self.game_state.create_memento.return_value
        )

    # Failure
    # Test undoing map initialization before executing command
    def test_undo_before_execute_raises_error(self):
        # Test undo raises ValueError
        with self.assertRaisesRegex(ValueError, "Map has not been initialized!"):
            self.command.undo()

        # Test game state was not restored
        self.game_state.restore_memento.assert_not_called()

    # Success
    # Test undoing map initialization only restores state once
    def test_undo_can_only_be_performed_once(self):
        # Execute command
        self.command.execute()

        # Undo command
        self.command.undo()

        # Attempt to undo again
        with self.assertRaisesRegex(ValueError, "Map has not been initialized!"):
            self.command.undo()

        # Test state was restored only once
        self.game_state.restore_memento.assert_called_once()

    # Redo Tests

    # Success
    # Test redoing map initialization after undo
    def test_redo_after_undo_reinitializes_map(self):
        # Execute command
        self.command.execute()

        # Undo command
        self.command.undo()

        # Reset mock call history
        self.game_state.create_grid.reset_mock()

        # Redo command
        self.command.redo()

        # Test grid was recreated
        self.game_state.create_grid.assert_called_once_with(25, 25)

    # Failure
    # Test redoing map initialization before undoing it
    def test_redo_before_undo_raises_error(self):
        # Execute command
        self.command.execute()

        # Test redo raises ValueError
        with self.assertRaisesRegex(ValueError, "Map has already been initialized!"):
            self.command.redo()

        # Test grid was only created once
        self.game_state.create_grid.assert_called_once_with(25, 25)

    # Success
    # Test getting the command name
    def test_get_name_returns_init_map(self):
        # Get command name
        name = self.command.get_name()

        # Test command name
        self.assertEqual(name, "Init Map")

    # Tests SaveCommand execute saves the current game state
    def test_save_command_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Verify game state was saved
        test_game_state_manager.save_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests SaveCommand undo deletes the created save file
    def test_save_command_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify save file was deleted
        test_game_state_manager.delete_save.assert_called_once_with("test_save")

    # Tests SaveCommand undo raises an error before execution
    def test_save_command_undo_before_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been saved!"):
            test_command.undo()

        # Verify save file was not deleted
        test_game_state_manager.delete_save.assert_not_called()

    # Tests SaveCommand undo cannot be performed twice
    def test_save_command_undo_twice(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been saved!"):
            test_command.undo()

        # Verify save file was deleted only once
        test_game_state_manager.delete_save.assert_called_once_with("test_save")

    # Tests SaveCommand redo saves the game again after undo
    def test_save_command_redo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Reset save game call history
        test_game_state_manager.save_game.reset_mock()

        # Redo Command
        test_command.redo()

        # Verify game was saved again
        test_game_state_manager.save_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests SaveCommand redo raises an error while already executed
    def test_save_command_redo_before_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has already been saved!"):
            test_command.redo()

        # Verify game was only saved once
        test_game_state_manager.save_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests SaveCommand execution failure prevents undo
    def test_save_command_execute_failure(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Simulate save failure
        test_game_state_manager.save_game.side_effect = OSError("Unable to save game!")

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify execution raises an error
        with self.assertRaises(OSError):
            test_command.execute()

        # Verify undo is not allowed
        with self.assertRaisesRegex(ValueError, "Game has not been saved!"):
            test_command.undo()

        # Verify save file was not deleted
        test_game_state_manager.delete_save.assert_not_called()

    # Tests SaveCommand get_name returns the command name
    def test_save_command_get_name(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify command name
        self.assertEqual(test_command.get_name(), "Save")

    # Tests LoadCommand execute loads the saved game state
    def test_load_command_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Verify current game state was saved
        test_game_state.create_memento.assert_called_once()

        # Verify saved game was loaded
        test_game_state_manager.load_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests LoadCommand undo restores the previous game state
    def test_load_command_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify previous game state was restored
        test_game_state.restore_memento.assert_called_once_with(test_memento)

    # Tests LoadCommand undo raises an error before execution
    def test_load_command_undo_before_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify game state was not restored
        test_game_state.restore_memento.assert_not_called()

    # Tests LoadCommand undo cannot be performed twice
    def test_load_command_undo_twice(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify previous game state was restored only once
        test_game_state.restore_memento.assert_called_once_with(test_memento)

    # Tests LoadCommand redo loads the saved game again after undo
    def test_load_command_redo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Reset load game call history
        test_game_state_manager.load_game.reset_mock()

        # Redo Command
        test_command.redo()

        # Verify saved game was loaded again
        test_game_state_manager.load_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests LoadCommand redo raises an error while already executed
    def test_load_command_redo_before_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has already been loaded!"):
            test_command.redo()

        # Verify game was only loaded once
        test_game_state_manager.load_game.assert_called_once_with(
            test_game_state, "test_save"
        )

    # Tests LoadCommand execution failure prevents undo
    def test_load_command_execute_failure(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Simulate load failure
        test_game_state_manager.load_game.side_effect = OSError("Unable to load game!")

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify execution raises an error
        with self.assertRaises(OSError):
            test_command.execute()

        # Verify undo is not allowed
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify game state was not restored
        test_game_state.restore_memento.assert_not_called()

    # Tests LoadCommand get_name returns the command name
    def test_load_command_get_name(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()

        # Create Load Command
        test_command = LoadCommand(
            test_game_state, test_game_state_manager, "test_save"
        )

        # Verify command name
        self.assertEqual(test_command.get_name(), "Load")

    # Test Inspect Command Initialization
    # Verify that InspectCommand stores the entity ID and command name
    # Returns: None
    def test_inspect_command_initialization(self):
        test_game_state = MagicMock()

        test_command = InspectCommand(test_game_state, "1")

        self.assertEqual(test_command.get_name(), "Inspect")

        # Verify that initialization does not retrieve the entity
        test_game_state.get_entity_info_from_list.assert_not_called()

    # Test Inspect Command With Invalid Entity
    # Verify that InspectCommand raises an error if the entity does not exist
    # Returns: None
    def test_inspect_command_invalid_entity(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = None

        test_command = InspectCommand(test_game_state, 999)

        with self.assertRaises(ValueError):
            test_command.execute()

        test_game_state.get_entity_info_from_list.assert_called_once_with(999)

    # Test Inspect Command Execute
    # Verify that executing the command displays the entity information
    # Returns: None
    def test_inspect_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            id=1,
            e_type="warrior",
            position=(2, 3),
            health=120,
            max_health=120,
            attack=15,
            defence=10,
            speed=5,
            active_modifiers=("strength",),
        )

        test_command = InspectCommand(test_game_state, 1)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Id: 1", output)
        self.assertIn("Type: warrior", output)
        self.assertIn("Position: (2, 3)", output)
        self.assertIn("Health: 120/120", output)
        self.assertIn("Attack: 15", output)
        self.assertIn("Defence: 10", output)
        self.assertIn("Speed: 5", output)
        self.assertIn("Active Modifiers: ('strength',)", output)

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inspect Command Undo
    # Verify that undo does not modify the game state
    # Returns: None
    def test_inspect_command_undo(self):
        test_game_state = MagicMock()

        test_command = InspectCommand(test_game_state, 1)

        test_command.undo()

        test_game_state.assert_not_called()

    # Test Inspect Command Execute And Undo
    # Verify that executing and undoing an inspect command does not modify game state
    # Returns: None
    def test_inspect_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            id=1,
            e_type="warrior",
            position=(2, 3),
            health=120,
            max_health=120,
            attack=15,
            defence=10,
            speed=5,
            active_modifiers=(),
        )

        test_command = InspectCommand(test_game_state, 1)

        with patch("sys.stdout", new_callable=StringIO):
            test_command.execute()
            test_command.undo()

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inspect Command Redo
    # Verify that redo displays the entity information again
    # Returns: None
    def test_inspect_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            id=1,
            e_type="warrior",
            position=(2, 3),
            health=120,
            max_health=120,
            attack=15,
            defence=10,
            speed=5,
            active_modifiers=(),
        )

        test_command = InspectCommand(test_game_state, 1)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.redo()

        output = mock_stdout.getvalue()

        self.assertIn("Id: 1", output)
        self.assertIn("Health: 120/120", output)

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inspect Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_inspect_command_get_name(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            id=1,
            e_type="warrior",
            position=(2, 3),
            health=120,
            max_health=120,
            attack=15,
            defence=10,
            speed=5,
            active_modifiers=(),
        )

        test_command = InspectCommand(test_game_state, 1)

        self.assertEqual(test_command.get_name(), "Inspect")

    # Test Inspect Command Is Not Undoable
    # Verify that InspectCommand cannot be undone
    # Returns: None
    def test_inspect_command_not_undoable(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            id=1,
            e_type="warrior",
            position=(2, 3),
            health=120,
            max_health=120,
            attack=15,
            defence=10,
            speed=5,
            active_modifiers=(),
        )

        test_command = InspectCommand(test_game_state, 1)

        self.assertFalse(test_command.is_undoable())

    # Test Inventory Command Initialization
    # Verify that InventoryCommand stores the entity ID and command name
    # Returns: None
    def test_inventory_command_initialization(self):
        test_game_state = MagicMock()

        test_command = InventoryCommand(test_game_state, "1")

        self.assertEqual(test_command.get_name(), "Inventory")

        # Verify that initialization does not retrieve the entity
        test_game_state.get_entity_info_from_list.assert_not_called()

    # Test Inventory Command With Invalid Entity
    # Verify that InventoryCommand raises an error if the entity does not exist
    # Returns: None
    def test_inventory_command_invalid_entity(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = None

        test_command = InventoryCommand(test_game_state, 999)

        with self.assertRaisesRegex(ValueError, "Player entity does not exist!"):
            test_command.execute()

        test_game_state.get_entity_info_from_list.assert_called_once_with(999)

    # Test Inventory Command With Dead Entity
    # Verify that InventoryCommand raises an error if the entity is dead
    # Returns: None
    def test_inventory_command_dead_entity(self):
        test_game_state = MagicMock()
        test_entity = MagicMock()
        test_entity.is_alive.return_value = False

        test_game_state.get_entity_from_list.return_value = test_entity
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            inventory=(None, None, None), backpack=()
        )

        test_command = InventoryCommand(test_game_state, 1)

        with self.assertRaisesRegex(ValueError, "Player entity is dead!"):
            test_command.execute()

        test_game_state.get_entity_from_list.assert_called_once_with(1)
        test_entity.is_alive.assert_called_once()

    # Test Inventory Command Execute
    # Verify that executing the command displays the entity inventory
    # Returns: None
    def test_inventory_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            health=120,
            inventory=("IronSword", "LeatherTunic", "RingOfHaste"),
            backpack=("HealthPotion", "IronShield"),
        )

        test_command = InventoryCommand(test_game_state, 1)

        with patch.object(Entity, "is_alive_from_info", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Weapon: IronSword", output)
        self.assertIn("Armor: LeatherTunic", output)
        self.assertIn("Accessory: RingOfHaste", output)
        self.assertIn("Backpack Slots:", output)
        self.assertIn("1. HealthPotion", output)
        self.assertIn("2. IronShield", output)

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inventory Command With Empty Slots
    # Verify that empty equipment and backpack slots are displayed correctly
    # Returns: None
    def test_inventory_command_empty_slots(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            health=120, inventory=(None, None, None), backpack=()
        )

        test_command = InventoryCommand(test_game_state, 1)

        with patch.object(Entity, "is_alive_from_info", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Weapon: None", output)
        self.assertIn("Armor: None", output)
        self.assertIn("Accessory: None", output)
        self.assertIn("Backpack Slots:", output)

        # Verify all backpack slots are displayed as empty
        for index in range(Entity.BACKPACK_SIZE):
            self.assertIn(f"{index + 1}. Empty", output)

    # Test Inventory Command Undo
    # Verify that undo does not modify the game state
    # Returns: None
    def test_inventory_command_undo(self):
        test_game_state = MagicMock()

        test_command = InventoryCommand(test_game_state, 1)

        test_command.undo()

        test_game_state.assert_not_called()

    # Test Inventory Command Execute And Undo
    # Verify that executing and undoing inventory does not modify game state
    # Returns: None
    def test_inventory_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            health=120, inventory=(None, None, None), backpack=()
        )

        test_command = InventoryCommand(test_game_state, 1)

        with patch.object(Entity, "is_alive_from_info", return_value=True):
            with patch("sys.stdout", new_callable=StringIO):
                test_command.execute()
                test_command.undo()

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inventory Command Redo
    # Verify that redo displays the inventory again
    # Returns: None
    def test_inventory_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            health=120,
            inventory=("IronSword", "LeatherTunic", "RingOfHaste"),
            backpack=("HealthPotion",),
        )

        test_command = InventoryCommand(test_game_state, 1)

        with patch.object(Entity, "is_alive_from_info", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.redo()

        output = mock_stdout.getvalue()

        self.assertIn("Weapon: IronSword", output)
        self.assertIn("Armor: LeatherTunic", output)
        self.assertIn("Accessory: RingOfHaste", output)
        self.assertIn("1. HealthPotion", output)

        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Test Inventory Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_inventory_command_get_name(self):
        test_game_state = MagicMock()

        test_command = InventoryCommand(test_game_state, 1)

        self.assertEqual(test_command.get_name(), "Inventory")

    # Test Inventory Command Is Not Undoable
    # Verify that InventoryCommand cannot be undone
    # Returns: None
    def test_inventory_command_not_undoable(self):
        test_game_state = MagicMock()

        test_command = InventoryCommand(test_game_state, 1)

        self.assertFalse(test_command.is_undoable())

    # Test Tile Command Initialization
    # Verify that TileCommand stores the coordinates and command name
    # Returns: None
    def test_tile_command_initialization(self):
        test_game_state = MagicMock()

        test_command = TileCommand(test_game_state, "2", "3")

        self.assertEqual(test_command.get_name(), "Tile")

        test_game_state.is_map_created.assert_not_called()

    # Test Tile Command With Missing Map
    # Verify that TileCommand raises an error if the map does not exist
    # Returns: None
    def test_tile_command_invalid_map(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = False

        test_command = TileCommand(test_game_state, 2, 3)

        with self.assertRaisesRegex(ValueError, "Map does not exist!"):
            test_command.execute()

        test_game_state.is_map_created.assert_called_once()

    # Test Tile Command With Invalid Coordinates
    # Verify that TileCommand raises an error if coordinates are not integers
    # Returns: None
    def test_tile_command_invalid_coordinates(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True

        test_command = TileCommand(test_game_state, "abc", "xyz")

        with patch("command.are_valid_ints", return_value=False):
            with self.assertRaisesRegex(ValueError, "x and y are not valid integers!"):
                test_command.execute()

        test_game_state.is_valid_grid_position.assert_not_called()

    # Test Tile Command With Out Of Bounds Coordinates
    # Verify that TileCommand raises an error if coordinates exceed grid bounds
    # Returns: None
    def test_tile_command_out_of_bounds(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = False

        test_command = TileCommand(test_game_state, "99", "99")

        with patch("command.are_valid_ints", return_value=True):
            with self.assertRaisesRegex(
                ValueError, "x and y exceed current grid bounds!"
            ):
                test_command.execute()

        test_game_state.is_valid_grid_position.assert_called_once_with("99", "99")

    # Test Tile Command With Missing Tile
    # Verify that TileCommand raises an error if no tile exists at the position
    # Returns: None
    def test_tile_command_missing_tile(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = True
        test_game_state.get_game_tile_info.return_value = None

        test_command = TileCommand(test_game_state, "2", "3")

        with patch("command.are_valid_ints", return_value=True):
            with self.assertRaisesRegex(ValueError, "No tile exists at this position!"):
                with patch("sys.stdout", new_callable=StringIO):
                    test_command.execute()

        test_game_state.get_game_tile_info.assert_called_once_with(2, 3)

    # Test Tile Command Execute
    # Verify that executing the command displays the tile information
    # Returns: None
    def test_tile_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = True
        test_game_state.get_game_tile_info.return_value = SimpleNamespace(
            tile_type="floor", passable=True, occupants=(1,)
        )

        test_command = TileCommand(test_game_state, "2", "3")

        with patch("command.are_valid_ints", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Coordinate: 2, 3", output)
        self.assertIn("Type: Floor", output)
        self.assertIn("Passable: True", output)
        self.assertIn("Occupants: 1", output)

        test_game_state.get_game_tile_info.assert_called_once_with(2, 3)

    # Test Tile Command Shallow Water
    # Verify that ShallowWater is capitalized correctly
    # Returns: None
    def test_tile_command_shallow_water(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = True
        test_game_state.get_game_tile_info.return_value = SimpleNamespace(
            tile_type="shallowwater", passable=True, occupants=()
        )

        test_command = TileCommand(test_game_state, 2, 3)

        with patch("command.are_valid_ints", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Type: ShallowWater", output)

    # Test Tile Command With No Occupants
    # Verify that TileCommand displays None when a tile has no occupants
    # Returns: None
    def test_tile_command_no_occupants(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = True
        test_game_state.get_game_tile_info.return_value = SimpleNamespace(
            tile_type="floor", passable=True, occupants=()
        )

        test_command = TileCommand(test_game_state, 2, 3)

        with patch("command.are_valid_ints", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("Occupants: None", output)

    # Test Tile Command Undo
    # Verify that undo does not modify the game state
    # Returns: None
    def test_tile_command_undo(self):
        test_game_state = MagicMock()

        test_command = TileCommand(test_game_state, 2, 3)

        test_command.undo()

        test_game_state.assert_not_called()

    # Test Tile Command Redo
    # Verify that redo displays the tile information again
    # Returns: None
    def test_tile_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.is_map_created.return_value = True
        test_game_state.is_valid_grid_position.return_value = True
        test_game_state.get_game_tile_info.return_value = SimpleNamespace(
            tile_type="wall", passable=False, occupants=()
        )

        test_command = TileCommand(test_game_state, 2, 3)

        with patch("command.are_valid_ints", return_value=True):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                test_command.redo()

        output = mock_stdout.getvalue()

        self.assertIn("Coordinate: 2, 3", output)
        self.assertIn("Type: Wall", output)
        self.assertIn("Passable: False", output)

        test_game_state.get_game_tile_info.assert_called_once_with(2, 3)

    # Test Tile Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_tile_command_get_name(self):
        test_game_state = MagicMock()

        test_command = TileCommand(test_game_state, 2, 3)

        self.assertEqual(test_command.get_name(), "Tile")

    # Test Tile Command Is Not Undoable
    # Verify that TileCommand cannot be undone
    # Returns: None
    def test_tile_command_not_undoable(self):
        test_game_state = MagicMock()

        test_command = TileCommand(test_game_state, 2, 3)

        self.assertFalse(test_command.is_undoable())

    # Test State Info Command Initialization
    # Verify that StateInfoCommand stores the command name
    # Returns: None
    def test_state_info_command_initialization(self):
        test_game_state = MagicMock()

        test_command = StateInfoCommand(test_game_state)

        self.assertEqual(test_command.get_name(), "State-Info")

        test_game_state.game_state_is_active.assert_not_called()

    # Test State Info Command With Inactive Game State
    # Verify that StateInfoCommand raises an error if the game state is not active
    # Returns: None
    def test_state_info_command_inactive_game_state(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = False

        test_command = StateInfoCommand(test_game_state)

        with self.assertRaisesRegex(ValueError, "Game State is not initialized!"):
            test_command.execute()

        test_game_state.game_state_is_active.assert_called_once()

        test_game_state.get_game_state_info.assert_not_called()

    # Test State Info Command Execute
    # Verify that executing the command displays the current game state information
    # Returns: None
    def test_state_info_command_execute(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = True
        test_game_state.get_game_state_info.return_value = (5, 3, True)

        test_command = StateInfoCommand(test_game_state)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("ok: turn 5, entities: 3, saved: true", output)

        test_game_state.game_state_is_active.assert_called_once()
        test_game_state.get_game_state_info.assert_called_once()

    # Test State Info Command With Unsaved Game State
    # Verify that the saved status displays false when the game is unsaved
    # Returns: None
    def test_state_info_command_unsaved_game_state(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = True
        test_game_state.get_game_state_info.return_value = (2, 4, False)

        test_command = StateInfoCommand(test_game_state)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.execute()

        output = mock_stdout.getvalue()

        self.assertIn("ok: turn 2, entities: 4, saved: false", output)

    # Test State Info Command With Invalid Game State Information
    # Verify that StateInfoCommand propagates errors retrieving game state information
    # Returns: None
    def test_state_info_command_invalid_game_state_info(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = True
        test_game_state.get_game_state_info.side_effect = ValueError("Invalid state!")

        test_command = StateInfoCommand(test_game_state)

        with self.assertRaisesRegex(ValueError, "Invalid state!"):
            test_command.execute()

    # Test State Info Command Undo
    # Verify that undo does not modify the game state
    # Returns: None
    def test_state_info_command_undo(self):
        test_game_state = MagicMock()

        test_command = StateInfoCommand(test_game_state)

        test_command.undo()

        test_game_state.assert_not_called()

    # Test State Info Command Execute And Undo
    # Verify that executing and undoing state-info does not modify game state
    # Returns: None
    def test_state_info_command_execute_and_undo(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = True
        test_game_state.get_game_state_info.return_value = (5, 3, True)

        test_command = StateInfoCommand(test_game_state)

        with patch("sys.stdout", new_callable=StringIO):
            test_command.execute()
            test_command.undo()

        test_game_state.game_state_is_active.assert_called_once()
        test_game_state.get_game_state_info.assert_called_once()

    # Test State Info Command Redo
    # Verify that redo displays the current game state information again
    # Returns: None
    def test_state_info_command_redo(self):
        test_game_state = MagicMock()
        test_game_state.game_state_is_active.return_value = True
        test_game_state.get_game_state_info.return_value = (5, 3, True)

        test_command = StateInfoCommand(test_game_state)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.redo()

        output = mock_stdout.getvalue()

        self.assertIn("ok: turn 5, entities: 3, saved: true", output)

        test_game_state.game_state_is_active.assert_called_once()
        test_game_state.get_game_state_info.assert_called_once()

    # Test State Info Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_state_info_command_get_name(self):
        test_game_state = MagicMock()

        test_command = StateInfoCommand(test_game_state)

        self.assertEqual(test_command.get_name(), "State-Info")

    # Test State Info Command Is Not Undoable
    # Verify that StateInfoCommand cannot be undone
    # Returns: None
    def test_state_info_command_not_undoable(self):
        test_game_state = MagicMock()

        test_command = StateInfoCommand(test_game_state)

        self.assertFalse(test_command.is_undoable())

    def test_history_command_initialization(self):
        test_command_manager = MagicMock()

        test_command = HistoryCommand(test_command_manager)

        self.assertEqual(test_command.get_name(), "History")
        test_command_manager.get_history_info.assert_not_called()

    # Test History Command Execution
    # Verify that HistoryCommand displays the undo and redo counts
    # Returns: None
    def test_history_command_execute(self):
        test_command_manager = MagicMock()
        test_command_manager.get_history_info.return_value = (3, 2)

        test_command = HistoryCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: undo_stack:3, redo_stack:2\n")
        test_command_manager.get_history_info.assert_called_once()

    # Test History Command Empty History
    # Verify that HistoryCommand displays zero when both histories are empty
    # Returns: None
    def test_history_command_empty_history(self):
        test_command_manager = MagicMock()
        test_command_manager.get_history_info.return_value = (0, 0)

        test_command = HistoryCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: undo_stack:0, redo_stack:0\n")

    # Test History Command Undo
    # Verify that undo does not change the history
    # Returns: None
    def test_history_command_undo(self):
        test_command_manager = MagicMock()
        test_command = HistoryCommand(test_command_manager)

        test_command.undo()

        test_command_manager.get_history_info.assert_not_called()

    # Test History Command Redo
    # Verify that redo displays the history information again
    # Returns: None
    def test_history_command_redo(self):
        test_command_manager = MagicMock()
        test_command_manager.get_history_info.return_value = (2, 1)

        test_command = HistoryCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            test_command.redo()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: undo_stack:2, redo_stack:1\n")
        test_command_manager.get_history_info.assert_called_once()

    # Test History Command Name
    # Verify that the command returns its correct name
    # Returns: None
    def test_history_command_get_name(self):
        test_command = HistoryCommand(MagicMock())

        self.assertEqual(test_command.get_name(), "History")

    # Test History Command Is Not Undoable
    # Verify that HistoryCommand cannot be added to undo history
    # Returns: None
    def test_history_command_is_not_undoable(self):
        test_command = HistoryCommand(MagicMock())

        self.assertFalse(test_command.is_undoable())

    def test_undo_command_initialization(self):
        test_command_manager = MagicMock()

        test_command = UndoCommand(test_command_manager)

        self.assertEqual(test_command.get_name(), "Undo")
        test_command_manager.undo_last_command.assert_not_called()

    # Test Undo Command Execute
    # Verify that UndoCommand undoes the last command and displays its name
    # Returns: None
    def test_undo_command_execute(self):
        test_command_manager = MagicMock()
        test_command = MagicMock()
        test_command.get_name.return_value = "Move"

        test_command_manager.undo_last_command.return_value = (True, test_command)

        undo_command = UndoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            undo_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: undone Move!\n")
        test_command_manager.undo_last_command.assert_called_once()
        test_command.get_name.assert_called_once()

    # Test Undo Command Empty History
    # Verify that UndoCommand displays an error when there are no commands to undo
    # Returns: None
    def test_undo_command_empty_history(self):
        test_command_manager = MagicMock()
        test_command_manager.undo_last_command.return_value = (False, None)

        undo_command = UndoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            undo_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "error: undo_failed - No commands to undo!\n")
        test_command_manager.undo_last_command.assert_called_once()

    # Test Undo Command Undo
    # Verify that undoing an UndoCommand does not modify command history
    # Returns: None
    def test_undo_command_undo(self):
        test_command_manager = MagicMock()

        undo_command = UndoCommand(test_command_manager)

        undo_command.undo()

        test_command_manager.undo_last_command.assert_not_called()

    # Test Undo Command Redo
    # Verify that redo repeats the undo operation
    # Returns: None
    def test_undo_command_redo(self):
        test_command_manager = MagicMock()
        test_command = MagicMock()
        test_command.get_name.return_value = "Move"

        test_command_manager.undo_last_command.return_value = (True, test_command)

        undo_command = UndoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            undo_command.redo()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: undone Move!\n")
        test_command_manager.undo_last_command.assert_called_once()

    # Test Undo Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_undo_command_get_name(self):
        test_command_manager = MagicMock()

        undo_command = UndoCommand(test_command_manager)

        self.assertEqual(undo_command.get_name(), "Undo")

    # Test Undo Command Is Not Undoable
    # Verify that UndoCommand cannot be added to undo history
    # Returns: None
    def test_undo_command_not_undoable(self):
        test_command_manager = MagicMock()

        undo_command = UndoCommand(test_command_manager)

        self.assertFalse(undo_command.is_undoable())

    def test_redo_command_initialization(self):
        test_command_manager = MagicMock()

        test_command = RedoCommand(test_command_manager)

        self.assertEqual(test_command.get_name(), "Redo")
        test_command_manager.redo_last_command.assert_not_called()

    # Test Redo Command Execute
    # Verify that RedoCommand re-executes the last undone command and displays its name
    # Returns: None
    def test_redo_command_execute(self):
        test_command_manager = MagicMock()
        test_command = MagicMock()
        test_command.get_name.return_value = "Move"

        test_command_manager.redo_last_command.return_value = (True, test_command)

        redo_command = RedoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            redo_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: redone Move!\n")
        test_command_manager.redo_last_command.assert_called_once()
        test_command.get_name.assert_called_once()

    # Test Redo Command Empty History
    # Verify that RedoCommand displays an error when there are no commands to redo
    # Returns: None
    def test_redo_command_empty_history(self):
        test_command_manager = MagicMock()
        test_command_manager.redo_last_command.return_value = (False, None)

        redo_command = RedoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            redo_command.execute()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "error: redo_failed - No commands to redo!\n")
        test_command_manager.redo_last_command.assert_called_once()

    # Test Redo Command Undo
    # Verify that undoing a RedoCommand does not modify command history
    # Returns: None
    def test_redo_command_undo(self):
        test_command_manager = MagicMock()

        redo_command = RedoCommand(test_command_manager)

        redo_command.undo()

        test_command_manager.redo_last_command.assert_not_called()

    # Test Redo Command Redo
    # Verify that redo repeats the redo operation
    # Returns: None
    def test_redo_command_redo(self):
        test_command_manager = MagicMock()
        test_command = MagicMock()
        test_command.get_name.return_value = "Move"

        test_command_manager.redo_last_command.return_value = (True, test_command)

        redo_command = RedoCommand(test_command_manager)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            redo_command.redo()

        output = mock_stdout.getvalue()

        self.assertEqual(output, "ok: redone Move!\n")
        test_command_manager.redo_last_command.assert_called_once()

    # Test Redo Command Get Name
    # Verify that get_name returns the command name
    # Returns: None
    def test_redo_command_get_name(self):
        test_command_manager = MagicMock()

        redo_command = RedoCommand(test_command_manager)

        self.assertEqual(redo_command.get_name(), "Redo")

    # Test Redo Command Is Not Undoable
    # Verify that RedoCommand cannot be added to undo history
    # Returns: None
    def test_redo_command_not_undoable(self):
        test_command_manager = MagicMock()

        redo_command = RedoCommand(test_command_manager)

        self.assertFalse(redo_command.is_undoable())


if __name__ == "__main__":
    unittest.main()
