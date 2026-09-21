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

# Imports
import unittest
from entity import Warrior, Mage, Goblin, Skeleton


# Class for testing entities
class TestEntity(unittest.TestCase):

    # Init for all entity types\
    # Init warrior with base stats
    def test_warrior_init(self):
        entity = Warrior(
            0,
            "warrior",
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
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
            "goblin",
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
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
            "skeleton",
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
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
            "mage",
            [0, 0],
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
        )
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
