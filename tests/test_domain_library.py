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


class TestDomainLibrary(unittest.TestCase):

    # Repeated Test Functions

    # Assert Enum Values
    # Checks that an enum contains the expected values in order
    # Params: enum_class - Enum - enum to check
    #         expected_values - tuple - expected enum values
    # Returns: None
    def assert_enum_values(self, enum_class, expected_values):
        self.assertEqual(
            tuple(enum_value.value for enum_value in enum_class),
            expected_values,
        )

    # Assert Spell Name
    # Checks that a spell name enum has the expected value
    # Params: spell_name - Enum - spell name to check
    #         expected_value - string - expected value
    # Returns: None
    def assert_spell_name(self, spell_name, expected_value):
        self.assertEqual(
            spell_name.value,
            expected_value,
        )

    # Integer Validation Tests

    # Test are_valid_ints with valid integers
    def test_are_valid_ints_true(self):
        self.assertTrue(
            dl.are_valid_ints(0, 0),
        )

    # Test are_valid_ints with an invalid integer
    def test_are_valid_ints_false(self):
        self.assertFalse(
            dl.are_valid_ints("zilch", 0),
        )

    # Base Inventory Tests

    # Test BASE_INVENTORY initialization
    def test_base_inventory(self):
        self.assertEqual(
            len(dl.BASE_INVENTORY),
            3,
        )
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

    # Test BASE_INVENTORY values
    def test_base_inventory_values(self):
        expected_inventory = (
            ("None", "Weapon", {}),
            ("None", "Armor", {}),
            ("None", "Accessory", {}),
        )

        for index, expected_values in enumerate(expected_inventory):
            with self.subTest(index=index):
                expected_name, expected_slot, expected_effects = expected_values
                temp_equipment = dl.BASE_INVENTORY[index]

                self.assertEqual(
                    temp_equipment.name,
                    expected_name,
                )
                self.assertEqual(
                    temp_equipment.slot,
                    expected_slot,
                )
                self.assertDictEqual(
                    temp_equipment.effects,
                    expected_effects,
                )

    # Enum Tests

    # Test valid equipment slots
    def test_valid_slots(self):
        self.assert_enum_values(
            dl.EquipmentSlot,
            ("Weapon", "Armor", "Accessory"),
        )

    # Test valid equipment slot indices
    def test_valid_slot_indices(self):
        self.assert_enum_values(
            dl.EquipmentSlotIndex,
            (0, 1, 2),
        )

    # Entity Validation Tests

    # Test is_valid_entity with warrior
    def test_is_valid_entity_warrior(self):
        self.assertTrue(
            dl.is_valid_entity("warrior"),
        )

    # Test is_valid_entity with mage
    def test_is_valid_entity_mage(self):
        self.assertTrue(
            dl.is_valid_entity("mage"),
        )

    # Test is_valid_entity with skeleton
    def test_is_valid_entity_skeleton(self):
        self.assertTrue(
            dl.is_valid_entity("skeleton"),
        )

    # Test is_valid_entity with goblin
    def test_is_valid_entity_goblin(self):
        self.assertTrue(
            dl.is_valid_entity("goblin"),
        )

    # Test is_valid_entity with an invalid entity type
    def test_is_valid_entity_invalid(self):
        self.assertFalse(
            dl.is_valid_entity("invalid"),
        )

    # Attack Type and Range Tests

    # Test valid attack types
    def test_attack_types(self):
        self.assert_enum_values(
            dl.AttackTypes,
            ("Melee", "Ranged"),
        )

    # Test melee attack range
    def test_melee_range(self):
        self.assertEqual(
            dl.MELEE_RANGE,
            1,
        )

    # Test ranged attack range
    def test_ranged_range(self):
        self.assertEqual(
            dl.RANGED_RANGE,
            3,
        )

    # Spell Type Tests

    # Test Offensive spell type
    def test_spell_types_offensive(self):
        self.assertEqual(
            dl.SpellTypes.OFFENSIVE.value,
            "Offensive",
        )

    # Test Support spell type
    def test_spell_types_support(self):
        self.assertEqual(
            dl.SpellTypes.SUPPORT.value,
            "Support",
        )

    # Test Control spell type
    def test_spell_types_control(self):
        self.assertEqual(
            dl.SpellTypes.CONTROL.value,
            "Control",
        )

    # Test that all spell types exist
    def test_spell_types_contains_all_types(self):
        self.assertEqual(
            len(dl.SpellTypes),
            3,
        )
        self.assertIn(dl.SpellTypes.OFFENSIVE, dl.SpellTypes)
        self.assertIn(dl.SpellTypes.SUPPORT, dl.SpellTypes)
        self.assertIn(dl.SpellTypes.CONTROL, dl.SpellTypes)

    # Status Effect Tests

    # Test DEAD_STATUS initialization
    def test_dead_status(self):
        self.assertDictEqual(
            dl.DEAD_STATUS,
            {
                "Name": "Dead",
                "Effects": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
                "Turns": 3,
            },
        )


if __name__ == "__main__":
    unittest.main()
