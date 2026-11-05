"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 26, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: main.py
Purpose: Runs the command line interface.
"""

# Imports
from command_line_interface import CLI


def main():
    # Create command line interface
    main_cli = CLI()
    try:
        while True:

            try:
                command = input()
            except EOFError:  # File redirection fix
                break

            # command = input("Enter Command (or 'quit' to exit)> ")

            # Exit command sent
            if command.lower() == "quit":
                break

            # Process command
            main_cli.process_command(command)
    # Handle keybaord interrupt
    except KeyboardInterrupt:
        pass
    # Finally with thank you message
    finally:
        print("Thank you for playing!")


if __name__ == "__main__":
    main()
