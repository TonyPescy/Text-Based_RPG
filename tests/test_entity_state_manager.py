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


if __name__ == "__main__":
    unittest.main()
