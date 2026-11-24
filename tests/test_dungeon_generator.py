"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 24, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_dungeon_generator.py
Purpose: Utilizes unittest to test all of the classes and methods in dungeon_generator.py file
"""

import random
import unittest
from collections import deque
from unittest.mock import patch

from dungeon_generator import DungeonGenerator
from dungeon_floor import DungeonFloor


class TestDungeonGenerator(unittest.TestCase):
    def make_generator(self, seed=42, wall_chance=0.45):
        # Seed the generator's internal RNG for reproducible tests.
        generator = DungeonGenerator(wall_chance=wall_chance)
        generator._DungeonGenerator__rng = random.Random(seed)
        return generator

    def make_walls(self, width, height, open_tiles=()):
        # True represents a wall; False represents an open tile.
        walls = [[True for _ in range(height)] for _ in range(width)]
        for x, y in open_tiles:
            walls[x][y] = False
        return walls

    def get_open_tiles(self, walls):
        return {
            (x, y)
            for x in range(len(walls))
            for y in range(len(walls[0]))
            if not walls[x][y]
        }

    def get_reachable_tiles(self, grid, start, width, height):
        # Explore the generated grid using four-directional movement.
        visited = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and (nx, ny) not in visited
                    and grid.is_passable(nx, ny)
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return visited

    def test_generates_floor_and_connected_endpoints(self):
        generator = self.make_generator(seed=42)
        floor = generator.generate(3, 25, 20)
        self.assertIsInstance(floor, DungeonFloor)
        info = floor.get_info()
        self.assertEqual((info.floor_number, info.width, info.height), (3, 25, 20))
        self.assertNotEqual(info.entrance, info.exit)
        grid = floor.get_grid()
        self.assertTrue(grid.is_passable(*info.entrance))
        self.assertTrue(grid.is_passable(*info.exit))

        visited = self.get_reachable_tiles(grid, info.entrance, info.width, info.height)
        self.assertIn(info.exit, visited)
        self.assertEqual(
            len(visited),
            sum(
                grid.is_passable(x, y)
                for x in range(info.width)
                for y in range(info.height)
            ),
        )

    def test_generated_floors_connected_across_multiple_seeds(self):
        # Different random layouts should still have exactly one open region.
        for seed in range(10):
            with self.subTest(seed=seed):
                generator = self.make_generator(seed=seed)
                floor = generator.generate(1, 15, 15)
                info = floor.get_info()
                grid = floor.get_grid()
                visited = self.get_reachable_tiles(grid, info.entrance, 15, 15)
                self.assertIn(info.exit, visited)
                self.assertEqual(
                    len(visited),
                    sum(grid.is_passable(x, y) for x in range(15) for y in range(15)),
                )

    def test_find_open_regions_separate_areas(self):
        generator = self.make_generator()
        first = {(1, 1), (2, 1), (2, 2)}
        second = {(6, 5), (6, 6)}
        walls = self.make_walls(9, 9, first | second)
        regions = generator._DungeonGenerator__find_open_regions(walls, 9, 9)
        self.assertEqual(len(regions), 2)
        self.assertEqual(
            {frozenset(region) for region in regions},
            {frozenset(first), frozenset(second)},
        )

    def test_find_open_regions_does_not_connect_diagonals(self):
        generator = self.make_generator()
        walls = self.make_walls(5, 5, {(1, 1), (2, 2)})
        regions = generator._DungeonGenerator__find_open_regions(walls, 5, 5)
        self.assertEqual(len(regions), 2)
        self.assertTrue(all(len(region) == 1 for region in regions))

    def test_find_open_regions_empty_map(self):
        generator = self.make_generator()
        walls = self.make_walls(7, 7)
        self.assertEqual(
            generator._DungeonGenerator__find_open_regions(walls, 7, 7), []
        )

    def test_find_open_regions_one_region(self):
        generator = self.make_generator()
        open_tiles = {(1, 1), (2, 1), (2, 2)}
        walls = self.make_walls(7, 7, open_tiles)
        regions = generator._DungeonGenerator__find_open_regions(walls, 7, 7)
        self.assertEqual(regions, [open_tiles])

    def test_find_open_regions_does_not_modify_walls(self):
        generator = self.make_generator()
        walls = self.make_walls(7, 7, {(1, 1), (4, 4)})
        before = [column.copy() for column in walls]
        generator._DungeonGenerator__find_open_regions(walls, 7, 7)
        self.assertEqual(walls, before)

    def test_carve_corridor_horizontal_first(self):
        generator = self.make_generator()
        walls = self.make_walls(9, 9)
        with patch.object(
            generator._DungeonGenerator__rng, "choice", return_value=True
        ):
            generator._DungeonGenerator__carve_corridor(walls, (2, 2), (6, 5))
        expected = {(x, 2) for x in range(2, 7)} | {(6, y) for y in range(2, 6)}
        self.assertEqual(self.get_open_tiles(walls), expected)

    def test_carve_corridor_vertical_first(self):
        generator = self.make_generator()
        walls = self.make_walls(9, 9)
        with patch.object(
            generator._DungeonGenerator__rng, "choice", return_value=False
        ):
            generator._DungeonGenerator__carve_corridor(walls, (2, 2), (6, 5))
        expected = {(2, y) for y in range(2, 6)} | {(x, 5) for x in range(2, 7)}
        self.assertEqual(self.get_open_tiles(walls), expected)

    def test_connect_regions_preserves_existing_open_tiles(self):
        generator = self.make_generator()
        original = {(1, 1), (2, 1), (6, 2), (6, 3), (3, 6), (4, 6)}
        walls = self.make_walls(9, 9, original)
        generator._DungeonGenerator__connect_regions(walls, 9, 9)
        self.assertTrue(original.issubset(self.get_open_tiles(walls)))
        regions = generator._DungeonGenerator__find_open_regions(walls, 9, 9)
        self.assertEqual(len(regions), 1)
        self.assertGreater(len(regions[0]), len(original))

    def test_connect_regions_already_connected_does_not_change_map(self):
        generator = self.make_generator()
        walls = self.make_walls(7, 7, {(1, 1), (2, 1), (2, 2)})
        before = [column.copy() for column in walls]
        generator._DungeonGenerator__connect_regions(walls, 7, 7)
        self.assertEqual(walls, before)

    def test_connect_regions_no_open_tiles_does_not_change_map(self):
        generator = self.make_generator()
        walls = self.make_walls(7, 7)
        generator._DungeonGenerator__connect_regions(walls, 7, 7)
        self.assertEqual(self.get_open_tiles(walls), set())

    def test_connect_regions_preserves_border_walls(self):
        generator = self.make_generator()
        walls = self.make_walls(9, 9, {(1, 1), (7, 7), (2, 6)})
        generator._DungeonGenerator__connect_regions(walls, 9, 9)
        for x in range(9):
            self.assertTrue(walls[x][0])
            self.assertTrue(walls[x][8])
        for y in range(9):
            self.assertTrue(walls[0][y])
            self.assertTrue(walls[8][y])

    def test_farthest_uses_path_distance(self):
        generator = self.make_generator()
        # The winding path makes (1, 3) farther than nearby-looking tiles.
        path = {(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3)}
        farthest = generator._DungeonGenerator__farthest((1, 1), path)
        self.assertEqual(farthest, (1, 3))

    def test_special_tile_percentages_total_100(self):
        generator = self.make_generator(seed=7)
        self.assertIsNone(generator.get_terrain_percentages())
        generator.generate(1, 15, 15)
        chances = generator.get_terrain_percentages()
        self.assertEqual(sum(chances.values()), 100)
        self.assertTrue(
            all(
                0 <= chances[t] <= generator.SPECIAL_TILE_PERCENT_MAX
                for t in generator.SPECIAL_TILES
            )
        )
        self.assertEqual(
            chances["Floor"], 100 - sum(chances[t] for t in generator.SPECIAL_TILES)
        )

    def test_terrain_percentages_returns_copy(self):
        generator = self.make_generator(seed=7)
        generator.generate(1, 10, 10)
        original = generator.get_terrain_percentages()
        changed = generator.get_terrain_percentages()
        changed["Forest"] = -1
        self.assertEqual(generator.get_terrain_percentages(), original)

    def test_exact_terrain_roll_thresholds(self):
        generator = self.make_generator()
        with patch.object(
            generator._DungeonGenerator__rng, "randint", side_effect=[10, 50]
        ):
            chances = generator._DungeonGenerator__roll_terrain_percentages()
        self.assertEqual(chances, {"ShallowWater": 10, "Forest": 50, "Floor": 40})

        def classify(roll):
            cumulative = 0
            for name, chance in chances.items():
                cumulative += chance
                if roll <= cumulative:
                    return name
            return None

        self.assertEqual(
            [classify(r) for r in (1, 10, 11, 60, 61, 100)],
            ["ShallowWater", "ShallowWater", "Forest", "Forest", "Floor", "Floor"],
        )

    def test_terrain_percentage_rolls_respect_remaining_total(self):
        generator = self.make_generator()
        with patch.object(
            generator._DungeonGenerator__rng, "randint", side_effect=[50, 50]
        ):
            chances = generator._DungeonGenerator__roll_terrain_percentages()
        self.assertEqual(chances, {"ShallowWater": 50, "Forest": 50, "Floor": 0})

    def test_different_floor_rolls(self):
        generator = self.make_generator(seed=5)
        generator.generate(1, 15, 15)
        first = generator.get_terrain_percentages()
        generator.generate(2, 15, 15)
        second = generator.get_terrain_percentages()
        self.assertNotEqual(first, second)

    def test_invalid_dimensions(self):
        generator = self.make_generator()
        for width, height in (
            (4, 10),
            (10, 4),
            (51, 10),
            (10, 51),
            (True, 10),
            (10, False),
            (10.5, 10),
            (10, "10"),
        ):
            with self.subTest(width=width, height=height):
                with self.assertRaises(ValueError):
                    generator.generate(1, width, height)

    def test_invalid_floor_numbers(self):
        generator = self.make_generator()
        for floor_number in (0, -1, True, 1.5, "1"):
            with self.subTest(floor_number=floor_number):
                with self.assertRaises(ValueError):
                    generator.generate(floor_number, 10, 10)

    def test_invalid_wall_chances(self):
        for chance in (-0.01, 1.01):
            with self.subTest(chance=chance):
                with self.assertRaises(ValueError):
                    DungeonGenerator(wall_chance=chance)

    def test_fallback_on_fully_walled_map(self):
        generator = self.make_generator(seed=4, wall_chance=1)
        floor = generator.generate(1, 5, 5)
        info = floor.get_info()
        self.assertNotEqual(info.entrance, info.exit)
        grid = floor.get_grid()
        for x in range(1, 4):
            for y in range(1, 4):
                self.assertTrue(grid.is_passable(x, y))

    def test_border_is_walled(self):
        generator = self.make_generator(seed=3, wall_chance=0)
        floor = generator.generate(1, 10, 10)
        grid = floor.get_grid()
        for x in range(10):
            self.assertFalse(grid.is_passable(x, 0))
            self.assertFalse(grid.is_passable(x, 9))
        for y in range(10):
            self.assertFalse(grid.is_passable(0, y))
            self.assertFalse(grid.is_passable(9, y))

    def test_smoothing_keeps_border_walls(self):
        generator = self.make_generator()
        walls = self.make_walls(
            7, 7, {(x, y) for x in range(1, 6) for y in range(1, 6)}
        )
        smoothed = generator._DungeonGenerator__smooth(walls, 7, 7)
        for x in range(7):
            self.assertTrue(smoothed[x][0])
            self.assertTrue(smoothed[x][6])
        for y in range(7):
            self.assertTrue(smoothed[0][y])
            self.assertTrue(smoothed[6][y])


if __name__ == "__main__":
    unittest.main()
