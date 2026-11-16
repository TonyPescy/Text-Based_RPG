"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 11, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_entity_state.py
Purpose: Utilizes unittest to test all of the classes and methods in entity_state.py file
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


import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from domain_library import AttackTypes, MELEE_RANGE, RANGED_RANGE
from entity_state import (
    EntityState,
    DefendingState,
    AttackingState,
    FleeingState,
    DETECTION_RANGE,
    FLEE_HEALTH_THRESHOLD,
    RECOVERED_HEALTH_THRESHOLD,
)


# Test Entity State
class TestEntityState(unittest.TestCase):

    # Test Abstract Entity State
    def test_entity_state_is_abstract(self):
        with self.assertRaises(TypeError):
            EntityState()

    # Test Abstract Methods Must Be Implemented
    def test_entity_state_requires_all_methods(self):
        class IncompleteState(EntityState):
            def enter(self, context):
                pass

        with self.assertRaises(TypeError):
            IncompleteState()


# Test Defending State
class TestDefendingState(unittest.TestCase):

    def setUp(self):
        self.state = DefendingState()
        self.context = MagicMock()

        self.context.get_entity_info.return_value = SimpleNamespace(
            health=100,
            max_health=100,
            position=[2, 2],
        )

        self.player = SimpleNamespace(
            id=1,
            position=[4, 2],
        )

        self.context.get_nearest_player.return_value = self.player
        self.context.get_distance_to_player.return_value = 2

    # Test State Name
    def test_get_name(self):
        self.assertEqual(self.state.get_name(), "Defending")

    # Test Enter And Exit
    def test_enter_exit(self):
        self.assertIsNone(self.state.enter(self.context))
        self.assertIsNone(self.state.exit(self.context))

    # Test Player Within Detection Range
    def test_player_detected(self):
        result = self.state.update(self.context)

        self.assertEqual(result, "Defending -> Attacking")

        self.context.transition_to.assert_called_once()

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, AttackingState)

    # Test Player At Detection Boundary
    def test_player_at_detection_range(self):
        self.context.get_distance_to_player.return_value = DETECTION_RANGE

        result = self.state.update(self.context)

        self.assertEqual(result, "Defending -> Attacking")
        self.context.transition_to.assert_called_once()

    # Test Player Outside Detection Range
    def test_player_outside_detection_range(self):
        self.context.get_distance_to_player.return_value = DETECTION_RANGE + 1

        result = self.state.update(self.context)

        self.assertEqual(result, "Defending")
        self.context.transition_to.assert_not_called()

    # Test No Player Found
    def test_no_player(self):
        self.context.get_nearest_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Defending")
        self.context.get_distance_to_player.assert_not_called()
        self.context.transition_to.assert_not_called()

    # Test Unreachable Player
    def test_unreachable_player(self):
        self.context.get_distance_to_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Defending")
        self.context.transition_to.assert_not_called()


# Test Attacking State
class TestAttackingState(unittest.TestCase):

    def setUp(self):
        self.state = AttackingState()
        self.context = MagicMock()

        self.entity_info = SimpleNamespace(
            health=100,
            max_health=100,
            position=[2, 2],
            attack_type=AttackTypes.MELEE,
        )

        self.player = SimpleNamespace(
            id=1,
            position=[4, 2],
        )

        self.context.get_entity_info.return_value = self.entity_info
        self.context.get_nearest_player.return_value = self.player
        self.context.get_distance_to_player.return_value = 2
        self.context.move_toward_target.return_value = True

    # Test State Name
    def test_get_name(self):
        self.assertEqual(self.state.get_name(), "Attacking")

    # Test Enter And Exit
    def test_enter_exit(self):
        self.assertIsNone(self.state.enter(self.context))
        self.assertIsNone(self.state.exit(self.context))

    # Test Low Health Causes Fleeing
    def test_low_health_transitions_to_fleeing(self):
        self.entity_info.health = 20

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Fleeing")

        self.context.transition_to.assert_called_once()
        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, FleeingState)

        self.context.attack_target.assert_not_called()
        self.context.move_toward_target.assert_not_called()

    # Test Health Exactly At Flee Threshold
    def test_health_at_flee_threshold(self):
        self.entity_info.health = 25

        result = self.state.update(self.context)

        self.assertNotEqual(result, "Attacking -> Fleeing")
        self.context.transition_to.assert_not_called()

    # Test Health Just Below Flee Threshold
    def test_health_below_flee_threshold(self):
        self.entity_info.health = 24

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Fleeing")

    # Test Zero Maximum Health
    def test_zero_max_health(self):
        self.entity_info.max_health = 0

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Fleeing")
        self.context.transition_to.assert_called_once()

    # Test No Player Found
    def test_no_player(self):
        self.context.get_nearest_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

    # Test Melee Attack
    def test_melee_attack(self):
        self.player.position = [2 + MELEE_RANGE, 2]

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Attack Made")
        self.context.attack_target.assert_called_once_with(1)
        self.context.move_toward_target.assert_not_called()

    # Test Ranged Attack
    def test_ranged_attack(self):
        self.entity_info.attack_type = AttackTypes.RANGED
        self.player.position = [2 + RANGED_RANGE, 2]

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Attack Made")
        self.context.attack_target.assert_called_once_with(1)

    # Test Ranged Attack Outside Range
    def test_ranged_attack_outside_range(self):
        self.entity_info.attack_type = AttackTypes.RANGED
        self.player.position = [2 + RANGED_RANGE + 1, 2]

        self.context.get_distance_to_player.return_value = RANGED_RANGE + 1

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Moving Towards Player")
        self.context.attack_target.assert_not_called()
        self.context.move_toward_target.assert_called_once_with(self.player)

    # Test Movement Toward Player
    def test_move_toward_player(self):
        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Moving Towards Player")
        self.context.move_toward_target.assert_called_once_with(self.player)
        self.context.attack_target.assert_not_called()

    # Test Movement Failure
    def test_movement_fails(self):
        self.context.move_toward_target.return_value = False

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking")
        self.context.move_toward_target.assert_called_once_with(self.player)

    # Test Player Outside Detection Range
    def test_player_outside_detection_range(self):
        self.player.position = [DETECTION_RANGE + 3, 2]
        self.context.get_distance_to_player.return_value = DETECTION_RANGE + 1

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

        self.context.attack_target.assert_not_called()
        self.context.move_toward_target.assert_not_called()

    # Test Unreachable Player
    def test_unreachable_player(self):
        self.context.get_distance_to_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

    # Test Movement At Detection Boundary
    def test_move_at_detection_boundary(self):
        self.player.position = [2 + DETECTION_RANGE, 2]
        self.context.get_distance_to_player.return_value = DETECTION_RANGE

        result = self.state.update(self.context)

        self.assertEqual(result, "Attacking -> Moving Towards Player")
        self.context.transition_to.assert_not_called()


