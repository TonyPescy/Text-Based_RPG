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
