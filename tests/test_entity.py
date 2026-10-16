"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 21, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_entity.py
Purpose: Utilizes unittest to test all of the classes and methods in entity.py file
"""

"""
NOTE: These commands are written with the idea that they will only be called with
the correct typing or the expected correct parameters from the CLIs process command. 
As such this testing may lack certain cases. This is handled in the CLI, which is
why the CLI test file is far larger than any other test file. To avoid the extra 
redundant code in this file as well as the grid.py, we will only be looking at 
cases that can be tested without an entire refactor of all of the entire game logic.

TLDR: This will primarily test only success cases as any and all error handling of 
these functions are handled within the CLI prior to calling this function.
"""

# Imports
import unittest

import domain_library as dl
from entity import Warrior, Mage, Goblin, Skeleton, create_entity
from equipment import Consumable
from game_state import GameState


# Class for testing entities
class TestEntity(unittest.TestCase):

    # Set Up Test
    # Resets the shared default inventory before each test.
    # Params: None
    # Returns: None
    def setUp(self):
        # Each entity must receive fresh empty equipment slots.
        dl.BASE_INVENTORY = [
            dl.create_equipment("none_wep"),
            dl.create_equipment("none_armor"),
            dl.create_equipment("none_acc"),
        ]

    # Repeated Test Functions

    # Create Test Entity
    # Creates an entity with a clean set of modifiers and inventory.
    # Params: entity_class - Entity class to create
    #         entity_id - int - entity ID
    #         position - list - entity position
    # Returns: entity - Entity - created entity
    def create_test_entity(self, entity_class, entity_id=1, position=None):
        if position is None:
            position = [0, 0]
        return entity_class(entity_id, position)

    # Create Test Game State
    # Creates a game state with a test grid.
    # Params: None
    # Returns: GameState - game state with a 5 by 5 grid
    def create_test_game_state(self):
        game_state = GameState()
        game_state.create_grid(5, 5)
        return game_state

    # Create Spawned Entity
    # Creates and registers an entity in the game state.
    # Params: game_state - GameState - active game state
    #         entity_type - str - type of entity
    #         x/y - int - entity position
    # Returns: Entity - registered entity
    def create_spawned_entity(self, game_state, entity_type="warrior", x=0, y=0):
        game_state.spawn_entity(x, y, entity_type)
        return game_state.get_entity_from_list(1)

    # Assert Base Stats
    # Checks common entity stats.
    # Params: entity_info - EntityInfo - entity information
    #         health/attack/defence/speed - expected stat values
    # Returns: None
    def assert_base_stats(self, entity_info, health, attack, defence, speed):
        self.assertEqual(entity_info.health, health)
        self.assertEqual(entity_info.attack, attack)
        self.assertEqual(entity_info.defence, defence)
        self.assertEqual(entity_info.speed, speed)

    # Get Modifier Dictionary
    # Converts immutable modifier information to a dictionary for assertions.
    # Params: entity_info - EntityInfo - entity information
    # Returns: dict - flat and percent modifiers
    def get_modifiers(self, entity_info):
        return {
            modifier_type: dict(modifiers)
            for modifier_type, modifiers in entity_info.active_modifiers
        }

    # Create Item
    # Creates an equipment item from the domain library.
    # Params: item_name - str - item key
    # Returns: Equipment - created item
    def create_item(self, item_name):
        return dl.create_equipment(item_name)

    # Init for all entity types

    # Init Warrior with base stats
    def test_warrior_init(self):
        entity = self.create_test_entity(Warrior, 0)
        entity_info = entity.get_info()
        self.assertEqual(entity_info.id, 0)
        self.assertEqual(entity_info.e_type, "warrior")
        self.assertEqual(entity_info.position, [0, 0])
        self.assert_base_stats(entity_info, 120, 15, 10, 5)
        self.assertEqual(entity_info.max_health, 120)
        self.assertEqual(entity_info.backpack, ())
        self.assertEqual(entity_info.temp_buffs, ())
        self.assertEqual(entity_info.attack_type.value, "Melee")
        self.assertEqual(
            self.get_modifiers(entity_info),
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )

    # Init Goblin with base stats
    def test_goblin_init(self):
        entity = self.create_test_entity(Goblin, 0)
        entity_info = entity.get_info()
        self.assertEqual(entity_info.id, 0)
        self.assertEqual(entity_info.e_type, "goblin")
        self.assertEqual(entity_info.position, [0, 0])
        self.assert_base_stats(entity_info, 45, 12, 3, 6)
        self.assertEqual(entity_info.max_health, 45)
        self.assertEqual(entity_info.backpack, ())
        self.assertEqual(entity_info.temp_buffs, ())
        self.assertEqual(entity_info.attack_type.value, "Melee")

    # Init Skeleton with base stats
    def test_skeleton_init(self):
        entity = self.create_test_entity(Skeleton, 0)
        entity_info = entity.get_info()
        self.assertEqual(entity_info.id, 0)
        self.assertEqual(entity_info.e_type, "skeleton")
        self.assertEqual(entity_info.position, [0, 0])
        self.assert_base_stats(entity_info, 60, 10, 8, 4)
        self.assertEqual(entity_info.max_health, 60)
        self.assertEqual(entity_info.backpack, ())
        self.assertEqual(entity_info.temp_buffs, ())
        self.assertEqual(entity_info.attack_type.value, "Ranged")

    # Init Mage with base stats
    def test_mage_init(self):
        entity = self.create_test_entity(Mage, 0)
        entity_info = entity.get_info()
        self.assertEqual(entity_info.id, 0)
        self.assertEqual(entity_info.e_type, "mage")
        self.assertEqual(entity_info.position, [0, 0])
        self.assert_base_stats(entity_info, 70, 8, 4, 5)
        self.assertEqual(entity_info.max_health, 70)
        self.assertEqual(entity_info.mana, 100)
        self.assertEqual(entity_info.max_mana, 100)
        self.assertEqual(entity_info.spell_power, 25)
        self.assertEqual(entity_info.backpack, ())
        self.assertEqual(entity_info.temp_buffs, ())

    # Tests for get_info and get_stat

    # Get info returns entity state
    def test_get_info_returns_entity_state(self):
        entity = self.create_test_entity(Warrior, 4, [2, 3])
        entity_info = entity.get_info()
        self.assertEqual(entity_info.id, 4)
        self.assertEqual(entity_info.position, [2, 3])
        self.assertEqual(entity_info.e_type, "warrior")

    # Get stat returns requested stat
    def test_get_stat_returns_common_stats(self):
        entity = self.create_test_entity(Warrior, 0)
        self.assertEqual(entity.get_stat("Health"), 120)
        self.assertEqual(entity.get_stat("Attack"), 15)
        self.assertEqual(entity.get_stat("Defence"), 10)
        self.assertEqual(entity.get_stat("Speed"), 5)

    # Get stat returns Mage-only stats
    def test_get_stat_returns_mage_stats(self):
        entity = self.create_test_entity(Mage, 0)
        self.assertEqual(entity.get_stat("Mana"), 100)
        self.assertEqual(entity.get_stat("Spell_power"), 25)

    # Tests for reset_stats

    # Reset stats restores Warrior base values
    def test_reset_stats_on_warrior(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.update_single_stat("Health", 1)
        entity.update_single_stat("Attack", 1)
        entity.update_single_stat("Defence", 1)
        entity.update_single_stat("Speed", 1)
        entity.reset_stats()
        self.assert_base_stats(entity.get_info(), 120, 15, 10, 5)

    # Reset stats restores Mage base values
    def test_reset_stats_on_mage(self):
        entity = self.create_test_entity(Mage, 0)
        entity.update_single_stat("Health", 1)
        entity.update_single_stat("Mana", 1)
        entity.update_single_stat("Attack", 1)
        entity.update_single_stat("Defence", 1)
        entity.update_single_stat("Speed", 1)
        entity.reset_stats()
        entity_info = entity.get_info()
        self.assert_base_stats(entity_info, 70, 8, 4, 5)
        self.assertEqual(entity_info.mana, 100)
        self.assertEqual(entity_info.spell_power, 25)

    # Tests for handle_modifiers

    # Handle flat modifier
    def test_handle_flat_modifier(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Attack", "+5")
        self.assertEqual(
            self.get_modifiers(entity.get_info())["Flat_modifiers"],
            {"Attack": 5},
        )

    # Handle percent modifier
    def test_handle_percent_modifier(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Attack", "+25%")
        self.assertEqual(
            self.get_modifiers(entity.get_info())["Percent_modifiers"],
            {"Attack": 25},
        )

    # Handle multiple modifiers of the same type
    def test_handle_multiple_flat_modifiers(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Attack", "-5")
        entity.handle_modifiers("Attack", "+10")
        self.assertEqual(
            self.get_modifiers(entity.get_info())["Flat_modifiers"],
            {"Attack": 5},
        )

    # Handle multiple percent modifiers
    def test_handle_multiple_percent_modifiers(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Attack", "+10%")
        entity.handle_modifiers("Attack", "+20%")
        self.assertEqual(
            self.get_modifiers(entity.get_info())["Percent_modifiers"],
            {"Attack": 30},
        )

    # Tests for calculate_final_stats

    # Calculate final stats with flat modifiers
    def test_calculate_final_stats_with_flat_modifiers(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Health", "+20")
        entity.handle_modifiers("Attack", "+5")
        entity.handle_modifiers("Defence", "+3")
        entity.handle_modifiers("Speed", "+2")
        entity.calculate_final_stats()
        self.assert_base_stats(entity.get_info(), 140, 20, 13, 7)

    # Calculate final stats with percent modifiers
    def test_calculate_final_stats_with_percent_modifiers(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Health", "+10%")
        entity.handle_modifiers("Attack", "+20%")
        entity.handle_modifiers("Defence", "+50%")
        entity.handle_modifiers("Speed", "+100%")
        entity.calculate_final_stats()
        self.assert_base_stats(entity.get_info(), 132, 18, 15, 10)

    # Calculate final stats with flat and percent modifiers
    def test_calculate_final_stats_with_flat_and_percent_modifiers(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_modifiers("Health", "+20")
        entity.handle_modifiers("Health", "+10%")
        entity.handle_modifiers("Attack", "+5")
        entity.handle_modifiers("Attack", "+20%")
        entity.handle_modifiers("Defence", "-2")
        entity.handle_modifiers("Defence", "+50%")
        entity.handle_modifiers("Speed", "+3")
        entity.handle_modifiers("Speed", "+100%")
        entity.calculate_final_stats()
        self.assert_base_stats(entity.get_info(), 154, 24, 12, 16)

    # Tests for update_stats with GameState

    # Update stats with no modifiers
    def test_update_stats_with_no_modifiers(self):
        game_state = self.create_test_game_state()
        entity = self.create_test_entity(Warrior, 0)
        entity.update_stats(game_state)
        self.assert_base_stats(entity.get_info(), 120, 15, 10, 5)
        self.assertEqual(
            self.get_modifiers(entity.get_info()),
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )

    # Update stats applies tile modifiers
    def test_update_stats_on_shallow_water(self):
        game_state = self.create_test_game_state()
        game_state.set_game_grid_tile(0, 0, "shallowwater")
        entity = self.create_test_entity(Warrior, 0)
        entity.update_stats(game_state)
        self.assert_base_stats(entity.get_info(), 120, 15, 10, 3)
        self.assertEqual(
            self.get_modifiers(entity.get_info())["Flat_modifiers"],
            {"Speed": -2},
        )

    # Update stats does not double modifiers
    def test_update_stats_does_not_double_modifiers(self):
        game_state = self.create_test_game_state()
        entity = self.create_test_entity(Warrior, 0)
        item = self.create_item("ironsword")
        entity.equip_item(item, "weapon")
        entity.update_stats(game_state)
        first_attack = entity.get_info().attack
        entity.update_stats(game_state)
        self.assertEqual(first_attack, 27)
        self.assertEqual(entity.get_info().attack, 27)

    # Tests for inventory and equipment

    # Equip weapon through GameState
    def test_equip_weapon_based_on_info(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.add_item_to_backpack_based_on_info(1, "ironsword")
        game_state.equip_item_based_on_info(1, "ironsword", "weapon")
        entity_info = entity.get_info()
        self.assertEqual(entity_info.attack, 27)
        self.assertIn("IronSword", [item.name for item in entity_info.backpack])

    # Equip armor through GameState
    def test_equip_armor_based_on_info(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.add_item_to_backpack_based_on_info(1, "ironchestplate")
        game_state.equip_item_based_on_info(1, "ironchestplate", "armor")
        entity_info = entity.get_info()
        self.assertEqual(entity_info.speed, 3)
        self.assertIn("IronChestplate", [item.name for item in entity_info.backpack])

    # Update inventory reconciles backpack and equipment
    def test_update_inventory_preserves_backpack_items(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.add_item_to_backpack(self.create_item("ironsword"))
        entity.update_inventory()
        self.assertIn("IronSword", [item.name for item in entity.get_info().backpack])

    # Remove item from backpack
    def test_remove_item_from_backpack(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.add_item_to_backpack(self.create_item("ironsword"))
        entity.remove_item_from_backpack("IronSword")
        self.assertNotIn("IronSword", entity.get_info().backpack)

    # Tests for entity factory

    # Create Warrior
    def test_create_entity_warrior(self):
        entity = create_entity("warrior", 5, 10, 4)
        self.assertEqual(entity.get_info().e_type, "warrior")
        self.assertEqual(entity.get_info().id, 4)
        self.assertEqual(entity.get_info().position, [5, 10])

    # Create Mage
    def test_create_entity_mage(self):
        entity = create_entity("mage", 5, 10, 4)
        self.assertEqual(entity.get_info().e_type, "mage")
        self.assertEqual(entity.get_info().position, [5, 10])

    # Create Skeleton
    def test_create_entity_skeleton(self):
        entity = create_entity("skeleton", 5, 10, 4)
        self.assertEqual(entity.get_info().e_type, "skeleton")
        self.assertEqual(entity.get_info().position, [5, 10])

    # Create Goblin
    def test_create_entity_goblin(self):
        entity = create_entity("goblin", 5, 10, 4)
        self.assertEqual(entity.get_info().e_type, "goblin")
        self.assertEqual(entity.get_info().position, [5, 10])

    # Tests for consumables

    # Use small health potion
    def test_use_small_health_potion(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.update_single_entity_stat(1, "Health", 50)
        game_state.use_consumable(1, "smallhealthpotion")
        self.assertEqual(entity.get_info().health, 70)

    # Use greater health potion
    def test_use_greater_health_potion(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.update_single_entity_stat(1, "Health", 50)
        game_state.use_consumable(1, "greaterhealthpotion")
        self.assertEqual(entity.get_info().health, 100)

    # Use superior health potion and cap at max health
    def test_use_superior_health_potion_caps_at_max_health(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.update_single_entity_stat(1, "Health", 50)
        game_state.use_consumable(1, "superiorhealthpotion")
        self.assertEqual(entity.get_info().health, 120)

    # Use Mana potion
    def test_use_mana_potion(self):
        game_state = self.create_test_game_state()
        game_state.spawn_entity(0, 0, "mage")
        entity = game_state.get_entity_from_list(1)
        game_state.update_single_entity_stat(1, "Mana", 25)
        game_state.use_consumable(1, "manapotion")
        self.assertEqual(entity.get_info().mana, 75)

    # Use over-time consumable
    def test_use_turtle_master_potion_adds_temporary_buff(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.use_consumable(1, "turtlemasterpotion")
        entity_info = entity.get_info()
        buff_names = [dict(buff)["Name"] for buff in entity_info.temp_buffs]
        self.assertIn("TurtleMasterPotion", buff_names)

    # Tests for combat

    # Attack with greater attack than defence
    def test_attack_entity_with_attack_greater_than_defence(self):
        attacker = self.create_test_entity(Warrior, 0)
        defender = self.create_test_entity(Goblin, 1, [1, 0])
        damage = attacker.attack_entity(defender)
        self.assertEqual(damage, 12)
        self.assertEqual(defender.get_info().health, 33)
        self.assertEqual(attacker.get_info().health, 120)

    # Attack deals minimum damage of one
    def test_attack_entity_minimum_damage(self):
        attacker = self.create_test_entity(Warrior, 0)
        defender = self.create_test_entity(Goblin, 1)
        attacker.update_single_stat("Attack", 1)
        defender.update_single_stat("Defence", 10)
        damage = attacker.attack_entity(defender)
        self.assertEqual(damage, 1)
        self.assertEqual(defender.get_info().health, 44)

    # Attack cannot reduce health below zero
    def test_attack_entity_does_not_reduce_health_below_zero(self):
        attacker = self.create_test_entity(Warrior, 0)
        defender = self.create_test_entity(Goblin, 1)
        defender.update_single_stat("Health", 5)
        damage = attacker.attack_entity(defender)
        self.assertEqual(damage, 12)
        self.assertEqual(defender.get_info().health, 0)
        self.assertFalse(defender.is_alive())

    # Attack marks defeated target as dead
    def test_attack_entity_marks_target_dead(self):
        attacker = self.create_test_entity(Warrior, 0)
        defender = self.create_test_entity(Goblin, 1)
        defender.update_single_stat("Health", 1)
        attacker.attack_entity(defender)
        self.assertFalse(defender.is_alive())
        self.assertFalse(Warrior.is_alive_from_info(defender.get_info()))

    # Tests for temporary buffs

    # Add temporary buff
    def test_add_temp_buff(self):
        entity = self.create_test_entity(Warrior, 0)
        buff = {
            "Name": "AttackBuff",
            "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
            "Turns": 2,
        }
        entity.add_temp_buff(buff)
        entity_info = entity.get_info()
        self.assertEqual(len(entity_info.temp_buffs), 1)
        self.assertEqual(dict(entity_info.temp_buffs[0])["Name"], "AttackBuff")

    # Update temporary buff duration
    def test_update_temp_buffs_decrements_turns(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.add_temp_buff(
            {
                "Name": "AttackBuff",
                "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
                "Turns": 2,
            }
        )
        self.assertEqual(entity.update_temp_buffs(), [])
        buff_info = dict(entity.get_info().temp_buffs[0])
        self.assertEqual(buff_info["Turns"], 1)

    # Remove expired temporary buff
    def test_remove_expired_temp_buff(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.add_temp_buff(
            {
                "Name": "AttackBuff",
                "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
                "Turns": 1,
            }
        )
        buffs_to_remove = entity.update_temp_buffs()
        self.assertEqual(buffs_to_remove, ["AttackBuff"])
        self.assertFalse(entity.remove_temp_buffs(buffs_to_remove))
        self.assertEqual(entity.get_info().temp_buffs, ())

    # Tests for alive status and death

    # Entity is alive without a Dead status
    def test_is_alive_without_dead_status(self):
        entity = self.create_test_entity(Warrior, 0)
        self.assertTrue(entity.is_alive())
        self.assertTrue(Warrior.is_alive_from_info(entity.get_info()))

    # Entity is dead with Dead status
    def test_is_alive_with_dead_status(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_death()
        self.assertFalse(entity.is_alive())
        self.assertFalse(Warrior.is_alive_from_info(entity.get_info()))

    # Handle death adds Dead status
    def test_handle_death_adds_dead_status(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_death()
        self.assertFalse(entity.is_alive())
        self.assertEqual(dict(entity.get_info().temp_buffs[0])["Name"], "Dead")

    # Process tick without buffs
    def test_process_tick_without_buffs(self):
        entity = self.create_test_entity(Warrior, 0)
        self.assertFalse(entity.process_tick_on_entity())

    # Process tick removes expired buff
    def test_process_tick_removes_expired_buff(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.add_temp_buff(
            {
                "Name": "AttackBuff",
                "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
                "Turns": 1,
            }
        )
        self.assertFalse(entity.process_tick_on_entity())
        self.assertEqual(entity.get_info().temp_buffs, ())

    # Process tick signals that a dead entity should be removed
    def test_process_tick_on_dead_entity(self):
        entity = self.create_test_entity(Warrior, 0)
        entity.handle_death()
        self.assertTrue(entity.process_tick_on_entity())

    # Tests for GameState entity management

    # Spawn entity registers it in GameState
    def test_game_state_spawn_entity(self):
        game_state = self.create_test_game_state()
        game_state.spawn_entity(2, 3, "warrior")
        entity_info = game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.id, 1)
        self.assertEqual(entity_info.e_type, "warrior")
        self.assertEqual(entity_info.position, [2, 3])
        self.assertTrue(game_state.is_grid_tile_occupied(2, 3))

    # Move entity updates its position
    def test_game_state_move_entity(self):
        game_state = self.create_test_game_state()
        game_state.spawn_entity(0, 0, "warrior")
        game_state.move_entity(1, 2, 2)
        entity_info = game_state.get_entity_info_from_list(1)
        self.assertEqual(entity_info.position, [2, 2])
        self.assertFalse(game_state.is_grid_tile_occupied(0, 0))
        self.assertTrue(game_state.is_grid_tile_occupied(2, 2))

    # GameState attack returns damage
    def test_game_state_attack_entity(self):
        game_state = self.create_test_game_state()
        game_state.spawn_entity(0, 0, "warrior")
        game_state.spawn_entity(1, 0, "goblin")
        damage = game_state.attack_entity(1, 2)
        self.assertEqual(damage, 12)
        self.assertEqual(game_state.get_entity_info_from_list(2).health, 33)


if __name__ == "__main__":
    unittest.main()