# Test Fleeing State
class TestFleeingState(unittest.TestCase):

    def setUp(self):
        self.state = FleeingState()
        self.context = MagicMock()

        self.entity_info = SimpleNamespace(
            health=20,
            max_health=100,
            position=[2, 2],
        )

        self.player = SimpleNamespace(
            id=1,
            position=[3, 2],
        )

        self.context.get_entity_info.return_value = self.entity_info
        self.context.get_nearest_player.return_value = self.player
        self.context.get_distance_to_player.return_value = 1
        self.context.move_away_from_target.return_value = True

    # Test State Name
    def test_get_name(self):
        self.assertEqual(self.state.get_name(), "Fleeing")

    # Test Enter And Exit
    def test_enter_exit(self):
        self.assertIsNone(self.state.enter(self.context))
        self.assertIsNone(self.state.exit(self.context))

    # Test Fleeing From Player
    def test_flee_from_player(self):
        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.move_away_from_target.assert_called_once_with(self.player)
        self.context.transition_to.assert_not_called()

    # Test Failed Flee Movement
    def test_flee_movement_fails(self):
        self.context.move_away_from_target.return_value = False

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.move_away_from_target.assert_called_once_with(self.player)

    # Test No Player Found
    def test_no_player(self):
        self.context.get_nearest_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.move_away_from_target.assert_not_called()
        self.context.transition_to.assert_not_called()

    # Test Recovered Health With No Player
    def test_recovered_no_player(self):
        self.entity_info.health = 50
        self.context.get_nearest_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

    # Test Recovered Health With Distant Player
    def test_recovered_player_outside_range(self):
        self.entity_info.health = 50
        self.context.get_distance_to_player.return_value = DETECTION_RANGE + 1

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

        self.context.move_away_from_target.assert_not_called()

    # Test Recovered Health With Unreachable Player
    def test_recovered_unreachable_player(self):
        self.entity_info.health = 50
        self.context.get_distance_to_player.return_value = None

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing -> Defending")

        new_state = self.context.transition_to.call_args.args[0]
        self.assertIsInstance(new_state, DefendingState)

    # Test Recovered Health With Nearby Player
    def test_recovered_nearby_player(self):
        self.entity_info.health = 50

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.transition_to.assert_not_called()
        self.context.move_away_from_target.assert_called_once_with(self.player)

    # Test Health Below Recovery Threshold
    def test_health_below_recovery_threshold(self):
        self.entity_info.health = 49
        self.context.get_distance_to_player.return_value = DETECTION_RANGE + 1

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.transition_to.assert_not_called()
        self.context.move_away_from_target.assert_called_once_with(self.player)

    # Test Zero Maximum Health
    def test_zero_max_health(self):
        self.entity_info.max_health = 0

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.transition_to.assert_not_called()

    # Test Recovered At Detection Boundary
    def test_recovered_at_detection_boundary(self):
        self.entity_info.health = 50
        self.context.get_distance_to_player.return_value = DETECTION_RANGE

        result = self.state.update(self.context)

        self.assertEqual(result, "Fleeing")
        self.context.transition_to.assert_not_called()


if __name__ == "__main__":
    unittest.main()
