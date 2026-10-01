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

# Always Update Stats before using or checking them in case changes have happened
# Examples: Tiles moved, item equipped, combat, etc
# Could also update after these movements - pick one to reduce redundancy (Probs do the latter)

# Imports
import domain_library as dl
from grid import Grid, Tile
from entity import Entity
from equipment import Consumable
from spell import Spell, get_spell


# Handles all Command Line Interface commands for the game
class CLI:
    # Constants
    # COMMAND_HEADERS = ("init", "set", "spawn", "equip", "inventory", "inspect", "tile")

    # Initialize CLI
    def __init__(self):
        self.grid = None
        self.entity_list = []
        self.entity_ids_issued = 0
        self.map_created = False  # Bool that checks to see if a map was already created

    # Reset Entity List Start
    # resets entity list back to empty to prevent errors with testing
    # Params: None
    # Return: None
    def reset_entity_list(self):
        self.entity_list = []

    # Reset ID Issuer Tracker Start
    # resets entity id issues number back to 0 to prevent errors with testing
    # Params: None
    # Return: None
    def reset_id_issuer_tracker(self):
        self.entity_ids_issued = 0

    # Process Command Start
    # Handles all commands that user can write
    # Params: command - string - The command entered by the user
    # Return: None
    def process_command(self, command):
        # Split command into command_pieces for use in match statements and the associated methods
        command_pieces = command.lower().split()

        # Check for empty command
        if not command_pieces:
            print("error: Empty command!")
            return

        # Dictionary with command handlers
        command_handlers = {
            "init": self.process_init_command,
            "set": self.process_set_command,
            "spawn": self.process_spawn_command,
            # "equip": self.process_equip_command,
            "inventory": self.process_inventory_command,
            "inspect": self.process_inspect_command,
            "tile": self.process_tile_command,
            "pickup": self.process_pickup_item_command,
            "give": self.process_give_item_command,
            "drop": self.process_drop_item_command,
            "swap": self.process_swap_item_command,
            "use": self.process_use_item_command,
            "move": self.process_move_command,
            "attack": self.process_attack_command,
            "cast": self.process_cast_command,
        }

        # Match handler to command
        handler = command_handlers.get(command_pieces[0])

        # Check for unknown command
        if handler is None:
            print("error: Unknown command!")
            return

        # Process Command
        handler(command_pieces)

    """
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
                    entity.lower() for entity in ENTITY_TYPES
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
    """

    # Process Init Command Start
    # Creates a map if one does not already exist
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_init_command(self, command_pieces):
        # Test for valid amount of command pieces and full command
        if len(command_pieces) == 4 and command_pieces[1] == "map":
            # Assign width and height
            width = command_pieces[2]
            height = command_pieces[3]
        else:
            print("error: map_init_failed due to invalid arguments.")
            return
        # Map already created
        if self.map_created:
            print("error: map_init_failed - Map is already created!")
            return
        # width and height are not valid ints
        elif not dl.are_valid_ints(width, height):
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
            self.reset_id_issuer_tracker()
            # Success message
            print(f"ok: map_initialized width: {width} height: {height}!")

    # Process set command
    # Sets tile at given position
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_set_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 5 and command_pieces[1] == "tile":
            # Set variables
            x = command_pieces[2]
            y = command_pieces[3]
            tile_type = command_pieces[4]
        else:
            print("error: set_tile_failed - Invalid arguments!")
            return

        # checks if map was created
        if not self.map_created:
            print("error: tile_set_failed - Map does not exist!")
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
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
            if tile_type.lower() == "shallowwater":
                print(f"ok: tile_set {x}, {y} type: ShallowWater!")
            else:
                print(f"ok: tile_set {x}, {y} type: {tile_type.capitalize()}!")
            # update entity if present

    # Process Spawn Command Start
    # Spawns a unit at designated position
    # Params: command_pieces - list - list of strings that make up the command
    # Return: None
    def process_spawn_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 4 and command_pieces[1].lower() in [  # SPAWN ENTITY
            entity.value.lower() for entity in dl.EntityType
        ]:
            x = command_pieces[2]
            y = command_pieces[3]
            entity_type = command_pieces[1]
            # Spawn entity
            self.spawn_entity_for_cli(x, y, entity_type)

        elif len(command_pieces) == 5 and command_pieces[1] == "loot":
            # Set variables
            item_name = command_pieces[2]
            x = command_pieces[3]
            y = command_pieces[4]
            # Spawn loot
            self.spawn_loot_for_cli(item_name, x, y)
        else:
            print("error: spawn_failed - Invalid arguments!")
            return

    """ # Equip Start
    # Equips item to designated slot or determines best slot based on item
    # Player system is not added yet so will default player to be first entity created entity_list[0]
    # Equip will overwrite previous items
    # Params: command_pieces - list - list of strings thate make up the command
    # Return: None
    def process_equip_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if (
            len(command_pieces) == 3
            and command_pieces[1]
            in [equipment.lower() for equipment in dl.EQUIPMENT_TYPES]
            and command_pieces[2] in [equipment.lower() for equipment in dl.VALID_SLOTS]
        ):
            # Run equip with item name and slot
            item = command_pieces[1]
            slot = command_pieces[2]

        # If slot is not included
        elif len(command_pieces) == 2 and command_pieces[1] in [
            equipment.lower() for equipment in dl.EQUIPMENT_TYPES
        ]:
            # Run equip with JUST item name
            item = command_pieces[1]
            slot = ""
        else:
            print("error: equip_failed - Invalid arguments!")
            return

        # Ensure "player" entity exists
        if not len(self.entity_list) > 0:
            print("error: equip_failed - Player entity does not exist!")
            return

        # Find equipment matching item name
        new_item = dl.create_equipment(item)

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
        Entity.equip_item(self.entity_list[0], new_item, slot.lower())
        # update stats of entity
        self.entity_list[0].update_stats(self.grid)
        # Success message
        print("Valid items:", ", ".join(dl.EQUIPMENT_TYPES))
        print("Valid slots:", ", ".join(dl.VALID_SLOTS))
        print(f"ok: Equipped {new_item.name} to {new_item.slot}!")"""

    # Process Inventory Command Start
    # displays current inventory to user
    # Player system is not added yet so will default player to be first entity created entity_list[0]
    # Params: command_pieces - list - list of strings that make up the command
    # Return: None
    def process_inventory_command(self, command_pieces):
        if len(command_pieces) != 2:
            print("error: inventory_failed - Invalid command!")
            return
        else:
            # Validate e_id as int
            try:
                e_id = int(command_pieces[1])
            except:
                print("error: inventory - Entity id is not valid integer!")
                return
        # Ensure "player" entity exists
        entity = None

        for temp_entity in self.entity_list:
            if temp_entity.id == e_id:
                entity = temp_entity
                break

        if entity is None:
            print("error: inventory_failed - Player entity does not exist!")
            return

        # Display inventory of entity
        print(f"Weapon: {entity.inventory[0].name}")
        print(f"Armor: {entity.inventory[1].name}")
        print(f"Accessory: {entity.inventory[2].name}")
        print("Backpack Slots:")
        # Iterate through all backpack slots
        for index in range(entity.BACKPACK_SIZE):
            # Check if slot contains an item
            if index < len(entity.backpack):
                item = entity.backpack[index]
                if item is None:
                    item_name = "Empty"
                else:
                    item_name = item.name
            else:
                # Slot is empty
                item_name = "Empty"
            # Display slot number and item
            print(f"{index + 1}. {item_name}")

    # Process Inspect Command Start
    # Inspects entity with given ID
    # Params:   command_pieces - list - list of strings that make up the command
    # Return: None
    def process_inspect_command(self, command_pieces):
        # Test for valid amount of command pieces
        if len(command_pieces) == 2:
            # Run inspect with entity ID
            e_id = command_pieces[1]
        else:
            print("error: inspect_failed - Invalid arguments!")
            return

        # Ensure entities exists
        if not len(self.entity_list) > 0:
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
        for entity in self.entity_list:
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
        found_entity.update_stats(self)
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

    # Process Tile Command Start
    # Will describe the tile at the given grid position
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_tile_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 3:
            # Run spawn with x and y - position checked in grid functions
            x = command_pieces[1]
            y = command_pieces[2]
        else:
            print("error: tile_failed - Invalid command!")
            return
        # Ensure map exists
        if not self.map_created:
            print("error: tile_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
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

        if current_tile is None:
            print("error: tile_failed - No tile exists at this position!")
            return
        # Special case with shallowwater for proper capitalization
        elif current_tile.t_type.lower() == "shallowwater":
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

    # Process Pickup Item Command
    # Handles picking up of items at position of entity's id
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_pickup_item_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 3:
            # assign commands
            entity_id = command_pieces[1]
            item_name = command_pieces[2]
        else:
            print("error: pickup_failed - Invalid command!")
            return

        # Ensure map exists
        if not self.map_created:
            print("error: pickup_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: pickup_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: pickup_failed - Item name not found!")
            return

        # Assign variables
        entity = self.assign_entity_from_list(int(entity_id))
        entity_x = entity.position[0]
        entity_y = entity.position[1]

        # Check for backpack space
        if len(entity.backpack) >= Entity.BACKPACK_SIZE:
            print("error: pickup_failed - Backpack if full!")
            return

        # Find the item at the entity's location
        e_tile = self.grid.grid[entity_x][entity_y]
        tile_item = None

        for grid_item in e_tile.item_list:

            # Tile contains an equipment class
            if isinstance(grid_item, type):
                if grid_item.__name__.lower() == item_name.lower():
                    tile_item = grid_item
                    break

            # Tile contains an equipment instance
            elif hasattr(grid_item, "name"):
                if grid_item.name.lower() == item_name.lower():
                    tile_item = grid_item
                    break

            # Tile contains an item name as a string
            elif isinstance(grid_item, str):
                if grid_item.lower() == item_name.lower():
                    tile_item = grid_item
                    break

        # Ensure item is on the tile
        if tile_item is None:
            print("error: pickup_failed - Item not in tiles item list!")
            return
        else:  # item is present and there is backpack space - pickup
            item = dl.create_equipment(item_name.lower())
            entity.add_item_to_backpack(item)
            # Remove item from item_list in grid
            self.grid.remove_item_from_tile_item_list(entity_x, entity_y, tile_item)
            # Success message
            print(f"ok: picked_up {item.name} into backpack!")

    # Process Give Item Command
    # Gives matching entity the provided item
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_give_item_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 3:
            # assign commands
            entity_id = command_pieces[1]
            item_name = command_pieces[2]
        else:
            print("error: give_failed - Invalid command!")
            return

        # Ensure map exists
        if not self.map_created:
            print("error: give_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: give_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: give_failed - Item name not found!")
            return
        # Assign variables
        item = dl.create_equipment(item_name.lower())
        entity = self.assign_entity_from_list(int(entity_id))

        # Check for backpack space
        if len(entity.backpack) >= Entity.BACKPACK_SIZE:
            print("error: give_failed - Backpack if full!")
            return
        else:
            # Give item to entity
            entity.add_item_to_backpack(item)
            # Success message
            print(f"ok: added {item.name} to {entity.id}'s backpack!")

    # Process Drop Item Command
    # Drop matching entitys provided item
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_drop_item_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 3:
            # assign commands
            entity_id = command_pieces[1]
            item_name = command_pieces[2]
        else:
            print("error: drop_failed - Invalid command!")
            return
        # Ensure map exists
        if not self.map_created:
            print("error: drop_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: drop_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: drop_failed - Item name not found!")
            return
        # Assign variables
        entity = self.assign_entity_from_list(int(entity_id))
        # Always valid as this is checked during spawning/moving of said entity
        entity_x = entity.position[0]
        entity_y = entity.position[1]

        # Find item in backpack
        item = None
        for temp_item in entity.backpack:
            if item_name.lower() == temp_item.name.lower():
                item = temp_item
                break

        # Ensure item is in backpack
        if item == None:
            print("error: drop_failed - Item not in backpack!")
        else:  # Success case
            # Add item to the tile
            self.grid.add_item_to_tile_item_list(entity_x, entity_y, item.name)
            # Remove item from entitys bag
            entity.remove_item_from_backpack(item)
            # Check if item was in entity's inventory
            entity.update_inventory()
            # update entity's stats - incase item removed was equipped
            entity.update_stats(self)
            # success message
            print(f"ok: dropped {item.name} onto tile!")

    # Process Swap Item Command
    # Swop matching entitys provided item with item in slot
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_swap_item_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 4:
            # assign commands
            entity_id = command_pieces[1]
            item_slot = command_pieces[2]
            item_name = command_pieces[3]
        else:
            print("error: swap_failed - Invalid command!")
            return
        # Ensure map exists
        if not self.map_created:
            print("error: swap_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: swap_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: swap_failed - Item name not found!")
            return
        # Ensure slot is valid - blocks consumables from equipping also
        slot = None

        for valid_slot in dl.EquipmentSlot:
            if item_slot.lower() == valid_slot.value.lower():
                slot = valid_slot
                break

        if slot is None:
            print("error: swap_failed - Item slot not valid inventory slot!")
            return

        # Assign variables
        item = dl.create_equipment(item_name.lower())
        entity = self.assign_entity_from_list(int(entity_id))

        # Check for correct slot for item assignment
        if item.slot.lower() != slot.value.lower():
            print("error: swap_failed - Slot inccorect for item type!")
            return
        # Ensure item is in units backpack
        elif not any(
            backpack_item is not None
            and item_name.lower() == backpack_item.name.lower()
            for backpack_item in entity.backpack
        ):
            print("error: swap_failed - Item not in backpack!")
            return
        else:  # Success - assign item
            entity.inventory[dl.EquipmentSlotIndex[slot.name].value] = item

        # Success message and stat update
        entity.update_stats(self)
        print("Valid items:", ", ".join(dl.EQUIPMENT_TYPES))
        print(
            "Valid slots:",
            ", ".join(valid_slot.value for valid_slot in dl.EquipmentSlot),
        )
        print(f"ok: swapped {item.slot} with backpack item!")

    # Uses the current consumable - Inputs cleaned in CLI - MAKE SURE ITEM IN BACKPACK
    # Process Use Item Command
    # Use matching entitys provided item
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_use_item_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 3:
            # assign commands
            entity_id = command_pieces[1]
            item_name = command_pieces[2]
        else:
            print("error: use_failed - Invalid command!")
            return
        # ensure entity_id is valid and within list
        if not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: use_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: use_failed - Item name not found!")
            return

        # Assign variables
        entity = self.assign_entity_from_list(int(entity_id))
        # Find item in backpack
        item = None
        for temp_item in entity.backpack:
            if item_name.lower() == temp_item.name.lower():
                item = temp_item
                break
        # Ensure item is in backpack
        if item == None:
            print("error: use_failed - Item not in backpack!")
        # Ensure that item is a consumable
        elif item.slot != "Consumable":
            print("error: use_failed - Item is not a consumable!")
            return
        else:  # Success case
            # Use consumable
            Consumable.use_consumable(item, entity)
            # Remove consumable from backpack
            entity.backpack.remove(item)
            print(f"ok: used {item.name}!")

    # Process Move Command
    # Moves the entity to the grid position if able
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_move_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 4:
            # assign commands
            entity_id = command_pieces[1]
            x = command_pieces[2]
            y = command_pieces[3]
        else:
            print("error: move_failed - Invalid command!")
            return
        # Map created?
        if not self.map_created:
            print("error: move_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: move_failed - x and y are not valid integers!")
            return
            """# x and y within bounds
            elif not Grid.within_bounds(x, y):
                print("error: spawn_failed - x and y exceed bound minimum and maximum!")"""
        # assign proper typing
        x = int(x)
        y = int(y)
        # x and y exceeds current grid bounds
        if not Grid.is_valid_grid_position(self.grid, x, y):
            print("error: move_failed - x and y exceed current grid bounds!")
            return
        # ensure grid location is empty
        elif Grid.is_occupied(self.grid, x, y):
            print(f"error: move_failed - Entity is already present at ({x}, {y})!")
            return
        # Ensure target tile is passable
        elif not Grid.is_passable(self.grid, x, y):
            print(f"error: move_failed - Target tile ({x}, {y}) is impassable!")
            return
        # invalid entity type
        # ensure entity_id is valid and within list
        if not any(entity_id == str(entity.id) for entity in self.entity_list):
            print("error: move_failed - Entity does not exist!")
            return
        # Assign entity
        entity = self.assign_entity_from_list(int(entity_id))
        # Check if target grid position is within range of entity
        if not Grid.is_within_range(
            self.grid, [entity.position[0], entity.position[1]], [x, y], entity.speed
        ):
            print(f"error: move_failed - Target: {x}, {y} is out of entity's range!")
            return
        # Success Case
        else:
            # Move entity
            self.move_entity(entity, x, y)
            # Update stats for entity - may have moved to shallowwater tile
            entity.update_stats(self)
            print(f"ok: moved {entity_id} to {x}, {y}!")
            return

    # Process Attack Command
    # Attacker entity attacks the defending entity and lowering their current health value (not max)
    # attack vs defence - Spells are done in cast command (involves spell power and defence)
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_attack_command(self, command_pieces):
        # Test for valid amount of command pieces and full command
        if len(command_pieces) == 3:
            # Assign ids
            attacker_id = command_pieces[1]
            defender_id = command_pieces[2]
        else:
            print("error: attack_failed due to invalid arguments.")
            return
        # Map created
        if not self.map_created:
            print("error: attack_failed - Map does not exist!")
            return
        # Valid ints for entity ids
        elif not dl.are_valid_ints(attacker_id, defender_id):
            print("error: attack_failed - entity ids are not valid integers!")
            return
        # Valid entity ids in entity list
        elif not any(attacker_id == str(entity.id) for entity in self.entity_list):
            print("error: attack_failed - Attacking entity does not exist!")
            return
        elif not any(defender_id == str(entity.id) for entity in self.entity_list):
            print("error: attack_failed - Defending entity does not exist!")
            return
        # Assign entities
        attacker = self.assign_entity_from_list(int(attacker_id))
        defender = self.assign_entity_from_list(int(defender_id))
        # assign grid positions
        attacker_x = attacker.position[0]
        attacker_y = attacker.position[1]
        defender_x = defender.position[0]
        defender_y = defender.position[1]
        # Determine whether Entity can engage from range or just melee
        if attacker.attack_type == dl.AttackTypes.MELEE:  # Melee assignment
            attack_range = dl.MELEE_RANGE
        else:  # Ranged assignment
            attack_range = dl.RANGED_RANGE

        # Determine if defender is within attack range
        if self.grid.is_within_range(
            [attacker_x, attacker_y], [defender_x, defender_y], attack_range
        ):
            # Continue attack as defender is within attack range
            damage = attacker.attack_entity(defender)
            # Print success message
            print(
                f"ok: attack {attacker_id} dealt {damage} {attacker.attack_type} damage to {defender_id}!"
            )
        else:  # Cancel attack as defender is out of range
            print("error: attack_failed - Defender is out of range!")
            return

    # Process Cast Command
    # Caster entity casts a spell on the targeted entity. This can be offensive/supportive/control
    # Spells use spell power * spell-specific multipliers vs. defence
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_cast_command(self, command_pieces):
        # Test for valid amount of command pieces and full command
        if len(command_pieces) == 4:
            # Assign variables
            caster_id = command_pieces[1]
            target_id = command_pieces[2]
            spell_name = command_pieces[3]
        else:
            print("error: cast_failed due to invalid arguments.")
            return
        # Map created
        if not self.map_created:
            print("error: cast_failed - Map does not exist!")
            return
        # Valid ints for entity ids
        elif not any(caster_id == str(entity.id) for entity in self.entity_list):
            print("error: cast_failed - Casting entity does not exist!")
            return
        elif not any(target_id == str(entity.id) for entity in self.entity_list):
            print("error: cast_failed - Targeted entity does not exist!")
            return
        # Check for spell name within enums
        elif any(spell_name.lower() == name.value.lower() for name in dl.SpellNames):
            # Assign spell
            spell = get_spell(spell_name)
            # Assign range for spell
            spell_range = spell.get_range()
        # Spell not found
        else:
            print("error: cast_failed - Spell does not exist!")
            return
        # Assign entities
        caster = self.assign_entity_from_list(int(caster_id))
        target = self.assign_entity_from_list(int(target_id))
        # Ensure entity is a spell caster - currently only mage
        if not caster.e_type.lower() == "mage":
            print(
                f"error: cast_failed - Caster is {caster.e_type}, which is not a valid spellcaster!"
            )
            return

        # assign grid positions
        caster_x = caster.position[0]
        caster_y = caster.position[1]
        target_x = target.position[0]
        target_y = target.position[1]

        # Determine if this spell is within range
        if self.grid.is_within_range(
            [caster_x, caster_y], [target_x, target_y], spell_range
        ):
            # cast spell on target
            effect = spell.cast_spell(caster, target)
            # update unit stats
            # target.update_stats(self)
            # Print success message
            print(
                f"ok: cast {spell.name} from {caster.id} to {target.id} effect: {effect}"
            )
        else:
            print(
                f"error: cast_failed - Target outside of range! {spell.name} Range: {spell_range}"
            )
            return

    # Spawn Entity For CLI
    # Contains logic for all entity spawning in the CLI
    # Params: x,y - ints - Grid coordinates to spawn entity at
    #           entity_type - string - String used to create the correct entity type
    # Return: None
    def spawn_entity_for_cli(self, x, y, entity_type):
        if not self.map_created:
            print("error: spawn_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: spawn_failed - x and y are not valid integers!")
            return
            """# x and y within bounds
            elif not Grid.within_bounds(x, y):
                print("error: spawn_failed - x and y exceed bound minimum and maximum!")"""
        # x and y exceeds current grid bounds
        elif not Grid.is_valid_grid_position(self.grid, x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")
            return
        # ensure grid location is empty
        elif Grid.is_occupied(self.grid, x, y):
            print(f"error: spawn_failed - Entity is already present at ({x}, {y})!")
            return
        # invalid entity type
        elif not dl.is_valid_entity(entity_type):
            print("error: spawn_failed - Invalid entity type!")
            return
        # All valid inputs
        else:
            # updates grid with new entity and returns entity
            entity = self.grid.spawn_entity(x, y, entity_type, self.entity_ids_issued)
            # success output
            print(f"ok: Spawned {entity_type} at {x}, {y}. id: {entity.id}!")
            # Increment entity_ids_issued to account for new entity
            self.entity_ids_issued += 1
            # Add new entity to entity list
            self.entity_list.append(entity)
            # Add current max stats to the dict
            if entity.e_type.lower() == "mage":  # spanws in with full health and mana
                entity.max_health = entity.health
                entity.max_mana = entity.mana
            else:  # Not a mage - spawns with max/full hp
                entity.max_health = entity.health
            # Add temp buffs for entity
            entity.temp_buffs = []
            # update stats - spawning on tile with effect
            entity.update_stats(self)
            return

    # Spawn Loot For CLI
    # Contains logic for all loot spawning in the CLI
    # Params:   item_name - string - String used to create the correct entity type
    #           x,y - ints - Grid coordinates to spawn loot at
    # Return: None
    def spawn_loot_for_cli(self, item_name, x, y):
        # checks if map was created
        if not self.map_created:
            print("error: spawn_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: spawn_failed - x and y are not valid integers!")
            return
        # x and y exceeds current grid bounds
        elif not Grid.is_valid_grid_position(self.grid, x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: spawn_failed - Item name not found!")
            return
        else:  # Success
            self.grid.add_item_to_tile_item_list(x, y, item_name)
            print(f"ok: spawn_loot {item_name} at {x}, {y}!")
            return

    # Move Entity
    # Contains logic to complete the full move of an entity
    # Params:   entity - entity instance - Entity that will move
    #           x,y - ints - cleaned valid ints with position to move entity to
    # Returns: None
    def move_entity(self, entity, x, y):
        # Update tile occupancy for atincipated move
        self.grid.occupy(x, y, entity.id)
        self.grid.clear_occupant(entity.position[0], entity.position[1], entity.id)
        # Change entity positions
        entity.position = [x, y]

    # Assign Entity from list
    # Assign entity with matching id from cli.entity_list
    # Entitys existence is confirmed prior to this being called - so will always return one
    # Params: e_id - int - Cleaned/valid int to look for in entity list
    # Return: entity - entity - Matching entity in entity list
    def assign_entity_from_list(self, e_id):
        for temp_entity in self.entity_list:
            if temp_entity.id == e_id:
                entity = temp_entity
                break
        return entity

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
