"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 11, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: entity_state.py
Purpose: Houses all state classes and methods.
"""

from abc import ABC, abstractmethod
from domain_library import AttackTypes, MELEE_RANGE, RANGED_RANGE

# Constants
DETECTION_RANGE = 8  # Entities will detect players up to 8 tiles away
FLEE_HEALTH_THRESHOLD = 0.25  # Threshold for when entities will start fleeing
RECOVERED_HEALTH_THRESHOLD = 0.5  # Threshold for when entities wil return to defending


# Entity State Class
class EntityState(ABC):

    # Enter
    # Performs any setup required when entering this state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    @abstractmethod
    def enter(self, context):
        pass

    # Update
    # Performs updates while in this state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    @abstractmethod
    def update(self, context):
        pass

    # Exit
    # Performs cleanup required when exiting this state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    @abstractmethod
    def exit(self, context):
        pass

    # Get Name
    # Gets the name of the current entity state
    # Params: None
    # Returns: name - String - state name
    @abstractmethod
    def get_name(self):
        pass


# Defending State extends EntityState
class DefendingState(EntityState):

    # Enter
    # Performs setup when the entity enters the defending state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def enter(self, context):
        pass

    # Update
    # Checks for nearby players and transitions to attacking
    # Params: context - EntityStateManager - entity state manager
    # Returns: String - action performed
    def update(self, context):
        # Get entity information
        entity_info = context.get_entity_info()

        # Find nearest player
        player = context.get_nearest_player()

        # No players found
        if player is None:
            return "Defending"

        # Get distance to player
        distance = context.get_distance_to_player(player)

        # Player is within detection range
        if distance is not None and distance <= DETECTION_RANGE:
            context.transition_to(AttackingState())
            return "Defending -> Attacking"

        return "Defending"

    # Exit
    # Performs cleanup when the entity leaves the defending state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def exit(self, context):
        pass

    # Get Name
    # Gets the name of the defending state
    # Params: None
    # Returns: name - String - state name
    def get_name(self):
        return "Defending"


# Attacking State extends EntityState
class AttackingState(EntityState):

    # Enter
    # Performs setup when the entity enters the attacking state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def enter(self, context):
        pass

    # Update
    # Executes attacking behavior and checks for state transition triggers
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: String - action performed
    def update(self, context):
        # Get entity information
        entity_info = context.get_entity_info()

        # Calculate health percentage
        health_percentage = (
            entity_info.health / entity_info.max_health
            if entity_info.max_health > 0
            else 0
        )

        # Transition to fleeing if health is low
        if health_percentage < FLEE_HEALTH_THRESHOLD:
            context.transition_to(FleeingState())
            return "Attacking -> Fleeing"

        # Find nearest player
        player = context.get_nearest_player()

        # No player found
        if player is None:
            context.transition_to(DefendingState())
            return "Attacking -> Defending"

        # Get movement distance using A*
        movement_distance = context.get_distance_to_player(player)

        # Get attack distance using Manhattan distance
        attack_distance = abs(entity_info.position[0] - player.position[0]) + abs(
            entity_info.position[1] - player.position[1]
        )

        # Determine attack range
        if entity_info.attack_type == AttackTypes.RANGED:
            attack_range = RANGED_RANGE
        else:
            attack_range = MELEE_RANGE

        # Attack if target is within attack range
        if attack_distance <= attack_range:
            context.attack_target(player.id)
            return "Attacking -> Attack Made"

        # Target is unreachable or outside detection range
        if movement_distance is None or movement_distance > DETECTION_RANGE:
            context.transition_to(DefendingState())
            return "Attacking -> Defending"

        # Move toward target
        if context.move_toward_target(player):
            return "Attacking -> Moving Towards Player"

        return "Attacking"

    # Exit
    # Performs cleanup when the entity leaves the attacking state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def exit(self, context):
        pass

    # Get Name
    # Gets the name of the attacking state
    # Params: None
    # Returns: name - String - state name
    def get_name(self):
        return "Attacking"


# Fleeing State extends EntityState
class FleeingState(EntityState):

    # Enter
    # Performs setup when the entity enters the fleeing state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def enter(self, context):
        pass

    # Update
    # Executes fleeing behavior and checks whether the entity is safe
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: String - action performed
    def update(self, context):
        # Get entity information
        entity_info = context.get_entity_info()

        # Find nearest player
        player = context.get_nearest_player()

        # Calculate health percentage
        health_percentage = (
            entity_info.health / entity_info.max_health
            if entity_info.max_health > 0
            else 0
        )

        # Check whether monster has recovered
        if health_percentage >= RECOVERED_HEALTH_THRESHOLD:
            # No player found
            if player is None:
                context.transition_to(DefendingState())
                return "Fleeing -> Defending"

            # Get distance to player
            distance = context.get_distance_to_player(player)

            # Player is outside detection range
            if distance is None or distance > DETECTION_RANGE:
                context.transition_to(DefendingState())
                return "Fleeing -> Defending"

        # No player found
        if player is None:
            return "Fleeing"

        # Move away from player
        if context.move_away_from_target(player):
            return "Fleeing"

        return "Fleeing"

    # Exit
    # Performs cleanup when the entity leaves the fleeing state
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def exit(self, context):
        pass

    # Get Name
    # Gets the name of the fleeing state
    # Params: None
    # Returns: name - String - state name
    def get_name(self):
        return "Fleeing"
