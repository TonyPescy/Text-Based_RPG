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
        self.entity = MagicMock()
        self.entity.get_info.return_value.e_type = "Goblin"

        self.game_state = MagicMock()

        self.manager = EntityStateManager(
            self.entity, self.game_state, DefendingState()
        )

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
            self.manager.transition_to(DefendingState())

    def test_invalid_transition_preserves_state(self):
        with self.assertRaises(ValueError):
            self.manager.transition_to(DefendingState())

        self.assertEqual(self.manager.get_current_state_name(), "Defending")

    def test_is_valid_transition(self):
        self.assertTrue(self.manager.is_valid_transition(AttackingState()))

        self.assertTrue(self.manager.is_valid_transition(FleeingState()))

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

    # Test State Lifecycle
    # Verifies that enter and exit are called during state transitions
    def test_state_lifecycle(self):
        old_state = MagicMock()
        old_state.get_name.return_value = "Defending"

        new_state = MagicMock()
        new_state.get_name.return_value = "Attacking"

        # Create manager using the entity and game state from setUp
        manager = EntityStateManager(self.entity, self.game_state, old_state)

        # Verify initial state was entered
        old_state.enter.assert_called_once_with(manager)

        # Transition to new state
        manager.transition_to(new_state)

        # Verify lifecycle methods
        old_state.exit.assert_called_once_with(manager)
        new_state.enter.assert_called_once_with(manager)

        # Verify current state
        self.assertIs(manager.get_current_state(), new_state)

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

    # Test move_away_from_target - successful movement
    def test_move_away_from_target_success(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        # Create target information
        target_info = MagicMock()
        target_info.position = [4, 3]

        # Set flee position
        game_state.get_flee_position.return_value = [2, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)

        game_state.get_flee_position.assert_called_once_with(entity_info, target_info)

        game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test move_away_from_target - no escape position
    def test_move_away_from_target_no_escape(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [4, 3]

        # No valid escape tile
        game_state.get_flee_position.return_value = None

        result = manager.move_away_from_target(target_info)

        self.assertFalse(result)
        game_state.move_entity.assert_not_called()

    # Test move_away_from_target - flee left
    def test_move_away_from_target_left(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [4, 3]

        game_state.get_flee_position.return_value = [2, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test move_away_from_target - flee right
    def test_move_away_from_target_right(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [2, 3]

        game_state.get_flee_position.return_value = [4, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 4, 3)

    # Test move_away_from_target - flee upward
    def test_move_away_from_target_up(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [3, 2]

        game_state.get_flee_position.return_value = [3, 4]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 4)

    # Test move_away_from_target - flee downward
    def test_move_away_from_target_down(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [3, 4]

        game_state.get_flee_position.return_value = [3, 2]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 3, 2)

    # Test move_away_from_target - correct entity ID
    def test_move_away_from_target_correct_entity_id(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        # Set different entity ID
        entity_info.id = 5

        target_info = MagicMock()
        target_info.position = [4, 3]

        game_state.get_flee_position.return_value = [2, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(5, 2, 3)

    # Test move_away_from_target - grid boundary
    def test_move_away_from_target_grid_boundary(self):
        manager, game_state, entity_info = self.create_test_manager(position=[0, 0])

        target_info = MagicMock()
        target_info.position = [1, 0]

        # Only valid escape position
        game_state.get_flee_position.return_value = [0, 1]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 0, 1)

    # Test move_away_from_target - speed does not affect movement
    def test_move_away_from_target_high_speed(self):
        manager, game_state, entity_info = self.create_test_manager(
            position=[3, 3], speed=5
        )

        target_info = MagicMock()
        target_info.position = [4, 3]

        # Current fleeing logic selects one neighboring tile
        game_state.get_flee_position.return_value = [2, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test set_game_state - updates GameState reference
    # Checks that the manager uses the new GameState
    def test_set_game_state_updates_reference(self):
        manager, old_game_state, entity_info = self.create_test_manager()

        # Create new GameState
        new_game_state = MagicMock()

        # Update GameState reference
        manager.set_game_state(new_game_state)

        # Set distance result on new GameState
        new_game_state.get_distance_between_entities.return_value = 5

        target_info = MagicMock()
        target_info.position = [5, 2]

        result = manager.get_distance_to_player(target_info)

        self.assertEqual(result, 5)

        # Verify new GameState was used
        new_game_state.get_distance_between_entities.assert_called_once_with(
            entity_info, target_info
        )

        # Verify old GameState was not used
        old_game_state.get_distance_between_entities.assert_not_called()

    # Test set_game_state - preserves current state
    # Checks that changing GameState does not reset behavioral state
    def test_set_game_state_preserves_current_state(self):
        manager, game_state, entity_info = self.create_test_manager()

        # Transition to Attacking
        manager.transition_to(AttackingState())

        self.assertEqual(manager.get_current_state_name(), "Attacking")

        # Replace GameState
        new_game_state = MagicMock()
        manager.set_game_state(new_game_state)

        # Behavioral state should remain unchanged
        self.assertEqual(manager.get_current_state_name(), "Attacking")

    # Test set_game_state - reconnect after None
    # Checks that a manager created without GameState can reconnect
    def test_set_game_state_reconnect_after_none(self):
        entity = MagicMock()
        entity_info = MagicMock()
        entity_info.id = 1
        entity.get_info.return_value = entity_info

        # Create manager without GameState
        manager = EntityStateManager(entity, None, DefendingState())

        # Reconnect to GameState
        game_state = MagicMock()
        manager.set_game_state(game_state)

        game_state.attack_entity.return_value = 10

        result = manager.attack_target(2)

        self.assertEqual(result, 10)
        game_state.attack_entity.assert_called_once_with(1, 2)

    # Test set_game_state - multiple replacements
    # Checks that the most recently assigned GameState is used
    def test_set_game_state_multiple_replacements(self):
        manager, original_game_state, entity_info = self.create_test_manager()

        first_game_state = MagicMock()
        second_game_state = MagicMock()

        # Replace GameState twice
        manager.set_game_state(first_game_state)
        manager.set_game_state(second_game_state)

        second_game_state.attack_entity.return_value = 8

        result = manager.attack_target(3)

        self.assertEqual(result, 8)
        second_game_state.attack_entity.assert_called_once_with(1, 3)

        # Previous references should not be used
        original_game_state.attack_entity.assert_not_called()
        first_game_state.attack_entity.assert_not_called()

    # Test set_game_state - preserves Fleeing state
    # Checks that a restored fleeing enemy remains fleeing
    def test_set_game_state_preserves_fleeing_state(self):
        entity = MagicMock()

        manager = EntityStateManager(entity, None, FleeingState())

        # Reconnect manager to active GameState
        game_state = MagicMock()
        manager.set_game_state(game_state)

        self.assertEqual(manager.get_current_state_name(), "Fleeing")

    # Test set_game_state - move away uses new GameState
    # Checks that fleeing movement uses the reconnected GameState
    def test_set_game_state_move_away_uses_new_game_state(self):
        manager, old_game_state, entity_info = self.create_test_manager(position=[3, 3])

        # Create replacement GameState
        new_game_state = MagicMock()
        new_game_state.get_flee_position.return_value = [2, 3]

        manager.set_game_state(new_game_state)

        target_info = MagicMock()
        target_info.position = [4, 3]

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)

        # Verify new GameState handles fleeing
        new_game_state.get_flee_position.assert_called_once_with(
            entity_info, target_info
        )
        new_game_state.move_entity.assert_called_once_with(1, 2, 3)

        # Verify old GameState was not used
        old_game_state.get_flee_position.assert_not_called()
        old_game_state.move_entity.assert_not_called()

    # Test move_away_from_target - tuple flee position
    # Checks that tuple coordinates work correctly
    def test_move_away_from_target_tuple_position(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.position = [4, 3]

        # GameState returns tuple instead of list
        game_state.get_flee_position.return_value = (2, 3)

        result = manager.move_away_from_target(target_info)

        self.assertTrue(result)
        game_state.move_entity.assert_called_once_with(1, 2, 3)

    # Test move_away_from_target - correct target information
    # Checks that the correct entity information is passed
    def test_move_away_from_target_correct_target(self):
        manager, game_state, entity_info = self.create_test_manager(position=[3, 3])

        target_info = MagicMock()
        target_info.id = 7
        target_info.position = [4, 3]

        game_state.get_flee_position.return_value = [2, 3]

        manager.move_away_from_target(target_info)

        game_state.get_flee_position.assert_called_once_with(entity_info, target_info)

    # Verify normal initialization enters the state once
    def test_initialization_enters_state_once(self):
        state = MagicMock()
        manager = EntityStateManager(MagicMock(), MagicMock(), state)
        state.enter.assert_called_once_with(manager)

    # Verify restoration does not reapply state entry effects
    def test_restoring_skips_state_enter(self):
        state = MagicMock()
        manager = EntityStateManager(MagicMock(), MagicMock(), state, restoring=True)
        state.enter.assert_not_called()
        self.assertIs(manager.get_current_state(), state)

    # Verify manager exposes the same entity and game state
    def test_get_entity_and_game_state(self):
        entity = MagicMock()
        game_state = MagicMock()
        manager = EntityStateManager(entity, game_state, MagicMock(), restoring=True)
        self.assertIs(manager.get_entity(), entity)
        self.assertIs(manager.get_game_state(), game_state)

    # Verify get_entity_info delegates to the entity
    def test_get_entity_info(self):
        entity = MagicMock()
        info = object()
        entity.get_info.return_value = info
        manager = EntityStateManager(entity, MagicMock(), MagicMock(), restoring=True)
        self.assertIs(manager.get_entity_info(), info)
        entity.get_info.assert_called_once_with()

    # Verify nearest-player lookup uses the managed entity's info
    def test_get_nearest_player(self):
        entity = MagicMock()
        game_state = MagicMock()
        info = entity.get_info.return_value
        player = object()
        game_state.get_nearest_player.return_value = player
        manager = EntityStateManager(entity, game_state, MagicMock(), restoring=True)
        self.assertIs(manager.get_nearest_player(), player)
        game_state.get_nearest_player.assert_called_once_with(info)

    # Verify update returns the current state's result
    def test_update_returns_state_result(self):
        state = MagicMock()
        state.update.return_value = "attacked"
        manager = EntityStateManager(MagicMock(), MagicMock(), state, restoring=True)
        self.assertEqual(manager.update(), "attacked")
        state.update.assert_called_once_with(manager)

    # Verify every allowed transition in the transition table
    def test_all_allowed_transitions(self):
        allowed = {
            "Defending": ("Attacking", "Raging", "Fleeing"),
            "Attacking": ("Defending", "Fleeing", "Raging"),
            "Fleeing": ("Defending",),
            "Raging": ("Attacking", "Defending"),
        }
        for start, destinations in allowed.items():
            for destination in destinations:
                with self.subTest(start=start, destination=destination):
                    current = MagicMock()
                    current.get_name.return_value = start
                    next_state = MagicMock()
                    next_state.get_name.return_value = destination
                    manager = EntityStateManager(
                        MagicMock(), MagicMock(), current, restoring=True
                    )
                    self.assertTrue(manager.is_valid_transition(next_state))

    # Verify disallowed and same-state transitions
    def test_disallowed_and_same_state_transitions(self):
        all_states = ("Defending", "Attacking", "Fleeing", "Raging")
        allowed = {
            "Defending": {"Attacking", "Raging", "Fleeing"},
            "Attacking": {"Defending", "Fleeing", "Raging"},
            "Fleeing": {"Defending"},
            "Raging": {"Attacking", "Defending"},
        }
        for start in all_states:
            for destination in all_states:
                if destination in allowed[start]:
                    continue
                with self.subTest(start=start, destination=destination):
                    current = MagicMock()
                    current.get_name.return_value = start
                    next_state = MagicMock()
                    next_state.get_name.return_value = destination
                    manager = EntityStateManager(
                        MagicMock(), MagicMock(), current, restoring=True
                    )
                    self.assertFalse(manager.is_valid_transition(next_state))
                    with self.assertRaisesRegex(ValueError, "Invalid state transition"):
                        manager.transition_to(next_state)
                    current.exit.assert_not_called()
                    next_state.enter.assert_not_called()
                    self.assertIs(manager.get_current_state(), current)

    # Verify valid transitions invoke exit before enter
    def test_transition_lifecycle_order(self):
        from unittest.mock import Mock, call

        events = Mock()
        current = MagicMock()
        current.get_name.return_value = "Defending"
        current.exit.side_effect = lambda manager: events.exit(manager)
        next_state = MagicMock()
        next_state.get_name.return_value = "Attacking"
        next_state.enter.side_effect = lambda manager: events.enter(manager)
        manager = EntityStateManager(MagicMock(), MagicMock(), current, restoring=True)
        manager.transition_to(next_state)
        self.assertEqual(events.mock_calls, [call.exit(manager), call.enter(manager)])
        self.assertIs(manager.get_current_state(), next_state)

    # Verify Ogre entities cannot flee even from an otherwise valid state
    def test_ogre_cannot_transition_to_fleeing(self):
        entity = MagicMock()
        entity.get_info.return_value.e_type = "OgRe"
        current = MagicMock()
        current.get_name.return_value = "Attacking"
        fleeing = MagicMock()
        fleeing.get_name.return_value = "Fleeing"
        manager = EntityStateManager(entity, MagicMock(), current, restoring=True)
        self.assertTrue(manager.is_valid_transition(fleeing))
        with self.assertRaisesRegex(ValueError, "Ogres cannot enter the Fleeing state"):
            manager.transition_to(fleeing)
        current.exit.assert_not_called()
        fleeing.enter.assert_not_called()
        self.assertIs(manager.get_current_state(), current)

    # Verify non-Ogres can flee from Attacking
    def test_non_ogre_can_transition_to_fleeing(self):
        entity = MagicMock()
        entity.get_info.return_value.e_type = "Goblin"
        current = MagicMock()
        current.get_name.return_value = "Attacking"
        fleeing = MagicMock()
        fleeing.get_name.return_value = "Fleeing"
        manager = EntityStateManager(entity, MagicMock(), current, restoring=True)
        manager.transition_to(fleeing)
        current.exit.assert_called_once_with(manager)
        fleeing.enter.assert_called_once_with(manager)

    # Verify a zero-length path does not move an entity
    def test_move_toward_target_empty_path(self):
        manager, game_state, _ = self.create_test_manager()
        game_state.get_shortest_path_between_entities.return_value = []
        self.assertFalse(manager.move_toward_target(MagicMock()))
        game_state.move_entity.assert_not_called()

    # Verify movement speed is converted to an integer
    def test_move_toward_target_fractional_speed(self):
        manager, game_state, _ = self.create_test_manager(speed=1.9)
        target = MagicMock()
        target.position = [6, 2]
        game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
        ]
        game_state.is_grid_tile_occupied.return_value = False
        self.assertTrue(manager.move_toward_target(target))
        game_state.move_entity.assert_called_once_with(1, 2, 2)

    # Verify moving toward a target does not use the previous game state
    def test_move_toward_target_after_game_state_replacement(self):
        manager, old_game_state, _ = self.create_test_manager(speed=1)
        new_game_state = MagicMock()
        new_game_state.get_shortest_path_between_entities.return_value = [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ]
        new_game_state.is_grid_tile_occupied.return_value = False
        manager.set_game_state(new_game_state)
        target = MagicMock()
        target.position = [5, 2]
        self.assertTrue(manager.move_toward_target(target))
        new_game_state.move_entity.assert_called_once_with(1, 2, 2)
        old_game_state.move_entity.assert_not_called()

    # Verify a failed escape does not move the entity
    def test_move_away_from_target_no_escape_does_not_move(self):
        manager, game_state, info = self.create_test_manager()
        target = MagicMock()
        game_state.get_flee_position.return_value = None
        self.assertFalse(manager.move_away_from_target(target))
        game_state.get_flee_position.assert_called_once_with(info, target)
        game_state.move_entity.assert_not_called()
