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
from unittest.mock import MagicMock, Mock, patch
from types import SimpleNamespace
from entity import Entity
from io import StringIO
from entity_state import FleeingState, AttackingState, DefendingState, RagingState
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
    StateCommand,
    ForceStateCommand,
    SimulateCommand,
)


# Test Command
class TestCommand(unittest.TestCase):

    def setUp(self):
        self.game_state = MagicMock()
        self.game_state.is_map_created.return_value = False

        self.command_manager = MagicMock()
        self.game_state_manager = MagicMock()

        # Shared fixtures for all command tests.
        self.game = self.game_state
        self.manager = self.command_manager
        self.state_manager = self.game_state_manager
        self.entity = MagicMock()
        self.entity.get_entity_state_name.return_value = "Defending"
        self.entity.create_state_manager_memento.return_value = (
            Entity.StateManagerMemento("Defending")
        )
        self.game_state.get_entity_from_list.return_value = self.entity

        self.command = InitCommand(
            self.game_state,
            25,
            25,
            self.command_manager,
            self.game_state_manager,
        )

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

        test_game_state.undo_cast.assert_called_once_with(1, 2, 100, 70)

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
        test_game_state.undo_cast.assert_called_once_with(1, 2, 80, 50)

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
        test_game_state.undo_cast.assert_called_once_with(1, 2, 100, 0)

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
        test_game_state.undo_cast.assert_called_once_with(1, 2, 100, 50)

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
        test_game_state.undo_cast.assert_called_once_with(1, 2, 100, 50)

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
        game_state.remove_item_from_backpack_based_on_info.assert_called_once_with(
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
        game_state.remove_item_from_backpack_based_on_info.assert_not_called()

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
        game_state.remove_item_from_backpack_based_on_info.assert_called_once_with(
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
        game_state.remove_item_from_backpack_based_on_info.assert_not_called()

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
        game_state.remove_item_from_backpack_based_on_info_based_on_info.assert_not_called()

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
        game_state.remove_item_from_backpack_based_on_info_based_on_info.reset_mock()

        # Redo command
        command.redo()

        # Check item was added to tile again
        game_state.add_item_to_tile.assert_called_once_with(1, 2, "SmallHealthPotion")

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
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

        # Execute Command
        test_command.execute()

        # Verify results
        test_game_state.create_memento.assert_called_once_with(self.command_manager)
        test_game_state.use_consumable.assert_called_once_with(1, "Small Health Potion")

    # Success
    def test_use_item_command_converts_entity_id_to_integer(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(
            test_game_state,
            "1",
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

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
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

        # Execute Command
        test_command.execute()

        # Reset restore method call history
        test_game_state.restore.reset_mock()

        # Undo Command
        test_command.undo()

        # Verify state was restored
        test_game_state.restore.assert_called_once_with(
            old_state, self.command_manager, self.game_state_manager
        )

    # Failure
    def test_use_item_command_undo_before_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Item has not been used!"):
            test_command.undo()

        # Verify state was not restored
        test_game_state.restore.assert_not_called()

    # Success
    def test_use_item_command_redo_after_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        old_state = MagicMock()
        test_game_state.create_memento.return_value = old_state

        # Create Use Item Command
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

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
        test_game_state.create_memento.assert_called_once_with(self.command_manager)
        test_game_state.use_consumable.assert_called_once_with(1, "Small Health Potion")

    # Failure
    def test_use_item_command_redo_before_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Create Use Item Command
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

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
        test_command = UseItemCommand(
            test_game_state,
            1,
            "Small Health Potion",
            self.command_manager,
            self.game_state_manager,
        )

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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        # Execute Command
        test_command.execute()

        # Verify AI behavior was processed
        test_game_state.process_ai_for_all_entities.assert_called_once_with()

        # Verify entity updates
        test_game_state.create_memento.assert_called_once_with(self.command_manager)
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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        # Execute Command
        test_command.execute()

        # Verify AI was not processed
        test_game_state.process_ai_for_all_entities.assert_not_called()

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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        # Execute Command
        test_command.execute()

        # Reset restore method call history
        test_game_state.restore.reset_mock()

        # Undo Command
        test_command.undo()

        # Verify game state was restored
        test_game_state.restore.assert_called_once_with(
            old_state, self.command_manager, self.game_state_manager
        )

    # Failure
    def test_tick_command_undo_before_execute(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Tick Command
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Tick has not been executed!"):
            test_command.undo()

        # Verify state was not restored
        test_game_state.restore.assert_not_called()

    # Success
    def test_tick_command_redo_after_undo(self):
        # Create GameState
        test_game_state = MagicMock()

        # Create Memento
        test_game_state.create_memento.return_value = MagicMock()

        # Mock entity updates
        test_game_state.entities_exists.return_value = False

        # Create Tick Command
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

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
        test_game_state.create_memento.assert_called_once_with(self.command_manager)
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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

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
        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        # Verify command name
        self.assertEqual(test_command.get_name(), "Tick")

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
        command = InitCommand(
            self.game_state, "10", "15", self.command_manager, self.game_state_manager
        )

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
        self.game_state.restore.assert_called_once_with(
            self.game_state.create_memento.return_value,
            self.command_manager,
            self.game_state_manager,
        )

    # Failure
    # Test undoing map initialization before executing command
    def test_undo_before_execute_raises_error(self):
        # Test undo raises ValueError
        with self.assertRaisesRegex(ValueError, "Map has not been initialized!"):
            self.command.undo()

        # Test game state was not restored
        self.game_state.restore.assert_not_called()

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
        self.game_state.restore.assert_called_once()

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
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
        )

        # Execute Command
        test_command.execute()

        # Verify game state was saved
        test_game_state_manager.save_game.assert_called_once_with(
            test_game_state, "test_save", test_command_manager
        )

    # Tests SaveCommand undo deletes the created save file
    def test_save_command_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
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
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
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
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
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
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
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
            test_game_state, "test_save", test_command_manager
        )

    # Tests SaveCommand redo raises an error while already executed
    def test_save_command_redo_before_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
        )

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has already been saved!"):
            test_command.redo()

        # Verify game was only saved once
        test_game_state_manager.save_game.assert_called_once_with(
            test_game_state, "test_save", test_command_manager
        )

    # Tests SaveCommand execution failure prevents undo
    def test_save_command_execute_failure(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Simulate save failure
        test_game_state_manager.save_game.side_effect = OSError("Unable to save game!")

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
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
        test_command_manager = MagicMock()

        # Create Save Command
        test_command = SaveCommand(
            test_game_state, test_game_state_manager, "test_save", test_command_manager
        )

        # Verify command name
        self.assertEqual(test_command.get_name(), "Save")

    # Tests LoadCommand execute loads the saved game state
    def test_load_command_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Execute Command
        test_command.execute()

        # Verify current game state was saved
        test_game_state.create_memento.assert_called_once()

        # Verify saved game was loaded
        test_game_state_manager.load_game.assert_called_once_with(
            test_game_state, "test_save.json", test_command_manager
        )

    # Tests LoadCommand undo restores the previous game state
    def test_load_command_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify previous game state was restored
        test_game_state.restore.assert_called_once_with(
            test_memento, test_command_manager, test_game_state_manager
        )

    # Tests LoadCommand undo raises an error before execution
    def test_load_command_undo_before_execute(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify game state was not restored
        test_game_state.restore.assert_not_called()

    # Tests LoadCommand undo cannot be performed twice
    def test_load_command_undo_twice(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Execute Command
        test_command.execute()

        # Undo Command
        test_command.undo()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify previous game state was restored only once
        test_game_state.restore.assert_called_once_with(
            test_memento, test_command_manager, test_game_state_manager
        )

    # Tests LoadCommand redo loads the saved game again after undo
    def test_load_command_redo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
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
            test_game_state, "test_save.json", test_command_manager
        )

    # Tests LoadCommand redo raises an error while already executed
    def test_load_command_redo_before_undo(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create mock Memento
        test_memento = MagicMock()
        test_game_state.create_memento.return_value = test_memento

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Execute Command
        test_command.execute()

        # Verify error is raised
        with self.assertRaisesRegex(ValueError, "Game has already been loaded!"):
            test_command.redo()

        # Verify game was only loaded once
        test_game_state_manager.load_game.assert_called_once_with(
            test_game_state, "test_save.json", test_command_manager
        )

    # Tests LoadCommand execution failure prevents undo
    def test_load_command_execute_failure(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Simulate load failure
        test_game_state_manager.load_game.side_effect = OSError("Unable to load game!")

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
        )

        # Verify execution raises an error
        with self.assertRaises(OSError):
            test_command.execute()

        # Verify undo is not allowed
        with self.assertRaisesRegex(ValueError, "Game has not been loaded!"):
            test_command.undo()

        # Verify game state was not restored
        test_game_state.restore.assert_not_called()

    # Tests LoadCommand get_name returns the command name
    def test_load_command_get_name(self):
        # Create mock GameState
        test_game_state = MagicMock()

        # Create mock GameStateManager
        test_game_state_manager = MagicMock()
        test_command_manager = MagicMock()

        # Create Load Command
        test_command = LoadCommand(
            test_game_state,
            test_game_state_manager,
            "test_save.json",
            test_command_manager,
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

        self.assertEqual(output, "ok: undo_stack: 3, redo_stack: 2\n")
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

        self.assertEqual(output, "ok: undo_stack: 0, redo_stack: 0\n")

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

        self.assertEqual(output, "ok: undo_stack: 2, redo_stack: 1\n")
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

    def test_move_command_memento(self):
        game_state = Mock()
        game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            position=(1, 2)
        )

        command = MoveCommand(game_state, 1, 4, 5)

        memento = command.create_memento()

        new_command = MoveCommand.__new__(MoveCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.command_type, restored.command_type)
        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["x"], 4)
        self.assertEqual(restored.data["y"], 5)
        self.assertEqual(restored.data["old_x"], 1)
        self.assertEqual(restored.data["old_y"], 2)

    # Test Spawn Command Memento
    # Verify that SpawnCommand saves and restores its entity information
    # Params: None
    # Returns: None
    def test_spawn_command_memento(self):
        game_state = Mock()
        game_state.spawn_entity.return_value = 10

        command = SpawnCommand(game_state, "Warrior", 2, 3)
        command.execute()

        memento = command.create_memento()

        new_command = SpawnCommand.__new__(SpawnCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_type"], "Warrior")
        self.assertEqual(restored.data["x"], 2)
        self.assertEqual(restored.data["y"], 3)
        self.assertEqual(restored.data["entity_id"], 10)

    # Test Spawn Loot Command Memento
    # Verify that SpawnLootCommand saves and restores its information
    # Params: None
    # Returns: None
    def test_spawn_loot_command_memento(self):
        game_state = Mock()

        command = SpawnLootCommand(game_state, "Potion", 3, 4)
        memento = command.create_memento()

        new_command = SpawnLootCommand.__new__(SpawnLootCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["item_name"], "Potion")
        self.assertEqual(restored.data["x"], 3)
        self.assertEqual(restored.data["y"], 4)

    # Test Attack Command Memento
    # Verify that AttackCommand saves and restores its damage information
    # Params: None
    # Returns: None
    def test_attack_command_memento(self):
        game_state = Mock()
        game_state.attack_entity.return_value = 15

        command = AttackCommand(game_state, 1, 2)
        command.execute()

        memento = command.create_memento()

        new_command = AttackCommand.__new__(AttackCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["attacker_id"], 1)
        self.assertEqual(restored.data["target_id"], 2)
        self.assertEqual(restored.data["damage"], 15)

    # Test Cast Spell Command Memento
    # Verify that CastSpellCommand saves and restores spell information
    # Params: None
    # Returns: None
    def test_cast_spell_command_memento(self):
        game_state = Mock()

        caster = Mock()
        caster.get_info.return_value = SimpleNamespace(mana=80)

        target = Mock()
        target.get_info.return_value = SimpleNamespace(health=50)

        game_state.get_entity_from_list.side_effect = [caster, target]
        game_state.cast_spell.return_value = {"damage": 20}

        command = CastSpellCommand(game_state, 1, 2, "Fire")
        command.execute()

        memento = command.create_memento()

        new_command = CastSpellCommand.__new__(CastSpellCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["caster_id"], 1)
        self.assertEqual(restored.data["target_id"], 2)
        self.assertEqual(restored.data["spell_name"], "Fire")
        self.assertEqual(restored.data["old_health"], 50)
        self.assertEqual(restored.data["old_mana"], 80)

    # Test Set Tile Command Memento
    # Verify that SetTileCommand saves and restores its original tile type
    # Params: None
    # Returns: None
    def test_set_tile_command_memento(self):
        game_state = Mock()

        command = SetTileCommand(game_state, 2, 3, "wall")

        command._SetTileCommand__old_tile = SimpleNamespace(tile_type="floor")
        command._SetTileCommand__executed = True

        memento = command.create_memento()

        new_command = SetTileCommand.__new__(SetTileCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["old_tile_type"], "floor")
        self.assertEqual(restored.data["tile_type"], "wall")
        self.assertTrue(restored.data["executed"])

    # Test Pickup Command Memento
    # Verify that PickupCommand saves and restores its item information
    # Params: None
    # Returns: None
    def test_pickup_command_memento(self):
        game_state = Mock()

        item = SimpleNamespace(name="Potion")
        entity_info = SimpleNamespace(backpack=[item])
        game_state.get_entity_info_from_list.return_value = entity_info

        command = PickupCommand(game_state, 1, "Potion")

        command._PickupCommand__old_position = (2, 3)
        command._PickupCommand__removed_item = item
        command._PickupCommand__executed = True

        memento = command.create_memento()

        new_command = PickupCommand.__new__(PickupCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["item_name"], "Potion")
        self.assertEqual(restored.data["old_position"], (2, 3))
        self.assertEqual(restored.data["removed_item_name"], "Potion")
        self.assertTrue(restored.data["executed"])

    # Test Give Item Command Memento
    # Verify that GiveItemCommand saves and restores its information
    # Params: None
    # Returns: None
    def test_give_item_command_memento(self):
        game_state = Mock()

        command = GiveItemCommand(game_state, 1, "Potion")
        command._GiveItemCommand__executed = True

        memento = command.create_memento()

        new_command = GiveItemCommand.__new__(GiveItemCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["item_name"], "Potion")
        self.assertTrue(restored.data["executed"])

    # Test Drop Item Command Memento
    # Verify that DropItemCommand saves and restores its information
    # Params: None
    # Returns: None
    def test_drop_item_command_memento(self):
        game_state = Mock()

        command = DropItemCommand(game_state, 1, "Potion")
        command._DropItemCommand__old_position = (3, 4)
        command._DropItemCommand__executed = True

        memento = command.create_memento()

        new_command = DropItemCommand.__new__(DropItemCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["item_name"], "Potion")
        self.assertEqual(restored.data["old_position"], (3, 4))
        self.assertTrue(restored.data["executed"])

    # Test Swap Item Command Memento
    # Verify that SwapItemCommand saves and restores its old equipped item
    # Params: None
    # Returns: None
    def test_swap_item_command_memento(self):
        game_state = Mock()

        old_item = SimpleNamespace(name="IronSword")
        new_item = SimpleNamespace(name="SteelSword")

        game_state.get_entity_info_from_list.return_value = SimpleNamespace(
            backpack=[old_item]
        )

        command = SwapItemCommand(game_state, 1, "Weapon", "SteelSword")

        command._SwapItemCommand__old_item = old_item
        command._SwapItemCommand__executed = True

        memento = command.create_memento()

        new_command = SwapItemCommand.__new__(SwapItemCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["item_slot"], "Weapon")
        self.assertEqual(restored.data["item_name"], "SteelSword")
        self.assertEqual(restored.data["old_item_name"], "IronSword")
        self.assertTrue(restored.data["executed"])

    # Test Use Item Command Memento
    # Verify that UseItemCommand saves and restores its previous game state
    # Params: None
    # Returns: None
    def test_use_item_command_memento(self):
        game_state = Mock()

        old_state = {"turn": 1, "health": 100}
        game_state.create_memento.return_value = old_state

        command = UseItemCommand(
            game_state, 1, "Potion", self.command_manager, self.game_state_manager
        )
        command.execute()

        memento = command.create_memento()

        new_command = UseItemCommand.__new__(UseItemCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["entity_id"], 1)
        self.assertEqual(restored.data["item_name"], "Potion")
        self.assertEqual(restored.data["old_state"], old_state)
        self.assertTrue(restored.data["executed"])

    # Test Tick Command Memento
    # Verify that TickCommand saves and restores its previous game state
    # Params: None
    # Returns: None
    def test_tick_command_memento(self):
        game_state = Mock()

        old_state = {"turn": 1}
        game_state.create_memento.return_value = old_state
        game_state.entities_exists.return_value = False

        command = TickCommand(game_state, self.command_manager, self.game_state_manager)
        command.execute()

        memento = command.create_memento()

        new_command = TickCommand.__new__(TickCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["old_state"], old_state)
        self.assertTrue(restored.data["executed"])

    # Test Init Command Memento
    # Verify that InitCommand saves and restores its previous game state
    # Params: None
    # Returns: None
    def test_init_command_memento(self):
        game_state = Mock()

        old_state = {"map_created": False}
        game_state.create_memento.return_value = old_state
        game_state.is_map_created.return_value = False

        command = InitCommand(
            game_state, 10, 12, self.command_manager, self.game_state_manager
        )
        command.execute()

        memento = command.create_memento()

        new_command = InitCommand.__new__(InitCommand)
        new_command.restore(memento, game_state)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["width"], 10)
        self.assertEqual(restored.data["height"], 12)
        self.assertEqual(restored.data["old_state"], old_state)
        self.assertTrue(restored.data["executed"])

    # Test Save Command Memento
    # Verify that SaveCommand saves and restores its filename
    # Params: None
    # Returns: None
    def test_save_command_memento(self):
        game_state = Mock()
        game_state_manager = Mock()
        command_manager = MagicMock()

        command = SaveCommand(
            game_state, game_state_manager, "save1.json", command_manager
        )
        command.execute()

        memento = command.create_memento()

        new_command = SaveCommand.__new__(SaveCommand)
        new_command.restore(
            memento, game_state, game_state_manager, self.game_state_manager
        )

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["filename"], "save1.json")
        self.assertTrue(restored.data["executed"])

    # Test Load Command Memento
    # Verify that LoadCommand saves and restores its previous game state
    # Params: None
    # Returns: None
    def test_load_command_memento(self):
        game_state = Mock()
        game_state_manager = Mock()
        command_manager = MagicMock()

        old_state = {"turn": 5}
        game_state.create_memento.return_value = old_state

        command = LoadCommand(
            game_state, game_state_manager, "save1.json", command_manager
        )
        command.execute()

        memento = command.create_memento()

        new_command = LoadCommand.__new__(LoadCommand)
        new_command.restore(memento, game_state, game_state_manager, command_manager)

        restored = new_command.create_memento()

        self.assertEqual(memento.data, restored.data)
        self.assertEqual(restored.data["filename"], "save1.json")
        self.assertEqual(restored.data["memento"], old_state)
        self.assertTrue(restored.data["executed"])

    # Test State Command Execute
    # Verify that the current behavioral state is displayed
    def test_state_command_execute(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        game_state.get_entity_from_list.return_value = entity

        command = StateCommand(game_state, 1)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            command.execute()

        game_state.get_entity_from_list.assert_called_once_with(1)
        entity.get_entity_state_name.assert_called_once()
        self.assertEqual(
            mock_stdout.getvalue().strip(), "ok: entity 1 state: Defending!"
        )

    # Test State Command With Different States
    # Verify that all behavioral state names display correctly
    def test_state_command_all_states(self):
        for state_name in ("Defending", "Attacking", "Fleeing"):
            with self.subTest(state=state_name):
                game_state = MagicMock()
                entity = MagicMock()

                entity.get_entity_state_name.return_value = state_name
                game_state.get_entity_from_list.return_value = entity

                command = StateCommand(game_state, 2)

                with patch("sys.stdout", new_callable=StringIO) as output:
                    command.execute()

                self.assertEqual(
                    output.getvalue().strip(), f"ok: entity 2 state: {state_name}!"
                )

    # Test State Command Invalid Entity
    # Verify that nonexistent entities raise an error
    def test_state_command_invalid_entity(self):
        game_state = MagicMock()
        game_state.get_entity_from_list.return_value = None

        command = StateCommand(game_state, 999)

        with self.assertRaisesRegex(ValueError, "Entity does not exist!"):
            command.execute()

    # Test State Command Without Behavioral State
    # Verify that player entities cannot query AI states
    def test_state_command_no_behavioral_state(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = None
        game_state.get_entity_from_list.return_value = entity

        command = StateCommand(game_state, 1)

        with self.assertRaisesRegex(
            ValueError, "Entity does not have a behavioral state"
        ):
            command.execute()

    # Test State Command Redo
    # Verify that redo executes the state query again
    def test_state_command_redo(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Attacking"
        game_state.get_entity_from_list.return_value = entity

        command = StateCommand(game_state, 1)

        with patch("sys.stdout", new_callable=StringIO) as output:
            command.redo()

        self.assertEqual(output.getvalue().strip(), "ok: entity 1 state: Attacking!")

    # Test State Command Undo
    # Verify that undo does not modify the game state
    def test_state_command_undo(self):
        game_state = MagicMock()

        command = StateCommand(game_state, 1)
        command.undo()

        game_state.assert_not_called()

    # Test State Command Get Name
    def test_state_command_get_name(self):
        command = StateCommand(MagicMock(), 1)

        self.assertEqual(command.get_name(), "State")

    # Test State Command Is Undoable
    def test_state_command_is_undoable(self):
        command = StateCommand(MagicMock(), 1)

        self.assertFalse(command.is_undoable())

    # Test State Command String Entity ID
    # Verify that string IDs are converted into integers
    def test_state_command_string_entity_id(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        game_state.get_entity_from_list.return_value = entity

        command = StateCommand(game_state, "5")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        game_state.get_entity_from_list.assert_called_once_with(5)

    # Test Force State Command Execute
    # Verify that an entity is forced into the requested state
    def test_force_state_command_execute(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO) as output:
            command.execute()

        entity.transition_entity_state.assert_called_once()
        self.assertIsInstance(
            entity.transition_entity_state.call_args.args[0], AttackingState
        )
        entity.create_state_manager_memento.assert_called_once()
        game_state.mark_as_unsaved.assert_called_once()

        self.assertEqual(
            output.getvalue().strip(), "ok: entity 1 transitioned to Attacking!"
        )

    # Test Force State Command All States
    # Verify that each supported state can be forced
    def test_force_state_command_all_states(self):
        for state_name in ("Defending", "Attacking", "Fleeing"):
            with self.subTest(state=state_name):
                game_state = MagicMock()
                entity = MagicMock()

                entity.get_entity_state_name.return_value = "Defending"
                entity.create_state_manager_memento.return_value = (
                    Entity.StateManagerMemento("Defending")
                )
                game_state.get_entity_from_list.return_value = entity

                command = ForceStateCommand(game_state, 1, state_name)

                with patch("sys.stdout", new_callable=StringIO):
                    command.execute()

                entity.transition_entity_state.assert_called_once()
                self.assertIsInstance(
                    entity.transition_entity_state.call_args.args[0],
                    {
                        "Defending": DefendingState,
                        "Attacking": AttackingState,
                        "Fleeing": FleeingState,
                    }[state_name],
                )

    # Test Force State Command Invalid Entity
    # Verify that nonexistent entities raise an error
    def test_force_state_command_invalid_entity(self):
        game_state = MagicMock()
        game_state.get_entity_from_list.return_value = None

        command = ForceStateCommand(game_state, 999, "Fleeing")

        with self.assertRaisesRegex(ValueError, "Entity does not exist!"):
            command.execute()

        game_state.mark_as_unsaved.assert_not_called()

    # Test Force State Command Without Behavioral State
    # Verify that player entities cannot be forced into AI states
    def test_force_state_command_no_behavioral_state(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = None
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with self.assertRaisesRegex(
            ValueError, "Entity does not have a behavioral state!"
        ):
            command.execute()

        entity.transition_entity_state.assert_not_called()
        game_state.mark_as_unsaved.assert_not_called()

    # Test Force State Command Undo
    # Verify that undo restores the original behavioral state
    def test_force_state_command_undo(self):
        game_state = MagicMock()
        entity = MagicMock()

        old_memento = Entity.StateManagerMemento("Defending")
        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = old_memento
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Fleeing")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        entity.transition_entity_state.reset_mock()
        game_state.mark_as_unsaved.reset_mock()

        command.undo()

        entity.transition_entity_state.assert_called()
        self.assertIsInstance(
            entity.transition_entity_state.call_args.args[0], DefendingState
        )
        game_state.mark_as_unsaved.assert_called_once()

    # Test Force State Command Undo Before Execute
    def test_force_state_command_undo_before_execute(self):
        game_state = MagicMock()
        command = ForceStateCommand(game_state, 1, "Attacking")

        with self.assertRaisesRegex(ValueError, "State has not been forced!"):
            command.undo()

        game_state.get_entity_from_list.assert_not_called()

    # Test Force State Command Undo Missing Entity
    def test_force_state_command_undo_missing_entity(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        game_state.get_entity_from_list.return_value = None

        with self.assertRaisesRegex(ValueError, "Entity does not exist!"):
            command.undo()

    # Test Force State Command Redo
    # Verify that redo forces the requested state again
    def test_force_state_command_redo(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        command.undo()
        entity.transition_entity_state.reset_mock()

        with patch("sys.stdout", new_callable=StringIO):
            command.redo()

        entity.transition_entity_state.assert_called_once()
        self.assertIsInstance(
            entity.transition_entity_state.call_args.args[0], AttackingState
        )

    # Test Force State Command Redo Before Undo
    def test_force_state_command_redo_before_undo(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        with self.assertRaisesRegex(ValueError, "State has already been forced!"):
            command.redo()

    # Test Force State Command Get Name
    def test_force_state_command_get_name(self):
        command = ForceStateCommand(MagicMock(), 1, "Fleeing")

        self.assertEqual(command.get_name(), "Force State")

    # Test Force State Command Create Memento
    def test_force_state_command_create_memento(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        memento = command.create_memento()

        self.assertIsInstance(memento, Command.Memento)
        self.assertEqual(memento.command_type, "ForceStateCommand")
        self.assertEqual(memento.data["entity_id"], 1)
        self.assertEqual(memento.data["state_name"], "Attacking")
        self.assertEqual(memento.data["old_state"], "Defending")
        self.assertTrue(memento.data["executed"])

    # Test Force State Command Memento Before Execute
    def test_force_state_command_memento_before_execute(self):
        command = ForceStateCommand(MagicMock(), 1, "Fleeing")

        memento = command.create_memento()

        self.assertIsNone(memento.data["old_state"])
        self.assertFalse(memento.data["executed"])

    # Test Force State Command Restore
    # Verify that command information is reconstructed
    def test_force_state_command_restore(self):
        game_state = MagicMock()
        original = ForceStateCommand(game_state, 2, "Fleeing")

        memento = original.create_memento()
        restored = ForceStateCommand.__new__(ForceStateCommand)

        restored.restore(memento, game_state)

        self.assertEqual(restored.get_name(), "Force State")
        self.assertEqual(restored.create_memento().data, memento.data)

    # Test Force State Command Restore With Previous State
    def test_force_state_command_restore_previous_state(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.create_state_manager_memento.return_value = Entity.StateManagerMemento(
            "Defending"
        )
        game_state.get_entity_from_list.return_value = entity

        command = ForceStateCommand(game_state, 1, "Attacking")

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        memento = command.create_memento()

        restored = ForceStateCommand.__new__(ForceStateCommand)
        restored.restore(memento, game_state)
        restored.undo()

        self.assertIsInstance(
            entity.transition_entity_state.call_args.args[0], DefendingState
        )

    # Test Force State Command Restore Invalid Memento
    def test_force_state_command_restore_invalid_memento(self):
        command = ForceStateCommand(MagicMock(), 1, "Attacking")

        with self.assertRaises(TypeError):
            command.restore("invalid", MagicMock())

    # Test Force State Command Restore Wrong Type
    def test_force_state_command_restore_wrong_type(self):
        command = ForceStateCommand(MagicMock(), 1, "Attacking")

        memento = Command.Memento(command_type="SimulateCommand", data={})

        with self.assertRaisesRegex(
            ValueError, "Incorrect Force State Command memento!"
        ):
            command.restore(memento, MagicMock())

    # Test Simulate Command Execute
    # Verify that AI behavior is evaluated
    def test_simulate_command_execute(self):
        game_state = MagicMock()
        command_manager = MagicMock()
        game_state_manager = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Attacking"
        entity.update_entity_state.return_value = "Attack"
        game_state.get_entity_from_list.return_value = entity

        command = SimulateCommand(game_state, 1, command_manager, game_state_manager)

        with patch("sys.stdout", new_callable=StringIO) as output:
            command.execute()

        game_state.get_entity_from_list.assert_called_once_with(1)
        game_state.create_memento.assert_called_once_with(command_manager)
        entity.update_entity_state.assert_called_once()
        game_state.mark_as_unsaved.assert_called_once()

        self.assertEqual(
            output.getvalue().strip(), "ok: simulated for 1 command: Attack!"
        )

    # Test Simulate Command Different Results
    # Verify that the AI result is displayed correctly
    def test_simulate_command_results(self):
        for result in ("Attack", "Move", "Defend", "Flee"):
            with self.subTest(result=result):
                game_state = MagicMock()
                entity = MagicMock()

                entity.get_entity_state_name.return_value = "Defending"
                entity.update_entity_state.return_value = result
                game_state.get_entity_from_list.return_value = entity

                command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

                with patch("sys.stdout", new_callable=StringIO) as output:
                    command.execute()

                self.assertEqual(
                    output.getvalue().strip(), f"ok: simulated for 1 command: {result}!"
                )

    # Test Simulate Command Invalid Entity
    def test_simulate_command_invalid_entity(self):
        game_state = MagicMock()
        game_state.get_entity_from_list.return_value = None

        command = SimulateCommand(game_state, 999, MagicMock(), MagicMock())

        with self.assertRaisesRegex(ValueError, "Entity does not exist!"):
            command.execute()

        game_state.create_memento.assert_not_called()

    # Test Simulate Command Without AI
    def test_simulate_command_no_behavioral_state(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = None
        game_state.get_entity_from_list.return_value = entity

        command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

        with self.assertRaisesRegex(
            ValueError, "Entity does not have a behavioral state!"
        ):
            command.execute()

        entity.update_entity_state.assert_not_called()
        game_state.create_memento.assert_not_called()

    # Test Simulate Command Execution Failure
    # Verify that a failed simulation restores the previous game state
    def test_simulate_command_execute_failure(self):
        game_state = MagicMock()
        command_manager = MagicMock()
        game_state_manager = MagicMock()
        entity = MagicMock()

        old_state = {"turn": 5}
        game_state.create_memento.return_value = old_state
        game_state.get_entity_from_list.return_value = entity

        entity.get_entity_state_name.return_value = "Attacking"
        entity.update_entity_state.side_effect = ValueError("AI failed!")

        command = SimulateCommand(game_state, 1, command_manager, game_state_manager)

        with self.assertRaisesRegex(ValueError, "AI failed!"):
            command.execute()

        game_state.restore.assert_called_once_with(
            old_state, command_manager, game_state_manager
        )
        game_state.mark_as_unsaved.assert_not_called()

    # Test Simulate Command Undo
    # Verify that the previous game state is restored
    def test_simulate_command_undo(self):
        game_state = MagicMock()
        command_manager = MagicMock()
        game_state_manager = MagicMock()
        entity = MagicMock()

        old_state = {"turn": 5}
        game_state.create_memento.return_value = old_state
        game_state.get_entity_from_list.return_value = entity
        entity.get_entity_state_name.return_value = "Defending"
        entity.update_entity_state.return_value = "Move"

        command = SimulateCommand(game_state, 1, command_manager, game_state_manager)

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        command.undo()

        game_state.restore.assert_called_once_with(
            old_state, command_manager, game_state_manager
        )

    # Test Simulate Command Undo Before Execute
    def test_simulate_command_undo_before_execute(self):
        game_state = MagicMock()

        command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

        with self.assertRaisesRegex(ValueError, "Simulation has not been executed!"):
            command.undo()

        game_state.restore.assert_not_called()

    # Test Simulate Command Redo
    # Verify that AI is evaluated again after undo
    def test_simulate_command_redo(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        entity.update_entity_state.return_value = "Move"
        game_state.get_entity_from_list.return_value = entity

        command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        command.undo()

        with patch("sys.stdout", new_callable=StringIO):
            command.redo()

        self.assertEqual(entity.update_entity_state.call_count, 2)

    # Test Simulate Command Redo Before Undo
    def test_simulate_command_redo_before_undo(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        game_state.get_entity_from_list.return_value = entity

        command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        with self.assertRaisesRegex(
            ValueError, "Simulation has already been executed!"
        ):
            command.redo()

    # Test Simulate Command Get Name
    def test_simulate_command_get_name(self):
        command = SimulateCommand(MagicMock(), 1, MagicMock(), MagicMock())

        self.assertEqual(command.get_name(), "Simulate")

    # Test Simulate Command Create Memento
    def test_simulate_command_create_memento(self):
        game_state = MagicMock()
        entity = MagicMock()

        old_state = {"turn": 5}
        game_state.create_memento.return_value = old_state
        game_state.get_entity_from_list.return_value = entity
        entity.get_entity_state_name.return_value = "Attacking"
        entity.update_entity_state.return_value = "Attack"

        command = SimulateCommand(game_state, 1, MagicMock(), MagicMock())

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        memento = command.create_memento()

        self.assertIsInstance(memento, Command.Memento)
        self.assertEqual(memento.command_type, "SimulateCommand")
        self.assertEqual(memento.data["entity_id"], 1)
        self.assertEqual(memento.data["old_state"], old_state)
        self.assertTrue(memento.data["executed"])

    # Test Simulate Command Memento Before Execute
    def test_simulate_command_memento_before_execute(self):
        command = SimulateCommand(MagicMock(), 1, MagicMock(), MagicMock())

        memento = command.create_memento()

        self.assertIsNone(memento.data["old_state"])
        self.assertFalse(memento.data["executed"])

    # Test Simulate Command Restore
    def test_simulate_command_restore(self):
        game_state = MagicMock()
        command_manager = MagicMock()
        game_state_manager = MagicMock()

        original = SimulateCommand(game_state, 1, command_manager, game_state_manager)

        memento = original.create_memento()

        restored = SimulateCommand.__new__(SimulateCommand)
        restored.restore(memento, game_state, game_state_manager, command_manager)

        self.assertEqual(restored.get_name(), "Simulate")
        self.assertEqual(restored.create_memento().data, memento.data)

    # Test Simulate Command Restore And Undo
    # Verify that a restored command retains its previous snapshot
    def test_simulate_command_restore_and_undo(self):
        game_state = MagicMock()
        command_manager = MagicMock()
        game_state_manager = MagicMock()
        entity = MagicMock()

        old_state = {"turn": 5}
        game_state.create_memento.return_value = old_state
        game_state.get_entity_from_list.return_value = entity
        entity.get_entity_state_name.return_value = "Defending"

        command = SimulateCommand(game_state, 1, command_manager, game_state_manager)

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        memento = command.create_memento()

        restored = SimulateCommand.__new__(SimulateCommand)
        restored.restore(memento, game_state, game_state_manager, command_manager)

        restored.undo()

        game_state.restore.assert_called_once_with(
            old_state, command_manager, game_state_manager
        )

    # Test Simulate Command Restore Invalid Memento
    def test_simulate_command_restore_invalid_memento(self):
        command = SimulateCommand(MagicMock(), 1, MagicMock(), MagicMock())

        with self.assertRaises(TypeError):
            command.restore("invalid", MagicMock())

    # Test Simulate Command Restore Wrong Type
    def test_simulate_command_restore_wrong_type(self):
        command = SimulateCommand(MagicMock(), 1, MagicMock(), MagicMock())

        memento = Command.Memento(command_type="ForceStateCommand", data={})

        with self.assertRaisesRegex(ValueError, "Incorrect Simulate Command memento!"):
            command.restore(memento, MagicMock())

    # Test Simulate Command String Entity ID
    def test_simulate_command_string_entity_id(self):
        game_state = MagicMock()
        entity = MagicMock()

        entity.get_entity_state_name.return_value = "Defending"
        game_state.get_entity_from_list.return_value = entity

        command = SimulateCommand(game_state, "5", MagicMock(), MagicMock())

        with patch("sys.stdout", new_callable=StringIO):
            command.execute()

        game_state.get_entity_from_list.assert_called_once_with(5)

    # Test Tick Command Processes AI
    # Verify that AI behavior is processed once per tick
    # Returns: None
    def test_tick_command_processes_ai(self):
        test_game_state = MagicMock()

        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()

        test_game_state.process_ai_for_all_entities.assert_called_once_with()
        test_game_state.advance_turn.assert_called_once_with()

    # Test Tick Command Skips AI Without Entities
    # Verify that AI is not processed when no entities exist
    # Returns: None
    def test_tick_command_skips_ai_without_entities(self):
        test_game_state = MagicMock()

        test_game_state.entities_exists.return_value = False

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()

        test_game_state.process_ai_for_all_entities.assert_not_called()
        test_game_state.process_tick_for_all_entities.assert_not_called()

        test_game_state.advance_turn.assert_called_once_with()

    # Test Tick Command AI After Entity Removal
    # Verify that expired entities are removed before AI processing
    # Returns: None
    def test_tick_command_ai_after_entity_removal(self):
        test_game_state = MagicMock()

        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = [2, 3]

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()

        # Verify expired entities were removed
        test_game_state.remove_entity_from_game.assert_any_call(2)
        test_game_state.remove_entity_from_game.assert_any_call(3)

        self.assertEqual(test_game_state.remove_entity_from_game.call_count, 2)

        # Verify AI was processed once
        test_game_state.process_ai_for_all_entities.assert_called_once_with()

        # Verify removal happened before AI processing
        method_calls = test_game_state.mock_calls

        remove_2_index = method_calls.index(
            unittest.mock.call.remove_entity_from_game(2)
        )

        remove_3_index = method_calls.index(
            unittest.mock.call.remove_entity_from_game(3)
        )

        ai_index = method_calls.index(unittest.mock.call.process_ai_for_all_entities())

        self.assertLess(remove_2_index, ai_index)
        self.assertLess(remove_3_index, ai_index)

    # Test Tick Command AI Before Turn Advancement
    # Verify that AI is processed before advancing the turn
    # Returns: None
    def test_tick_command_ai_before_turn_advance(self):
        test_game_state = MagicMock()

        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()

        method_calls = test_game_state.mock_calls

        ai_index = method_calls.index(unittest.mock.call.process_ai_for_all_entities())

        advance_index = method_calls.index(unittest.mock.call.advance_turn())

        self.assertLess(ai_index, advance_index)

    # Test Tick Command AI Undo
    # Verify that undo restores the state before AI processing
    # Returns: None
    def test_tick_command_ai_undo(self):
        test_game_state = MagicMock()
        old_state = MagicMock()

        test_game_state.create_memento.return_value = old_state
        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()
        test_command.undo()

        # Verify the original state was restored
        test_game_state.restore.assert_called_once_with(
            old_state,
            self.command_manager,
            self.game_state_manager,
        )

        # Verify AI was processed once during execution
        test_game_state.process_ai_for_all_entities.assert_called_once_with()

    # Test Tick Command AI Redo
    # Verify that AI is processed again after undo and redo
    # Returns: None
    def test_tick_command_ai_redo(self):
        test_game_state = MagicMock()

        test_game_state.entities_exists.return_value = True
        test_game_state.process_tick_for_all_entities.return_value = []

        test_command = TickCommand(
            test_game_state, self.command_manager, self.game_state_manager
        )

        test_command.execute()
        test_command.undo()
        test_command.redo()

        # Verify AI ran once per execution
        self.assertEqual(test_game_state.process_ai_for_all_entities.call_count, 2)

        # Verify turn advanced once per execution
        self.assertEqual(test_game_state.advance_turn.call_count, 2)

        # Verify undo restored the previous state
        test_game_state.restore.assert_called_once()

    def force(self, state="Raging"):
        return ForceStateCommand(self.game, 1, state)

    def simulate(self):
        return SimulateCommand(self.game, 1, self.manager, self.state_manager)

    def test_force_undo_transitions_back_to_original_state(self):
        command = self.force()
        command.execute()
        command.undo()
        self.assertEqual(self.entity.transition_entity_state.call_count, 2)
        self.assertIsInstance(
            self.entity.transition_entity_state.call_args.args[0], DefendingState
        )
        self.assertEqual(command.create_memento().data["old_state"], "Defending")

    def test_force_redo_preserves_first_state_snapshot(self):
        command = self.force()
        command.execute()
        command.undo()
        self.entity.create_state_manager_memento.return_value = SimpleNamespace(
            state_name="Attacking"
        )
        command.redo()
        self.assertEqual(self.entity.create_state_manager_memento.call_count, 1)
        self.assertEqual(command.create_memento().data["old_state"], "Defending")

    def test_force_all_states_transition_to_correct_class(self):
        for name, state_class in (
            ("Defending", DefendingState),
            ("Attacking", AttackingState),
            ("Fleeing", FleeingState),
            ("Raging", RagingState),
        ):
            with self.subTest(state=name):
                self.entity.reset_mock()
                self.entity.get_entity_state_name.return_value = "Defending"
                self.force(name).execute()
                self.assertIsInstance(
                    self.entity.transition_entity_state.call_args.args[0], state_class
                )

    def test_force_invalid_state_does_not_transition(self):
        with self.assertRaisesRegex(ValueError, "Invalid entity state"):
            self.force("Unknown").execute()
        self.entity.transition_entity_state.assert_not_called()
        self.game.mark_as_unsaved.assert_not_called()

    def test_force_transition_failure_does_not_mark_unsaved(self):
        self.entity.transition_entity_state.side_effect = ValueError("Blocked")
        with self.assertRaisesRegex(ValueError, "Blocked"):
            self.force().execute()
        self.game.mark_as_unsaved.assert_not_called()

    def test_force_undo_uses_original_raging_state(self):
        self.entity.create_state_manager_memento.return_value = SimpleNamespace(
            state_name="Raging"
        )
        command = self.force("Defending")
        command.execute()
        command.undo()
        self.assertIsInstance(
            self.entity.transition_entity_state.call_args.args[0], RagingState
        )

    def test_simulate_saves_snapshot_before_ai_update(self):
        snapshot = SimpleNamespace(turn_number=3)
        self.game.create_memento.return_value = snapshot
        command = self.simulate()
        command.execute()
        self.game.create_memento.assert_called_once_with(self.manager)
        self.entity.update_entity_state.assert_called_once_with()
        saved_snapshot = command.create_memento().data["old_state"]
        self.assertEqual(saved_snapshot, snapshot)
        self.assertIsNot(saved_snapshot, snapshot)

    def test_simulate_undo_restores_full_game_snapshot(self):
        snapshot = SimpleNamespace(turn_number=3)
        self.game.create_memento.return_value = snapshot
        command = self.simulate()
        command.execute()
        command.undo()
        self.game.restore.assert_called_once_with(
            snapshot, self.manager, self.state_manager
        )
        self.assertFalse(command.create_memento().data["executed"])

    def test_simulate_failure_rolls_back_snapshot(self):
        snapshot = SimpleNamespace(turn_number=3)
        self.game.create_memento.return_value = snapshot
        self.entity.update_entity_state.side_effect = RuntimeError("AI error")
        with self.assertRaisesRegex(RuntimeError, "AI error"):
            self.simulate().execute()
        self.game.restore.assert_called_once_with(
            snapshot, self.manager, self.state_manager
        )
        self.game.mark_as_unsaved.assert_not_called()

    def test_simulate_redo_after_undo(self):
        snapshot = SimpleNamespace(turn_number=3)
        self.game.create_memento.return_value = snapshot
        command = self.simulate()
        command.execute()
        command.undo()
        command.redo()
        self.assertEqual(self.entity.update_entity_state.call_count, 2)
        self.assertTrue(command.create_memento().data["executed"])

    def test_simulate_undo_without_execution_rejected(self):
        with self.assertRaises(ValueError):
            self.simulate().undo()
        self.game.restore.assert_not_called()

    def test_simulate_redo_without_undo_rejected(self):
        command = self.simulate()
        command.execute()
        with self.assertRaises(ValueError):
            command.redo()
        self.assertEqual(self.entity.update_entity_state.call_count, 1)


if __name__ == "__main__":
    unittest.main()
