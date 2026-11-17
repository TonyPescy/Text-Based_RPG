"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 11, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: entity_state_manager.py
Purpose: Houses all functions necessary for proper entity state management in the game
"""

# Imports
from domain_library import AttackTypes
from entity_state import RagingState


# Entity State Manager
class EntityStateManager:

    # Initialize
    # Initializes the entity state manager with an initial state
    # Params: entity - Entity - entity
    #         game_state - GameState - current game world
    #         initial_state - EntityState - initial behavioral state
    # Returns: None
    def __init__(self, entity, game_state, initial_state, restoring=False):
        self.__entity = entity
        self.__game_state = game_state
        self.__current_state = initial_state

        # Only call enter during normal initialization - Prevents errors when loading from save
        if not restoring:
            self.__current_state.enter(self)

    # Transition To
    # Transitions the entity from its current state to a new state
    # Params: new_state - EntityState - state to transition into
    # Returns: None
    def transition_to(self, new_state):
        # Check if transition is valid
        if not self.is_valid_transition(new_state):
            raise ValueError("Invalid state transition!")
        entity_info = self.__entity.get_info()
        # Prevent Ogres from entering Fleeing
        if (
            entity_info.e_type.lower() == "ogre"
            and new_state.get_name().lower() == "fleeing"
        ):
            raise ValueError("Ogres cannot enter the Fleeing state!")

        # Only Ogres can enter the Raging state
        if isinstance(new_state, RagingState):

            if entity_info.e_type.lower() != "ogre":
                raise ValueError("Only Ogres can enter the Raging state!")

        # Exit current state
        self.__current_state.exit(self)

        # Set new state
        self.__current_state = new_state

        # Enter new state
        self.__current_state.enter(self)

    # Is Valid Transition
    # Checks whether the requested state transition is allowed
    # Params: new_state - EntityState - requested destination state
    # Returns: is_valid - Bool - whether the transition is allowed
    def is_valid_transition(self, new_state):
        valid_transitions = {
            "Defending": ["Attacking", "Raging", "Fleeing"],
            "Attacking": ["Defending", "Fleeing", "Raging"],
            "Fleeing": ["Defending"],
            "Raging": ["Attacking", "Defending"],
        }

        current_name = self.__current_state.get_name()
        new_name = new_state.get_name()

        return new_name in valid_transitions.get(current_name, [])

    # Update
    # Executes the active state's behavior and evaluates transition triggers
    # Params: None
    # Returns: command - String - action performed by the entity
    def update(self):
        return self.__current_state.update(self)

    # Get Current State
    # Gets the entity's current behavioral state
    # Params: None
    # Returns: current_state - EntityState - active behavioral state
    def get_current_state(self):
        return self.__current_state

    # Get Entity
    # Returns the entity
    # Params: None
    # Returns the entity managed by this state manager
    def get_entity(self):
        return self.__entity

    # Get Game State
    # Returns the game state associated with this manager
    # Params: None
    # Returns: GameState - current game state
    def get_game_state(self):
        return self.__game_state

    # Get Current State Name
    # Gets the name of the entity's current behavioral state
    # Params: None
    # Returns: name - String - current state name
    def get_current_state_name(self):
        return self.__current_state.get_name()

    # Get Entity Info
    # Gets the information of the entity controlled by this manager
    # Params: None
    # Returns: entity_info - EntityInfo - information about the entity
    def get_entity_info(self):
        return self.__entity.get_info()

    # Get Nearest Player
    # Finds the nearest living player-controlled entity
    # Params: None
    # Returns: player_info - EntityInfo | None - nearest player information
    def get_nearest_player(self):
        return self.__game_state.get_nearest_player(self.__entity.get_info())

    # Get Distance To Player
    # Gets the shortest reachable distance to the target player
    # Params: player_info - EntityInfo - target player
    # Returns: distance - int/None - distance or None if unreachable
    def get_distance_to_player(self, player_info):
        entity_info = self.get_entity_info()

        return self.__game_state.get_distance_between_entities(
            entity_info,
            player_info,
        )

    # Attack Target
    # Makes the entity attack another entity
    # Params: target_id - int - target entity ID
    # Returns: damage - int - damage dealt
    def attack_target(self, target_id):
        entity_info = self.get_entity_info()

        return self.__game_state.attack_entity(
            entity_info.id,
            target_id,
        )

    # Move Toward Target
    # Moves the entity toward its target using A* pathfinding
    # Stops when within attack range or movement speed is exhausted
    # Params: target_info - EntityInfo - target player information
    # Returns: bool - True if movement was successful, False otherwise
    def move_toward_target(self, target_info):
        # Get entity information
        entity_info = self.get_entity_info()

        # Get shortest path to target
        path = self.__game_state.get_shortest_path_between_entities(
            entity_info,
            target_info,
        )

        # Check if path exists
        if path is None or len(path) < 2:
            return False

        # Determine attack range
        if entity_info.attack_type == AttackTypes.RANGED:
            attack_range = 3
        else:
            attack_range = 1

        # Get maximum movement distance
        movement_speed = max(0, int(entity_info.speed))

        # Track best position
        best_position = None

        # Check each tile along path
        for step in range(1, min(movement_speed, len(path) - 1) + 1):
            # Get position along path
            next_x, next_y = path[step]

            # Stop before occupied tile
            if self.__game_state.is_grid_tile_occupied(next_x, next_y):
                break

            # Update best position
            best_position = [next_x, next_y]

            # Calculate attack distance from this tile
            attack_distance = abs(next_x - target_info.position[0]) + abs(
                next_y - target_info.position[1]
            )

            # Stop once within attack range
            if attack_distance <= attack_range:
                break

        # No valid movement found
        if best_position is None:
            return False

        # Move entity to selected position
        self.__game_state.move_entity(
            entity_info.id,
            best_position[0],
            best_position[1],
        )

        return True

    # Move Away From Target
    # Moves the entity one tile away from the target
    # Uses GameState to find the best available escape position
    # Params: target_info - EntityInfo - threatening entity information
    # Returns: bool - True if movement was successful, False otherwise
    def move_away_from_target(self, target_info):
        # Get entity information
        entity_info = self.get_entity_info()

        # Get best escape position
        flee_position = self.__game_state.get_flee_position(
            entity_info,
            target_info,
        )

        # No valid escape position found
        if flee_position is None:
            return False

        # Move entity to escape position
        self.__game_state.move_entity(
            entity_info.id,
            flee_position[0],
            flee_position[1],
        )

        return True

    # Set Game State
    # Updates the GameState reference used by this manager
    # Params: game_state - GameState - current game state
    # Returns: None
    def set_game_state(self, game_state):
        self.__game_state = game_state
