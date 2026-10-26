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
        # Execute before recording so failed commands aren't added
        command.execute()
        self.__undo_history.append(command)

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

    # Clear History
    # Clears history when starting a different game state
    # Params: None
    # Returns: None
    def clear_history(self):
        self.__undo_history.clear()
        self.__redo_history.clear()
