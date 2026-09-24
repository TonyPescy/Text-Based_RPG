"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 21, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_domain_library.py
Purpose: Utilizes unittest to test all of the classes and methods in domain_library.py file
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
import domain_library as dl
import equipment
from entity import Warrior, Mage, Goblin, Skeleton


class TestDomainLibrary(unittest.TestCase):

    # test to see if ints provided are valid - ints are valid
    def test_are_valid_ints_true(self):
        self.assertEqual(dl.are_valid_ints(0, 0), True)

    # test to see if ints provided are valid - ints are not valid
    def test_are_valid_ints_true(self):
        self.assertEqual(dl.are_valid_ints("zilch", 0), False)

    # Tests for equipment types dictionary
    def test_equipment_types(self):
        self.assertEqual(
            set(dl.EQUIPMENT_TYPES.keys()),
            {
                "ironsword",
                "curseddagger",
                "magestaff",
                "ironchestplate",
                "leathertunic",
                "scoutarmor",
                "ringofthesorcerer",
                "amuletofvitality",
                "ringofhaste",
                "none_wep",
                "none_armor",
                "none_acc",
            },
        )

    # Tests for equipment types dictionary values
    def test_equipment_types_values(self):
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["ironsword"],
            equipment.IronSword,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["curseddagger"],
            equipment.CursedDagger,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["magestaff"],
            equipment.MageStaff,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["ironchestplate"],
            equipment.IronChestplate,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["leathertunic"],
            equipment.LeatherTunic,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["scoutarmor"],
            equipment.ScoutArmor,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["ringofthesorcerer"],
            equipment.RingOfTheSorcerer,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["amuletofvitality"],
            equipment.AmuletOfVitality,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["ringofhaste"],
            equipment.RingOfHaste,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["none_wep"],
            equipment.NoneWeapon,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["none_armor"],
            equipment.NoneArmor,
        )
        self.assertIsInstance(
            dl.EQUIPMENT_TYPES["none_acc"],
            equipment.NoneAccessory,
        )

    # Tests for valid equipment slots
    def test_valid_slots(self):
        self.assertEqual(
            dl.VALID_SLOTS,
            ("Weapon", "Armor", "Accessory"),
        )

    # Tests for entity types
    def test_entity_types(self):
        self.assertEqual(
            dl.ENTITY_TYPES,
            ("Warrior", "Mage", "Skeleton", "Goblin"),
        )

    # Tests that all equipment types are Equipment objects
    def test_equipment_types_are_equipment(self):
        for item in dl.EQUIPMENT_TYPES.values():
            self.assertIsInstance(item, equipment.Equipment)

    # Test create_equipment with valid equipment
    def test_create_equipment_success(self):
        temp_equipment = dl.create_equipment("ironsword")

        self.assertIsInstance(
            temp_equipment,
            equipment.IronSword,
        )
        self.assertEqual(temp_equipment.name, "IronSword")
        self.assertEqual(temp_equipment.slot, "Weapon")
        self.assertDictEqual(
            temp_equipment.effects,
            {"Attack": "+12"},
        )

    # Test create_equipment with invalid equipment
    def test_create_equipment_invalid(self):
        temp_equipment = dl.create_equipment("invalid_equipment")

        self.assertIsNone(temp_equipment)

    # Test create_equipment with each equipment type
    def test_create_equipment_all_types(self):
        test_equipment = {
            "ironsword": equipment.IronSword,
            "curseddagger": equipment.CursedDagger,
            "magestaff": equipment.MageStaff,
            "ironchestplate": equipment.IronChestplate,
            "leathertunic": equipment.LeatherTunic,
            "scoutarmor": equipment.ScoutArmor,
            "ringofthesorcerer": equipment.RingOfTheSorcerer,
            "amuletofvitality": equipment.AmuletOfVitality,
            "ringofhaste": equipment.RingOfHaste,
            "none_wep": equipment.NoneWeapon,
            "none_armor": equipment.NoneArmor,
            "none_acc": equipment.NoneAccessory,
        }

        for item_name, expected_class in test_equipment.items():
            temp_equipment = dl.create_equipment(item_name)

            self.assertIsInstance(
                temp_equipment,
                expected_class,
            )

    # Test BASE_INVENTORY initialization
    def test_base_inventory(self):
        self.assertEqual(len(dl.BASE_INVENTORY), 3)

        self.assertIsInstance(
            dl.BASE_INVENTORY[0],
            equipment.NoneWeapon,
        )

        self.assertIsInstance(
            dl.BASE_INVENTORY[1],
            equipment.NoneArmor,
        )

        self.assertIsInstance(
            dl.BASE_INVENTORY[2],
            equipment.NoneAccessory,
        )

    # Test BASE_INVENTORY equipment values
    def test_base_inventory_values(self):
        self.assertEqual(dl.BASE_INVENTORY[0].name, "None")
        self.assertEqual(dl.BASE_INVENTORY[0].slot, "Weapon")
        self.assertDictEqual(dl.BASE_INVENTORY[0].effects, {})

        self.assertEqual(dl.BASE_INVENTORY[1].name, "None")
        self.assertEqual(dl.BASE_INVENTORY[1].slot, "Armor")
        self.assertDictEqual(dl.BASE_INVENTORY[1].effects, {})

        self.assertEqual(dl.BASE_INVENTORY[2].name, "None")
        self.assertEqual(dl.BASE_INVENTORY[2].slot, "Accessory")
        self.assertDictEqual(dl.BASE_INVENTORY[2].effects, {})

    # Test create_entity with warrior
    def test_create_entity_warrior(self):
        temp_entity = dl.create_entity("warrior", 5, 10, 0)

        self.assertIsInstance(temp_entity, Warrior)
        self.assertEqual(temp_entity.id, 0)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with mage
    def test_create_entity_mage(self):
        temp_entity = dl.create_entity("mage", 5, 10, 1)

        self.assertIsInstance(temp_entity, Mage)
        self.assertEqual(temp_entity.id, 1)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with skeleton
    def test_create_entity_skeleton(self):
        temp_entity = dl.create_entity("skeleton", 5, 10, 2)

        self.assertIsInstance(temp_entity, Skeleton)
        self.assertEqual(temp_entity.id, 2)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with goblin
    def test_create_entity_goblin(self):
        temp_entity = dl.create_entity("goblin", 5, 10, 3)

        self.assertIsInstance(temp_entity, Goblin)
        self.assertEqual(temp_entity.id, 3)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity converts string coordinates to integers
    def test_create_entity_string_coordinates(self):
        temp_entity = dl.create_entity("warrior", "5", "10", 0)

        self.assertIsInstance(temp_entity, Warrior)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with invalid entity type
    def test_create_entity_invalid_type(self):
        temp_entity = dl.create_entity("invalid", 5, 10, 0)

        self.assertIsNone(temp_entity)

    # Test is_valid_entity with warrior
    def test_is_valid_entity_warrior(self):
        self.assertTrue(dl.is_valid_entity("warrior"))

    # Test is_valid_entity with mage
    def test_is_valid_entity_mage(self):
        self.assertTrue(dl.is_valid_entity("mage"))

    # Test is_valid_entity with skeleton
    def test_is_valid_entity_skeleton(self):
        self.assertTrue(dl.is_valid_entity("skeleton"))

    # Test is_valid_entity with goblin
    def test_is_valid_entity_goblin(self):
        self.assertTrue(dl.is_valid_entity("goblin"))

    # Test is_valid_entity with invalid entity type
    def test_is_valid_entity_invalid(self):
        self.assertFalse(dl.is_valid_entity("invalid"))
