"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 26, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: command_manager.py
Purpose: Runs commands and helps manage command history.
"""

# Command Manager
from dataclasses import dataclass
from command import (
    MoveCommand,
    SpawnCommand,
    SpawnLootCommand,
    AttackCommand,
    CastSpellCommand,
    SetTileCommand,
    PickupCommand,
    GiveItemCommand,
    DropItemCommand,
    SwapItemCommand,
    UseItemCommand,
    TickCommand,
    InitCommand,
    SaveCommand,
    LoadCommand,
)


# Create Command From Memento
# Creates a command object from its saved memento
# Params: command_memento - Command.Memento - Saved command information
#         game_state - GameState - Current game state
#           game_state_manager
#           command_manager
# Returns: command - Command - Restored command object
def create_command_from_memento(
    command_memento, game_state, game_state_manager, command_manager
):
    # Map command type names to their respective classes
    command_types = {
        "MoveCommand": MoveCommand,
        "SpawnCommand": SpawnCommand,
        "SpawnLootCommand": SpawnLootCommand,
        "AttackCommand": AttackCommand,
        "CastSpellCommand": CastSpellCommand,
        "SetTileCommand": SetTileCommand,
        "PickupCommand": PickupCommand,
        "GiveItemCommand": GiveItemCommand,
        "DropItemCommand": DropItemCommand,
        "SwapItemCommand": SwapItemCommand,
        "UseItemCommand": UseItemCommand,
        "TickCommand": TickCommand,
        "InitCommand": InitCommand,
        "SaveCommand": SaveCommand,
        "LoadCommand": LoadCommand,
    }

    # Get the command type
    command_type = command_memento.command_type

    # Verify that the command type is supported
    if command_type not in command_types:
        raise ValueError("Invalid command type!")

    # Create an uninitialized command object
    command_class = command_types[command_type]
    command = command_class.__new__(command_class)

    # Restore the command's attributes
    command.restore(command_memento, game_state, game_state_manager, command_manager)

    return command


class CommandManager:

    # Initialize Command Manager
    def __init__(self):
        self.__undo_history = []
        self.__redo_history = []

    # Execute Command
    # Executes a command and adds it to history
    # Params: command - Command - Command to execute
    # Returns: None
    def execute_command(self, command):
        """print("DEBUG executing:", command.get_name())
        print("DEBUG undoable:", command.is_undoable())
        print("DEBUG history before:", self.get_history_info())"""

        command.execute()
        # print("DEBUG redo history cleared!")

        # print("DEBUG history after execute:", self.get_history_info())

        if command.is_undoable():
            self.__undo_history.append(command)
            self.__redo_history.clear()

        # print("DEBUG history after append:", self.get_history_info())

    # Undo Last Command
    # Reverses the most recently executed command
    # Params: None
    # Returns:  bool - True if a command was undone
    #           command - Command - command that was undone
    def undo_last_command(self):
        if len(self.__undo_history) == 0:
            return False, None

        command = self.__undo_history.pop()

        # print("DEBUG before undo:", self.get_history_info())

        # Undo command
        command.undo()

        # print("DEBUG after undo:", self.get_history_info())

        # Add command to redo history AFTER undoing
        self.__redo_history.append(command)

        # print("DEBUG after append:", self.get_history_info())

        return True, command

    # Redo Last Command
    # Reverses the most recently undone command
    # Params: None
    # Returns:  bool - True if a command was redone
    #           command - Command - command that was redone
    def redo_last_command(self):
        if len(self.__redo_history) == 0:
            return False, None

        # Get last undone command
        command = self.__redo_history.pop()

        # Redo command
        command.redo()

        # Add command to undo history AFTER redoing
        self.__undo_history.append(command)

        return True, command

    # Clear History
    # Clears history when starting a different game state
    # Params: None
    # Returns: None
    def clear_history(self):
        self.__undo_history.clear()
        self.__redo_history.clear()

    # Get History Information
    # Returns the number of commands in the undo and redo histories
    # Params: None
    # Returns: tuple - (undo_count, redo_count)
    def get_history_info(self):
        undo_count = len(self.__undo_history)
        redo_count = len(self.__redo_history)

        return undo_count, redo_count

    # Memento DataClass
    # Stores the undo and redo histories
    @dataclass(frozen=True)
    class Memento:
        undo_history: tuple
        redo_history: tuple

    # Create Memento
    # Creates a memento of the command manager's history
    # Params: None
    # Returns: Memento
    def create_memento(self):
        undo_mementos = []
        redo_mementos = []

        # Create mementos for undo history
        for command in self.__undo_history:
            undo_mementos.append(command.create_memento())

        # Create mementos for redo history
        for command in self.__redo_history:
            redo_mementos.append(command.create_memento())

        return CommandManager.Memento(
            undo_history=tuple(undo_mementos), redo_history=tuple(redo_mementos)
        )

    # Restore
    # Restores the command manager's history based on its memento
    # Params: memento - Memento - saved command history
    #         game_state - GameState - current game state
    # Returns: None
    def restore(self, memento, game_state, game_state_manager, command_manager):
        if not isinstance(memento, CommandManager.Memento):
            raise TypeError("Invalid Command Manager memento")

        undo_history = []
        redo_history = []

        # Restore undo history
        for command_memento in memento.undo_history:
            undo_history.append(
                create_command_from_memento(
                    command_memento, game_state, game_state_manager, command_manager
                )
            )

        # Restore redo history
        for command_memento in memento.redo_history:
            redo_history.append(
                create_command_from_memento(
                    command_memento, game_state, game_state_manager, command_manager
                )
            )

        self.__undo_history = undo_history
        self.__redo_history = redo_history
