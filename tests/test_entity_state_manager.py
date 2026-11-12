"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 11, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_entity_state_manager.py
Purpose: Utilizes unittest to test all of the classes and methods in entity_state_manager.py file
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
from unittest.mock import MagicMock
from entity_state_manager import EntityStateManager
from entity_state import DefendingState, AttackingState, FleeingState
from domain_library import AttackTypes


# Class for testing entity state manager
class TestEntityStateManager(unittest.TestCase):

    def setUp(self):
        self.manager = EntityStateManager(None, None, DefendingState())

    def test_initial_state(self):
        self.assertEqual(self.manager.get_current_state_name(), "Defending")

    def test_defending_to_attacking(self):
        self.manager.transition_to(AttackingState())

        self.assertEqual(self.manager.get_current_state_name(), "Attacking")

    def test_attacking_to_fleeing(self):
        self.manager.transition_to(AttackingState())
        self.manager.transition_to(FleeingState())

        self.assertEqual(self.manager.get_current_state_name(), "Fleeing")

    def test_fleeing_to_defending(self):
        self.manager.transition_to(AttackingState())
        self.manager.transition_to(FleeingState())
        self.manager.transition_to(DefendingState())

        self.assertEqual(self.manager.get_current_state_name(), "Defending")

    def test_invalid_transition(self):
        with self.assertRaises(ValueError):
            self.manager.transition_to(FleeingState())

    def test_invalid_transition_preserves_state(self):
        with self.assertRaises(ValueError):
            self.manager.transition_to(FleeingState())

        self.assertEqual(self.manager.get_current_state_name(), "Defending")

    def test_is_valid_transition(self):
        self.assertTrue(self.manager.is_valid_transition(AttackingState()))

        self.assertFalse(self.manager.is_valid_transition(FleeingState()))

    def test_get_current_state(self):
        self.assertIsInstance(self.manager.get_current_state(), DefendingState)

    def test_multiple_transitions(self):
        self.manager.transition_to(AttackingState())
        self.manager.transition_to(FleeingState())
        self.manager.transition_to(DefendingState())
        self.manager.transition_to(AttackingState())

        self.assertEqual(self.manager.get_current_state_name(), "Attacking")

    def test_update(self):
        mock_state = MagicMock()
        mock_state.get_name.return_value = "Defending"

        manager = EntityStateManager(None, None, mock_state)

        manager.update()

        mock_state.update.assert_called_once_with(manager)

    def test_state_lifecycle(self):
        old_state = MagicMock()
        old_state.get_name.return_value = "Defending"

        new_state = MagicMock()
        new_state.get_name.return_value = "Attacking"

        manager = EntityStateManager(None, None, old_state)

        old_state.enter.assert_called_once_with(manager)

        manager.transition_to(new_state)

        old_state.exit.assert_called_once_with(manager)
        new_state.enter.assert_called_once_with(manager)

    # Create Test Entity State Manager
    # Creates a manager with mocked GameState and entity information
    # Params: position - list - entity coordinates
    #         speed - int - movement speed
    #         attack_type - AttackTypes - entity attack type
    # Returns: tuple - manager, game_state, entity_info
    def create_test_manager(
        self, position=None, speed=4, attack_type=AttackTypes.MELEE
    ):
        if position is None:
            position = [1, 2]

        # Create mock GameState
        game_state = MagicMock()

        # Create mock entity information
        entity_info = MagicMock()
        entity_info.id = 1
        entity_info.position = position
        entity_info.speed = speed
        entity_info.attack_type = attack_type

        # Create manager with mock entity
        entity = MagicMock()
        entity.get_info.return_value = entity_info

        manager = EntityStateManager(entity, game_state, DefendingState())

        return manager, game_state, entity_info

    # Test get_distance_to_player - reachable target
    def test_get_distance_to_player_reachable(self):
        manager, game_state, entity_info = self.create_test_manager()

        # Create target information
        target_info = MagicMock()
        target_info.position = [5, 2]

        # Set expected distance
        game_state.get_distance_between_entities.return_value = 4

        result = manager.get_distance_to_player(target_info)

        self.assertEqual(result, 4)
        game_state.get_distance_between_entities.assert_called_once_with(
            entity_info, target_info
        )

    # Test get_distance_to_player - unreachable target
    def test_get_distance_to_player_unreachable(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [5, 2]

        # No reachable path
        game_state.get_distance_between_entities.return_value = None

        result = manager.get_distance_to_player(target_info)

        self.assertIsNone(result)
        game_state.get_distance_between_entities.assert_called_once_with(
            entity_info, target_info
        )

    # Test get_distance_to_player - same position
    def test_get_distance_to_player_same_position(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [1, 2]

        game_state.get_distance_between_entities.return_value = 0

        result = manager.get_distance_to_player(target_info)

        self.assertEqual(result, 0)

    # Test attack_target - successful attack
    def test_attack_target_success(self):
        manager, game_state, entity_info = self.create_test_manager()

        # Set damage dealt
        game_state.attack_entity.return_value = 15

        result = manager.attack_target(2)

        self.assertEqual(result, 15)
        game_state.attack_entity.assert_called_once_with(1, 2)

    # Test attack_target - zero damage
    def test_attack_target_zero_damage(self):
        manager, game_state, entity_info = self.create_test_manager()

        game_state.attack_entity.return_value = 0

        result = manager.attack_target(2)

        self.assertEqual(result, 0)
        game_state.attack_entity.assert_called_once_with(1, 2)

    # Test attack_target - correct attacker ID
    def test_attack_target_correct_attacker(self):
        manager, game_state, entity_info = self.create_test_manager()

        entity_info.id = 5
        game_state.attack_entity.return_value = 10

        result = manager.attack_target(8)

        self.assertEqual(result, 10)
        game_state.attack_entity.assert_called_once_with(5, 8)

    # Test move_toward_target - melee stops within attack range
    def test_move_toward_target_melee_attack_range(self):
        manager, game_state, entity_info = self.create_test_manager(
            speed=5, attack_type=AttackTypes.MELEE
        )

        target_info = MagicMock()
        target_info.position = [5, 2]

        # Path to target
        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # Stop one tile away from target
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 4, 2)

    # Test move_toward_target - ranged stops within attack range
    def test_move_toward_target_ranged_attack_range(self):
        manager, game_state, entity_info = self.create_test_manager(
            speed=5, attack_type=AttackTypes.RANGED
        )

        target_info = MagicMock()
        target_info.position = [7, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
            (7, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # Stop three tiles away
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 4, 2)

    # Test move_toward_target - limited movement speed
    def test_move_toward_target_limited_speed(self):
        manager, game_state, entity_info = self.create_test_manager(
            speed=2, attack_type=AttackTypes.MELEE
        )

        target_info = MagicMock()
        target_info.position = [6, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # Move exactly two tiles
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 2)

    # Test move_toward_target - speed greater than required
    def test_move_toward_target_speed_exceeds_distance(self):
        manager, game_state, entity_info = self.create_test_manager(
            speed=10, attack_type=AttackTypes.MELEE
        )

        target_info = MagicMock()
        target_info.position = [4, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # Stop before entering target tile
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 2)

    # Test move_toward_target - zero movement speed
    def test_move_toward_target_zero_speed(self):
        manager, game_state, entity_info = self.create_test_manager(speed=0)

        target_info = MagicMock()
        target_info.position = [5, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]

        result = manager.move_toward_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_toward_target - negative movement speed
    def test_move_toward_target_negative_speed(self):
        manager, game_state, entity_info = self.create_test_manager(speed=-3)

        target_info = MagicMock()
        target_info.position = [5, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]

        result = manager.move_toward_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_toward_target - no path exists
    def test_move_toward_target_no_path(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [5, 2]

        game_state.get_shortest_path_between_entities.return_value = None

        result = manager.move_toward_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_toward_target - path contains only current position
    def test_move_toward_target_same_position(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [1, 2]

        game_state.get_shortest_path_between_entities.return_value = [(1, 2)]

        result = manager.move_toward_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_toward_target - first tile occupied
    def test_move_toward_target_first_tile_occupied(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [5, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]

        # First movement tile occupied
        game_state.is_grid_tile_occupied.side_effect = lambda x, y: (x, y) == (2, 2)

        result = manager.move_toward_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_toward_target - occupied tile during movement
    def test_move_toward_target_occupied_tile_mid_path(self):
        manager, game_state, entity_info = self.create_test_manager(speed=4)

        target_info = MagicMock()
        target_info.position = [6, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
        ]

        # Tile at (4, 2) is occupied
        game_state.is_grid_tile_occupied.side_effect = lambda x, y: (x, y) == (4, 2)

        result = manager.move_toward_target(target_info)

        # Stop at last available tile
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 2)

    # Test move_toward_target - path around wall
    def test_move_toward_target_around_wall(self):
        manager, game_state, entity_info = self.create_test_manager(speed=3)

        target_info = MagicMock()
        target_info.position = [4, 2]

        # A* path navigates around wall
        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (4, 3),
            (4, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # Move three tiles along path
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 3)

    # Test move_toward_target - ranged stops along alternate path
    def test_move_toward_target_ranged_around_wall(self):
        manager, game_state, entity_info = self.create_test_manager(
            speed=5, attack_type=AttackTypes.RANGED
        )

        target_info = MagicMock()
        target_info.position = [4, 2]

        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (4, 3),
            (4, 2),
        ]

        game_state.is_grid_tile_occupied.return_value = False

        result = manager.move_toward_target(target_info)

        # First step is within Manhattan attack range (3)
        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test move_toward_target - path lookup uses correct entities
    def test_move_toward_target_path_arguments(self):
        manager, game_state, entity_info = self.create_test_manager()

        target_info = MagicMock()
        target_info.position = [5, 2]

        game_state.get_shortest_path_between_entities.return_value = None

        manager.move_toward_target(target_info)

        game_state.get_shortest_path_between_entities.assert_called_once_with(
            entity_info, target_info
        )


if __name__ == "__main__":
    unittest.main()
