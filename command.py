"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 26, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: command.py
Purpose: Houses all the logic needed for the commands.
"""

# Imports
from abc import ABC, abstractmethod


# Command
class Command(ABC):

    # Execute
    # Executes the requested game action
    # Params: None
    # Returns: None
    @abstractmethod
    def execute(self):
        pass

    # Undo
    # Reverses the requested game action
    # Params: None
    # Returns: None
    @abstractmethod
    def undo(self):
        pass

    """ MIGHT JUST USE EXECUTE
        # Redo
        # Re-executes the requested game action
        # Params: None
        # Returns: None
        @abstractmethod
        def redo(self):
            pass
    """

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    @abstractmethod
    def get_name(self):
        pass


# Move Command extends from command
class MoveCommand(Command):

    # Initialize Move Command
    # Stores the information required to move and undo movement
    def __init__(self, game_state, entity_id, x, y):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__x = int(x)
        self.__y = int(y)
        self.__name = "Move"

        # Store original position for undo
        entity_info = game_state.get_entity_info_from_list(entity_id)

        if entity_info is None:
            raise ValueError("Entity does not exist!")

        self.__old_x = entity_info.position[0]
        self.__old_y = entity_info.position[1]

    # Execute
    # Moves the entity to its destination
    # Params: None
    # Returns: None
    def execute(self):
        self.__game_state.move_entity(self.__entity_id, self.__x, self.__y)

    # Undo
    # Moves the entity back to its original position
    # Params: None
    # Returns: None
    def undo(self):
        self.__game_state.move_entity(self.__entity_id, self.__old_x, self.__old_y)

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name
