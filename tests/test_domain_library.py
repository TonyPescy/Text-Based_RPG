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
    # Saves repeated setup and assertion code while keeping individual tests readable

    # Get all expected equipment classes
    def get_expected_equipment_types(self):
        return {
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
            "smallhealthpotion": equipment.SmallHealthPotion,
            "greaterhealthpotion": equipment.GreaterHealthPotion,
            "superiorhealthpotion": equipment.SuperiorHealthPotion,
            "manapotion": equipment.ManaPotion,
            "turtlemasterpotion": equipment.TurtleMasterPotion,
        }

    # Get expected equipment dictionary keys
    def get_expected_equipment_keys(self):
        return set(self.get_expected_equipment_types().keys())

    # Verify an equipment dictionary entry creates the expected class
    def assert_equipment_type(self, item_name, expected_class):
        temp_equipment = dl.EQUIPMENT_TYPES[item_name]()
        self.assertIsInstance(
            temp_equipment,
            expected_class,
        )

    # Verify create_equipment creates the expected class
    def assert_created_equipment_type(self, item_name, expected_class):
        temp_equipment = dl.create_equipment(item_name)
        self.assertIsInstance(
            temp_equipment,
            expected_class,
        )

    # Verify an enum contains the expected values
    def assert_enum_values(self, enum_class, expected_values):
        self.assertEqual(
            tuple(enum_value.value for enum_value in enum_class),
            expected_values,
        )

    # Verify a spell name
    def assert_spell_name(self, spell_name, expected_value):
        self.assertEqual(
            spell_name.value,
            expected_value,
        )

    # Verify all spell names exist
    def assert_spell_names_exist(self):
        self.assertIn(dl.SpellNames.FIREBALL, dl.SpellNames)
        self.assertIn(dl.SpellNames.HEAL, dl.SpellNames)
        self.assertIn(dl.SpellNames.FROSTBOLT, dl.SpellNames)

    # Verify all spell types exist
    def assert_spell_types_exist(self):
        self.assertIn(dl.SpellTypes.OFFENSIVE, dl.SpellTypes)
        self.assertIn(dl.SpellTypes.SUPPORT, dl.SpellTypes)
        self.assertIn(dl.SpellTypes.CONTROL, dl.SpellTypes)

    # Test to see if ints provided are valid - ints are valid
    def test_are_valid_ints_true(self):
        self.assertEqual(
            dl.are_valid_ints(0, 0),
            True,
        )

    # Test to see if ints provided are valid - ints are not valid
    def test_are_valid_ints_false(self):
        self.assertEqual(
            dl.are_valid_ints("zilch", 0),
            False,
        )

    # Tests for equipment types dictionary
    def test_equipment_types(self):
        self.assertEqual(
            set(dl.EQUIPMENT_TYPES.keys()),
            self.get_expected_equipment_keys(),
        )

    # Tests for equipment types dictionary values
    def test_equipment_types_values(self):
        expected_equipment_types = self.get_expected_equipment_types()

        for item_name, expected_class in expected_equipment_types.items():
            self.assert_equipment_type(
                item_name,
                expected_class,
            )

    # Tests for valid equipment slots
    def test_valid_slots(self):
        self.assert_enum_values(
            dl.EquipmentSlot,
            ("Weapon", "Armor", "Accessory"),
        )

    # Tests for valid equipment slot indices
    def test_valid_slot_indices(self):
        self.assert_enum_values(
            dl.EquipmentSlotIndex,
            (0, 1, 2),
        )

    # Tests for valid consumables
    def test_valid_consumables(self):
        self.assert_enum_values(
            dl.ConsumableType,
            (
                "smallhealthpotion",
                "greaterhealthpotion",
                "superiorhealthpotion",
                "manapotion",
                "turtlemasterpotion",
            ),
        )

    # Tests for entity types
    def test_entity_types(self):
        self.assert_enum_values(
            dl.EntityType,
            (
                "Warrior",
                "Mage",
                "Skeleton",
                "Goblin",
            ),
        )

    # Tests that all equipment types are Equipment objects
    def test_equipment_types_are_equipment(self):
        for item_type in dl.EQUIPMENT_TYPES.values():
            item = item_type()

            self.assertIsInstance(
                item,
                equipment.Equipment,
            )

    # Test create_equipment with valid equipment
    def test_create_equipment_success(self):
        temp_equipment = dl.create_equipment("ironsword")

        self.assertIsInstance(
            temp_equipment,
            equipment.IronSword,
        )
        self.assertEqual(
            temp_equipment.name,
            "IronSword",
        )
        self.assertEqual(
            temp_equipment.slot,
            "Weapon",
        )
        self.assertDictEqual(
            temp_equipment.effects,
            {"Attack": "+12"},
        )

    # Test create_equipment with invalid equipment
    def test_create_equipment_invalid(self):
        temp_equipment = dl.create_equipment("invalid_equipment")

        self.assertIsNone(
            temp_equipment,
        )

    # Test create_equipment with each equipment type
    def test_create_equipment_all_types(self):
        expected_equipment_types = self.get_expected_equipment_types()

        for item_name, expected_class in expected_equipment_types.items():
            self.assert_created_equipment_type(
                item_name,
                expected_class,
            )

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

    # Test BASE_INVENTORY equipment values
    def test_base_inventory_values(self):
        expected_inventory = [
            (
                "None",
                "Weapon",
                {},
            ),
            (
                "None",
                "Armor",
                {},
            ),
            (
                "None",
                "Accessory",
                {},
            ),
        ]

        for index, expected_values in enumerate(expected_inventory):
            expected_name = expected_values[0]
            expected_slot = expected_values[1]
            expected_effects = expected_values[2]

            self.assertEqual(
                dl.BASE_INVENTORY[index].name,
                expected_name,
            )
            self.assertEqual(
                dl.BASE_INVENTORY[index].slot,
                expected_slot,
            )
            self.assertDictEqual(
                dl.BASE_INVENTORY[index].effects,
                expected_effects,
            )

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

    # Test is_valid_entity with invalid entity type
    def test_is_valid_entity_invalid(self):
        self.assertFalse(
            dl.is_valid_entity("invalid"),
        )

    # Tests for attack types
    def test_attack_types(self):
        self.assert_enum_values(
            dl.AttackTypes,
            (
                "Melee",
                "Ranged",
            ),
        )

    # Tests for melee attack range
    def test_melee_range(self):
        self.assertEqual(
            dl.MELEE_RANGE,
            1,
        )

    # Tests for ranged attack range
    def test_ranged_range(self):
        self.assertEqual(
            dl.RANGED_RANGE,
            3,
        )

    # success
    def test_spell_names_fireball(self):
        # Verify Fireball spell name
        self.assert_spell_name(
            dl.SpellNames.FIREBALL,
            "Fireball",
        )

    # success
    def test_spell_names_heal(self):
        # Verify Heal spell name
        self.assert_spell_name(
            dl.SpellNames.HEAL,
            "Heal",
        )

    # success
    def test_spell_names_frostbolt(self):
        # Verify Frostbolt spell name
        self.assert_spell_name(
            dl.SpellNames.FROSTBOLT,
            "Frostbolt",
        )

    # success
    def test_spell_names_contains_all_spells(self):
        # Verify all spell names exist
        self.assertEqual(
            len(dl.SpellNames),
            3,
        )

        # Verify Fireball exists
        self.assert_spell_names_exist()

    # success
    def test_spell_types_offensive(self):
        # Verify Offensive spell type
        self.assertEqual(
            dl.SpellTypes.OFFENSIVE.value,
            "Offensive",
        )

    # success
    def test_spell_types_support(self):
        # Verify Support spell type
        self.assertEqual(
            dl.SpellTypes.SUPPORT.value,
            "Support",
        )

    # success
    def test_spell_types_control(self):
        # Verify Control spell type
        self.assertEqual(
            dl.SpellTypes.CONTROL.value,
            "Control",
        )

    # success
    def test_spell_types_contains_all_types(self):
        # Verify all spell types exist
        self.assertEqual(
            len(dl.SpellTypes),
            3,
        )

        # Verify Offensive, Support, and Control exist
        self.assert_spell_types_exist()

    # Test DEAD_STATUS initialization
    def test_dead_status(self):
        self.assertEqual(
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
