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
from entity import Warrior, Mage, Goblin, Skeleton
from grid import Grid
from domain_library import EQUIPMENT_TYPES


# Class for testing entities
class TestEntity(unittest.TestCase):

    # Init for all entity types
    # Init warrior with base stats
    def test_warrior_init(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # Check values
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type, "warrior")
        self.assertEqual(entity.position, [0, 0])
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertEqual(entity.inventory[1].name, "None")
        self.assertEqual(entity.inventory[2].name, "None")
        self.assertEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )

    # Init goblin with base stats
    def test_goblin_init(self):
        entity = Goblin(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # Check values
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type, "goblin")
        self.assertEqual(entity.position, [0, 0])
        self.assertEqual(entity.health, 45)
        self.assertEqual(entity.attack, 12)
        self.assertEqual(entity.defence, 3)
        self.assertEqual(entity.speed, 6)
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertEqual(entity.inventory[1].name, "None")
        self.assertEqual(entity.inventory[2].name, "None")
        self.assertEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )

    # Init skeleton with base stats
    def test_skeleton_init(self):
        entity = Skeleton(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # Check values
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type, "skeleton")
        self.assertEqual(entity.position, [0, 0])
        self.assertEqual(entity.health, 60)
        self.assertEqual(entity.attack, 10)
        self.assertEqual(entity.defence, 8)
        self.assertEqual(entity.speed, 4)
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertEqual(entity.inventory[1].name, "None")
        self.assertEqual(entity.inventory[2].name, "None")
        self.assertEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )

    # Init Mage with base stats
    def test_mage_init(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # Check values
        self.assertEqual(entity.id, 0)
        self.assertEqual(entity.e_type, "mage")
        self.assertEqual(entity.position, [0, 0])
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertEqual(entity.inventory[1].name, "None")
        self.assertEqual(entity.inventory[2].name, "None")
        self.assertEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(entity.mana, 100)
        self.assertEqual(entity.spell_power, 25)

    # Tests for universal entity method testing
    # Tests for get_stats on warrior
    def test_get_stats_on_warrior(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "warrior",
                "Position": [0, 0],
                "Health": 120,
                "Attack": 15,
                "Defence": 10,
                "Speed": 5,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for get_stats on goblin
    def test_get_stats_on_goblin(self):
        entity = Goblin(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "goblin",
                "Position": [0, 0],
                "Health": 45,
                "Attack": 12,
                "Defence": 3,
                "Speed": 6,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for get_stats on skeleton
    def test_get_stats_on_skeleton(self):
        entity = Skeleton(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "skeleton",
                "Position": [0, 0],
                "Health": 60,
                "Attack": 10,
                "Defence": 8,
                "Speed": 4,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for get_stats on mage
    def test_get_stats_on_mage(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "mage",
                "Position": [0, 0],
                "Health": 70,
                "Mana": 100,
                "Attack": 8,
                "Defence": 4,
                "Speed": 5,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for reset_stats on warrior
    def test_reset_stats_on_warrior(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # change stats that can change
        entity.attack = 999
        entity.health = 999
        entity.defence = 999
        entity.speed = 999
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.reset_stats()
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "warrior",
                "Position": [0, 0],
                "Health": 120,
                "Attack": 15,
                "Defence": 10,
                "Speed": 5,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for reset_stats on goblin
    def test_reset_stats_on_goblin(self):
        entity = Goblin(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # change stats that can change
        entity.attack = 999
        entity.health = 999
        entity.defence = 999
        entity.speed = 999
        # Reset
        entity.reset_stats()
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "goblin",
                "Position": [0, 0],
                "Health": 45,
                "Attack": 12,
                "Defence": 3,
                "Speed": 6,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for reset_stats on skeleton
    def test_reset_stats_on_skeleton(self):
        entity = Skeleton(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # change stats that can change
        entity.attack = 999
        entity.health = 999
        entity.defence = 999
        entity.speed = 999
        # Reset
        entity.reset_stats()
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "skeleton",
                "Position": [0, 0],
                "Health": 60,
                "Attack": 10,
                "Defence": 8,
                "Speed": 4,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for reset_stats on mage
    def test_reset_stats_on_mage(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # change stats that can change
        entity.attack = 999
        entity.health = 999
        entity.defence = 999
        entity.speed = 999
        entity.mana = 999
        entity.spell_power = 999
        # Reset
        entity.reset_stats()
        stat_dict = entity.get_stats()
        # check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "mage",
                "Position": [0, 0],
                "Health": 70,
                "Mana": 100,
                "Attack": 8,
                "Defence": 4,
                "Speed": 5,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )
        self.assertEqual(entity.spell_power, 25)

    # Tests for handle_modifiers with a flat modifier
    def test_handle_flat_modifier(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Add flat modifier
        entity.handle_modifiers("Attack", "+5")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Attack": 5,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for handle_modifiers with a percent modifier
    def test_handle_percent_modifier(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # Add percent modifier
        entity.handle_modifiers("Attack", "+25%")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Attack": 25,
                },
            },
        )

    # Tests for handle_modifiers with multiple flat modifiers
    def test_handle_multiple_flat_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # Add flat modifiers
        entity.handle_modifiers("Attack", "-5")
        entity.handle_modifiers("Attack", "+10")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Attack": 5,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for handle_modifiers with multiple percent modifiers
    def test_handle_multiple_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # Add percent modifiers
        entity.handle_modifiers("Attack", "+10%")
        entity.handle_modifiers("Attack", "+20%")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Attack": 30,
                },
            },
        )

    # Tests for handle_modifiers with multiple modifier types
    def test_handle_multiple_modifier_types(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        # Add flat and percent modifiers
        entity.handle_modifiers("Attack", "+5")
        entity.handle_modifiers("Attack", "+10%")
        entity.handle_modifiers("Defence", "+3")
        entity.handle_modifiers("Speed", "+20%")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Attack": 5,
                    "Defence": 3,
                },
                "Percent_modifiers": {
                    "Attack": 10,
                    "Speed": 20,
                },
            },
        )

    # Tests for handle_modifiers with mage entity
    def test_handle_multiple_modifier_types_on_mage(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        # Add flat and percent modifiers
        entity.handle_modifiers("Attack", "+5")
        entity.handle_modifiers("Attack", "+10%")
        entity.handle_modifiers("Defence", "+3")
        entity.handle_modifiers("Speed", "+20%")
        entity.handle_modifiers("Spell_power", "+5")
        entity.handle_modifiers("Mana", "+20%")
        # Check values
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {"Attack": 5, "Defence": 3, "Spell_power": 5},
                "Percent_modifiers": {"Attack": 10, "Speed": 20, "Mana": 20},
            },
        )

    # Test for calculate_final_stats with flat modifiers
    def test_calculate_final_stats_with_flat_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                    "Attack": 5,
                    "Defence": 3,
                    "Speed": 2,
                },
                "Percent_modifiers": {},
            },
        )
        # Calculate final stats
        entity.calculate_final_stats()
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 140)
        self.assertEqual(stat_dict["Attack"], 20)
        self.assertEqual(stat_dict["Defence"], 13)
        self.assertEqual(stat_dict["Speed"], 7)

    # Test for calculate_final_stats with percent modifiers
    def test_calculate_final_stats_with_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Health": 10,
                    "Attack": 20,
                    "Defence": 50,
                    "Speed": 100,
                },
            },
        )
        # Calculate final stats
        entity.calculate_final_stats()
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 132)
        self.assertEqual(stat_dict["Attack"], 18)
        self.assertEqual(stat_dict["Defence"], 15)
        self.assertEqual(stat_dict["Speed"], 10)

    # Test for calculate_final_stats with flat and percent modifiers
    def test_calculate_final_stats_with_flat_and_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                    "Attack": 5,
                    "Defence": -2,
                    "Speed": 3,
                },
                "Percent_modifiers": {
                    "Health": 10,
                    "Attack": 20,
                    "Defence": 50,
                    "Speed": 100,
                },
            },
        )
        # Calculate final stats
        entity.calculate_final_stats()
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 154)
        self.assertEqual(stat_dict["Attack"], 24)
        self.assertEqual(stat_dict["Defence"], 12)
        self.assertEqual(stat_dict["Speed"], 16)

    # Tests for calculate_final_stats with mage only stats
    def test_calculate_final_stats_with_mage_stats(self):
        entity = Mage(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                    "Attack": 5,
                    "Defence": -2,
                    "Speed": 3,
                    "Spell_power": 75,
                },
                "Percent_modifiers": {
                    "Health": 10,
                    "Attack": 20,
                    "Defence": 50,
                    "Speed": 100,
                    "Mana": 50,
                },
            },
        )
        # Calculate final stats
        entity.calculate_final_stats()
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 99)
        self.assertEqual(stat_dict["Attack"], 15.6)
        self.assertEqual(stat_dict["Defence"], 3)
        self.assertEqual(stat_dict["Speed"], 16)
        self.assertEqual(stat_dict["Mana"], 150)
        self.assertEqual(entity.spell_power, 100)

    # Bookmark
    # Tests for update_stats with no modifiers on warrior
    def test_update_stats_on_warrior_with_no_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertDictEqual(
            stat_dict,
            {
                "Id": 0,
                "Type": "warrior",
                "Position": [0, 0],
                "Health": 120,
                "Attack": 15,
                "Defence": 10,
                "Speed": 5,
                "Active_modifiers": {
                    "Flat_modifiers": {},
                    "Percent_modifiers": {},
                },
            },
        )

    # Tests for update_stats with inventory flat modifiers on warrior
    def test_update_stats_on_warrior_with_inventory_flat_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
            "Defence": "+3",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 20)
        self.assertEqual(stat_dict["Defence"], 13)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": 5,
                    "Defence": 3,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for update_stats with inventory negative flat modifiers on warrior
    def test_update_stats_on_warrior_with_negative_inventory_flat_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "-5",
            "Defence": "-2",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 10)
        self.assertEqual(stat_dict["Defence"], 8)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": -5,
                    "Defence": -2,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for update_stats with inventory percent modifiers on warrior
    def test_update_stats_on_warrior_with_inventory_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+20%",
            "Defence": "+50%",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 18)
        self.assertEqual(stat_dict["Defence"], 15)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Attack": 20,
                    "Defence": 50,
                },
            },
        )

    # Tests for update_stats with negative inventory percent modifiers on warrior
    def test_update_stats_on_warrior_with_negative_inventory_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "-20%",
            "Defence": "-50%",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 12)
        self.assertEqual(stat_dict["Defence"], 5)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Attack": -20,
                    "Defence": -50,
                },
            },
        )

    # Tests for update_stats with tile flat modifiers on warrior
    def test_update_stats_on_warrior_with_tile_flat_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add tile modifiers
        active_grid.grid[0][0].modifiers = {
            "Attack": "-2",
            "Defence": "3",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 13)
        self.assertEqual(stat_dict["Defence"], 13)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": -2,
                    "Defence": 3,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for update_stats with tile percent modifiers on warrior
    def test_update_stats_on_warrior_with_tile_percent_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add tile modifiers
        active_grid.grid[0][0].modifiers = {
            "Attack": "-20%",
            "Defence": "50%",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 12)
        self.assertEqual(stat_dict["Defence"], 15)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Attack": -20,
                    "Defence": 50,
                },
            },
        )

    # Tests for update_stats with inventory and tile modifiers on warrior
    def test_update_stats_on_warrior_with_inventory_and_tile_modifiers(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
            "Defence": "-2",
        }
        # Add tile modifiers
        active_grid.grid[0][0].modifiers = {
            "Attack": "+3",
            "Defence": "+10%",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 23)
        self.assertEqual(stat_dict["Defence"], 8.8)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": 8,
                    "Defence": -2,
                },
                "Percent_modifiers": {
                    "Defence": 10,
                },
            },
        )

    # Tests for update_stats ignoring Mana and Spell_power modifiers on warrior
    def test_update_stats_on_warrior_ignores_mana_and_spell_power(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Mana": "+50",
            "Spell_power": "+10",
            "Attack": "+5",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 20)
        self.assertEqual(stat_dict["Defence"], 10)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": 5,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for update_stats clearing previous modifiers on warrior
    def test_update_stats_clears_previous_modifiers_on_warrior(self):
        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Attack": "5",
                },
                "Percent_modifiers": {
                    "Defence": "20",
                },
            },
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
        }
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 20)
        self.assertEqual(stat_dict["Defence"], 10)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Attack": 5,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for update_stats with shallow water tile on warrior
    def test_update_stats_on_warrior_on_shallow_water(self):
        entity = Warrior(
            0,
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Set entity tile to shallow water
        active_grid.set_tile(0, 0, "shallowwater")
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 120)
        self.assertEqual(stat_dict["Attack"], 15)
        self.assertEqual(stat_dict["Defence"], 10)
        self.assertEqual(stat_dict["Speed"], 3)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Speed": -2,
                },
                "Percent_modifiers": {},
            },
        )

    # Test for update_stats on mage with mage stats changing
    def test_update_stats_on_mage_with_mage_only_stats_affected(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        entity.inventory[0].effects = {"Mana": "100", "Spell_power": "100%"}
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 70)
        self.assertEqual(stat_dict["Attack"], 8)
        self.assertEqual(stat_dict["Defence"], 4)
        self.assertEqual(stat_dict["Speed"], 5)
        self.assertEqual(stat_dict["Mana"], 200)
        self.assertEqual(entity.spell_power, 50)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {"Mana": 100},
                "Percent_modifiers": {"Spell_power": 100},
            },
        )

    # Tests for update_stats with shallow water tile on mage
    def test_update_stats_on_mage_on_shallow_water(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}
        active_grid = Grid(5, 5)
        # Set entity tile to shallow water
        active_grid.set_tile(0, 0, "shallowwater")
        # Update stats
        entity.update_stats(active_grid)
        stat_dict = entity.get_stats()
        # Check values
        self.assertEqual(stat_dict["Health"], 70)
        self.assertEqual(stat_dict["Attack"], 8)
        self.assertEqual(stat_dict["Defence"], 4)
        self.assertEqual(stat_dict["Speed"], 3)
        self.assertDictEqual(
            stat_dict["Active_modifiers"],
            {
                "Flat_modifiers": {
                    "Speed": -2,
                },
                "Percent_modifiers": {},
            },
        )

    # Tests for equip item
    # weapon
    def test_equip_item_weapon(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip weapon
        weapon = EQUIPMENT_TYPES["ironsword"]
        entity.equip_item(weapon, weapon.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "IronSword")
        self.assertEqual(entity.attack, 27)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Attack": 12,
                },
                "Percent_modifiers": {},
            },
        )

    # armor
    def test_equip_item_armor(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip armor
        armor = EQUIPMENT_TYPES["ironchestplate"]
        entity.equip_item(armor, armor.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[1].name, "IronChestplate")
        self.assertEqual(entity.speed, 3)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {"Defence": 15, "Speed": -2},
                "Percent_modifiers": {},
            },
        )

    # acc
    def test_equip_item_accessory(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip acc
        acc = EQUIPMENT_TYPES["ringofhaste"]
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[2].name, "RingOfHaste")
        self.assertEqual(entity.speed, 7)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Speed": 2,
                },
                "Percent_modifiers": {},
            },
        )

    # all
    def test_equip_item_all(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip items
        weapon = EQUIPMENT_TYPES["ironsword"]
        armor = EQUIPMENT_TYPES["ironchestplate"]
        acc = EQUIPMENT_TYPES["amuletofvitality"]
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "IronSword")
        self.assertEqual(entity.inventory[1].name, "IronChestplate")
        self.assertEqual(entity.inventory[2].name, "AmuletOfVitality")
        self.assertEqual(entity.health, 132)
        self.assertEqual(entity.defence, 28)
        self.assertEqual(entity.attack, 27)
        self.assertEqual(entity.speed, 3)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {"Attack": 12, "Defence": 18, "Speed": -2},
                "Percent_modifiers": {"Health": 10},
            },
        )

    # all on warrior with mage effects
    def test_equip_item_all_on_warrior_with_mage_effects(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip items
        weapon = EQUIPMENT_TYPES["magestaff"]
        armor = EQUIPMENT_TYPES["ironchestplate"]
        acc = EQUIPMENT_TYPES["ringofthesorcerer"]
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "MageStaff")
        self.assertEqual(entity.inventory[1].name, "IronChestplate")
        self.assertEqual(entity.inventory[2].name, "RingOfTheSorcerer")
        self.assertEqual(entity.defence, 25)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.speed, 3)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {
                    "Defence": 15,
                    "Speed": -2,
                },
                "Percent_modifiers": {},
            },
        )

    # all on mage with mage effects
    def test_equip_item_all_on_mage_with_mage_effects(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip items
        weapon = EQUIPMENT_TYPES["magestaff"]
        armor = EQUIPMENT_TYPES["ironchestplate"]
        acc = EQUIPMENT_TYPES["ringofthesorcerer"]
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "MageStaff")
        self.assertEqual(entity.inventory[1].name, "IronChestplate")
        self.assertEqual(entity.inventory[2].name, "RingOfTheSorcerer")
        self.assertEqual(entity.defence, 19)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.speed, 3)
        self.assertEqual(entity.spell_power, 35)
        self.assertEqual(entity.mana, 115)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {"Defence": 15, "Speed": -2, "Spell_power": 10},
                "Percent_modifiers": {"Mana": 15},
            },
        )

    # wrong slot
    def test_equip_item_with_wrong_slot(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip acc
        acc = EQUIPMENT_TYPES["ringofhaste"]
        entity.equip_item(acc, "weapon")
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertEqual(entity.inventory[2].name, "None")
        self.assertEqual(entity.speed, 5)
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )

    # no existing weapon
    def test_equip_item_without_item(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]
        # create and equip acc
        entity.equip_item("unobtainium", "weapon")
        # update stats
        active_grid = Grid(5, 5)
        entity.update_stats(active_grid)
        # Check values
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
