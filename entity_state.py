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
    # Executes defending behavior and checks for nearby threats
    # Params: context - EntityStateManager - manager handling the entity's state transitions
    # Returns: None
    def update(self, context):
        entity_info = context.get_entity_info()
        # Get nearest player
        player = context.get_nearest_player()

        # No players found
        if player is None:
            return f"Entity {entity_info.id} is Defending!"

        # Get distance to player
        distance = context.get_distance_to_player(player)

        # Check detection range
        if distance <= int(entity_info.speed):
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
    # Returns: None
    def update(self, context):
        # Get entity information
        entity_info = context.get_entity_info()

        # Check health percentage
        health_percentage = (
            entity_info.health / entity_info.max_health
            if entity_info.max_health > 0
            else 0
        )

        # Transition to fleeing if health is low
        if health_percentage < 0.25:
            context.transition_to(FleeingState())
            return "Attacking -> Fleeing"

        # Find nearest player
        player = context.get_nearest_player()

        # No player found
        if player is None:
            context.transition_to(DefendingState())
            return "Attacking -> Defending"

        # Get distance
        distance = context.get_distance_to_player(player)

        # Target too far away
        if distance > entity_info.speed:
            context.transition_to(DefendingState())
            return "Attacking -> Defending"

        # Target within attack range
        if distance <= 1:
            context.attack_target(player.id)
            return "Attack"

        # Move toward target
        context.move_toward_target(player)
        return "Move"

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
    # Returns: None
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

        # Return to defending when recovered and safe
        if health_percentage >= 0.50:
            if (
                player is None
                or context.get_distance_to_player(player) > entity_info.speed
            ):
                context.transition_to(DefendingState())
                return "Fleeing -> Defending"

        # No player found
        if player is None:
            return "Fleeing"

        # Move away from nearest player
        context.move_away_from_target(player)

        return "Flee"

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
