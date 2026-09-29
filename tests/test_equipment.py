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

    # Test Equipment base class init
    def test_item_init(self):
        item = equipment.Equipment(
            "test",
            "Weapon",
            {"Attack": "+10"},
        )

        self.assertEqual(item.name, "test")
        self.assertEqual(item.slot, "Weapon")
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

        self.assertEqual(item.name, "SmallHealthPotion")
        self.assertEqual(item.slot, "Consumable")
        self.assertEqual(item.effects, {})
        self.assertEqual(
            item.instant_effects,
            {
                "Flat_modifiers": {
                    "Health": "20",
                },
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(
            item.over_time_effects,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(item.duration, 0)

    # Test GreaterHealthPotion initialization
    def test_greater_health_potion_init(self):
        item = equipment.GreaterHealthPotion()

        self.assertEqual(item.name, "GreaterHealthPotion")
        self.assertEqual(item.slot, "Consumable")
        self.assertEqual(item.effects, {})
        self.assertEqual(
            item.instant_effects,
            {
                "Flat_modifiers": {
                    "Health": "50",
                },
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(
            item.over_time_effects,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(item.duration, 0)

    # Test SuperiorHealthPotion initialization
    def test_superior_health_potion_init(self):
        item = equipment.SuperiorHealthPotion()

        self.assertEqual(item.name, "SuperiorHealthPotion")
        self.assertEqual(item.slot, "Consumable")
        self.assertEqual(item.effects, {})
        self.assertEqual(
            item.instant_effects,
            {
                "Flat_modifiers": {
                    "Health": "100",
                },
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(
            item.over_time_effects,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(item.duration, 0)

    # Test ManaPotion initialization
    def test_mana_potion_init(self):
        item = equipment.ManaPotion()

        self.assertEqual(item.name, "ManaPotion")
        self.assertEqual(item.slot, "Consumable")
        self.assertEqual(item.effects, {})
        self.assertEqual(
            item.instant_effects,
            {
                "Flat_modifiers": {
                    "Mana": "50",
                },
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(
            item.over_time_effects,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(item.duration, 0)

    # Test TurtleMasterPotion initialization
    def test_turtle_master_potion_init(self):
        item = equipment.TurtleMasterPotion()

        self.assertEqual(item.name, "TurtleMasterPotion")
        self.assertEqual(item.slot, "Consumable")
        self.assertEqual(item.effects, {})
        self.assertEqual(
            item.instant_effects,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Health": "10",
                },
            },
        )
        self.assertEqual(
            item.over_time_effects,
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
        )
        self.assertEqual(item.duration, 5)

    # Test use_consumable with Small Health Potion
    def test_use_consumable_small_health_potion(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health increased by 20
        self.assertEqual(entity.health, 70)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Greater Health Potion
    def test_use_consumable_greater_health_potion(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = 50

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["greaterhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health increased by 50
        self.assertEqual(entity.health, 100)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Superior Health Potion
    def test_use_consumable_superior_health_potion(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = 50

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["superiorhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health is capped at max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable when Health would exceed max Health
    def test_use_consumable_health_exceeds_max(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = 110

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["greaterhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health does not exceed max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable when Health is already at max Health
    def test_use_consumable_health_at_max(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = entity.max_health

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health remains at max Health
        self.assertEqual(entity.health, 120)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Turtle Master Potion percentage effect
    def test_use_consumable_turtle_master_percent_health(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = 50

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health increased by 10 percent
        self.assertEqual(entity.health, 55)

        # Check other stats remain unchanged immediately
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)

        # Check max Health remains unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Turtle Master Potion at max Health
    def test_use_consumable_turtle_master_at_max_health(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.health = entity.max_health

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Health does not exceed max Health
        self.assertEqual(entity.health, 120)

        # Check max Health remains unchanged
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Mana Potion
    def test_use_consumable_mana_potion(self):

        # Create test entity
        entity = Mage(0, [0, 0])
        entity.mana = 25

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Mana increased by 50
        self.assertEqual(entity.mana, 75)

        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable when Mana would exceed max Mana
    def test_use_consumable_mana_exceeds_max(self):

        # Create test entity
        entity = Mage(0, [0, 0])
        entity.mana = 90

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Mana does not exceed max Mana
        self.assertEqual(entity.mana, 100)

        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable when Mana is already at max Mana
    def test_use_consumable_mana_at_max(self):

        # Create test entity
        entity = Mage(0, [0, 0])
        entity.mana = entity.max_mana

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check Mana remains at max Mana
        self.assertEqual(entity.mana, 100)

        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)

        # Check max stats remain unchanged
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable with Turtle Master Potion over-time effects
    def test_use_consumable_turtle_master_over_time_effects(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check buff name
        self.assertEqual(
            entity.temp_buffs[0]["Name"],
            "TurtleMasterPotion",
        )

        # Check buff effects
        self.assertEqual(
            entity.temp_buffs[0]["Effects"],
            consumable.over_time_effects,
        )

        # Check buff duration
        self.assertEqual(
            entity.temp_buffs[0]["Turns"],
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
        entity = Warrior(0, [0, 0])

        # Get consumables
        first_consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()
        second_consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use first consumable
        equipment.Consumable.use_consumable(first_consumable, entity)

        # Use second consumable
        equipment.Consumable.use_consumable(second_consumable, entity)

        # Check first buff
        self.assertEqual(
            entity.temp_buffs[0]["Name"],
            "TurtleMasterPotion",
        )
        self.assertEqual(entity.temp_buffs[0]["Turns"], 5)

        # Check second buff
        self.assertEqual(
            entity.temp_buffs[1]["Name"],
            "TurtleMasterPotion",
        )
        self.assertEqual(entity.temp_buffs[1]["Turns"], 5)

    # Test use_consumable with consumable without over-time effects
    def test_use_consumable_no_over_time_effects(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check no temporary buffs were added
        self.assertEqual(entity.temp_buffs, [])

        # Check stats
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable preserves existing temporary buffs
    def test_use_consumable_preserves_existing_temp_buffs(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

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

        # Get consumable
        consumable = dl.EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        equipment.Consumable.use_consumable(consumable, entity)

        # Check existing buff was preserved
        self.assertEqual(
            entity.temp_buffs[0]["Name"],
            "ExistingBuff",
        )
        self.assertEqual(
            entity.temp_buffs[1]["Name"],
            "TurtleMasterPotion",
        )

        # Check stats remain unchanged immediately, except instant Health
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)
