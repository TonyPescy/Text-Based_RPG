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
        # Execute command
        command.execute()

        # Only add undoable commands to history
        if command.is_undoable():
            self.__undo_history.append(command)
            # Resets redo history - prevents undoing a move then redoing one that should not be possible
            self.__redo_history.clear()

    # Undo Last Command
    # Reverses the most recently executed command
    # Params: None
    # Returns:  bool - True if a command was undone
    #           command - Command - command that was undone
    def undo_last_command(self):
        if len(self.__undo_history) == 0:
            return False, None

        command = self.__undo_history.pop()
        # Add commmand to redo history
        self.__redo_history.append(command)
        command.undo()
        return True, command

    # Redo Last Command
    # Reverses the most recently undone command
    # Params: None
    # Returns:  bool - True if a command was redone
    #           command - Command - command that was redone
    def redo_last_command(self):
        if len(self.__redo_history) == 0:
            return False, None

        command = self.__redo_history.pop()
        # Add command to undo history
        self.__undo_history.append(command)
        command.redo()
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
