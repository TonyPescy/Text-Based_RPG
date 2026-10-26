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
import equipment
import domain_library as dl
from grid import Grid, Tile
from entity import Entity, EntityInfo, MageInfo
from game_state_manager import GameStateManager
from command_manager import CommandManager
from command import MoveCommand

# from spell import get_spell
from game_state import GameState


# Handles all Command Line Interface commands for the game
class CLI:

    # Initialize CLI
    def __init__(self):
        self.game_state = GameState()
        self.game_state_manager = GameStateManager()
        self.command_manager = CommandManager()

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
            "tick": self.process_tick_command,
            "save": self.process_save_command,
            "load": self.process_load_command,
            "state-info": self.process_state_info_command,
            "undo": self.process_undo_command,
        }

        # Match handler to command
        handler = command_handlers.get(command_pieces[0])

        # Check for unknown command
        if handler is None:
            print("error: Unknown command!")
            return

        # Process Command
        handler(command_pieces)

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
        if self.game_state.is_map_created():
            # Reset map and continue
            self.game_state.reset_map()
        # width and height are not valid ints
        elif not dl.are_valid_ints(width, height):
            print("error: map_init_failed - Width and height are not valid integers!")
            return
        # width and heigth within bounds
        elif not Grid.within_bounds(width, height):
            print(
                "error: map_init_failed - Width and height exceed bound minimum and maximum!"
            )
            return
        # Valid inputs
        # Create grid with width and height
        self.game_state.create_grid(width, height)
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
        if not self.game_state.is_map_created():
            print("error: tile_set_failed - Map does not exist!")
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: set_tile_failed - x and y are not valid integers!")
        # x and y exceeds current grid bounds
        elif not self.game_state.is_valid_grid_position(x, y):
            print("error: set_tile_failed - x and y exceed current grid bounds!")
        # tile is not valid
        elif not Tile.is_valid_tile(tile_type):
            print("error: set_tile_failed - Tile type provided was invalid!")

        else:
            # updates grid with new tile
            self.game_state.set_game_grid_tile(x, y, tile_type)
            # update entity if present
            if self.game_state.is_grid_tile_occupied(x, y):
                # update entity
                self.game_state.update_entity(
                    self.game_state.get_entity_id_from_tile(x, y)
                )
            else:
                pass
            # success output -  with special case for shallowwater
            if tile_type.lower() == "shallowwater":
                print(f"ok: tile_set {x}, {y} type: ShallowWater!")
            else:
                print(f"ok: tile_set {x}, {y} type: {tile_type.capitalize()}!")

    # Process Spawn Command Start
    # Spawns an entity at designated position
    # Params: command_pieces - list - list of strings that make up the command
    # Return: None
    def process_spawn_command(self, command_pieces):
        # Test for valid amount of command pieces and correct commands/typing
        if len(command_pieces) == 4 and dl.is_valid_entity(command_pieces[1]):
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
            except ValueError:
                print("error: inventory - Entity id is not valid integer!")
                return
        # Get player entity
        entity_info = self.game_state.get_entity_info_from_list(e_id)

        if entity_info is None:
            print("error: inventory_failed - Player entity does not exist!")
            return
        # Check to see if entity is dead
        elif not Entity.is_alive_from_info(entity_info):
            print("error: inventory_failed - Player entity is dead!")
            return

        # Get entity inventory

        # Display inventory of entity - Invetory is list of equipment names
        print(f"Weapon: {entity_info.inventory[0]}")
        print(f"Armor: {entity_info.inventory[1]}")
        print(f"Accessory: {entity_info.inventory[2]}")
        print("Backpack Slots:")
        # Iterate through all backpack slots
        for index in range(Entity.BACKPACK_SIZE):
            # Check if slot contains an item
            if index < len(entity_info.backpack):
                item = entity_info.backpack[index]
                if item is None:
                    item_name = "Empty"
                else:
                    item_name = item
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
        if not self.game_state.entities_exists():
            print("error: inspect_failed - No entities exist yet!")
            return

        # Validate e_id as int
        try:
            e_id = int(e_id)
        except ValueError:
            print("error: inspect_failed - Entity id is not valid integer!")
            return

        entity_info = self.game_state.get_entity_info_from_list(e_id)
        # Error message for entity existence
        if entity_info is None:
            print("error: inspect_failed - Entity does not exist!")
            return
        # Check to see if entity is dead
        elif not Entity.is_alive_from_info(entity_info):
            print("error: inspect_failed - Player entity is dead!")
            return

        # update entity stats - in case changes occurred
        self.game_state.update_entity(entity_info.id)
        # Display stats of entity   # UPDATE ASAP
        # Display stats of entity
        for stat, value in entity_info.__dict__.items():
            # Special case for active modifiers
            if stat == "active_modifiers":
                count = 0

                # Count all modifiers
                for modifier_type, contents in value:
                    count += len(contents)

                print(f"Active_modifiers: {count}")

            # Display all other stats
            else:
                # Capitalize stat name and value if string
                stat = stat.capitalize()
                value = CLI.capitalize_if_string(value)
                print(f"{stat}: {value}")

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
        if not self.game_state.is_map_created():
            print("error: tile_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: tile_failed - x and y are not valid integers!")
            return
        # x and y exceeds current grid bounds
        elif not self.game_state.is_valid_grid_position(x, y):
            print("error: tile_failed - x and y exceed current grid bounds!")
            return

        # display - handles special cases
        print(f"Coordinate: {x}, {y}")
        # Get tile
        current_tile_info = self.game_state.get_game_tile_info(int(x), int(y))

        if current_tile_info is None:
            print("error: tile_failed - No tile exists at this position!")
            return
        # Special case with shallowwater for proper capitalization
        elif current_tile_info.tile_type.lower() == "shallowwater":
            print("Type: ShallowWater")
        else:
            print(f"Type: {current_tile_info.tile_type.capitalize()}")

        # Passable
        print(f"Passable: {current_tile_info.passable}")

        # occupants - special case for empty list (should logic be changed to just one occupant this can be cleaner)
        if len(current_tile_info.occupants) == 0:
            print("Occupants: None")
        else:
            print(f"Occupants: {current_tile_info.occupants[0]}")

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

        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: pickup_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: pickup_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
            print("error: pickup_failed - Item name not found!")
            return

        # Assign variables
        entity_x = entity_info.position[0]
        entity_y = entity_info.position[1]

        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: pickup_failed - Entity is dead!")
            return

        # Check for backpack space
        if len(entity_info.backpack) >= Entity.BACKPACK_SIZE:
            print("error: pickup_failed - Backpack if full!")
            return

        # Find the item at the entity's location
        ent_tile_info = self.game_state.get_game_tile_info(entity_x, entity_y)

        if ent_tile_info is None:
            print("error: pickup_failed - No tile found!")
            return

        # Get tile item
        tile_item = None

        for item in ent_tile_info.item_list:
            if item.lower() == item_name.lower():
                tile_item = item  # Just the item name
                break

        # Ensure item is on the tile
        if tile_item is None:
            print("error: pickup_failed - Item not in tiles item list!")
            return
        else:  # item is present and there is backpack space - pickup
            # Remove item from item_list in grid - returns immutable item info object
            removed_item = self.game_state.remove_item_from_tile(
                entity_x, entity_y, tile_item
            )
            if removed_item is None:
                print("error: pickup_failed - Item not found!")
            # Add to backpack
            self.game_state.add_item_to_backpack_based_on_info(
                entity_info.id, removed_item.name
            )
            # Success message
            print(
                f"ok: picked_up {removed_item.name} into backpack!"
            )  # change to get name when item is encapsulated

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

        # Get entity
        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: give_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: give_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
            print("error: give_failed - Item name not found!")
            return

        """# Create Item
        item = dl.create_equipment(item_name.lower())"""

        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: give_failed - Entity is dead!")
            return

        # Check for backpack space
        if len(entity_info.backpack) >= Entity.BACKPACK_SIZE:
            print("error: give_failed - Backpack if full!")
            return
        else:
            # Give item to entity
            self.game_state.add_item_to_backpack_based_on_info(
                entity_info.id, item_name
            )
            # Success message
            print(f"ok: added {item_name} to {entity_info.id}'s backpack!")

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

        # Get Entity
        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: drop_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: drop_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
            print("error: drop_failed - Item name not found!")
            return

        # Always valid as this is checked during spawning/moving of said entity
        entity_x = entity_info.position[0]
        entity_y = entity_info.position[1]

        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: drop_failed - Entity is dead!")
            return

        # Find item in backpack
        item = None
        for temp_item in entity_info.backpack:  # Immutable copy of item
            if item_name.lower() == temp_item.name.lower():
                item = temp_item.name
                break

        # Ensure item is in backpack
        if item == None:
            print("error: drop_failed - Item not in backpack!")
        else:  # Success case
            # Add item to the tile
            self.game_state.add_item_to_tile(entity_x, entity_y, item)
            # Remove item from entitys bag
            self.game_state.remove_item_from_backpack_based_on_info(
                entity_info.id, item
            )
            # Check if item was in entity's inventory
            self.game_state.update_inventory_based_on_info(entity_info.id)
            # update entity's stats - incase item removed was equipped
            self.game_state.update_entity(entity_info.id)
            # success message
            print(f"ok: dropped {item} onto tile!")

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

        # Get Entity
        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: swap_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: swap_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
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

        # Find item in backpack
        item = None
        for temp_item in entity_info.backpack:  # Immutable copy of item
            if item_name.lower() == temp_item.name.lower():
                item = temp_item
                break

        if item is None:
            print("error: swap_failed - Item not in backpack!")
            return
        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: swap_failed - Entity is dead!")
            return
        # Check for correct slot for item assignment
        elif item.slot.lower() != slot.value.lower():
            print("error: swap_failed - Slot incorrect for item type!")
            return
        else:  # Success - assign item
            self.game_state.equip_item_based_on_info(entity_info.id, item.name, slot)

        # Success message and stat update
        self.game_state.update_entity(entity_info.id)
        print("Valid items:", ", ".join(equipment.get_equipment_names()))
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

        # Get Entity
        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # ensure entity_id is valid and within list
        if not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: use_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
            print("error: use_failed - Item name not found!")
            return

        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: use_failed - Entity is dead!")
            return
        # Find item in backpack
        item = None
        for temp_item in entity_info.backpack:  # Backpack is collection of item names
            if item_name.lower() == temp_item.name.lower():
                item = temp_item
                break
        # Ensure item is in backpack
        if item == None:
            print("error: use_failed - Item not in backpack!")
        # Ensure that item is a consumable
        elif not isinstance(item, equipment.ConsumableInfo):
            print("error: use_failed - Item is not a consumable!")
            return
        else:  # Success case
            # Use consumable
            self.game_state.use_consumable(entity_info.id, item.name)
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
        if not self.game_state.is_map_created():
            print("error: move_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: move_failed - x and y are not valid integers!")
            return

        # assign proper typing
        x = int(x)
        y = int(y)

        # x and y exceeds current grid bounds
        if not self.game_state.is_valid_grid_position(x, y):
            print("error: move_failed - x and y exceed current grid bounds!")
            return
        # ensure grid location is empty
        elif self.game_state.is_grid_tile_occupied(x, y):
            print(f"error: move_failed - Entity is already present at ({x}, {y})!")
            return
        # Ensure target tile is passable
        elif not self.game_state.is_tile_passable(x, y):
            print(f"error: move_failed - Target tile ({x}, {y}) is impassable!")
            return

        # Get Entity
        entity_info = self.game_state.get_entity_info_from_list(entity_id)

        # invalid entity type
        # ensure entity_id is valid and within list
        if not (
            (isinstance(entity_info, EntityInfo) or isinstance(entity_info, MageInfo))
            and entity_id == str(entity_info.id)
        ):
            print("error: move_failed - Entity does not exist!")
            return

        # Ensure entity is alive
        if not Entity.is_alive_from_info(entity_info):
            print("error: move_failed - Entity is dead!")
            return
        # Check if target grid position is within range of entity
        elif not self.game_state.is_within_range(
            entity_info.position[0],
            entity_info.position[1],
            x,
            y,
            entity_info.speed,
        ):
            print(f"error: move_failed - Target: {x}, {y} is out of entity's range!")
            return
        # Success Case
        else:
            # Create and execute move command
            command = MoveCommand(self.game_state, entity_info.id, x, y)
            # Move entity
            self.command_manager.execute_command(command)

            # self.game_state.move_entity(entity_info.id, x, y)
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

        # Valid ints for entity ids
        if not dl.are_valid_ints(attacker_id, defender_id):
            print("error: attack_failed - entity ids are not valid integers!")
            return

        # Get entities
        attacker_info = self.game_state.get_entity_info_from_list(int(attacker_id))
        defender_info = self.game_state.get_entity_info_from_list(int(defender_id))

        # Map created
        if not self.game_state.is_map_created():
            print("error: attack_failed - Map does not exist!")
            return
        # Valid entity ids in entity list
        elif not (attacker_info is not None and attacker_id == str(attacker_info.id)):
            print("error: attack_failed - Attacking entity does not exist!")
            return
        elif not (defender_info is not None and defender_id == str(defender_info.id)):
            print("error: attack_failed - Defending entity does not exist!")
            return
        # assign grid positions
        attacker_x = attacker_info.position[0]
        attacker_y = attacker_info.position[1]
        defender_x = defender_info.position[0]
        defender_y = defender_info.position[1]
        # Ensure entity is alive
        if not Entity.is_alive_from_info(attacker_info):
            print("error: attack_failed - Attacker is dead!")
            return
        elif not Entity.is_alive_from_info(defender_info):
            print("error: attack_failed - Defender is dead!")
            return
        # Determine whether Entity can engage from range or just melee
        if attacker_info.attack_type == dl.AttackTypes.MELEE:  # Melee assignment
            attack_range = dl.MELEE_RANGE
        else:  # Ranged assignment
            attack_range = dl.RANGED_RANGE

        # Determine if defender is within attack range
        if self.game_state.is_within_range(
            attacker_x, attacker_y, defender_x, defender_y, attack_range
        ):
            # Continue attack as defender is within attack range
            damage = self.game_state.attack_entity(attacker_info.id, defender_info.id)
            # Print success message
            print(
                f"ok: attack {attacker_id} dealt {damage} {attacker_info.attack_type} damage to {defender_id}!"
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

        # Valid ints for entity ids
        if not dl.are_valid_ints(caster_id, target_id):
            print("error: cast_failed - entity ids are not valid integers!")
            return

        # Get entities
        caster_info = self.game_state.get_entity_info_from_list(int(caster_id))
        target_info = self.game_state.get_entity_info_from_list(int(target_id))

        # Map created
        if not self.game_state.is_map_created():
            print("error: cast_failed - Map does not exist!")
            return

        # Valid ints for entity ids
        elif not (caster_info is not None and caster_id == str(caster_info.id)):
            print("error: cast_failed - Casting entity does not exist!")
            return
        elif not (target_info is not None and target_id == str(target_info.id)):
            print("error: cast_failed - Targeted entity does not exist!")
            return
        # Check for spell name within enums
        elif dl.is_valid_spell(spell_name):
            # Get spell info
            spell_info = self.game_state.get_spell_info(spell_name.lower())
        # Spell not found
        else:
            print("error: cast_failed - Spell does not exist!")
            return

        # Ensure entities are alive
        if not Entity.is_alive_from_info(caster_info):
            print("error: cast_failed - Caster is dead!")
            return
        # CHANGE THIS LOGIC WHEN REVIVAL IS ADDED
        elif not Entity.is_alive_from_info(target_info):
            print("error: cast_failed - Target is dead!")
            return
        # Ensure entity is a spell caster - currently only mage
        elif not caster_info.e_type.lower() == "mage":
            print(
                f"error: cast_failed - Caster is {caster_info.e_type}, which is not a valid spellcaster!"
            )
            return

        # assign grid positions
        caster_x = caster_info.position[0]
        caster_y = caster_info.position[1]
        target_x = target_info.position[0]
        target_y = target_info.position[1]

        # Determine if this spell is within range
        if self.game_state.is_within_range(
            caster_x, caster_y, target_x, target_y, spell_info.spell_range
        ):
            # cast spell on target
            effect = self.game_state.cast_spell(
                caster_info.id, target_info.id, spell_info.name
            )
            # update unit stats
            # target.update_stats(self)
            # Print success message
            print(
                f"ok: cast {spell_info.name} from {caster_info.id} to {target_info.id} effect: {effect}"
            )
        else:
            print(
                f"error: cast_failed - Target outside of range! {spell_info.name} Range: {spell_info.spell_range}"
            )
            return

    # Process Tick Command Start
    # Increases turn ticker by 1 and updates all entities turn timers if they have one
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_tick_command(self, command_pieces):
        # init entities to remove from list/grid
        entities_to_remove = []
        # Test for valid amount of command pieces
        if not len(command_pieces) == 1:
            print("error: tick_failed due to invalid arguments!")
            return
        elif not self.game_state.is_map_created():
            print("error: tick_failed - Map does not exist!")
            return
        # Check to see if there are entities to update
        if self.game_state.entities_exists():
            entities_to_remove = self.game_state.process_tick_for_all_entities()

        # If there are entities to be removed from the game
        if len(entities_to_remove) > 0:
            for entity_id in entities_to_remove:
                self.game_state.remove_entity_from_game(entity_id)

        # Mark game state as unsaved
        self.game_state.mark_as_unsaved()
        # Advance turn
        self.game_state.advance_turn()

    # Process Save Command
    # Saves the game state to given file
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_save_command(self, command_pieces):
        if len(command_pieces) == 2:
            filename = command_pieces[1]
        else:
            print("error: save_failed - Invalid command!")
            return

        # Check to see if game state is active and able to be saved
        if not self.game_state.game_state_is_active():
            # Not active
            print(
                "error: save_failed - Game State is not initialized and cannot be saved!"
            )
            return

        else:
            # Success - can be saved
            try:
                # Try save game
                self.game_state_manager.save_game(self.game_state, filename)
                # Sucess Message
                print(f"ok: game saved to {filename}")
            # Extensive error catching
            except (OSError, ValueError, TypeError, KeyError) as error:
                print(f"error: save_failed - {error}!")

    # Process Load Command
    # Loads the game state from given file
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_load_command(self, command_pieces):
        if len(command_pieces) == 2:
            filename = command_pieces[1]
        else:
            print("error: load_failed - Invalid command!")
            return

        # Attempt to load game
        try:
            # Load Game
            self.game_state_manager.load_game(self.game_state, filename)
            # Success Message
            print(f"ok: game loaded from {filename}!")
        # Extensive error catching
        except (OSError, ValueError, TypeError, KeyError) as error:
            print(f"error: load_failed - {error}!")

    # Process State-Info Command
    # Displays the current game state info
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_state_info_command(self, command_pieces):
        # Check that game state exists and is active
        if not self.game_state.game_state_is_active():
            print("error: state-info_failed - Game State is not initialized!")
            return
        else:
            # Success
            try:
                game_state_info = self.game_state.get_game_state_info()

                print(
                    f"ok: turn {game_state_info[0]}, entities: {game_state_info[1]}, saved: {str(game_state_info[2]).lower()}"
                )
            # Extensive error checking
            except (AttributeError, TypeError, ValueError) as error:
                print(f"error: state_info_failed {error}")

    # Spawn Entity For CLI
    # Contains logic for all entity spawning in the CLI
    # Params: x,y - ints - Grid coordinates to spawn entity at
    #           entity_type - string - String used to create the correct entity type
    # Return: None
    def spawn_entity_for_cli(self, x, y, entity_type):
        if not self.game_state.is_map_created():
            print("error: spawn_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: spawn_failed - x and y are not valid integers!")
            return
        # x and y exceeds current grid bounds
        elif not self.game_state.is_valid_grid_position(x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")
            return
        # ensure grid location is empty
        elif self.game_state.is_grid_tile_occupied(x, y):
            print(f"error: spawn_failed - Entity is already present at ({x}, {y})!")
            return
        # invalid entity type
        elif not dl.is_valid_entity(entity_type):
            print("error: spawn_failed - Invalid entity type!")
            return
        # All valid inputs
        else:
            # updates grid with new entity
            self.game_state.spawn_entity(x, y, entity_type)
            # success output
            print(
                f"ok: Spawned {entity_type} at {x}, {y}. id: {self.game_state.get_entity_id_from_tile(x, y)}!"
            )
            return

    # Spawn Loot For CLI
    # Contains logic for all loot spawning in the CLI
    # Params:   item_name - string - String used to create the correct entity type
    #           x,y - ints - Grid coordinates to spawn loot at
    # Return: None
    def spawn_loot_for_cli(self, item_name, x, y):
        # checks if map was created
        if not self.game_state.is_map_created():
            print("error: spawn_failed - Map does not exist!")
            return
        # x and y are not valid ints
        elif not dl.are_valid_ints(x, y):
            print("error: spawn_failed - x and y are not valid integers!")
            return
        # x and y exceeds current grid bounds
        elif not self.game_state.is_valid_grid_position(x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")
            return
        # ensure item_name is valid
        elif equipment.create_equipment(item_name) is None:
            print("error: spawn_failed - Item name not found!")
            return
        else:  # Success
            self.game_state.spawn_loot(x, y, item_name)
            print(f"ok: spawn_loot {item_name} at {x}, {y}!")
            return

    # Process Undo Command
    # Reverses the last successfully executed command
    # Params: command_pieces - list - list of strings that make up the command
    # Returns: None
    def process_undo_command(self, command_pieces):
        if len(command_pieces) != 1:
            print("error: undo_failed - Invalid command!")
            return

        # Get command after undoing it
        is_undone, command_undone = self.command_manager.undo_last_command()

        if is_undone:
            name = command_undone.get_name()
            print(f"ok: undone {name}!")
        else:
            print("error: undo_failed - No commands to undo!")

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
