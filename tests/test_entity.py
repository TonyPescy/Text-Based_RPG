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
from dataclasses import replace
from copy import deepcopy
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch
from entity_state import DefendingState, AttackingState, FleeingState, RagingState
import domain_library as dl
from entity import Warrior, Mage, Goblin, Skeleton, Ogre, create_entity, Entity
import equipment
from game_state import GameState


# Class for testing entities
class TestEntity(unittest.TestCase):

    def setUp(self):
        # Give each test fresh default equipment and an isolated game state.
        dl.BASE_INVENTORY = [
            equipment.create_equipment("none_wep"),
            equipment.create_equipment("none_armor"),
            equipment.create_equipment("none_acc"),
        ]
        self.game_state = self.create_test_game_state()

    def create_test_entity(self, entity_class=Warrior, entity_id=1, position=None):
        return entity_class(
            entity_id, list(position) if position is not None else [0, 0]
        )

    def create_test_game_state(self):
        game_state = GameState()
        game_state.create_grid(5, 5)
        return game_state

    def create_test_enemy(self, entity_class, entity_id=1, position=None):
        enemy = self.create_test_entity(entity_class, entity_id, position)
        enemy.initialize_state_manager(self.game_state)
        return enemy, self.game_state

    def create_spawned_entity(self, game_state=None, entity_type="warrior", x=0, y=0):
        game_state = game_state if game_state is not None else self.game_state
        game_state.spawn_entity(x, y, entity_type)
        return game_state.get_entity_from_list(1)

    def create_item(self, item_name="ironsword"):
        item = equipment.create_equipment(item_name)
        self.assertIsNotNone(
            item, f"Equipment factory does not recognize {item_name!r}"
        )
        return item

    def create_equipment_memento(self, item_name="ironsword"):
        return self.create_item(item_name).create_memento()

    def create_inventory_memento(self, *item_mementos):
        return Entity.InventoryMemento(data=tuple(item_mementos))

    def create_backpack_memento(self, *item_mementos):
        return Entity.BackpackMemento(items=tuple(item_mementos))

    def create_test_buff(self, name="AttackBuff", turns=2, stat="Attack", amount=5):
        return {
            "Name": name,
            "Effects": {"Flat_modifiers": {stat: amount}, "Percent_modifiers": {}},
            "Turns": turns,
        }

    def assert_base_stats(self, entity_info, health, attack, defence, speed):
        self.assertEqual(
            (
                entity_info.health,
                entity_info.attack,
                entity_info.defence,
                entity_info.speed,
            ),
            (health, attack, defence, speed),
        )

    def get_modifiers(self, entity_info):
        return {
            modifier_type: dict(modifiers)
            for modifier_type, modifiers in entity_info.active_modifiers
        }

    def assert_item_mementos_equal(self, expected, actual):
        self.assertEqual(expected, actual)
        self.assertEqual(type(expected), type(actual))

    def assert_entity_items_round_trip(self, entity):
        original = entity.create_memento()
        restored = self.create_test_entity(type(entity), entity.get_info().id)
        restored.restore(original)
        actual = restored.create_memento()
        self.assertEqual(original.inventory, actual.inventory)
        self.assertEqual(original.backpack, actual.backpack)
        return restored

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
        game_state.update_entity(1)
        entity_info = entity.get_info()
        self.assertEqual(entity_info.attack, 27)
        self.assertIn("IronSword", [item.name for item in entity_info.backpack])

    # Equip armor through GameState
    def test_equip_armor_based_on_info(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state)
        game_state.add_item_to_backpack_based_on_info(1, "ironchestplate")
        game_state.equip_item_based_on_info(1, "ironchestplate", "armor")
        game_state.update_entity(1)
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
        self.assertNotIn(
            "IronSword", [item.name for item in entity.get_info().backpack]
        )

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
        self.assertEqual(damage, 5)
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
        entity.process_tick_on_entity()
        entity.process_tick_on_entity()
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

    def test_entity_create_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_memento()

        self.assertIsInstance(memento, Entity.Memento)
        self.assertEqual(memento.entity_id, 1)
        self.assertEqual(memento.e_type, "warrior")

        # Check nested Mementos
        self.assertIsInstance(memento.position, Entity.PositionMemento)
        self.assertIsInstance(memento.inventory, Entity.InventoryMemento)
        self.assertIsInstance(memento.active_modifiers, Entity.ActiveModifiersMemento)
        self.assertIsInstance(memento.backpack, Entity.BackpackMemento)
        self.assertIsInstance(memento.temp_buffs, Entity.TempBuffsMemento)

        # Check saved values
        self.assertEqual(memento.position.data, [2, 3])
        self.assertEqual(memento.health, memento.max_health)
        self.assertEqual(memento.attack, 15)
        self.assertEqual(memento.defence, 10)
        self.assertEqual(memento.speed, 5)
        self.assertEqual(len(memento.inventory.data), len(dl.BASE_INVENTORY))
        self.assertEqual(memento.backpack.items, ())
        self.assertEqual(memento.temp_buffs.data, [])

    # Restore Entity Memento
    # Checks that restoring a Memento restores the entity's saved state.
    # Params: None
    # Returns: None
    def test_entity_restore_memento(self):
        entity = self.create_test_entity(Warrior)
        original_memento = entity.create_memento()

        memento = replace(
            original_memento,
            entity_id=2,
            position=Entity.PositionMemento(data=[4, 5]),
            health=50,
            attack=20,
            defence=8,
            speed=7,
        )

        entity.restore(memento)
        restored_memento = entity.create_memento()

        self.assertEqual(restored_memento.entity_id, 2)
        self.assertEqual(restored_memento.position.data, [4, 5])
        self.assertEqual(restored_memento.health, 50)
        self.assertEqual(restored_memento.attack, 20)
        self.assertEqual(restored_memento.defence, 8)
        self.assertEqual(restored_memento.speed, 7)

    # Restore Invalid Entity Memento
    # Checks that restoring an invalid Memento raises a TypeError.
    # Params: None
    # Returns: None
    def test_entity_restore_invalid_memento(self):
        entity = self.create_test_entity(Warrior)

        with self.assertRaises(TypeError):
            entity.restore(None)

    # Entity Memento Deep Copy
    # Checks that changing the entity's position does not change its saved Memento.
    # Params: None
    # Returns: None
    def test_entity_memento_deep_copy(self):
        entity = self.create_test_entity(Warrior, position=[0, 0])

        memento = entity.create_memento()

        changed_memento = replace(memento, position=Entity.PositionMemento(data=[5, 5]))

        entity.restore(changed_memento)

        self.assertEqual(memento.position.data, [0, 0])

    # Restore Entity Memento Deep Copy
    # Checks that modifying nested Memento data does not affect the restored entity.
    # Params: None
    # Returns: None
    def test_entity_restore_memento_deep_copy(self):
        entity = self.create_test_entity(Warrior)
        entity.add_temp_buff(
            {
                "Name": "Strength",
                "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
                "Turns": 2,
            }
        )

        memento = entity.create_memento()

        entity.restore(memento)

        # Change the nested Memento data after restoring.
        memento.position.data.append(4)
        memento.temp_buffs.data[0]["Turns"] = 99

        restored_memento = entity.create_memento()

        self.assertEqual(restored_memento.position.data, [0, 0])
        self.assertEqual(restored_memento.temp_buffs.data[0]["Turns"], 2)

    # Tests for Mage Memento

    # Create Mage Memento
    # Checks that the Mage Memento preserves inherited and Mage-specific state.
    # Params: None
    # Returns: None
    def test_mage_create_memento(self):
        mage = self.create_test_entity(Mage, 1, [2, 3])

        memento = mage.create_memento()

        self.assertIsInstance(memento, Mage.Memento)
        self.assertIsInstance(memento.entity_memento, Entity.Memento)

        self.assertEqual(memento.entity_memento.entity_id, 1)
        self.assertEqual(memento.entity_memento.e_type, "mage")
        self.assertEqual(memento.entity_memento.position.data, [2, 3])
        self.assertEqual(memento.entity_memento.health, 70)
        self.assertEqual(memento.entity_memento.attack, 8)
        self.assertEqual(memento.entity_memento.defence, 4)
        self.assertEqual(memento.entity_memento.speed, 5)

        self.assertEqual(memento.mana, memento.max_mana)
        self.assertEqual(memento.max_mana, 100)
        self.assertEqual(memento.spell_power, 25)

    # Restore Mage Memento
    # Checks that restoring a Mage Memento restores inherited and Mage-specific state.
    # Params: None
    # Returns: None
    def test_mage_restore_memento(self):
        mage = self.create_test_entity(Mage)
        original_memento = mage.create_memento()

        changed_entity_memento = replace(
            original_memento.entity_memento,
            entity_id=2,
            position=Entity.PositionMemento(data=[4, 5]),
            health=30,
            attack=12,
            defence=6,
            speed=4,
        )

        memento = Mage.Memento(
            entity_memento=changed_entity_memento,
            mana=25,
            max_mana=original_memento.max_mana,
            spell_power=40,
        )

        mage.restore(memento)
        restored_memento = mage.create_memento()

        self.assertEqual(restored_memento.entity_memento.entity_id, 2)
        self.assertEqual(restored_memento.entity_memento.position.data, [4, 5])
        self.assertEqual(restored_memento.entity_memento.health, 30)
        self.assertEqual(restored_memento.entity_memento.attack, 12)
        self.assertEqual(restored_memento.mana, 25)
        self.assertEqual(restored_memento.spell_power, 40)

    # Restore Invalid Mage Memento
    # Checks that restoring an invalid Memento raises a TypeError.
    # Params: None
    # Returns: None
    def test_mage_restore_invalid_memento(self):
        mage = self.create_test_entity(Mage)

        with self.assertRaises(TypeError):
            mage.restore(None)

    # Mage Memento Deep Copy
    # Checks that changing Mage state does not change its saved Memento.
    # Params: None
    # Returns: None
    def test_mage_memento_deep_copy(self):
        mage = self.create_test_entity(Mage, position=[0, 0])

        memento = mage.create_memento()

        changed_entity_memento = replace(
            memento.entity_memento, position=Entity.PositionMemento(data=[5, 5])
        )

        mage.restore(
            Mage.Memento(
                entity_memento=changed_entity_memento,
                mana=10,
                max_mana=memento.max_mana,
                spell_power=50,
            )
        )

        self.assertEqual(memento.entity_memento.position.data, [0, 0])
        self.assertEqual(memento.mana, 100)
        self.assertEqual(memento.spell_power, 25)

    # Restore Mage Memento Deep Copy
    # Checks that modifying nested Memento data does not affect the restored Mage.
    # Params: None
    # Returns: None
    def test_mage_restore_memento_deep_copy(self):
        mage = self.create_test_entity(Mage)
        mage.add_temp_buff(
            {
                "Name": "Strength",
                "Effects": {"Flat_modifiers": {"Attack": 5}, "Percent_modifiers": {}},
                "Turns": 2,
            }
        )

        memento = mage.create_memento()

        mage.restore(memento)

        # Change the nested Memento data after restoring.
        memento.entity_memento.position.data.append(4)
        memento.entity_memento.temp_buffs.data[0]["Turns"] = 99

        restored_memento = mage.create_memento()

        self.assertEqual(restored_memento.entity_memento.position.data, [0, 0])
        self.assertEqual(restored_memento.entity_memento.temp_buffs.data[0]["Turns"], 2)
        self.assertEqual(restored_memento.mana, 100)
        self.assertEqual(restored_memento.spell_power, 25)

    def test_entity_create_inventory_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_inventory_memento()

        self.assertIsInstance(memento, Entity.InventoryMemento)
        self.assertEqual(len(memento.data), len(dl.BASE_INVENTORY))

    def test_entity_restore_inventory(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])
        original = entity.create_inventory_memento()
        entity.equip_item(self.create_item("ironsword"), "weapon")
        entity.restore_inventory(original)
        self.assertEqual(entity.create_inventory_memento(), original)
        self.assertTrue(
            all(
                item is None or hasattr(item, "create_memento")
                for item in entity._Entity__inventory
            )
        )

    def test_entity_restore_inventory_invalid_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        with self.assertRaises(TypeError):
            entity.restore_inventory("invalid")

    def test_entity_create_position_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_position_memento()

        self.assertIsInstance(memento, Entity.PositionMemento)
        self.assertEqual(memento.data, [2, 3])

    def test_entity_restore_position(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_position_memento()

        # Change position
        entity.move_to(4, 5)

        # Restore original position
        entity.restore_position(memento)

        self.assertEqual(
            entity.create_position_memento().data,
            [2, 3],
        )

    def test_entity_restore_position_invalid_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        with self.assertRaises(TypeError):
            entity.restore_position("invalid")

    def test_entity_create_active_modifiers_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_active_modifiers_memento()

        self.assertIsInstance(memento, Entity.ActiveModifiersMemento)
        self.assertEqual(memento.data, {"Flat_modifiers": {}, "Percent_modifiers": {}})

    def test_entity_restore_active_modifiers(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_active_modifiers_memento()

        # Restore original modifiers
        entity.restore_active_modifiers(memento)

        self.assertEqual(
            entity.create_active_modifiers_memento().data,
            memento.data,
        )

    def test_entity_restore_active_modifiers_invalid_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        with self.assertRaises(TypeError):
            entity.restore_active_modifiers("invalid")

    def test_entity_create_temp_buffs_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_temp_buffs_memento()

        self.assertIsInstance(memento, Entity.TempBuffsMemento)
        self.assertEqual(memento.data, [])

    def test_entity_restore_temp_buffs(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_temp_buffs_memento()

        # Add a temporary buff
        entity.add_temp_buff(
            {
                "name": "Test Buff",
                "effects": {"Attack": 5},
                "duration": 3,
            }
        )

        # Restore original buffs
        entity.restore_temp_buffs(memento)

        self.assertEqual(
            entity.create_temp_buffs_memento().data,
            memento.data,
        )

    def test_entity_restore_temp_buffs_invalid_memento(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        with self.assertRaises(TypeError):
            entity.restore_temp_buffs("invalid")

    def test_entity_position_memento_is_independent(self):
        entity = self.create_test_entity(Warrior, 1, [2, 3])

        memento = entity.create_position_memento()

        # Modify the original position list
        entity.move_to(4, 5)

        # Memento should retain its original position
        self.assertEqual(memento.data, [2, 3])

    # Tests for Entity State Manager

    # Create State Manager Memento - Warrior
    # Checks that player entities have no behavioral state
    def test_create_state_manager_memento_warrior(self):
        entity = self.create_test_entity(Warrior)

        memento = entity.create_state_manager_memento()

        self.assertIsInstance(memento, Entity.StateManagerMemento)
        self.assertIsNone(memento.state_name)

    # Create State Manager Memento - Mage
    # Checks that Mage entities have no behavioral state
    def test_create_state_manager_memento_mage(self):
        entity = self.create_test_entity(Mage)

        memento = entity.create_state_manager_memento()

        self.assertIsInstance(memento, Entity.StateManagerMemento)
        self.assertIsNone(memento.state_name)

    # Create State Manager Memento - Goblin
    # Checks that the current Goblin state is saved
    def test_create_state_manager_memento_goblin(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state, "goblin")

        memento = entity.create_state_manager_memento()

        self.assertIsInstance(memento, Entity.StateManagerMemento)
        self.assertEqual(memento.state_name, "Defending")

    # Create State Manager Memento - Skeleton
    # Checks that the current Skeleton state is saved
    def test_create_state_manager_memento_skeleton(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state, "skeleton")

        memento = entity.create_state_manager_memento()

        self.assertEqual(memento.state_name, "Defending")

    # State Manager Memento Is Frozen
    # Checks that the saved state name cannot be reassigned
    def test_state_manager_memento_frozen(self):
        memento = Entity.StateManagerMemento(state_name="Defending")

        with self.assertRaises(FrozenInstanceError):
            memento.state_name = "Attacking"

    # Restore State Manager - Defending
    # Checks that a Goblin can restore DefendingState
    def test_restore_state_manager_defending(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name="Defending")

        entity.restore_state_manager(memento, game_state)

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    # Restore State Manager - Attacking
    # Checks that a Goblin can restore AttackingState
    def test_restore_state_manager_attacking(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name="Attacking")

        entity.restore_state_manager(memento, game_state)

        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Restore State Manager - Fleeing
    # Checks that a Goblin can restore FleeingState
    def test_restore_state_manager_fleeing(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name="Fleeing")

        entity.restore_state_manager(memento, game_state)

        self.assertEqual(entity.get_entity_state_name(), "Fleeing")

    # Restore State Manager - Skeleton
    # Checks that Skeleton entities can restore their state
    def test_restore_state_manager_skeleton(self):
        entity = self.create_test_entity(Skeleton)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name="Attacking")

        entity.restore_state_manager(memento, game_state)

        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Restore State Manager - Player
    # Checks that player entities can restore a None state
    def test_restore_state_manager_player(self):
        entity = self.create_test_entity(Warrior)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name=None)

        entity.restore_state_manager(memento, game_state)

        self.assertIsNone(entity.get_entity_state_name())

    # Restore State Manager - Mage
    # Checks that Mage entities can restore a None state
    def test_restore_state_manager_mage(self):
        entity = self.create_test_entity(Mage)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name=None)

        entity.restore_state_manager(memento, game_state)

        self.assertIsNone(entity.get_entity_state_name())

    # Restore State Manager - Invalid Memento
    # Checks that invalid Memento types raise TypeError
    def test_restore_state_manager_invalid_memento(self):
        entity = self.create_test_entity(Goblin)

        with self.assertRaises(TypeError):
            entity.restore_state_manager("invalid", None)

    # Restore State Manager - Missing Enemy State
    # Checks that enemy entities cannot restore a None state
    def test_restore_state_manager_enemy_none(self):
        entity = self.create_test_entity(Goblin)

        memento = Entity.StateManagerMemento(state_name=None)

        with self.assertRaises(ValueError):
            entity.restore_state_manager(memento, None)

    # Restore State Manager - Player With Enemy State
    # Checks that player entities cannot restore enemy states
    def test_restore_state_manager_player_invalid_state(self):
        entity = self.create_test_entity(Warrior)

        memento = Entity.StateManagerMemento(state_name="Attacking")

        with self.assertRaises(ValueError):
            entity.restore_state_manager(memento, None)

    # Restore State Manager - Invalid State Name
    # Checks that unknown behavioral states raise ValueError
    def test_restore_state_manager_invalid_state_name(self):
        entity = self.create_test_entity(Goblin)

        memento = Entity.StateManagerMemento(state_name="Unknown")

        with self.assertRaises(ValueError):
            entity.restore_state_manager(memento, None)

    # Initialize State Manager - Goblin
    # Checks that Goblins initialize in DefendingState
    def test_initialize_state_manager_goblin(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    # Initialize State Manager - Skeleton
    # Checks that Skeletons initialize in DefendingState
    def test_initialize_state_manager_skeleton(self):
        entity = self.create_test_entity(Skeleton)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    # Initialize State Manager - Warrior
    # Checks that Warriors do not receive a state manager
    def test_initialize_state_manager_warrior(self):
        entity = self.create_test_entity(Warrior)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        self.assertIsNone(entity.get_entity_state_name())

    # Initialize State Manager - Mage
    # Checks that Mages do not receive a state manager
    def test_initialize_state_manager_mage(self):
        entity = self.create_test_entity(Mage)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        self.assertIsNone(entity.get_entity_state_name())

    # Initialize State Manager - Preserve Existing State
    # Checks that reconnecting does not reset the current state
    def test_initialize_state_manager_preserves_state(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        memento = Entity.StateManagerMemento(state_name="Fleeing")

        entity.restore_state_manager(memento, None)
        entity.initialize_state_manager(game_state)

        self.assertEqual(entity.get_entity_state_name(), "Fleeing")

    # Get Entity State Name - Uninitialized
    # Checks that entities without a manager return None
    def test_get_entity_state_name_uninitialized(self):
        entity = self.create_test_entity(Goblin)

        self.assertIsNone(entity.get_entity_state_name())

    # Get Entity State Name - Initialized
    # Checks that the current behavioral state is returned
    def test_get_entity_state_name_initialized(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    # Update Entity State - No Manager
    # Checks that player entities do not update AI states
    def test_update_entity_state_no_manager(self):
        entity = self.create_test_entity(Warrior)

        result = entity.update_entity_state()

        self.assertIsNone(result)

    # Update Entity State - Calls Manager Update
    # Checks that updating an enemy delegates to its state manager
    def test_update_entity_state_calls_manager(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        entity.initialize_state_manager(game_state)

        # Mock the State Manager update method
        with patch(
            "entity.EntityStateManager.update", return_value=True
        ) as mock_update:
            result = entity.update_entity_state()

        mock_update.assert_called_once_with()
        self.assertTrue(result)

    # State Manager Memento - Round Trip
    # Checks that a saved behavioral state can be restored
    def test_state_manager_memento_round_trip(self):
        entity = self.create_test_entity(Goblin)
        game_state = self.create_test_game_state()

        # Restore an attacking state
        entity.restore_state_manager(
            Entity.StateManagerMemento("Attacking"), game_state
        )

        # Save the current state
        memento = entity.create_state_manager_memento()

        # Change the state
        entity.restore_state_manager(
            Entity.StateManagerMemento("Defending"), game_state
        )

        # Restore the saved state
        entity.restore_state_manager(memento, game_state)

        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Entity Memento - Includes State Manager
    # Checks that the full Entity Memento includes behavioral state
    def test_entity_memento_includes_state_manager(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state, "goblin")

        memento = entity.create_memento()

        self.assertIsInstance(memento.state_manager, Entity.StateManagerMemento)
        self.assertEqual(memento.state_manager.state_name, "Defending")

    # Entity Memento - Restore Behavioral State
    # Checks that restoring an Entity Memento restores AI state
    def test_entity_memento_restores_state_manager(self):
        game_state = self.create_test_game_state()
        entity = self.create_spawned_entity(game_state, "goblin")

        # Set initial state to Attacking
        entity.restore_state_manager(
            Entity.StateManagerMemento("Attacking"), game_state
        )

        # Save full entity Memento
        memento = entity.create_memento()

        # Change current state to Defending
        entity.restore_state_manager(
            Entity.StateManagerMemento("Defending"), game_state
        )

        # Restore full entity Memento
        entity.restore(memento)

        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    # Ogre and State Manager Tests

    def test_ogre_init(self):
        entity = self.create_test_entity(Ogre, 0)
        entity_info = entity.get_info()

        self.assertEqual(entity_info.e_type, "ogre")
        self.assertEqual(entity.get_entity_state_name(), None)

        game_state = self.create_test_game_state()
        entity.initialize_state_manager(game_state)

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    def test_create_entity_ogre(self):
        entity = create_entity("ogre", 2, 3, 7)
        self.assertIsInstance(entity, Ogre)
        self.assertEqual(entity.get_info().position, [2, 3])
        self.assertEqual(entity.get_info().id, 7)

    def test_create_entity_ogre_case_insensitive(self):
        entity = create_entity("OGRE", 2, 3, 7)
        self.assertIsInstance(entity, Ogre)

    def test_ogre_state_manager_memento(self):
        entity, game_state = self.create_test_enemy(Ogre)
        memento = entity.create_state_manager_memento()
        self.assertEqual(memento.state_name, "Defending")

    def test_ogre_restore_raging_state(self):
        entity = self.create_test_entity(Ogre)
        entity.restore_state_manager(Entity.StateManagerMemento("Raging"), None)
        self.assertEqual(entity.get_entity_state_name(), "Raging")
        self.assertEqual(entity.get_info().state_manager, "Raging")

    def test_goblin_cannot_restore_raging_state(self):
        entity = self.create_test_entity(Goblin)
        with self.assertRaises(ValueError):
            entity.restore_state_manager(Entity.StateManagerMemento("Raging"), None)

    def test_skeleton_cannot_restore_raging_state(self):
        entity = self.create_test_entity(Skeleton)
        with self.assertRaises(ValueError):
            entity.restore_state_manager(Entity.StateManagerMemento("Raging"), None)

    def test_ogre_cannot_restore_missing_state(self):
        entity = self.create_test_entity(Ogre)
        with self.assertRaises(ValueError):
            entity.restore_state_manager(Entity.StateManagerMemento(None), None)

    def test_ogre_memento_preserves_raging_state(self):
        entity = self.create_test_entity(Ogre)
        entity.restore_state_manager(Entity.StateManagerMemento("Raging"), None)
        memento = entity.create_memento()
        self.assertEqual(memento.state_manager.state_name, "Raging")
        entity.restore_state_manager(Entity.StateManagerMemento("Defending"), None)
        entity.restore(memento)
        self.assertEqual(entity.get_entity_state_name(), "Raging")

    def test_transition_entity_state_without_manager(self):
        entity = self.create_test_entity(Warrior)
        with self.assertRaises(ValueError):
            entity.transition_entity_state(AttackingState())

    def test_transition_entity_state_goblin(self):
        entity, game_state = self.create_test_enemy(Goblin)
        entity.transition_entity_state(AttackingState())
        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    def test_transition_entity_state_invalid(self):
        entity, game_state = self.create_test_enemy(Goblin)

        with self.assertRaises(ValueError):
            entity.transition_entity_state(RagingState())

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    def test_transition_entity_state_ogre_cannot_flee(self):
        entity, game_state = self.create_test_enemy(Ogre)

        with self.assertRaises(ValueError):
            entity.transition_entity_state(FleeingState())

        self.assertEqual(entity.get_entity_state_name(), "Defending")

    def test_reconnect_state_manager_keeps_existing_state(self):
        entity, game_state = self.create_test_enemy(Goblin)
        entity.transition_entity_state(AttackingState())
        game_state = self.create_test_game_state()
        entity.reconnect_state_manager(game_state)
        self.assertEqual(entity.get_entity_state_name(), "Attacking")

    def test_reconnect_state_manager_does_not_add_player_state(self):
        entity = self.create_test_entity(Warrior)
        entity.reconnect_state_manager(self.create_test_game_state())
        self.assertIsNone(entity.get_entity_state_name())

    def test_ogre_get_info_exposes_state(self):
        entity, game_state = self.create_test_enemy(Ogre)
        self.assertEqual(entity.get_info().state_manager, "Defending")
        entity.transition_entity_state(AttackingState())
        self.assertEqual(entity.get_info().state_manager, "Attacking")

    # Additional inventory and backpack Memento tests

    def test_inventory_memento_contains_item_mementos(self):
        entity = self.create_test_entity()
        saved = entity.create_inventory_memento()
        self.assertEqual(len(saved.data), 3)
        for item in saved.data:
            self.assertIsInstance(item, equipment.EquipmentMemento)

    def test_inventory_memento_preserves_equipped_item(self):
        entity = self.create_test_entity()
        entity.equip_item(self.create_item("ironsword"), "weapon")
        saved = entity.create_inventory_memento()
        self.assertEqual(saved.data[0], entity.create_inventory_memento().data[0])
        self.assertEqual(saved.data[0].name, self.create_item("ironsword").name)

    def test_inventory_restore_preserves_full_item_memento(self):
        entity = self.create_test_entity()
        entity.equip_item(self.create_item("ironsword"), "weapon")
        saved = entity.create_inventory_memento()
        entity.restore_inventory(saved)
        self.assertEqual(entity.create_inventory_memento(), saved)

    def test_inventory_restore_supports_empty_slots(self):
        entity = self.create_test_entity()
        saved = self.create_inventory_memento(None, None, None)
        entity.restore_inventory(saved)
        self.assertEqual(entity.create_inventory_memento(), saved)

    def test_inventory_restore_rejects_invalid_item_memento(self):
        entity = self.create_test_entity()
        with self.assertRaises(TypeError):
            entity.restore_inventory(self.create_inventory_memento("not a memento"))

    def test_backpack_memento_empty(self):
        entity = self.create_test_entity()
        self.assertEqual(
            entity.create_backpack_memento(), self.create_backpack_memento()
        )

    def test_backpack_memento_preserves_equipment(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        saved = entity.create_backpack_memento()
        self.assertIsInstance(saved.items[0], equipment.EquipmentMemento)
        self.assertEqual(saved.items[0].name, self.create_item("ironsword").name)

    def test_backpack_restore_preserves_equipment(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        saved = entity.create_backpack_memento()
        entity.remove_item_from_backpack("IronSword")
        entity.restore_backpack(saved)
        self.assertEqual(entity.create_backpack_memento(), saved)

    def test_backpack_restore_rejects_invalid_memento(self):
        with self.assertRaises(TypeError):
            self.create_test_entity().restore_backpack("invalid")

    def test_backpack_restore_rejects_invalid_item_memento(self):
        with self.assertRaises(TypeError):
            self.create_test_entity().restore_backpack(
                self.create_backpack_memento("invalid item")
            )

    def test_backpack_restores_duplicate_items_independently(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        entity.add_item_to_backpack(self.create_item("ironsword"))
        saved = entity.create_backpack_memento()
        entity.restore_backpack(saved)
        self.assertEqual(entity.create_backpack_memento(), saved)
        items = entity._Entity__backpack
        self.assertIsNot(items[0], items[1])

    def test_backpack_memento_independent_of_later_changes(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        saved = entity.create_backpack_memento()
        entity.remove_item_from_backpack("IronSword")
        self.assertEqual(len(saved.items), 1)
        self.assertEqual(entity.create_backpack_memento().items, ())

    def test_backpack_restore_consumable(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("smallhealthpotion"))
        saved = entity.create_backpack_memento()
        self.assertIsInstance(saved.items[0], equipment.ConsumableMemento)
        entity.restore_backpack(saved)
        self.assertEqual(entity.create_backpack_memento(), saved)

    def test_backpack_restore_mixed_equipment_and_consumables(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        entity.add_item_to_backpack(self.create_item("smallhealthpotion"))
        saved = entity.create_backpack_memento()
        entity.restore_backpack(saved)
        self.assertEqual(entity.create_backpack_memento(), saved)
        self.assertIsInstance(saved.items[0], equipment.EquipmentMemento)
        self.assertIsInstance(saved.items[1], equipment.ConsumableMemento)

    def test_entity_full_memento_restores_items(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        entity.add_item_to_backpack(self.create_item("smallhealthpotion"))
        entity.equip_item(self.create_item("ironsword"), "weapon")
        self.assert_entity_items_round_trip(entity)

    def test_mage_full_memento_restores_items(self):
        mage = self.create_test_entity(Mage)
        mage.add_item_to_backpack(self.create_item("smallhealthpotion"))
        original = mage.create_memento()
        restored = self.create_test_entity(Mage)
        restored.restore(original)
        self.assertEqual(restored.create_memento(), original)

    def test_restored_equipment_is_new_object(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("ironsword"))
        original_item = entity._Entity__backpack[0]
        saved = entity.create_backpack_memento()
        entity.restore_backpack(saved)
        self.assertIsNot(entity._Entity__backpack[0], original_item)

    def test_restore_equipment_from_memento_none(self):
        self.assertIsNone(
            self.create_test_entity().restore_equipment_from_memento(None)
        )

    def test_restore_equipment_from_memento_invalid_type(self):
        with self.assertRaises(TypeError):
            self.create_test_entity().restore_equipment_from_memento(
                {"name": "IronSword"}
            )

    def test_restore_equipment_from_memento_unknown_name(self):
        saved = self.create_equipment_memento("ironsword")
        invalid = replace(saved, name="ThisItemDoesNotExist")
        with self.assertRaises(ValueError):
            self.create_test_entity().restore_equipment_from_memento(invalid)

    def test_full_entity_memento_preserves_temp_buff_and_items(self):
        entity = self.create_test_entity()
        entity.add_item_to_backpack(self.create_item("smallhealthpotion"))
        entity.add_temp_buff(self.create_test_buff())
        saved = entity.create_memento()
        restored = self.create_test_entity()
        restored.restore(saved)
        self.assertEqual(restored.create_memento().backpack, saved.backpack)
        self.assertEqual(restored.create_memento().temp_buffs, saved.temp_buffs)


if __name__ == "__main__":
    unittest.main()
