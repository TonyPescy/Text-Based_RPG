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


# Test Init Map Command
# Tests all methods in InitMapCommand
class TestInitMapCommand(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
