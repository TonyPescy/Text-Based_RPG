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


# Entity State Manager
class EntityStateManager:

    # Initialize
    # Initializes the entity state manager with an initial state
    # Params: entity - Entity - entity
    #         game_state - GameState - current game world
    #         initial_state - EntityState - initial behavioral state
    # Returns: None
    def __init__(self, entity, game_state, initial_state):
        self.__entity = entity
        self.__game_state = game_state
        self.__current_state = initial_state

        # Enter initial state
        self.__current_state.enter(self)

    # Transition To
    # Transitions the entity from its current state to a new state
    # Params: new_state - EntityState - state to transition into
    # Returns: None
    def transition_to(self, new_state):
        # Check if transition is valid
        if not self.is_valid_transition(new_state):
            raise ValueError("Invalid state transition!")

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
            "Defending": ["Attacking"],
            "Attacking": ["Defending", "Fleeing"],
            "Fleeing": ["Defending", "Attacking"],
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
