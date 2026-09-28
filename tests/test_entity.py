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
from entity import Warrior, Mage, Goblin, Skeleton, create_entity
from grid import Grid
from domain_library import EQUIPMENT_TYPES, create_equipment, use_consumable
import command_line_interface as cli


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
        entity.backpack = []
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
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
        self.assertEqual(entity.backpack, [])
        self.assertEqual(entity.max_health, 120)
        self.assertEqual(entity.temp_buffs, [])

    # Init goblin with base stats
    def test_goblin_init(self):
        entity = Goblin(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
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
        self.assertEqual(entity.backpack, [])
        self.assertEqual(entity.max_health, 45)
        self.assertEqual(entity.temp_buffs, [])

    # Init skeleton with base stats
    def test_skeleton_init(self):
        entity = Skeleton(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
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
        self.assertEqual(entity.backpack, [])
        self.assertEqual(entity.max_health, 60)
        self.assertEqual(entity.temp_buffs, [])

    # Init Mage with base stats
    def test_mage_init(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
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
        self.assertEqual(entity.backpack, [])
        self.assertEqual(entity.mana, 100)
        self.assertEqual(entity.spell_power, 25)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.temp_buffs, [])
        self.assertEqual(entity.max_mana, 100)

    # Tests for universal entity method testing
    # Tests for get_stats on warrior
    def test_get_stats_on_warrior(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
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
        entity.backpack = []
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
        entity.backpack = []
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
        entity.backpack = []
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
        entity.backpack = []
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
        self.assertEqual(entity.max_health, 120)

    # Tests for reset_stats on goblin
    def test_reset_stats_on_goblin(self):
        entity = Goblin(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []

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
        self.assertEqual(entity.max_health, 45)

    # Tests for reset_stats on skeleton
    def test_reset_stats_on_skeleton(self):
        entity = Skeleton(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []

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
        self.assertEqual(entity.max_health, 60)

    # Tests for reset_stats on mage
    def test_reset_stats_on_mage(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
        # Reset
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
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
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Tests for handle_modifiers with a flat modifier
    def test_handle_flat_modifier(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # Reset
        entity.active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        entity.backpack = []
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
        entity.backpack = []

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
        entity.backpack = []

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
        entity.backpack = []

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
        entity.backpack = []

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
        entity.backpack = []
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
            "Defence": "+3",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "-5",
            "Defence": "-2",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+20%",
            "Defence": "+50%",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "-20%",
            "Defence": "-50%",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add tile modifiers
        active_cli.grid.grid[0][0].modifiers = {
            "Attack": "-2",
            "Defence": "3",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add tile modifiers
        active_cli.grid.grid[0][0].modifiers = {
            "Attack": "-20%",
            "Defence": "50%",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
            "Defence": "-2",
        }
        # Add tile modifiers
        active_cli.grid.grid[0][0].modifiers = {
            "Attack": "+3",
            "Defence": "+10%",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Mana": "+50",
            "Spell_power": "+10",
            "Attack": "+5",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add inventory modifiers
        entity.inventory[0].effects = {
            "Attack": "+5",
        }
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Set entity tile to shallow water
        active_cli.grid.set_tile(0, 0, "shallowwater")
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.inventory[0].effects = {"Mana": "100", "Spell_power": "100%"}
        # Update stats
        entity.update_stats(active_cli)
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
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Set entity tile to shallow water
        active_cli.grid.set_tile(0, 0, "shallowwater")
        # Update stats
        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack, [])
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip weapon
        weapon = EQUIPMENT_TYPES["ironsword"]()
        entity.equip_item(weapon, weapon.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[0])

    # armor
    def test_equip_item_armor(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        self.assertEqual(entity.backpack, [])
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip armor
        armor = EQUIPMENT_TYPES["ironchestplate"]()
        entity.equip_item(armor, armor.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[1])

    # acc
    def test_equip_item_accessory(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip acc
        acc = EQUIPMENT_TYPES["ringofhaste"]()
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[2])

    # all
    def test_equip_item_all(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.backpack = []
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip items
        weapon = EQUIPMENT_TYPES["ironsword"]()
        armor = EQUIPMENT_TYPES["ironchestplate"]()
        acc = EQUIPMENT_TYPES["amuletofvitality"]()
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[0])
        self.assertEqual(entity.backpack[1], entity.inventory[1])
        self.assertEqual(entity.backpack[2], entity.inventory[2])

    # all on warrior with mage effects
    def test_equip_item_all_on_warrior_with_mage_effects(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.backpack = []
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip items
        weapon = EQUIPMENT_TYPES["magestaff"]()
        armor = EQUIPMENT_TYPES["ironchestplate"]()
        acc = EQUIPMENT_TYPES["ringofthesorcerer"]()
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[0])
        self.assertEqual(entity.backpack[1], entity.inventory[1])
        self.assertEqual(entity.backpack[2], entity.inventory[2])

    # all on mage with mage effects
    def test_equip_item_all_on_mage_with_mage_effects(self):
        entity = Mage(
            0,
            [0, 0],
        )
        # RESET
        entity.backpack = []
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip items
        weapon = EQUIPMENT_TYPES["magestaff"]()
        armor = EQUIPMENT_TYPES["ironchestplate"]()
        acc = EQUIPMENT_TYPES["ringofthesorcerer"]()
        entity.equip_item(weapon, weapon.slot.lower())
        entity.equip_item(armor, armor.slot.lower())
        entity.equip_item(acc, acc.slot.lower())
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(entity.backpack[0], entity.inventory[0])
        self.assertEqual(entity.backpack[1], entity.inventory[1])
        self.assertEqual(entity.backpack[2], entity.inventory[2])

    # wrong slot
    def test_equip_item_with_wrong_slot(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.backpack = []
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip acc
        acc = EQUIPMENT_TYPES["ringofhaste"]()
        entity.equip_item(acc, "weapon")
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
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
        self.assertEqual(len(entity.backpack), 0)

    # no existing weapon
    def test_equip_item_without_item(self):
        entity = Warrior(
            0,
            [0, 0],
        )
        # RESET
        entity.backpack = []
        entity.inventory[0] = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[1] = EQUIPMENT_TYPES["none_armor"]()
        entity.inventory[2] = EQUIPMENT_TYPES["none_acc"]()
        # create and equip acc
        entity.equip_item("unobtainium", "weapon")
        # update stats
        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        entity.update_stats(active_cli)
        # Check values
        self.assertEqual(entity.inventory[0].name, "None")
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(len(entity.backpack), 0)

    # Test create_entity with warrior
    def test_create_entity_warrior(self):
        temp_entity = create_entity("warrior", 5, 10, 0)

        self.assertIsInstance(temp_entity, Warrior)
        self.assertEqual(temp_entity.id, 0)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with mage
    def test_create_entity_mage(self):
        temp_entity = create_entity("mage", 5, 10, 1)

        self.assertIsInstance(temp_entity, Mage)
        self.assertEqual(temp_entity.id, 1)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with skeleton
    def test_create_entity_skeleton(self):
        temp_entity = create_entity("skeleton", 5, 10, 2)

        self.assertIsInstance(temp_entity, Skeleton)
        self.assertEqual(temp_entity.id, 2)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with goblin
    def test_create_entity_goblin(self):
        temp_entity = create_entity("goblin", 5, 10, 3)

        self.assertIsInstance(temp_entity, Goblin)
        self.assertEqual(temp_entity.id, 3)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity converts string coordinates to integers
    def test_create_entity_string_coordinates(self):
        temp_entity = create_entity("warrior", "5", "10", 0)

        self.assertIsInstance(temp_entity, Warrior)
        self.assertEqual(temp_entity.position, [5, 10])

    # Test create_entity with invalid entity type
    def test_create_entity_invalid_type(self):
        temp_entity = create_entity("invalid", 5, 10, 0)

        self.assertIsNone(temp_entity)

    # Test inventory remains unchanged when item exists in backpack
    def test_update_inventory_item_in_backpack(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        entity.inventory[0] = EQUIPMENT_TYPES["ironsword"]()

        # Get item from inventory
        item = entity.inventory[0]

        # Add item to backpack
        entity.backpack.append(item)

        # Update inventory
        entity.update_inventory()

        # Check item remains in inventory
        self.assertIn(item, entity.inventory)

    # Test inventory removes item that is not in backpack
    def test_update_inventory_remove_phantom_item(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]
        entity.inventory[0] = EQUIPMENT_TYPES["ironsword"]()
        entity.backpack.append(entity.inventory[0])
        # Get item from inventory
        item = entity.inventory[0]

        # Ensure item is not in backpack
        entity.backpack.clear()

        # Update inventory
        entity.update_inventory()

        # Check item was removed from inventory
        self.assertNotIn(item, entity.inventory)

    # Test inventory preserves None slots
    def test_update_inventory_preserve_none(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        # Add None item to inventory
        none_wep = EQUIPMENT_TYPES["none_wep"]()
        entity.inventory[0] = none_wep

        # Update inventory
        entity.update_inventory()

        # Check None item remains
        self.assertIn(none_wep, entity.inventory)

    # Test duplicate items remain equipped if duplicate exists in backpack
    def test_update_inventory_duplicate_item_in_backpack(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        # Get item from inventory
        item = entity.inventory[0]

        # Add duplicate item to backpack
        entity.backpack.append(item)

        # Update inventory
        entity.update_inventory()

        # Check equipped item remains
        self.assertIn(item, entity.inventory)

    # Test inventory removes phantom items but preserves valid items
    def test_update_inventory_mixed_items(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        # Get items from inventory
        equipped_item = entity.inventory[0]
        phantom_item = EQUIPMENT_TYPES["ironsword"]()

        # Add equipped item to backpack
        entity.backpack.append(equipped_item)

        # Add phantom item to inventory
        entity.inventory.append(phantom_item)

        # Update inventory
        entity.update_inventory()

        # Check valid item remains
        self.assertIn(equipped_item, entity.inventory)

        # Check phantom item is removed
        self.assertNotIn(phantom_item, entity.inventory)

    # Test inventory with multiple phantom items
    def test_update_inventory_multiple_phantom_items(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        # Get items from inventory
        item_one = EQUIPMENT_TYPES["ironsword"]()
        item_two = EQUIPMENT_TYPES["leathertunic"]()
        item_three = EQUIPMENT_TYPES["none_acc"]()

        # Add phantom items to inventory
        entity.inventory = [item_one, item_two, item_three]

        # Ensure backpack is empty
        entity.backpack.clear()

        # Update inventory
        entity.update_inventory()

        # Check phantom items were removed
        self.assertNotIn(item_one, entity.inventory)
        self.assertNotIn(item_two, entity.inventory)

    # Test inventory preserves duplicate equipped items
    def test_update_inventory_duplicate_equipped_items(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"],
            EQUIPMENT_TYPES["none_armor"],
            EQUIPMENT_TYPES["none_acc"],
        ]

        # Get item
        item = EQUIPMENT_TYPES["ironsword"]

        # Add duplicate items to inventory
        entity.inventory = [item, item]

        # Add item to backpack
        entity.backpack.append(item)

        # Update inventory
        entity.update_inventory()

        # Check both equipped duplicates remain
        self.assertEqual(entity.inventory.count(item), 2)

    # Test inventory containing only None items
    def test_update_inventory_only_none_items(self):

        # Create test entity
        entity = Warrior(0, [0, 0])
        # reset
        entity.backpack = []
        entity.inventory = [
            EQUIPMENT_TYPES["none_wep"](),
            EQUIPMENT_TYPES["none_armor"](),
            EQUIPMENT_TYPES["none_acc"](),
        ]

        # Get None items
        none_wep = EQUIPMENT_TYPES["none_wep"]()
        none_armor = EQUIPMENT_TYPES["none_armor"]()
        none_acc = EQUIPMENT_TYPES["none_acc"]()

        # Set inventory to None items
        entity.inventory = [none_wep, none_armor, none_acc]

        # Clear backpack
        entity.backpack.clear()

        # Update inventory
        entity.update_inventory()

        # Check None items remain
        self.assertEqual(
            entity.inventory,
            [none_wep, none_armor, none_acc],
        )

    # Test for calculate_max_stats with no modifiers
    def test_calculate_max_stats_with_no_modifiers(self):

        entity = Warrior(
            0,
            [0, 0],
        )

        # Calculate max stats
        entity.calculate_max_stats()

        # Check values
        self.assertEqual(entity.max_health, 120)

        # Test for calculate_max_stats with flat modifiers

    def test_calculate_max_stats_with_flat_modifiers(self):

        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                },
                "Percent_modifiers": {},
            },
        )

        # Calculate max stats
        entity.calculate_max_stats()

        # Check values
        self.assertEqual(entity.max_health, 140)

    # Test for calculate_max_stats with percent modifiers
    def test_calculate_max_stats_with_percent_modifiers(self):

        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Health": 10,
                },
            },
        )

        # Calculate max stats
        entity.calculate_max_stats()

        # Check values
        self.assertEqual(entity.max_health, 132)

    # Test for calculate_max_stats with flat and percent modifiers
    def test_calculate_max_stats_with_flat_and_percent_modifiers(self):

        entity = Warrior(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                },
                "Percent_modifiers": {
                    "Health": 10,
                },
            },
        )

        # Calculate max stats
        entity.calculate_max_stats()

        # Check values
        self.assertEqual(entity.max_health, 154)

    # Test for calculate_max_stats with Mage stats
    def test_calculate_max_stats_with_mage_stats(self):

        entity = Mage(
            0,
            [0, 0],
            {
                "Flat_modifiers": {
                    "Health": 20,
                    "Mana": 25,
                },
                "Percent_modifiers": {
                    "Health": 10,
                    "Mana": 50,
                },
            },
        )

        # Calculate max stats
        entity.calculate_max_stats()

        # Check values
        self.assertEqual(entity.max_health, 99)
        self.assertEqual(entity.max_mana, 187.5)

    # Tests for update_stats with max health modifier on warrior
    def test_update_stats_on_warrior_with_max_health_modifier(self):

        entity = Warrior(
            0,
            [0, 0],
        )

        # RESET
        entity.inventory[0].effects = {}
        entity.inventory[1].effects = {}
        entity.inventory[2].effects = {}

        # Create active CLI
        active_cli = cli.CLI()

        # Create active grid
        active_cli.grid = Grid(5, 5)

        # Add health modifier
        entity.inventory[0].effects = {
            "Health": "+20%",
        }

        # Update stats
        entity.update_stats(active_cli)

        entity.health -= 24

        # Check current and max health
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.max_health, 144)

        # Check modifiers
        self.assertDictEqual(
            entity.active_modifiers,
            {
                "Flat_modifiers": {},
                "Percent_modifiers": {
                    "Health": 20,
                },
            },
        )

    # Test use_consumable with Small Health Potion
    def test_use_consumable_small_health_potion(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health increased by 20
        self.assertEqual(entity.health, 70)
        # Check stats after using potion
        # Check Health increased by 20
        self.assertEqual(entity.health, 70)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Greater Health Potion
    def test_use_consumable_greater_health_potion(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = EQUIPMENT_TYPES["greaterhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health increased by 50
        self.assertEqual(entity.health, 100)

        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Superior Health Potion
    def test_use_consumable_superior_health_potion(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = EQUIPMENT_TYPES["superiorhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health is capped at max Health
        self.assertEqual(entity.health, 120)
        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Health Potion exceeding max Health
    def test_use_consumable_health_potion_exceeds_max(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 110

        # Get consumable
        consumable = EQUIPMENT_TYPES["greaterhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health does not exceed max Health
        self.assertEqual(entity.health, 120)
        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Health Potion at max Health
    def test_use_consumable_health_potion_at_max_health(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = entity.max_health

        # Get consumable
        consumable = EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health remains at max Health
        self.assertEqual(entity.health, 120)
        # Check other stats remain unchanged
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Turtle Master Potion instant effect
    def test_use_consumable_turtle_master_instant_effect(self):
        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Health increased by 10 percent of current Health
        self.assertEqual(entity.health, 55)
        # Check other stats remain unchanged immediately
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with Mana Potion
    def test_use_consumable_mana_potion(self):
        # Create test entity
        entity = Mage(0, [0, 0])

        # Set current Mana
        entity.mana = 25

        # Get consumable
        consumable = EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Mana increased by 50
        self.assertEqual(entity.mana, 75)
        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable with Mana Potion exceeding max Mana
    def test_use_consumable_mana_potion_exceeds_max(self):
        # Create test entity
        entity = Mage(0, [0, 0])

        # Set current Mana
        entity.mana = 90

        # Get consumable
        consumable = EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Mana does not exceed max Mana
        self.assertEqual(entity.mana, 100)
        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable with Mana Potion at max Mana
    def test_use_consumable_mana_potion_at_max_mana(self):
        # Create test entity
        entity = Mage(0, [0, 0])

        # Set current Mana
        entity.mana = entity.max_mana

        # Get consumable
        consumable = EQUIPMENT_TYPES["manapotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check Mana remains at max Mana
        self.assertEqual(entity.mana, 100)
        # Check other stats remain unchanged
        self.assertEqual(entity.health, 70)
        self.assertEqual(entity.attack, 8)
        self.assertEqual(entity.defence, 4)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 70)
        self.assertEqual(entity.max_mana, 100)

    # Test use_consumable with Turtle Master Potion over-time effects
    def test_use_consumable_turtle_master_over_time_effects(self):
        # Create test entity
        entity = Warrior(0, [0, 0])
        entity.temp_buffs.clear()

        # Get consumable
        consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check buff name
        self.assertEqual(
            entity.temp_buffs[0]["Name"],
            "TurtleMasterPotion",
        )

        # Check buff effects
        self.assertEqual(
            entity.temp_buffs[0]["Effects"],
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

        # Check buff duration
        self.assertEqual(
            entity.temp_buffs[0]["Turns"],
            5,
        )
        # Check stats remain unchanged immediately
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
        first_consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()
        second_consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use first consumable
        use_consumable(first_consumable, entity)

        # Use second consumable
        use_consumable(second_consumable, entity)

        # Check first buff duration
        self.assertEqual(
            entity.temp_buffs[0]["Turns"],
            5,
        )

        # Check second buff duration
        self.assertEqual(
            entity.temp_buffs[1]["Turns"],
            5,
        )
        # Check stats remain unchanged immediately
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with consumable without over-time effects
    def test_use_consumable_no_over_time_effects(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # Get consumable
        consumable = EQUIPMENT_TYPES["smallhealthpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check no temporary buffs were added
        self.assertEqual(entity.temp_buffs, [])
        # Check stats remain unchanged immediately
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)

    # Test use_consumable with instant and over-time effects
    def test_use_consumable_instant_and_over_time_effects(self):

        # Create test entity
        entity = Warrior(0, [0, 0])

        # Set current Health
        entity.health = 50

        # Get consumable
        consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check instant Health effect
        self.assertEqual(entity.health, 55)

        # Check buff duration
        self.assertEqual(
            entity.temp_buffs[0]["Turns"],
            5,
        )
        # Check stats remain unchanged immediately
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
        consumable = EQUIPMENT_TYPES["turtlemasterpotion"]()

        # Use consumable
        use_consumable(consumable, entity)

        # Check existing buff was preserved
        self.assertEqual(
            entity.temp_buffs[0]["Name"],
            "ExistingBuff",
        )

        # Check new buff was added
        self.assertEqual(
            entity.temp_buffs[1]["Name"],
            "TurtleMasterPotion",
        )
        # Check stats remain unchanged immediately
        self.assertEqual(entity.health, 120)
        self.assertEqual(entity.attack, 15)
        self.assertEqual(entity.defence, 10)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.max_health, 120)
