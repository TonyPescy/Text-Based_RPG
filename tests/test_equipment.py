"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 21, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_item.py
Purpose: Utilizes unittest to test all of the classes and methods in item.py file
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

# imports
import unittest

import equipment
import domain_library as dl

from entity import Warrior, Mage


class TestEquipment(unittest.TestCase):

    # Repeated Test Functions
    # Saves repeated setup and assertion code while keeping individual tests readable

    # Create a test Warrior
    def create_warrior(self):
        return Warrior(0, [0, 0])

    # Create a test Mage
    def create_mage(self):
        return Mage(0, [0, 0])

    # Get a consumable from EQUIPMENT_TYPES
    def get_consumable(self, consumable_name):
        return dl.EQUIPMENT_TYPES[consumable_name]()

    # Use a consumable on an entity
    def use_consumable(self, consumable_name, entity):
        consumable = self.get_consumable(consumable_name)
        equipment.Consumable.use_consumable(
            consumable,
            entity,
        )
        return consumable

    # Verify standard Warrior stats
    def assert_base_warrior_stats(self, entity):
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Verify standard Mage stats
    def assert_base_mage_stats(self, entity):
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Verify common consumable attributes
    def assert_consumable_attributes(
        self,
        item,
        name,
        instant_effects,
        over_time_effects,
        duration,
    ):
        self.assertEqual(
            item.name,
            name,
        )
        self.assertEqual(
            item.slot,
            "Consumable",
        )
        self.assertEqual(
            item.effects,
            {},
        )
        self.assertEqual(
            item.instant_effects,
            instant_effects,
        )
        self.assertEqual(
            item.over_time_effects,
            over_time_effects,
        )
        self.assertEqual(
            item.duration,
            duration,
        )

    # Verify a standard instant health consumable
    def assert_health_potion(
        self,
        item,
        name,
        health_amount,
    ):
        self.assert_consumable_attributes(
            item,
            name,
            {
                "Flat_modifiers": {
                    "Health": health_amount,
                },
                "Percent_modifiers": {},
            },
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
            0,
        )

    # Verify standard entity stats after a health potion
    def assert_warrior_health_stats(self, entity):
        self.assert_base_warrior_stats(entity)

    # Verify standard entity stats after a mana potion
    def assert_mage_mana_stats(self, entity):
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Verify a temporary buff
    def assert_temp_buff(
        self,
        entity,
        index,
        name,
        effects,
        turns,
    ):
        self.assertEqual(
            entity.temp_buffs[index]["Name"],
            name,
        )
        self.assertEqual(
            entity.temp_buffs[index]["Effects"],
            effects,
        )
        self.assertEqual(
            entity.temp_buffs[index]["Turns"],
            turns,
        )

    # Test Equipment base class init
    def test_item_init(self):
        item = equipment.Equipment(
            "test",
            "Weapon",
            {"Attack": "+10"},
        )

        self.assertEqual(
            item.name,
            "test",
        )
        self.assertEqual(
            item.slot,
            "Weapon",
        )
        self.assertDictEqual(
            item.effects,
            {"Attack": "+10"},
        )

    # Test NoneWeapon init
    def test_none_weapon_init(self):
        item = equipment.NoneWeapon()

        self.assertEqual(item.name, "None")
        self.assertEqual(item.slot, "Weapon")
        self.assertDictEqual(item.effects, {})

    # Test NoneArmor init
    def test_none_armor_init(self):
        item = equipment.NoneArmor()

        self.assertEqual(item.name, "None")
        self.assertEqual(item.slot, "Armor")
        self.assertDictEqual(item.effects, {})

    # Test NoneAccessory init
    def test_none_accessory_init(self):
        item = equipment.NoneAccessory()

        self.assertEqual(item.name, "None")
        self.assertEqual(item.slot, "Accessory")
        self.assertDictEqual(item.effects, {})

    # Test IronSword init
    def test_iron_sword_init(self):
        item = equipment.IronSword()

        self.assertEqual(item.name, "IronSword")
        self.assertEqual(item.slot, "Weapon")
        self.assertDictEqual(
            item.effects,
            {"Attack": "+12"},
        )

    # Test CursedDagger init
    def test_cursed_dagger_init(self):
        item = equipment.CursedDagger()

        self.assertEqual(item.name, "CursedDagger")
        self.assertEqual(item.slot, "Weapon")
        self.assertDictEqual(
            item.effects,
            {
                "Attack": "+18",
                "Defence": "-5",
            },
        )

    # Test MageStaff init
    def test_mage_staff_init(self):
        item = equipment.MageStaff()

        self.assertEqual(item.name, "MageStaff")
        self.assertEqual(item.slot, "Weapon")
        self.assertDictEqual(
            item.effects,
            {"Spell_power": "+5"},
        )

    # Test IronChestplate init
    def test_iron_chestplate_init(self):
        item = equipment.IronChestplate()

        self.assertEqual(item.name, "IronChestplate")
        self.assertEqual(item.slot, "Armor")
        self.assertDictEqual(
            item.effects,
            {
                "Defence": "+15",
                "Speed": "-2",
            },
        )

    # Test LeatherTunic init
    def test_leather_tunic_init(self):
        item = equipment.LeatherTunic()

        self.assertEqual(item.name, "LeatherTunic")
        self.assertEqual(item.slot, "Armor")
        self.assertDictEqual(
            item.effects,
            {"Defence": "+5"},
        )

    # Test ScoutArmor init
    def test_scout_armor_init(self):
        item = equipment.ScoutArmor()

        self.assertEqual(item.name, "ScoutArmor")
        self.assertEqual(item.slot, "Armor")
        self.assertDictEqual(
            item.effects,
            {
                "Defence": "+3",
                "Speed": "+10%",
            },
        )

    # Test RingOfTheSorcerer init
    def test_ring_of_the_sorcerer_init(self):
        item = equipment.RingOfTheSorcerer()

        self.assertEqual(item.name, "RingOfTheSorcerer")
        self.assertEqual(item.slot, "Accessory")
        self.assertDictEqual(
            item.effects,
            {
                "Spell_power": "+5",
                "Mana": "+15%",
            },
        )

    # Test AmuletOfVitality init
    def test_amulet_of_vitality_init(self):
        item = equipment.AmuletOfVitality()

        self.assertEqual(item.name, "AmuletOfVitality")
        self.assertEqual(item.slot, "Accessory")
        self.assertDictEqual(
            item.effects,
            {
                "Health": "+10%",
                "Defence": "+3",
            },
        )

    # Test RingOfHaste init
    def test_ring_of_haste_init(self):
        item = equipment.RingOfHaste()

        self.assertEqual(item.name, "RingOfHaste")
        self.assertEqual(item.slot, "Accessory")
        self.assertDictEqual(
            item.effects,
            {"Speed": "+2"},
        )

    # Test SmallHealthPotion initialization
    def test_small_health_potion_init(self):
        item = equipment.SmallHealthPotion()

        self.assert_health_potion(
            item,
            "SmallHealthPotion",
            "20",
        )

    # Test GreaterHealthPotion initialization
    def test_greater_health_potion_init(self):
        item = equipment.GreaterHealthPotion()

        self.assert_health_potion(
            item,
            "GreaterHealthPotion",
            "50",
        )

    # Test SuperiorHealthPotion initialization
    def test_superior_health_potion_init(self):
        item = equipment.SuperiorHealthPotion()

        self.assert_health_potion(
            item,
            "SuperiorHealthPotion",
            "100",
        )

    # Test ManaPotion initialization
    def test_mana_potion_init(self):
        item = equipment.ManaPotion()

        self.assert_consumable_attributes(
            item,
            "ManaPotion",
            {
                "Flat_modifiers": {
                    "Mana": "50",
                },
                "Percent_modifiers": {},
            },
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
            0,
        )

    # Test TurtleMasterPotion initialization
    def test_turtle_master_potion_init(self):
        item = equipment.TurtleMasterPotion()

        self.assert_consumable_attributes(
            item,
            "TurtleMasterPotion",
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Health": "10",
                },
            },
            {
                "Flat_modifiers": {
                    "Speed": "-3",
                    "Defence": "10",
                },
                "Percent_modifiers": {
                    "Health": "10",
                    "Defence": "20",
                },
            },
            5,
        )

    # Test use_consumable with Small Health Potion
    def test_use_consumable_small_health_potion(self):
        # Create test entity
        entity = self.create_warrior()

        # Set current Health
        entity.health = 50

        # Use consumable
        self.use_consumable(
            "smallhealthpotion",
            entity,
        )

        # Check Health increased by 20
        self.assertEqual(entity.health, 70)

        # Check other stats remain unchanged
        self.assert_warrior_health_stats(entity)

    # Test use_consumable with Greater Health Potion
    def test_use_consumable_greater_health_potion(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = 50

        # Use consumable
        self.use_consumable(
            "greaterhealthpotion",
            entity,
        )

        # Check Health increased by 50
        self.assertEqual(entity.health, 100)

        # Check other stats remain unchanged
        self.assert_warrior_health_stats(entity)

    # Test use_consumable with Superior Health Potion
    def test_use_consumable_superior_health_potion(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = 50

        # Use consumable
        self.use_consumable(
            "superiorhealthpotion",
            entity,
        )

        # Check Health is capped at max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assert_warrior_health_stats(entity)

    # Test use_consumable when Health would exceed max Health
    def test_use_consumable_health_exceeds_max(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = 110

        # Use consumable
        self.use_consumable(
            "greaterhealthpotion",
            entity,
        )

        # Check Health does not exceed max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assert_warrior_health_stats(entity)

    # Test use_consumable when Health is already at max Health
    def test_use_consumable_health_at_max(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = entity.max_health

        # Use consumable
        self.use_consumable(
            "smallhealthpotion",
            entity,
        )

        # Check Health remains at max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assert_warrior_health_stats(entity)

    # Test use_consumable with Turtle Master Potion percentage effect
    def test_use_consumable_turtle_master_percent_health(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = 50

        # Use consumable
        self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Check Health increased by 10 percent
        self.assertEqual(entity.health, 55)

        # Check other stats remain unchanged immediately
        self.assert_warrior_health_stats(entity)

    # Test use_consumable with Turtle Master Potion at max Health
    def test_use_consumable_turtle_master_at_max_health(self):
        # Create test entity
        entity = self.create_warrior()
        entity.health = entity.max_health

        # Use consumable
        self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Check Health does not exceed max Health
        self.assertEqual(entity.health, 120)

        # Check max Health remains unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Mana Potion
    def test_use_consumable_mana_potion(self):
        # Create test entity
        entity = self.create_mage()
        entity.mana = 25

        # Use consumable
        self.use_consumable(
            "manapotion",
            entity,
        )

        # Check Mana increased by 50
        self.assertEqual(entity.mana, 75)

        # Check other stats remain unchanged
        self.assert_mage_mana_stats(entity)

    # Test use_consumable when Mana would exceed max Mana
    def test_use_consumable_mana_exceeds_max(self):
        # Create test entity
        entity = self.create_mage()
        entity.mana = 90

        # Use consumable
        self.use_consumable(
            "manapotion",
            entity,
        )

        # Check Mana does not exceed max Mana
        self.assertEqual(entity.mana, 100)

        # Check other stats remain unchanged
        self.assert_mage_mana_stats(entity)

    # Test use_consumable when Mana is already at max Mana
    def test_use_consumable_mana_at_max(self):
        # Create test entity
        entity = self.create_mage()
        entity.mana = entity.max_mana

        # Use consumable
        self.use_consumable(
            "manapotion",
            entity,
        )

        # Check Mana remains at max Mana
        self.assertEqual(entity.mana, 100)

        # Check other stats remain unchanged
        self.assert_mage_mana_stats(entity)

    # Test use_consumable with Turtle Master Potion over-time effects
    def test_use_consumable_turtle_master_over_time_effects(self):
        # Create test entity
        entity = self.create_warrior()

        # Use consumable
        consumable = self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Check buff
        self.assert_temp_buff(
            entity,
            0,
            "TurtleMasterPotion",
            consumable.over_time_effects,
            5,
        )

        # Check stats were not changed by storing the buff
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with multiple over-time buffs
    def test_use_consumable_multiple_over_time_buffs(self):
        # Create test entity
        entity = self.create_warrior()

        # Use first consumable
        first_consumable = self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Use second consumable
        second_consumable = self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Check first buff
        self.assert_temp_buff(
            entity,
            0,
            "TurtleMasterPotion",
            first_consumable.over_time_effects,
            5,
        )

        # Check second buff
        self.assert_temp_buff(
            entity,
            1,
            "TurtleMasterPotion",
            second_consumable.over_time_effects,
            5,
        )

    # Test use_consumable with consumable without over-time effects
    def test_use_consumable_no_over_time_effects(self):
        # Create test entity
        entity = self.create_warrior()

        # Use consumable
        self.use_consumable(
            "smallhealthpotion",
            entity,
        )

        # Check no temporary buffs were added
        self.assertEqual(
            entity.temp_buffs,
            [],
        )

        # Check stats
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable preserves existing temporary buffs
    def test_use_consumable_preserves_existing_temp_buffs(self):
        # Create test entity
        entity = self.create_warrior()

        # Add existing temporary buff
        entity.temp_buffs.append(
            {
                "Name": "ExistingBuff",
                "Effects": {
                    "Flat_modifiers": {
                        "Attack": "5",
                    },
                    "Percent_modifiers": {},
                },
                "Turns": 2,
            }
        )

        # Use consumable
        consumable = self.use_consumable(
            "turtlemasterpotion",
            entity,
        )

        # Check existing buff was preserved
        self.assert_temp_buff(
            entity,
            0,
            "ExistingBuff",
            {
                "Flat_modifiers": {
                    "Attack": "5",
                },
                "Percent_modifiers": {},
            },
            2,
        )

        # Check new buff was added
        self.assert_temp_buff(
            entity,
            1,
            "TurtleMasterPotion",
            consumable.over_time_effects,
            5,
        )

        # Check stats remain unchanged immediately, except instant Health
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)
