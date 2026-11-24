"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 23, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_dungeon_floor.py
Purpose: Utilizes unittest to test all of the classes and methods in dungeon_floor.py file
"""

# Imports
import unittest
from dungeon_floor import DungeonFloor
from grid import Grid


# Testing class
class TestDungeonFloor(unittest.TestCase):
    def test_initialization(self):
        floor = DungeonFloor(1, 10, 8)
        info = floor.get_info()
        self.assertEqual((info.floor_number, info.width, info.height), (1, 10, 8))
        self.assertIsNone(info.entrance)
        self.assertIsNone(info.exit)

    def test_accepts_existing_grid(self):
        grid = Grid(5, 5)
        self.assertIs(DungeonFloor(2, grid=grid).get_grid(), grid)

    def test_invalid_floor_number(self):
        with self.assertRaises(ValueError):
            DungeonFloor(0, 5, 5)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            DungeonFloor(1, 4, 5)

    def test_entrance_and_exit(self):
        floor = DungeonFloor(1, 5, 5)
        floor.set_entrance(0, 0)
        floor.set_exit(4, 4)
        self.assertEqual(floor.get_info().entrance, (0, 0))
        self.assertEqual(floor.get_info().exit, (4, 4))

    def test_rejects_wall_entrance(self):
        floor = DungeonFloor(1, 5, 5)
        floor.get_grid().set_tile(1, 1, "wall")
        with self.assertRaises(ValueError):
            floor.set_entrance(1, 1)

    def test_rejects_same_entrance_and_exit(self):
        floor = DungeonFloor(1, 5, 5)
        floor.set_entrance(2, 2)
        with self.assertRaises(ValueError):
            floor.set_exit(2, 2)

    def test_round_trip_memento(self):
        floor = DungeonFloor(3, 5, 5)
        floor.get_grid().set_tile(2, 2, "wall")
        floor.set_entrance(0, 0)
        floor.set_exit(4, 4)
        saved = floor.create_memento()
        floor.get_grid().set_tile(2, 2, "floor")
        floor.set_exit(3, 3)
        floor.restore(saved)
        self.assertFalse(floor.get_grid().is_passable(2, 2))
        self.assertEqual(floor.get_info().exit, (4, 4))
        self.assertEqual(floor.create_memento(), saved)

    def test_rejects_invalid_memento(self):
        with self.assertRaises(TypeError):
            DungeonFloor(1, 5, 5).restore(None)


if __name__ == "__main__":
    unittest.main()
