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
from spell import get_spell
from game_state import GameState


# Handles all Command Line Interface commands for the game
class CLI:

    # Initialize CLI
    def __init__(self):
        self.game_state = GameState()

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
        elif not self.game_state.is_valid_grid_position(self.grid, x, y):
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
        # Get player entity
        entity = self.game_state.get_entity_from_list(e_id)

        if entity is None:
            print("error: inventory_failed - Player entity does not exist!")
            return
        # Check to see if entity is dead
        elif not entity.is_alive():
            print("error: inventory_failed - Player entity is dead!")
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
        if not self.game_state.entities_exists():
            print("error: inspect_failed - No entities exist yet!")
            return

        # Validate e_id as int
        try:
            e_id = int(e_id)
        except:
            print("error: inspect_failed - Entity id is not valid integer!")
            return

        entity = self.game_state.get_entity_from_list(e_id)
        # Error message for entity existence
        if entity is None:
            print("error: inspect_failed - Entity does not exist!")
            return
        # Check to see if entity is dead
        elif not entity.is_alive():
            print("error: inspect_failed - Player entity is dead!")
            return

        # update entity stats - in case changes occurred
        entity.update_stats(self)
        # get stats of entity
        entity_stats = entity.get_stats()
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
        current_tile = self.game_state.get_game_tile(int(x), int(y))

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

        entity = self.game_state.get_entity_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: pickup_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id)):
            print("error: pickup_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: pickup_failed - Item name not found!")
            return

        # Assign variables
        entity_x = entity.position[0]
        entity_y = entity.position[1]

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: pickup_failed - Entity is dead!")
            return

        # Check for backpack space
        if len(entity.backpack) >= Entity.BACKPACK_SIZE:
            print("error: pickup_failed - Backpack if full!")
            return

        # Find the item at the entity's location
        e_tile = self.game_state.get_game_tile(entity_x, entity_y)
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

        # Get entity
        entity = self.game_state.get_entity_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: give_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id)):
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

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: give_failed - Entity is dead!")
            return

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

        # Get Entity
        entity = self.game_state.get_entity_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: drop_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id)):
            print("error: drop_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: drop_failed - Item name not found!")
            return

        # Always valid as this is checked during spawning/moving of said entity
        entity_x = entity.position[0]
        entity_y = entity.position[1]

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: drop_failed - Entity is dead!")
            return

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
            self.game_state.add_item_from_tile(entity_x, entity_y, item_name)
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

        # Get Entity
        entity = self.game_state.get_entity_from_list(entity_id)

        # Ensure map exists
        if not self.game_state.is_map_created():
            print("error: swap_failed - Map does not exist!")
            return
        # ensure entity_id is valid and within list
        elif not any(entity_id == str(entity.id)):
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

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: swap_failed - Entity is dead!")
            return
        # Check for correct slot for item assignment
        elif item.slot.lower() != slot.value.lower():
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

        # Get Entity
        entity = self.game_state.get_entity_from_list(entity_id)

        # ensure entity_id is valid and within list
        if not any(entity_id == str(entity.id)):
            print("error: use_failed - Entity does not exist!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: use_failed - Item name not found!")
            return

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: use_failed - Entity is dead!")
            return
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
        if not self.game_state.is_valid_grid_position(self.grid, x, y):
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
        entity = self.game_state.get_entity_from_list(entity_id)

        # invalid entity type
        # ensure entity_id is valid and within list
        if not any(entity_id == str(entity.id)):
            print("error: move_failed - Entity does not exist!")
            return

        # Ensure entity is alive
        if not entity.is_alive():
            print("error: move_failed - Entity is dead!")
            return
        # Check if target grid position is within range of entity
        elif not self.game_state.is_within_range(
            [entity.position[0], entity.position[1]], [x, y], entity.speed
        ):
            print(f"error: move_failed - Target: {x}, {y} is out of entity's range!")
            return
        # Success Case
        else:
            # Move entity
            self.game_state.move_entity(entity, x, y)
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

        # Get entities
        attacker = self.game_state.get_entity_from_list(int(attacker_id))
        defender = self.game_state.get_entity_from_list(int(defender_id))

        # Map created
        if not self.game_state.is_map_created():
            print("error: attack_failed - Map does not exist!")
            return
        # Valid ints for entity ids
        elif not dl.are_valid_ints(attacker_id, defender_id):
            print("error: attack_failed - entity ids are not valid integers!")
            return
        # Valid entity ids in entity list
        elif not (attacker is not None and attacker_id == str(attacker.id)):
            print("error: attack_failed - Attacking entity does not exist!")
            return
        elif not (defender is not None and defender_id == str(defender.id)):
            print("error: attack_failed - Defending entity does not exist!")
            return
        # assign grid positions
        attacker_x = attacker.position[0]
        attacker_y = attacker.position[1]
        defender_x = defender.position[0]
        defender_y = defender.position[1]
        # Ensure entity is alive
        if not attacker.is_alive():
            print("error: attack_failed - Attacker is dead!")
            return
        elif not defender.is_alive():
            print("error: attack_failed - Defender is dead!")
            return
        # Determine whether Entity can engage from range or just melee
        if attacker.attack_type == dl.AttackTypes.MELEE:  # Melee assignment
            attack_range = dl.MELEE_RANGE
        else:  # Ranged assignment
            attack_range = dl.RANGED_RANGE

        # Determine if defender is within attack range
        if self.game_state.is_within_range(
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

        # Get entities
        caster = self.game_state.get_entity_from_list(int(caster_id))
        target = self.game_state.get_entity_from_list(int(target_id))

        # Map created
        if not self.game_state.is_map_created():
            print("error: cast_failed - Map does not exist!")
            return

        # Valid ints for entity ids
        elif not any(caster_id == str(caster.id)):
            print("error: cast_failed - Casting entity does not exist!")
            return
        elif not any(target_id == str(target.id)):
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

        # Ensure entities are alive
        if not caster.is_alive():
            print("error: cast_failed - Caster is dead!")
            return
        # CHANGE THIS LOGIC WHEN REVIVAL IS ADDED
        elif not target.is_alive():
            print("error: cast_failed - Target is dead!")
            return
        # Ensure entity is a spell caster - currently only mage
        elif not caster.e_type.lower() == "mage":
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
        if self.game_state.is_within_range(
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
            for entity in entities_to_remove:
                self.game_state.remove_entity_from_game(entity)

        # Mark game state as unsaved
        self.game_state.mark_as_unsaved()
        # Advance turn
        self.game_state.advance_turn()

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
        elif not self.game_state.is_valid_grid_position(self.grid, x, y):
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
        elif not self.game_state.is_valid_grid_position(self.grid, x, y):
            print("error: spawn_failed - x and y exceed current grid bounds!")
            return
        # ensure item_name is valid
        elif not any(
            item_name.lower() == item_type.lower() for item_type in dl.EQUIPMENT_TYPES
        ):
            print("error: spawn_failed - Item name not found!")
            return
        else:  # Success
            self.game_state.spawn_loot(x, y, item_name)
            print(f"ok: spawn_loot {item_name} at {x}, {y}!")
            return

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
