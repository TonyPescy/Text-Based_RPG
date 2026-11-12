"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 16, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_game_state.py
Purpose: Utilizes unittest to test all of the classes and methods in game_state.py file
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
import contextlib
import io
import unittest
from unittest.mock import patch, MagicMock
import domain_library as dl
import equipment
import entity as ent
from game_state import GameState
from command_manager import CommandManager
from game_state_manager import GameStateManager


# Class for testing GameState
class TestGameState(unittest.TestCase):

    # Set Up Test
    # Resets shared default inventory and creates a new GameState.
    # Params: None
    # Returns: None
    def setUp(self):
        # Reset shared inventory to prevent modifiers from carrying over.
        dl.BASE_INVENTORY = [
            equipment.create_equipment("none_wep"),
            equipment.create_equipment("none_armor"),
            equipment.create_equipment("none_acc"),
        ]

        # Create a new game state.
        self.game_state = GameState()

    # Create Test Grid
    # Creates a grid for testing.
    # Params: width/height - int - grid dimensions
    # Returns: None
    def create_test_grid(self, width=5, height=5):
        self.game_state.create_grid(width, height)

    # Create Spawned Entity
    # Creates and registers an entity for testing.
    # Params: entity_type - str - type of entity
    #         x/y - int - entity position
    # Returns: Entity - spawned entity
    def create_spawned_entity(self, entity_type="warrior", x=0, y=0):
        self.game_state.spawn_entity(x, y, entity_type)
        return self.game_state.get_entity_from_list(1)

    # Get Backpack Names
    # Gets the names of items in an entity's backpack.
    # Params: entity_id - int - entity ID
    # Returns: List - item names
    def get_backpack_names(self, entity_id):
        entity_info = self.game_state.get_entity_info_from_list(entity_id)
        return [item.name for item in entity_info.backpack]

    # Init Tests

    # Init Game State
    # Checks that a new game state has the expected initial values.
    # Params: None
    # Returns: None
    def test_init_game_state(self):
        self.assertFalse(self.game_state.is_map_created())
        self.assertFalse(self.game_state.entities_exists())
        self.assertIsNone(self.game_state.get_entity_from_list(1))
        self.assertIsNone(self.game_state.get_entity_info_from_list(1))

    # Is Map Created
    # Checks whether the map-created flag is returned correctly.
    # Params: None
    # Returns: None
    def test_is_map_created(self):
        self.assertFalse(self.game_state.is_map_created())

        self.game_state.mark_map_created()

        self.assertTrue(self.game_state.is_map_created())

    # Mark Map Created
    # Checks that the map-created flag becomes True.
    # Params: None
    # Returns: None
    def test_mark_map_created(self):
        self.game_state.mark_map_created()
        self.assertTrue(self.game_state.is_map_created())

    # Create Grid
    # Checks that creating a grid marks the map as created.
    # Params: None
    # Returns: None
    def test_create_grid(self):
        self.create_test_grid(10, 8)

        self.assertTrue(self.game_state.is_map_created())
        self.assertTrue(self.game_state.is_valid_grid_position(9, 7))
        self.assertFalse(self.game_state.is_valid_grid_position(10, 7))

    # Reset Map
    # Checks that resetting the map clears the grid and entities.
    # Params: None
    # Returns: None
    def test_reset_map(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.reset_map()

        self.assertFalse(self.game_state.is_map_created())
        self.assertFalse(self.game_state.entities_exists())
        self.assertIsNone(self.game_state._GameState__grid)

    # Reset Entity List
    # Checks that resetting the entity list removes registered entities.
    # Params: None
    # Returns: None
    def test_reset_entity_list(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.reset_entity_list()

        self.assertFalse(self.game_state.entities_exists())
        self.assertIsNone(self.game_state.get_entity_from_list(1))

    # Reset ID Issuer Tracker
    # Checks that the entity ID tracker resets to one.
    # Params: None
    # Returns: None
    def test_reset_id_issuer_tracker(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.reset_map()
        self.create_test_grid()
        self.game_state.reset_id_issuer_tracker()
        self.create_spawned_entity()

        self.assertEqual(self.game_state.get_entity_info_from_list(1).id, 1)

    # Reset Turn Number
    # Checks that resetting the turn number sets it to one.
    # Params: None
    # Returns: None
    def test_reset_turn_number(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.game_state.advance_turn()
            self.game_state.advance_turn()

        self.game_state.reset_turn_number()

        self.assertEqual(self.game_state._GameState__turn_number, 1)

    # Advance Turn
    # Checks that advancing a turn increases the turn number.
    # Params: None
    # Returns: None
    def test_advance_turn(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            self.game_state.advance_turn()

        self.assertEqual(self.game_state._GameState__turn_number, 2)
        self.assertIn("advanced to turn 2", output.getvalue())

    # Mark As Unsaved
    # Checks that the saved-state flag becomes False.
    # Params: None
    # Returns: None
    def test_mark_as_unsaved(self):
        self.game_state.mark_as_unsaved()

        self.assertFalse(self.game_state._GameState__is_saved)

    # Mark As Saved
    # Checks that the saved-state flag becomes True.
    # Params: None
    # Returns: None
    def test_mark_as_saved(self):
        self.game_state.mark_as_unsaved()
        self.game_state.mark_as_saved()

        self.assertTrue(self.game_state._GameState__is_saved)

    # Grid Tests

    # Set Game Grid Tile
    # Checks that a tile can be changed through GameState.
    # Params: None
    # Returns: None
    def test_set_game_grid_tile(self):
        self.create_test_grid()

        self.game_state.set_game_grid_tile("1", "1", "wall")

        self.assertFalse(self.game_state.is_tile_passable(1, 1))

    # Is Grid Tile Occupied
    # Checks whether a tile is occupied.
    # Params: None
    # Returns: None
    def test_is_grid_tile_occupied(self):
        self.create_test_grid()

        self.assertFalse(self.game_state.is_grid_tile_occupied(0, 0))

        self.create_spawned_entity()

        self.assertTrue(self.game_state.is_grid_tile_occupied(0, 0))

    # Is Tile Passable
    # Checks passability for floor and wall tiles.
    # Params: None
    # Returns: None
    def test_is_tile_passable(self):
        self.create_test_grid()

        self.assertTrue(self.game_state.is_tile_passable(0, 0))

        self.game_state.set_game_grid_tile(1, 1, "wall")

        self.assertFalse(self.game_state.is_tile_passable(1, 1))

    # Get Game Tile Info
    # Checks that tile information can be retrieved.
    # Params: None
    # Returns: None
    def test_get_game_tile_info(self):
        self.create_test_grid()

        tile_info = self.game_state.get_game_tile_info("0", "0")

        self.assertIsNotNone(tile_info)
        self.assertEqual(tile_info.occupants, ())

    # Is Within Range
    # Checks whether a position is within range of another position.
    # Params: None
    # Returns: None
    def test_is_within_range(self):
        self.create_test_grid()

        self.assertTrue(self.game_state.is_within_range(0, 0, 1, 0, 1))
        self.assertFalse(self.game_state.is_within_range(0, 0, 3, 3, 1))

    # Is Valid Grid Position
    # Checks valid and invalid grid positions.
    # Params: None
    # Returns: None
    def test_is_valid_grid_position(self):
        self.create_test_grid(6, 7)

        self.assertTrue(self.game_state.is_valid_grid_position(5, 6))
        self.assertFalse(self.game_state.is_valid_grid_position(-1, 0))
        self.assertFalse(self.game_state.is_valid_grid_position(6, 6))

    # Entity Tests

    # Spawn Entity
    # Checks that spawning registers an entity and occupies its tile.
    # Params: None
    # Returns: None
    def test_spawn_entity(self):
        self.create_test_grid()

        self.game_state.spawn_entity(2, 3, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)

        self.assertEqual(entity_info.id, 1)
        self.assertEqual(entity_info.e_type, "warrior")
        self.assertEqual(entity_info.position, [2, 3])
        self.assertTrue(self.game_state.entities_exists())
        self.assertTrue(self.game_state.is_grid_tile_occupied(2, 3))

    # Spawn Multiple Entities
    # Checks that each spawned entity receives a unique ID.
    # Params: None
    # Returns: None
    def test_spawn_multiple_entities(self):
        self.create_test_grid()

        self.game_state.spawn_entity(0, 0, "warrior")
        self.game_state.spawn_entity(1, 0, "goblin")

        self.assertEqual(self.game_state.get_entity_info_from_list(1).id, 1)
        self.assertEqual(self.game_state.get_entity_info_from_list(2).id, 2)
        self.assertEqual(self.game_state.get_entity_info_from_list(2).e_type, "goblin")

    # Get Entity From List
    # Checks that entity lookup returns the entity object.
    # Params: None
    # Returns: None
    def test_get_entity_from_list(self):
        self.create_test_grid()
        entity = self.create_spawned_entity()

        self.assertIs(self.game_state.get_entity_from_list("1"), entity)
        self.assertIsNone(self.game_state.get_entity_from_list(99))

    # Get Entity Info From List
    # Checks that entity info can be retrieved by ID.
    # Params: None
    # Returns: None
    def test_get_entity_info_from_list(self):
        self.create_test_grid()
        self.create_spawned_entity()

        entity_info = self.game_state.get_entity_info_from_list("1")

        self.assertEqual(entity_info.id, 1)
        self.assertIsNone(self.game_state.get_entity_info_from_list(99))

    # Get Entity ID From Tile
    # Checks that the occupying entity ID can be retrieved.
    # Params: None
    # Returns: None
    def test_get_entity_id_from_tile(self):
        self.create_test_grid()
        self.game_state.spawn_entity(2, 2, "warrior")

        self.assertEqual(self.game_state.get_entity_id_from_tile(2, 2), 1)

    # Entities Exist
    # Checks entity-existence status before and after spawning.
    # Params: None
    # Returns: None
    def test_entities_exists(self):
        self.create_test_grid()

        self.assertFalse(self.game_state.entities_exists())

        self.create_spawned_entity()

        self.assertTrue(self.game_state.entities_exists())

    # Update Entity
    # Checks that updating an existing entity does not raise an error.
    # Params: None
    # Returns: None
    def test_update_entity(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.update_entity(1)

        self.assertEqual(self.game_state.get_entity_info_from_list(1).id, 1)

    # Update Missing Entity
    # Checks that updating a nonexistent entity safely does nothing.
    # Params: None
    # Returns: None
    def test_update_missing_entity(self):
        self.create_test_grid()

        self.game_state.update_entity(99)

        self.assertIsNone(self.game_state.get_entity_from_list(99))

    # Remove Entity From Game
    # Checks that removing an entity clears its tile and registration.
    # Params: None
    # Returns: None
    def test_remove_entity_from_game(self):
        self.create_test_grid()
        self.game_state.spawn_entity(1, 1, "warrior")

        self.game_state.remove_entity_from_game(1)

        self.assertIsNone(self.game_state.get_entity_from_list(1))
        self.assertFalse(self.game_state.entities_exists())
        self.assertFalse(self.game_state.is_grid_tile_occupied(1, 1))

    # Process Tick For All Entities
    # Checks that IDs of entities requiring removal are returned.
    # Params: None
    # Returns: None
    def test_process_tick_for_all_entities(self):
        self.create_test_grid()
        entity = self.create_spawned_entity()

        with patch.object(entity, "process_tick_on_entity", return_value=True):
            self.assertEqual(self.game_state.process_tick_for_all_entities(), [1])

    # Loot Tests

    # Spawn Loot
    # Checks that loot can be added to a tile.
    # Params: None
    # Returns: None
    def test_spawn_loot(self):
        self.create_test_grid()

        self.game_state.spawn_loot(1, 1, "ironsword")

        tile_info = self.game_state.get_game_tile_info(1, 1)
        self.assertIn("ironsword", tile_info.item_list[0].lower())

    # Add Item To Tile
    # Checks that an item can be added to a tile.
    # Params: None
    # Returns: None
    def test_add_item_to_tile(self):
        self.create_test_grid()

        self.game_state.add_item_to_tile(1, 1, "smallhealthpotion")

        tile_info = self.game_state.get_game_tile_info(1, 1)
        self.assertIn("smallhealthpotion", tile_info.item_list[0].lower())

    # Remove Item From Tile
    # Checks that an item can be removed from a tile.
    # Params: None
    # Returns: None
    def test_remove_item_from_tile(self):
        self.create_test_grid()
        self.game_state.add_item_to_tile(1, 1, "ironsword")

        removed_item = self.game_state.remove_item_from_tile(1, 1, "ironsword")

        self.assertEqual(removed_item.name.lower(), "ironsword")
        self.assertNotIn(
            "ironsword", self.game_state.get_game_tile_info(1, 1).item_list
        )

    # Backpack Tests

    # Add Item To Backpack Based On Info
    # Checks that an item can be added to an entity's backpack.
    # Params: None
    # Returns: None
    def test_add_item_to_backpack_based_on_info(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.add_item_to_backpack_based_on_info(1, "ironsword")

        self.assertIn("IronSword", self.get_backpack_names(1))

    # Remove Item From Backpack Based On Info
    # Checks that an item can be removed from an entity's backpack.
    # Params: None
    # Returns: None
    def test_remove_item_from_backpack_based_on_info(self):
        self.create_test_grid()
        self.create_spawned_entity()
        self.game_state.add_item_to_backpack_based_on_info(1, "ironsword")

        self.game_state.remove_item_from_backpack_based_on_info(1, "IronSword")

        self.assertNotIn("IronSword", self.get_backpack_names(1))

    # Update Inventory Based On Info
    # Checks that updating inventory preserves backpack items.
    # Params: None
    # Returns: None
    def test_update_inventory_based_on_info(self):
        self.create_test_grid()
        self.create_spawned_entity()
        self.game_state.add_item_to_backpack_based_on_info(1, "ironsword")

        self.game_state.update_inventory_based_on_info(1)

        self.assertIn("IronSword", self.get_backpack_names(1))

    # Equip Item Based On Info
    # Checks that equipping a weapon increases attack.
    # Params: None
    # Returns: None
    def test_equip_item_based_on_info(self):
        self.create_test_grid()
        self.create_spawned_entity()
        attack_before = self.game_state.get_entity_info_from_list(1).attack

        self.game_state.equip_item_based_on_info(1, "ironsword", "Weapon")
        self.game_state.update_entity(1)
        attack_after = self.game_state.get_entity_info_from_list(1).attack
        self.assertGreater(attack_after, attack_before)

    # Use Consumable
    # Checks that using a health potion restores health and removes it.
    # Params: None
    # Returns: None
    def test_use_consumable(self):
        self.create_test_grid()
        self.create_spawned_entity("warrior")
        self.game_state.add_item_to_backpack_based_on_info(1, "smallhealthpotion")
        self.game_state.update_single_entity_stat(1, "Health", 50)

        self.game_state.use_consumable(1, "SmallHealthPotion")

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertGreater(entity_info.health, 50)
        self.assertNotIn("SmallHealthPotion", self.get_backpack_names(1))

    # Movement Tests

    # Move Entity
    # Checks that moving an entity updates its position and grid occupancy.
    # Params: None
    # Returns: None
    def test_move_entity(self):
        self.create_test_grid()
        self.game_state.spawn_entity(0, 0, "warrior")

        self.game_state.move_entity(1, 2, 2)

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.position, [2, 2])
        self.assertFalse(self.game_state.is_grid_tile_occupied(0, 0))
        self.assertTrue(self.game_state.is_grid_tile_occupied(2, 2))

    # Combat Tests

    # Attack Entity
    # Checks that attacking returns damage and reduces defender health.
    # Params: None
    # Returns: None
    def test_attack_entity(self):
        self.create_test_grid()
        self.game_state.spawn_entity(0, 0, "warrior")
        self.game_state.spawn_entity(1, 0, "goblin")

        health_before = self.game_state.get_entity_info_from_list(2).health
        damage = self.game_state.attack_entity(1, 2)
        health_after = self.game_state.get_entity_info_from_list(2).health

        self.assertGreater(damage, 0)
        self.assertLess(health_after, health_before)

    # Cast Spell
    # Checks that a mage can cast Fireball on a target.
    # Params: None
    # Returns: None
    def test_cast_spell(self):
        self.create_test_grid()
        self.game_state.spawn_entity(0, 0, "mage")
        self.game_state.spawn_entity(1, 0, "goblin")

        health_before = self.game_state.get_entity_info_from_list(2).health
        effect = self.game_state.cast_spell(1, 2, "Fireball")
        health_after = self.game_state.get_entity_info_from_list(2).health

        self.assertIsNotNone(effect)
        self.assertLess(health_after, health_before)

    # Stat Tests

    # Update Single Entity Stat
    # Checks that a single entity stat can be updated.
    # Params: None
    # Returns: None
    def test_update_single_entity_stat(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.update_single_entity_stat(1, "Health", 50)

        self.assertEqual(self.game_state.get_entity_info_from_list(1).health, 50)

    # Add Temp Buff To Entity
    # Checks that a temporary buff can be added.
    # Params: None
    # Returns: None
    def test_add_temp_buff_to_entity(self):
        self.create_test_grid()
        self.create_spawned_entity()

        buff = {
            "Name": "TestBuff",
            "Effects": {"Flat_modifiers": {"Attack": "+2"}, "Percent_modifiers": {}},
            "Turns": 3,
        }

        self.game_state.add_temp_buff_to_entity(1, buff)

        buffs = self.game_state.get_entity_info_from_list(1).temp_buffs
        self.assertIn("TestBuff", [temp_buff[0][1] for temp_buff in buffs])

    # Spell Tests

    # Get Spell Info
    # Checks that spell information can be retrieved by name.
    # Params: None
    # Returns: None
    def test_get_spell_info(self):
        spell_info = self.game_state.get_spell_info("fireball")

        self.assertEqual(spell_info.name, "Fireball")
        self.assertEqual(spell_info.spell_type, "Offensive")

    # Placeholder Tests

    # Checks that the Memento preserves the game state's current values.
    # Checks that the Memento preserves the game state's current values.
    def test_create_memento(self):
        self.create_test_grid(5, 6)
        self.create_spawned_entity("warrior", 1, 2)

        command_manager = CommandManager()

        memento = self.game_state.create_memento(command_manager)

        self.assertIsInstance(memento, GameState.Memento)
        self.assertIsNotNone(memento.grid_memento)
        self.assertEqual(memento.grid_memento.width, 5)
        self.assertEqual(memento.grid_memento.height, 6)
        self.assertEqual(len(memento.entity_mementos), 1)

        # Get the base Entity Memento if the entity is a Mage.
        entity_memento = memento.entity_mementos[0]

        if isinstance(entity_memento, ent.Mage.Memento):
            entity_memento = entity_memento.entity_memento

        self.assertEqual(entity_memento.entity_id, 1)
        self.assertEqual(memento.entity_ids_issued, 2)
        self.assertTrue(memento.map_created)
        self.assertEqual(memento.turn_number, 1)
        self.assertTrue(memento.is_saved)

        # Check that creating a Memento marks the game state as saved.
        self.assertTrue(self.game_state.get_game_state_info()[2])

    # Checks that creating a Memento works when no grid or entities exist.
    def test_create_memento_empty_game_state(self):
        command_manager = CommandManager()
        memento = self.game_state.create_memento(command_manager)

        self.assertIsNone(memento.grid_memento)
        self.assertEqual(memento.entity_mementos, ())
        self.assertEqual(memento.entity_ids_issued, 1)
        self.assertFalse(memento.map_created)
        self.assertEqual(memento.turn_number, 1)

    # Checks that restoring a Memento restores the grid and entity state.
    def test_restore_memento(self):
        self.create_test_grid(5, 6)
        entity = self.create_spawned_entity("warrior", 1, 2)
        command_manager = CommandManager()
        game_state_manager = GameStateManager()
        original_memento = self.game_state.create_memento(command_manager)

        self.game_state.restore(original_memento, command_manager, game_state_manager)

        restored_memento = self.game_state.create_memento(command_manager)

        self.assertEqual(
            restored_memento.grid_memento.width, original_memento.grid_memento.width
        )
        self.assertEqual(
            restored_memento.grid_memento.height, original_memento.grid_memento.height
        )

        self.assertEqual(
            len(restored_memento.entity_mementos), len(original_memento.entity_mementos)
        )

        for restored_entity, original_entity in zip(
            restored_memento.entity_mementos, original_memento.entity_mementos
        ):
            # Access the base Entity Memento for each entity.
            if isinstance(original_entity, ent.Mage.Memento):
                restored_base = restored_entity.entity_memento
                original_base = original_entity.entity_memento
            else:
                restored_base = restored_entity
                original_base = original_entity

            self.assertEqual(restored_base.entity_id, original_base.entity_id)
            self.assertEqual(restored_base.e_type, original_base.e_type)
            self.assertEqual(restored_base.position, original_base.position)
            self.assertEqual(restored_base.health, original_base.health)
            self.assertEqual(restored_base.max_health, original_base.max_health)
            self.assertEqual(restored_base.attack, original_base.attack)
            self.assertEqual(restored_base.defence, original_base.defence)
            self.assertEqual(restored_base.speed, original_base.speed)
            self.assertEqual(
                restored_base.inventory.data[0].name,
                original_base.inventory.data[0].name,
            )
            self.assertEqual(
                restored_base.active_modifiers, original_base.active_modifiers
            )
            self.assertEqual(restored_base.backpack, original_base.backpack)
            self.assertEqual(restored_base.attack_type, original_base.attack_type)
            self.assertEqual(restored_base.temp_buffs, original_base.temp_buffs)

            # Compare Mage-specific state when applicable.
            if isinstance(original_entity, ent.Mage.Memento):
                self.assertEqual(restored_entity.mana, original_entity.mana)
                self.assertEqual(restored_entity.max_mana, original_entity.max_mana)
                self.assertEqual(
                    restored_entity.spell_power, original_entity.spell_power
                )

        self.assertEqual(
            restored_memento.entity_ids_issued, original_memento.entity_ids_issued
        )
        self.assertEqual(restored_memento.turn_number, original_memento.turn_number)
        self.assertIsNot(self.game_state.get_entity_from_list(1), entity)
        # testing
        game_state_manager = GameStateManager()
        self.game_state.restore(original_memento, command_manager, game_state_manager)

        print("Getter result:", self.game_state.get_game_state_info())
        self.assertFalse(self.game_state.get_game_state_info()[2])
        # Check that restoring marks the game state as unsaved.
        self.assertFalse(self.game_state.get_game_state_info()[2])

    # Checks that restoring an invalid Memento raises a TypeError.
    def test_restore_invalid_memento(self):
        with self.assertRaises(TypeError):
            self.game_state.restore(None)

    # Checks that restoring a Memento with no grid clears the current grid.
    def test_restore_memento_without_grid(self):
        self.create_test_grid()
        command_manager_memento1 = CommandManager().create_memento()
        command_manager = CommandManager()
        memento = GameState.Memento(
            grid_memento=None,
            entity_mementos=(),
            entity_ids_issued=1,
            map_created=False,
            turn_number=1,
            is_saved=True,
            command_manager_memento=command_manager_memento1,
        )
        game_state_manager = GameStateManager()
        self.game_state.restore(memento, command_manager, game_state_manager)

        restored_memento = self.game_state.create_memento(command_manager)

        self.assertIsNone(restored_memento.grid_memento)
        self.assertEqual(restored_memento.entity_mementos, ())
        self.assertFalse(restored_memento.map_created)

    # Checks that restoring a Memento reconstructs multiple entity types.
    def test_restore_memento_multiple_entities(self):
        self.create_test_grid()
        self.create_spawned_entity("warrior", 0, 0)
        self.game_state.spawn_entity(1, 1, "mage")
        self.game_state.spawn_entity(2, 2, "goblin")
        command_manager = CommandManager()
        game_state_manager = GameStateManager()
        memento = self.game_state.create_memento(command_manager)

        self.game_state.restore(memento, command_manager, game_state_manager)

        restored_memento = self.game_state.create_memento(command_manager)

        self.assertEqual(len(restored_memento.entity_mementos), 3)

        self.assertEqual(
            len(restored_memento.entity_mementos), len(memento.entity_mementos)
        )

        for restored_entity, original_entity in zip(
            restored_memento.entity_mementos, memento.entity_mementos
        ):
            if isinstance(original_entity, ent.Mage.Memento):
                restored_type = restored_entity.entity_memento.e_type
                original_type = original_entity.entity_memento.e_type
            else:
                restored_type = restored_entity.e_type
                original_type = original_entity.e_type

            self.assertEqual(restored_type, original_type)
        self.assertEqual(
            [
                (
                    entity.entity_memento.entity_id
                    if isinstance(entity, ent.Mage.Memento)
                    else entity.entity_id
                )
                for entity in restored_memento.entity_mementos
            ],
            [1, 2, 3],
        )

    # Checks that restored entities preserve their inventory and backpack contents.
    def test_restore_memento_preserves_entity_items(self):
        self.create_test_grid()
        self.create_spawned_entity("warrior")
        command_manager = CommandManager()
        original_backpack = self.get_backpack_names(1)
        game_state_manager = GameStateManager()
        memento = self.game_state.create_memento(command_manager)

        self.game_state.restore(memento, command_manager, game_state_manager)

        self.assertEqual(self.get_backpack_names(1), original_backpack)

    # Checks that modifying the live game state does not change an existing Memento.
    def test_memento_preserves_original_state(self):
        self.create_test_grid()
        self.create_spawned_entity("warrior", 1, 1)
        command_manager = CommandManager()
        memento = self.game_state.create_memento(command_manager)

        self.game_state.spawn_entity(2, 2, "mage")

        self.assertEqual(len(memento.entity_mementos), 1)
        self.assertEqual(memento.entity_mementos[0].position.data, [1, 1])

    # Checks that restoring a Memento marks the game state as saved.
    def test_restore_memento_marks_game_as_saved(self):
        self.create_test_grid()
        self.create_spawned_entity("warrior")
        command_manager = CommandManager()
        game_state_manager = GameStateManager()
        memento = self.game_state.create_memento(command_manager)

        self.game_state.restore(memento, command_manager, game_state_manager)

        restored_memento = self.game_state.create_memento(command_manager)

        self.assertTrue(restored_memento.is_saved)

    # Checks that game state information is returned correctly.
    def test_get_game_state_info(self):
        self.create_test_grid(5, 6)
        self.create_spawned_entity("warrior", 1, 2)

        game_state_info = self.game_state.get_game_state_info()

        self.assertEqual(game_state_info[0], 1)
        self.assertEqual(game_state_info[1], 1)
        self.assertFalse(game_state_info[2])

    # Checks that an uninitialized game state is not active.
    def test_game_state_is_active_false(self):
        self.assertFalse(self.game_state.game_state_is_active())

    # Checks that a game state with an initialized grid is active.
    def test_game_state_is_active_true(self):
        self.create_test_grid(5, 6)

        self.assertTrue(self.game_state.game_state_is_active())

    # Test Undo Spawn
    def test_undo_spawn(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.undo_spawn(1)

        self.assertIsNone(self.game_state.get_entity_from_list(1))

    # Test Undo Spawn Decreases Entity Counter
    def test_undo_spawn_decreases_entity_counter(self):
        self.create_test_grid()
        self.create_spawned_entity()

        self.game_state.undo_spawn(1)

        # Spawn another entity and verify its ID
        self.game_state.spawn_entity(1, 1, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertIsNotNone(entity_info)

    # Test Undo Spawn Removes Entity From Grid
    def test_undo_spawn_removes_entity_from_grid(self):
        self.create_test_grid()
        self.create_spawned_entity(x=0, y=0)

        self.game_state.undo_spawn(1)

        # Verify the entity no longer occupies its original tile
        self.assertIsNone(self.game_state.get_entity_id_from_tile(0, 0))

        # Test Restore Entity Health

    def test_restore_entity_health(self):
        self.create_test_grid()
        self.create_spawned_entity()

        original_health = self.game_state.get_entity_info_from_list(1).health

        self.game_state.update_single_entity_stat(1, "Health", 100)
        self.game_state.restore_entity_health(1, 20)

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.health, original_health)

    # Test Restore Entity Health With Partial Damage
    def test_restore_entity_health_partial_damage(self):
        self.create_test_grid()
        self.create_spawned_entity()

        damage = 10

        self.game_state.update_single_entity_stat(1, "Health", 100)
        self.game_state.restore_entity_health(1, damage)

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.health, 110)

    # Test Restore Entity Health With Zero Damage
    def test_restore_entity_health_zero_damage(self):
        self.create_test_grid()
        self.create_spawned_entity()

        original_health = self.game_state.get_entity_info_from_list(1).health

        self.game_state.restore_entity_health(1, 0)

        entity_info = self.game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.health, original_health)

    # Success
    def test_undo_cast_restores_mana_and_health(self):
        # Create test grid
        self.create_test_grid()

        # Create caster and target
        self.create_spawned_entity("mage")
        self.game_state.spawn_entity(1, 1, "goblin")

        # Set original stats
        self.game_state.update_single_entity_stat(1, "Mana", 100)
        self.game_state.update_single_entity_stat(2, "Health", 45)

        # Change stats to simulate casting a spell
        self.game_state.update_single_entity_stat(1, "Mana", 75)
        self.game_state.update_single_entity_stat(2, "Health", 20)

        # Undo the spell cast
        self.game_state.undo_cast(1, 2, 100, 45)

        # Get updated entity info
        caster_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        # Check restored stats
        self.assertEqual(caster_info.mana, 100)
        self.assertEqual(target_info.health, 45)

    # Success
    def test_undo_cast_marks_game_state_as_unsaved(self):
        # Create test grid
        self.create_test_grid()

        # Create caster and target
        self.create_spawned_entity("mage")
        self.game_state.spawn_entity(1, 1, "goblin")

        # Mark game state as saved
        self.game_state.mark_as_saved()

        # Undo the spell cast
        self.game_state.undo_cast(1, 2, 100, 45)

        # Check game state is marked as unsaved
        self.assertFalse(self.game_state._GameState__is_saved)

    # Success
    def test_undo_cast_restores_mana_without_changing_other_stats(self):
        # Create test grid
        self.create_test_grid()

        # Create caster and target
        self.create_spawned_entity("mage")
        self.game_state.spawn_entity(1, 1, "goblin")

        # Get original target attack
        original_attack = self.game_state.get_entity_info_from_list(2).attack

        # Set mana and health to restore
        self.game_state.undo_cast(1, 2, 100, 45)

        # Get updated entity info
        caster_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        # Check restored stats
        self.assertEqual(caster_info.mana, 100)
        self.assertEqual(target_info.health, 45)

        # Check unrelated stats remain unchanged
        self.assertEqual(target_info.attack, original_attack)

    # Success
    def test_get_equipped_item_info_returns_matching_slot(self):
        # Create GameState
        test_game_state = GameState.__new__(GameState)

        # Create equipped items
        weapon = MagicMock()
        weapon.name = "Iron Sword"
        weapon.slot = "Weapon"

        armor = MagicMock()
        armor.name = "Iron Chestplate"
        armor.slot = "Armor"

        # Create entity info
        entity_info = MagicMock()
        entity_info.inventory = [weapon, armor]

        # Mock entity info lookup
        test_game_state.get_entity_info_from_list = MagicMock(return_value=entity_info)

        # Get equipped weapon info
        result = test_game_state.get_equipped_item_info(1, "Weapon")

        # Verify result
        self.assertIs(result, weapon)
        test_game_state.get_entity_info_from_list.assert_called_once_with(1)

    # Success
    def test_get_equipped_item_info_returns_matching_slot_case_insensitive(self):
        # Create GameState
        test_game_state = GameState.__new__(GameState)

        # Create equipped item
        weapon = MagicMock()
        weapon.name = "Iron Sword"
        weapon.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.inventory = [weapon]

        # Mock entity info lookup
        test_game_state.get_entity_info_from_list = MagicMock(return_value=entity_info)

        # Get equipped item info
        result = test_game_state.get_equipped_item_info(1, "weapon")

        # Verify result
        self.assertIs(result, weapon)

    # Success
    def test_get_equipped_item_info_accepts_equipment_slot_enum(self):
        # Create GameState
        test_game_state = GameState.__new__(GameState)

        # Create equipped item
        weapon = MagicMock()
        weapon.name = "Iron Sword"
        weapon.slot = "Weapon"

        # Create entity info
        entity_info = MagicMock()
        entity_info.inventory = [weapon]

        # Mock entity info lookup
        test_game_state.get_entity_info_from_list = MagicMock(return_value=entity_info)

        # Get equipped item info
        result = test_game_state.get_equipped_item_info(1, dl.EquipmentSlot.WEAPON)

        # Verify result
        self.assertIs(result, weapon)

    # Failure
    def test_get_equipped_item_info_returns_none_for_empty_slot(self):
        # Create GameState
        test_game_state = GameState.__new__(GameState)

        # Create equipped item
        armor = MagicMock()
        armor.name = "Iron Chestplate"
        armor.slot = "Armor"

        # Create entity info
        entity_info = MagicMock()
        entity_info.inventory = [armor]

        # Mock entity info lookup
        test_game_state.get_entity_info_from_list = MagicMock(return_value=entity_info)

        # Get item info for an empty slot
        result = test_game_state.get_equipped_item_info(1, "Weapon")

        # Verify result
        self.assertIsNone(result)

    # Failure
    def test_get_equipped_item_info_returns_none_for_invalid_slot(self):
        # Create GameState
        test_game_state = GameState.__new__(GameState)

        # Create entity info
        entity_info = MagicMock()
        entity_info.inventory = []

        # Mock entity info lookup
        test_game_state.get_entity_info_from_list = MagicMock(return_value=entity_info)

        # Get item info for an invalid slot
        result = test_game_state.get_equipped_item_info(1, "Invalid")

        # Verify result
        self.assertIsNone(result)

    # Test get_nearest_player - no players
    def test_get_nearest_player_no_players(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertIsNone(result)

    # Test get_nearest_player - single warrior
    def test_get_nearest_player_single_warrior(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(4, 2, "warrior")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertEqual(result.id, 2)

    # Test get_nearest_player - single mage
    def test_get_nearest_player_single_mage(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 5, "mage")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertEqual(result.id, 2)

    # Test get_nearest_player - closest of two players
    def test_get_nearest_player_two_players(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(3, 2, "warrior")
        self.game_state.spawn_entity(6, 6, "mage")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertEqual(result.id, 2)

    # Test get_nearest_player - ignores monsters
    def test_get_nearest_player_ignores_monsters(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(2, 2, "skeleton")
        self.game_state.spawn_entity(5, 2, "warrior")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertEqual(result.id, 3)

    # Test get_nearest_player - unreachable player
    def test_get_nearest_player_unreachable(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(3, 3, "warrior")

        # Surround Warrior with walls
        self.game_state.set_game_grid_tile(2, 3, "wall")
        self.game_state.set_game_grid_tile(4, 3, "wall")
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertIsNone(result)

    # Test get_nearest_player - chooses reachable player
    def test_get_nearest_player_reachable_over_blocked(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(3, 3, "warrior")
        self.game_state.spawn_entity(5, 5, "mage")

        # Surround Warrior with walls
        self.game_state.set_game_grid_tile(2, 3, "wall")
        self.game_state.set_game_grid_tile(4, 3, "wall")
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertEqual(result.id, 3)

    # Test get_nearest_player - shortest path instead of Manhattan
    def test_get_nearest_player_shortest_path(self):
        self.create_test_grid(7, 7)

        # Goblin
        self.game_state.spawn_entity(1, 2, "goblin")

        # Warrior is geometrically closer
        self.game_state.spawn_entity(5, 2, "warrior")

        # Mage has shorter walking path
        self.game_state.spawn_entity(1, 5, "mage")

        # Wall blocks direct route to Warrior
        for y in range(4):
            self.game_state.set_game_grid_tile(3, y, "wall")

        goblin_info = self.game_state.get_entity_info_from_list(1)

        result = self.game_state.get_nearest_player(goblin_info)

        # Mage should be selected
        self.assertEqual(result.id, 3)

    # Test get_nearest_player - no grid
    def test_get_nearest_player_no_grid(self):
        # No grid has been created
        goblin_info = MagicMock()
        goblin_info.position = [1, 2]

        result = self.game_state.get_nearest_player(goblin_info)

        self.assertIsNone(result)

    # Test get_distance_between_entities - no grid
    def test_get_distance_between_entities_no_grid(self):
        entity_info = MagicMock()
        entity_info.position = [1, 2]

        target_info = MagicMock()
        target_info.position = [4, 2]

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_distance_between_entities - horizontal path
    def test_get_distance_between_entities_horizontal(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertEqual(result, 4)

    # Test get_distance_between_entities - diagonal positions
    def test_get_distance_between_entities_diagonal(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(4, 4, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertEqual(result, 6)

    # Test get_distance_between_entities - path around wall
    def test_get_distance_between_entities_around_wall(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")

        # Block direct path
        self.game_state.set_game_grid_tile(3, 2, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertEqual(result, 6)

    # Test get_distance_between_entities - unreachable target
    def test_get_distance_between_entities_unreachable(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(3, 3, "warrior")

        # Surround target with walls
        self.game_state.set_game_grid_tile(2, 3, "wall")
        self.game_state.set_game_grid_tile(4, 3, "wall")
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_distance_between_entities - occupied tile blocks path
    def test_get_distance_between_entities_occupied_corridor(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")
        self.game_state.spawn_entity(3, 2, "skeleton")

        # Create corridor
        for x in range(7):
            self.game_state.set_game_grid_tile(x, 1, "wall")
            self.game_state.set_game_grid_tile(x, 3, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_distance_between_entities(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_flee_position - no grid
    def test_get_flee_position_no_grid(self):
        entity_info = MagicMock()
        entity_info.position = [2, 2]

        target_info = MagicMock()
        target_info.position = [3, 2]

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_flee_position - flee left
    def test_get_flee_position_left(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(4, 3, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        # Block alternative escape routes
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertEqual(result, [2, 3])

    # Test get_flee_position - flee right
    def test_get_flee_position_right(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(2, 3, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        # Block alternative escape routes
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertEqual(result, [4, 3])

    # Test get_flee_position - flee upward
    def test_get_flee_position_up(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(3, 2, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertEqual(result, [3, 4])

    # Test get_flee_position - flee downward
    def test_get_flee_position_down(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(3, 4, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertEqual(result, [3, 2])

    # Test get_flee_position - surrounded by walls
    def test_get_flee_position_surrounded_by_walls(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(5, 5, "warrior")

        # Surround monster with walls
        self.game_state.set_game_grid_tile(2, 3, "wall")
        self.game_state.set_game_grid_tile(4, 3, "wall")
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_flee_position - occupied escape tile
    def test_get_flee_position_occupied_tile(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(4, 3, "warrior")

        # Occupy preferred escape tile
        self.game_state.spawn_entity(2, 3, "skeleton")

        # Block other escape routes
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_flee_position - alternative escape tile
    def test_get_flee_position_alternative_tile(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(3, 3, "goblin")
        self.game_state.spawn_entity(4, 3, "warrior")

        # Block left escape route
        self.game_state.set_game_grid_tile(2, 3, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        # Both vertical directions increase distance
        self.assertIn(result, [[3, 2], [3, 4]])

    # Test get_flee_position - does not move closer
    def test_get_flee_position_no_better_tile(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(0, 0, "goblin")
        self.game_state.spawn_entity(1, 1, "warrior")

        # Block both possible escape tiles
        self.game_state.set_game_grid_tile(1, 0, "wall")
        self.game_state.set_game_grid_tile(0, 1, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertIsNone(result)

    # Test get_flee_position - stays within grid bounds
    def test_get_flee_position_grid_boundary(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(0, 0, "goblin")
        self.game_state.spawn_entity(1, 0, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_flee_position(entity_info, target_info)

        self.assertEqual(result, [0, 1])

    # Test get_shortest_path_between_entities - no grid
    def test_get_shortest_path_between_entities_no_grid(self):
        entity_info = MagicMock()
        entity_info.position = [1, 2]

        target_info = MagicMock()
        target_info.position = [4, 2]

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        self.assertIsNone(result)

    # Test get_shortest_path_between_entities - horizontal path
    def test_get_shortest_path_between_entities_horizontal(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        expected_path = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]

        self.assertEqual(result, expected_path)

    # Test get_shortest_path_between_entities - diagonal path
    def test_get_shortest_path_between_entities_diagonal(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(4, 4, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        self.assertIsNotNone(result)
        self.assertEqual(result[0], (1, 1))
        self.assertEqual(result[-1], (4, 4))
        self.assertEqual(len(result), 7)

    # Test get_shortest_path_between_entities - around wall
    def test_get_shortest_path_between_entities_around_wall(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")

        # Block direct path
        self.game_state.set_game_grid_tile(3, 2, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        self.assertIsNotNone(result)
        self.assertEqual(result[0], (1, 2))
        self.assertEqual(result[-1], (5, 2))
        self.assertEqual(len(result), 7)
        self.assertNotIn((3, 2), result)

    # Test get_shortest_path_between_entities - unreachable target
    def test_get_shortest_path_between_entities_unreachable(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 1, "goblin")
        self.game_state.spawn_entity(3, 3, "warrior")

        # Surround target with walls
        self.game_state.set_game_grid_tile(2, 3, "wall")
        self.game_state.set_game_grid_tile(4, 3, "wall")
        self.game_state.set_game_grid_tile(3, 2, "wall")
        self.game_state.set_game_grid_tile(3, 4, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        self.assertIsNone(result)

    # Test get_shortest_path_between_entities - occupied corridor
    def test_get_shortest_path_between_entities_occupied_corridor(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")
        self.game_state.spawn_entity(3, 2, "skeleton")

        # Create corridor
        for x in range(7):
            self.game_state.set_game_grid_tile(x, 1, "wall")
            self.game_state.set_game_grid_tile(x, 3, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        self.assertIsNone(result)

    # Test get_shortest_path_between_entities - occupied target
    def test_get_shortest_path_between_entities_occupied_target(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(4, 2, "warrior")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        result = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        expected_path = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
        ]

        self.assertEqual(result, expected_path)

    # Test get_shortest_path_between_entities - distance consistency
    def test_get_shortest_path_between_entities_matches_distance(self):
        self.create_test_grid(7, 7)

        self.game_state.spawn_entity(1, 2, "goblin")
        self.game_state.spawn_entity(5, 2, "warrior")

        # Place obstacle
        self.game_state.set_game_grid_tile(3, 2, "wall")

        entity_info = self.game_state.get_entity_info_from_list(1)
        target_info = self.game_state.get_entity_info_from_list(2)

        path = self.game_state.get_shortest_path_between_entities(
            entity_info, target_info
        )

        distance = self.game_state.get_distance_between_entities(
            entity_info, target_info
        )

        self.assertIsNotNone(path)
        self.assertEqual(distance, len(path) - 1)
        self.assertEqual(distance, 6)


# Run the tests
if __name__ == "__main__":
    unittest.main()
