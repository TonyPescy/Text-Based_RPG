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
from unittest.mock import patch

import domain_library as dl
from game_state import GameState
import equipment


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

    # Create Momento
    # Checks the current placeholder method returns None.
    # Params: None
    # Returns: None
    def test_create_momento_placeholder(self):
        self.assertIsNone(GameState.create_momento())

    # Restore Momento
    # Checks the current placeholder method returns None.
    # Params: None
    # Returns: None
    def test_restore_momento_placeholder(self):
        self.assertIsNone(GameState.restore(None))


# Run the tests
if __name__ == "__main__":
    unittest.main()
