"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: command_line_interface.py
Purpose: Run all public facing functions that the player will use to interact with the game. Handles user inputted commands and parses them accordingly.
"""

# Imports
from domain_library import Entity, Equipment, Grid, Tile


# Handles all Command Line Interface commands for the game
class CLI:
    # Constants
    # COMMAND_HEADERS = ("init", "set", "spawn", "equip", "inventory", "inspect", "tile")

    # Initialize CLI
    def __init__(self):
        self.grid = None
        # self.entities = []
        self.map_created = False  # Bool that checks to see if a map was already created

    # Process Command Start
    # Handles all commands that user can write
    def process_command(self, command):
        # Split command into command_pieces for use in match statements and the associated methods
        command_pieces = command.lower().split()
        # print(command_pieces)
        # Match first word of command
        match command_pieces[0]:

            # init commands
            case "init":
                # Test for valid amount of command pieces and full command
                if len(command_pieces) == 4 and command_pieces[1] == "map":
                    # Run init_map with width and height
                    self.init_map(command_pieces[2], command_pieces[3])
                else:
                    print("error: map_init_failed due to invalid arguments.")

            # set commands
            case "set":
                # Test for valid amount of command pieces and correct commands/typing
                if len(command_pieces) == 5 and command_pieces[1] == "tile":
                    # Run set_tile with x and y - grid position checked in grid functions
                    self.set_tile(
                        command_pieces[2], command_pieces[3], command_pieces[4]
                    )
                else:
                    print("error: set_tile_failed - Invalid arguments!")

            # spawn commands
            case "spawn":
                # Test for valid amount of command pieces and correct commands/typing
                if len(command_pieces) == 4 and command_pieces[1] in [
                    entity.lower() for entity in Entity.ENTITY_TYPES
                ]:
                    self.spawn(command_pieces[1], command_pieces[2], command_pieces[3])
                else:
                    print("error: spawn_failed - Invalid arguments!")

            # equip commands
            case "equip":
                # Test for valid amount of command pieces and correct commands/typing
                if (
                    len(command_pieces) == 3
                    and command_pieces[1]
                    in [equipment.lower() for equipment in Equipment.VALID_ITEMS]
                    and command_pieces[2]
                    in [equipment.lower() for equipment in Equipment.VALID_SLOTS]
                ):
                    # Run equip with item name and slot
                    CLI.equip(self, command_pieces[1], command_pieces[2])

                # If slot is not included
                elif len(command_pieces) == 2 and command_pieces[1] in [
                    equipment.lower() for equipment in Equipment.VALID_ITEMS
                ]:
                    # Run equip with JUST item name
                    CLI.equip(self, command_pieces[1])
                else:
                    print("error: equip_failed - Invalid arguments!")

            # inventory commands
            case "inventory":
                # Validate command
                if len(command_pieces) > 1:
                    print("error: inventory_failed - Too many command arguemnts!")
                    return
                # Run inventory
                CLI.inventory()

            # inspect commands
            case "inspect":
                # Test for valid amount of command pieces
                if len(command_pieces) == 2:
                    # Run inspect with entity ID
                    self.inspect(command_pieces[1])
                else:
                    print("error: inspect_failed - Invalid arguments!")

            # tile commands
            case "tile":
                # Test for valid amount of command pieces and correct commands/typing
                if len(command_pieces) == 3:
                    # Run spawn with x and y - position checked in grid functions
                    self.tile(command_pieces[1], command_pieces[2])
                else:
                    print("error: tile_failed - Invalid command!")

            # default command - unknown command
            case _:
                print("error: Unknown command!")

    # Init Map Start
    # Creates a map if one does not already exist
    # Params: wdith/height - ints - grid position
    def init_map(self, width, height):
        # Map already created
        if self.map_created:
            print("error: map_init_failed - Map is already created!")

        # width and height are not valid ints
        elif not Grid.are_valid_ints(width, height):
            print("error: map_init_failed - Width and height are not valid integers!")

        # width and heigth within bounds
        elif not Grid.within_bounds(width, height):
            print(
                "error: map_init_failed - Width and height exceed bound minimum and maximum!"
            )

        # Valid inputs
        else:
            # Create grid with width and height
            self.grid = Grid(width, height)
            # mark Create map as True
            self.map_created = True
            # Set entity tracker for mapp
            Entity.reset_id_issuer_tracker()
            # Success message
            print(f"ok: map_initialized width: {width} height: {height}!")

    # Set Tile Start
    # Sets tile at given position
    # Params: x/y - ints - grid position
    #       tile_type - string - Type of tile to set
    def set_tile(self, x, y, tile_type):
        # checks if map was created
        if not self.map_created:
            print("error: tile_set_failed - Map does not exist!")

        # x and y are not valid ints
        elif not Grid.are_valid_ints(x, y):
            print("error: set_tile_failed - x and y are not valid integers!")

            """# x and y within bounds
            elif not Grid.within_bounds(x, y):
                print("error: set_tile_failed - x and y exceed bound minimum and maximum!")"""

        # x and y exceeds current grid bounds
        elif not Grid.is_valid_grid_position(self.grid, x, y):
            print("error: set_tile_failed - x and y exceed current grid bounds!")

        # tile is not valid
        elif not Tile.is_valid_tile(tile_type):
            print("error: set_tile_failed - Tile type provided was invalid!")

        else:
            # updates grid with new tile
            self.grid.set_tile(x, y, tile_type)
            # success output -  with special case for shallowwater
            if tile_type == "shallowwater":
                print(f"ok: tile_set {x}, {y} type: ShallowWater!")
            else:
                print(f"ok: tile_set {x}, {y} type: {tile_type.capitalize()}!")
            # update entity if present

    # Spawn Start
    # Spawns a unit at designated position
    # Params: x/y - ints - grid position
    #       entity_type - string - Type of entity to set
    def spawn(self, entity_type, x, y):
        # Ensure map exists
        if not self.map_created:
            print("error: spawn_failed - Map does not exist!")

        # x and y are not valid ints
        elif not Grid.are_valid_ints(x, y):
            print("error: spawn_failed - x and y are not valid integers!")

            """# x and y within bounds
            elif not Grid.within_bounds(x, y):
                print("error: spawn_failed - x and y exceed bound minimum and maximum!")"""

        # x and y exceeds current grid bounds
        elif not Grid.is_valid_grid_position(self.grid, x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")

        # ensure grid location is empty
        elif Grid.is_occupied(self.grid, x, y):
            print(f"error: spawn_failed - Entity is already present at ({x}, {y})!")

        # invalid entity type
        elif not Entity.is_valid_entity(entity_type):
            print("error: spawn_failed - Invalid entity type!")

        # All valid inputs
        else:
            # updates grid with new entity and returns entity
            entity = self.grid.spawn_entity(x, y, entity_type)
            # success output
            print(f"ok: Spawned {entity_type} at {x}, {y}. id: {entity.id}!")

    # Equip Start
    # Equips item to designated slot or determines best slot based on item
    # Player system is not added yet so will default player to be first entity created entity_list[0]
    # Equip will overwrite previous items
    # Params: Item - Equipment - item to be equipped
    #       slot - string - slot to equip item in
    def equip(self, item, slot=""):
        # Ensure "player" entity exists
        if not len(Entity.entity_list) > 0:
            print("error: equip_failed - Player entity does not exist!")
            return

        # Find equipment matching item name
        new_item = Equipment.create_equipment(item)

        # check that slot was provided
        if slot != "":
            # check that slot matches
            if slot != new_item.slot.lower():
                print("error: equip_failed - Slot provided does not match items slot!")
                return
        # set slot to correct slot if not provided
        else:
            slot = new_item.slot

        # Equip new item to correct slot
        Entity.equip_item(Entity.entity_list[0], new_item, slot.lower())
        # update stats of entity
        Entity.entity_list[0].update_stats(self.grid)
        # Success message
        print("Valid items:", ", ".join(Equipment.VALID_ITEMS))
        print("Valid slots:", ", ".join(Equipment.VALID_SLOTS))
        print(f"ok: Equipped {new_item.name} to {new_item.slot}!")

    # Inventory Start
    # displays current inventory to user
    # Player system is not added yet so will default player to be first entity created entity_list[0]
    def inventory():
        # Ensure "player" entity exists
        if not len(Entity.entity_list) > 0:
            print("error: inventory_failed - Player entity does not exist!")
            return

        # Display inventory of entity
        print(f"Weapon: {Entity.entity_list[0].inventory[0].name}")
        print(f"Armor: {Entity.entity_list[0].inventory[1].name}")
        print(f"Accessory: {Entity.entity_list[0].inventory[2].name}")

    # Inspect Start
    # Inspects entity with given ID
    # Params:   e_id - int - entity id
    def inspect(self, e_id):
        # Ensure entities exists
        if not len(Entity.entity_list) > 0:
            print("error: inspect_failed - No entities exist yet!")
            return

        # Validate e_id as int
        try:
            e_id = int(e_id)
        except:
            print("error: inspect_failed - Entity id is not valid integer!")
            return

        # Ensure entity exists
        entity_exists = False
        # Check list of entities for entity with given ID
        for entity in Entity.entity_list:
            if int(entity.id) == e_id:
                # Set existence to true
                entity_exists = True
                # assign found entity
                found_entity = entity
                break
        # Error message for entity existence
        if not entity_exists:
            print("error: inspect_failed - Entity does not exist!")
            return

        # update entity stats - in case changes occurred
        found_entity.update_stats(self.grid)
        # get stats of entity
        entity_stats = found_entity.get_stats()
        # Display stats of entity
        for stat, value in entity_stats.items():
            if stat != "Active_modifiers":
                value = CLI.capitalize_if_string(value)
                print(f"{stat}: {value}")
            # Special case for dictionaries inside of active modifiers
            elif stat == "Active_modifiers":
                count = 0
                # count all modifiers
                for (
                    dict,
                    contents,
                ) in value.items():  # dictionaries inside of dictionaries
                    count += len(contents)
                print(f"{stat}: {count}")

    # Tile Start
    # Will describe the tile at the given grid position
    # Params: x,y - ints - Grid position
    def tile(self, x, y):
        # Ensure map exists
        if not self.map_created:
            print("error: tile_failed - Map does not exist!")
            return

        # x and y are not valid ints
        elif not Grid.are_valid_ints(x, y):
            print("error: tile_failed - x and y are not valid integers!")
            return

        # x and y exceeds current grid bounds
        elif not self.grid.is_valid_grid_position(x, y):
            print("error: tile_failed - x and y exceed current grid bounds!")
            return

        # display - handles special cases
        print(f"Coordinate: {x}, {y}")
        # Get tile
        current_tile = self.grid.grid[int(x)][int(y)]

        # Special case with shallowwater for proper capitalization
        if current_tile.t_type == "shallowwater":
            print("Type: ShallowWater")
        else:
            print(f"Type: {current_tile.t_type.capitalize()}")

        # Passable
        print(f"Passable: {current_tile.passable}")

        # occupants - special case for empty list (shoudl logic be changed to just one occupant this can be cleaner)
        if len(current_tile.occupants) == 0:
            print("Occupants: None")
        else:
            print(f"Occupants: {current_tile.occupants[0]}")

    # Capitalize If String Start
    # Will capitalize and return string if it is a string
    # Params: value - Any - Value to be tested if a string
    # Returns: value - Any - value will be Capitalized if a string
    def capitalize_if_string(value):
        # if value is a string
        if isinstance(value, str):
            return value.capitalize()
        else:
            return value


# Main to run the command line interface
# While true to get user inputs
def main():
    # Create command line interface
    main_cli = CLI()
    while True:
        command = input("Enter Command (or 'quit' to exit)> ")
        # Exit command sent
        if command.lower() == "quit":
            print("Thank you for playing!")
            break

        # Process command
        main_cli.process_command(command)


if __name__ == "__main__":
    main()
