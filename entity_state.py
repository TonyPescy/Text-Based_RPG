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
from copy import deepcopy

# Constants
DETECTION_RANGE = 8  # Entities will detect players up to 8 tiles away
FLEE_HEALTH_THRESHOLD = 0.25  # Threshold for when entities will start fleeing
RECOVERED_HEALTH_THRESHOLD = 0.5  # Threshold for when entities wil return to defending
RAGE_HEALTH_THRESHOLD = 0.5  # Treshold for when Ogres will enter a Raging state

# Ogre Raging Buff for Raging State - 25% more attack
# -1 so buff remains active as long as the ogre is raging
RAGING_BUFF = {
    "Name": "Raging",
    "Effects": {
        "Flat_modifiers": {},
        "Percent_modifiers": {"Attack": 25},
    },
    "Turns": -1,
}


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

        # Ogre enters raging state below 50% health
        if entity_info.e_type.lower() == "ogre":
            health_percentage = (
                entity_info.health / entity_info.max_health
                if entity_info.max_health > 0
                else 0
            )

            if health_percentage < RAGE_HEALTH_THRESHOLD:
                context.transition_to(RagingState())
                return "Defending -> Raging"

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

        # Ogre-specific rage transition
        if entity_info.e_type.lower() == "ogre":
            if health_percentage < RAGE_HEALTH_THRESHOLD:
                context.transition_to(RagingState())
                return "Attacking -> Raging"

        # Other enemies can flee
        elif health_percentage < FLEE_HEALTH_THRESHOLD:
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


# Raging State extends EntityState
# Ogre-exclusive state triggered below 50% health
class RagingState(EntityState):

    # Enter
    # Performs setup when entering the raging state
    # Params: context - EntityStateManager
    # Returns: None
    def enter(self, context):
        # Get Ogre entity
        entity = context.get_entity()

        # Check if Raging buff already exists
        has_raging_buff = any(
            dict(buff).get("Name") == "Raging" for buff in entity.get_info().temp_buffs
        )

        # Apply buff only if it doesn't already exist
        if not has_raging_buff:
            entity.add_temp_buff(deepcopy(RAGING_BUFF))

        # Only recalculate stats when GameState is available - GameState not available when loading a save but the stats would already be calculated by the time a save can happen
        if context.get_game_state() is not None:
            entity.update_stats(context.get_game_state())

    # Update
    # Aggressively pursues and attacks players
    # Params: context - EntityStateManager
    # Returns: String - action performed
    def update(self, context):
        # Get entity information
        entity_info = context.get_entity_info()

        # Ensure entity is an Ogre
        if entity_info.e_type.lower() != "ogre":
            context.transition_to(DefendingState())
            return "Raging -> Defending"

        # Calculate health percentage
        health_percentage = (
            entity_info.health / entity_info.max_health
            if entity_info.max_health > 0
            else 0
        )

        # Stop raging once health recovers
        if health_percentage >= RAGE_HEALTH_THRESHOLD:
            context.transition_to(AttackingState())
            return "Raging -> Attacking"

        # Find nearest player
        player = context.get_nearest_player()

        # No player found
        if player is None:
            return "Raging"

        # Get movement distance using A*
        movement_distance = context.get_distance_to_player(player)

        # Get attack distance using Manhattan distance
        attack_distance = abs(entity_info.position[0] - player.position[0]) + abs(
            entity_info.position[1] - player.position[1]
        )

        # Attack if target is within melee range
        if attack_distance <= MELEE_RANGE:
            context.attack_target(player.id)
            return "Raging -> Attack Made"

        # Target is unreachable
        if movement_distance is None:
            return "Raging"

        # Move toward target
        if context.move_toward_target(player):
            return "Raging -> Moving Towards Player"

        return "Raging"

    # Exit
    # Performs cleanup when leaving the raging state
    # Params: context - EntityStateManager
    # Returns: None
    def exit(self, context):
        # Get Ogre entity
        entity = context.get_entity()

        # Remove Raging buff
        entity.remove_temp_buffs(["Raging"])

        # Recalculate stats
        entity.update_stats(context.get_game_state())

    # Get Name
    # Returns current state name
    def get_name(self):
        return "Raging"
