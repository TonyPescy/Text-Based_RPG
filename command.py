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


# Move Command extends from Command
class MoveCommand(Command):

    # Initialize Move Command
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

    # Redo
    # Spawns the entity again at its original position
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Spawn Command extends from Command
class SpawnCommand(Command):

    # Initialize Spawn Command
    def __init__(self, game_state, entity_type, x, y):
        self.__game_state = game_state
        self.__entity_type = entity_type
        self.__x = int(x)
        self.__y = int(y)
        self.__name = "Spawn"
        self.__entity_id = None

    # Execute
    # Spawns an entity at the specified position
    # Params: None
    # Returns: None
    def execute(self):
        self.__entity_id = self.__game_state.spawn_entity(
            self.__x,
            self.__y,
            self.__entity_type,
        )

    # Undo
    # Removes the spawned entity from the game
    # Params: None
    # Returns: None
    def undo(self):
        if self.__entity_id is None:
            raise ValueError("Entity has not been spawned!")

        self.__game_state.undo_spawn(self.__entity_id)

    # Redo
    # Spawns the entity again at its original position
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Spawn Command extends from Command
class SpawnLootCommand(Command):

    # Initialize Spawn Command
    def __init__(self, game_state, item_name, x, y):
        self.__game_state = game_state
        self.__item_name = item_name
        self.__x = int(x)
        self.__y = int(y)
        self.__name = "Spawn Loot"

    # Execute
    # Spawns an entity at the specified position
    # Params: None
    # Returns: None
    def execute(self):
        self.__game_state.spawn_loot(self.__x, self.__y, self.__item_name)

    # Undo
    # Removes the spawned entity from the game
    # Params: None
    # Returns: None
    def undo(self):
        self.__game_state.remove_item_from_tile(self.__x, self.__y, self.__item_name)

    # Redo
    # Spawns the entity again at its original position
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Attack Command extends from Command
class AttackCommand(Command):

    # Initialize Attack Command
    def __init__(self, game_state, attacker_id, target_id):
        self.__game_state = game_state
        self.__attacker_id = int(attacker_id)
        self.__target_id = int(target_id)
        self.__name = "Attack"
        self.__damage = None

    # Execute
    # Attacks the target and stores the damage dealt
    # Params: None
    # Returns: None
    def execute(self):
        # Perform the attack and store the damage dealt
        self.__damage = self.__game_state.attack_entity(
            self.__attacker_id, self.__target_id
        )

    # Undo
    # Restores the damage dealt to the target
    # Params: None
    # Returns: None
    def undo(self):
        if self.__damage is None:
            raise ValueError("Attack has not been executed!")

        self.__game_state.restore_entity_health(self.__target_id, self.__damage)

    # Redo
    # Applies the previously recorded damage to the target
    # Params: None
    # Returns: None
    def redo(self):
        if self.__damage is None:
            raise ValueError("Attack has not been executed!")

        self.__game_state.attack_entity(self.__attacker_id, self.__target_id)

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Get Damage
    # Gets damage of command
    # Params: None
    # Returns: damage - int - command name
    def get_damage(self):
        return self.__damage
