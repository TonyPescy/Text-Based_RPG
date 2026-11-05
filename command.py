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
from domain_library import SpellEffects, are_valid_ints
from entity import Entity


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

    # Redo
    # Re-executes the requested game action
    # Params: None
    # Returns: None
    @abstractmethod
    def redo(self):
        pass

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    @abstractmethod
    def get_name(self):
        pass

    # Is Undoable
    # Determines whether the command should be added to undo history
    # Params: None
    # Returns: bool - True if command can be undone
    def is_undoable(self):
        return True


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
        # Get entity and check for dead status
        entity = self.__game_state.get_entity_from_list(self.__target_id)
        entity_info = entity.get_info()
        # Check if entity has the Dead status
        is_dead = any(
            dict(temp_buff).get("Name") == "Dead"
            for temp_buff in entity_info.temp_buffs
        )

        # If entity had Dead status
        if is_dead:
            # Remove it
            entity.remove_temp_buffs(["Dead"])

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


# Cast Spell Command extends from Command
class CastSpellCommand(Command):

    # Initialize Cast Spell Command
    def __init__(self, game_state, caster_id, target_id, spell_name):
        self.__game_state = game_state
        self.__caster_id = int(caster_id)
        self.__target_id = int(target_id)
        self.__spell_name = spell_name
        self.__name = "Cast"
        self.__spell_result = None
        self.__old_health = None
        self.__old_mana = None

    # Execute
    # Casts a spell at the specified target
    # Params: None
    # Returns: None
    def execute(self):
        # Cast the spell and store the result for undo
        # Store original stats before casting
        caster_info = self.__game_state.get_entity_from_list(
            self.__caster_id
        ).get_info()
        target_info = self.__game_state.get_entity_from_list(
            self.__target_id
        ).get_info()

        self.__old_mana = caster_info.mana
        self.__old_health = target_info.health

        # Cast the spell
        self.__spell_result = self.__game_state.cast_spell(
            self.__caster_id,
            self.__target_id,
            self.__spell_name,
        )

    # Undo
    # Reverses the effects of the cast spell
    # Params: None
    # Returns: None
    def undo(self):
        if self.__spell_result is None:
            raise ValueError("Spell has not been cast!")

        # Get target and check for dead status
        target = self.__game_state.get_entity_from_list(self.__target_id)
        target_info = target.get_info()

        # Check if entity has the Dead status
        is_dead = any(
            dict(temp_buff).get("Name") == "Dead"
            for temp_buff in target_info.temp_buffs
        )

        # If entity had Dead status
        if is_dead:
            # Remove it
            target.remove_temp_buffs(["Dead"])

        # Remove any spell effects
        # Get temporary buff names
        temp_buff_names = [
            dict(temp_buff).get("Name") for temp_buff in target_info.temp_buffs
        ]
        # Get spell effect names from enums
        spell_effect_names = {effect.value for effect in SpellEffects}

        # Find active spell effects
        spell_effects = [name for name in temp_buff_names if name in spell_effect_names]

        # Remove active spell effects matching current spell
        for name in spell_effects:
            if name.lower() == self.__spell_name.lower():
                target.remove_temp_buffs([name])

        # Restore the original stats and spell effects
        self.__game_state.undo_cast(
            self.__caster_id,
            self.__target_id,
            self.__spell_name,
            self.__old_mana,
            self.__old_health,
        )

    # Redo
    # Casts the spell again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__spell_result is None:
            raise ValueError("Spell has not been cast!")

        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Get Spell Result
    # Gets the result of the cast spell
    # Params: None
    # Returns: spell_result - result of the spell
    def get_spell_result(self):
        return self.__spell_result


# Set Tile Command extends from Command
class SetTileCommand(Command):

    # Initialize Set Tile Command
    def __init__(self, game_state, x, y, tile_type):
        self.__game_state = game_state
        self.__x = int(x)
        self.__y = int(y)
        self.__tile_type = tile_type
        self.__name = "Set"
        self.__old_tile = None
        self.__executed = False

    # Execute
    # Sets the tile at the specified position
    # Params: None
    # Returns: None
    def execute(self):
        # Get original tile type for undo
        if not self.__executed:
            self.__old_tile = self.__game_state.get_game_tile_info(self.__x, self.__y)

        # Set the new tile
        self.__game_state.set_game_grid_tile(self.__x, self.__y, self.__tile_type)

        # Update entity if tile is occupied
        if self.__game_state.is_grid_tile_occupied(self.__x, self.__y):
            # Update entity
            self.__game_state.update_entity(
                self.__game_state.get_entity_id_from_tile(self.__x, self.__y)
            )

        # Mark command as executed
        self.__executed = True

    # Undo
    # Restores the original tile at the specified position
    # Params: None
    # Returns: None
    def undo(self):
        if not self.__executed:
            raise ValueError("Tile has not been set!")

        # Restore original tile
        self.__game_state.set_game_grid_tile(
            self.__x, self.__y, self.__old_tile.tile_type
        )

        # Update entity if tile is occupied
        if self.__game_state.is_grid_tile_occupied(self.__x, self.__y):
            # Update entity
            self.__game_state.update_entity(
                self.__game_state.get_entity_id_from_tile(self.__x, self.__y)
            )

        # Mark command as no longer executed
        self.__executed = False

    # Redo
    # Sets the tile again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__executed:
            raise ValueError("Tile has already been set!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Pickup Command extends from Command
class PickupCommand(Command):

    # Initialize Pickup Command
    def __init__(self, game_state, entity_id, item_name):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__item_name = item_name
        self.__name = "Pickup"
        self.__old_position = None
        self.__removed_item = None
        self.__executed = False

    # Execute
    # Picks up an item from the entity's current tile
    # Params: None
    # Returns: None
    def execute(self):
        # Get entity info
        entity_info = self.__game_state.get_entity_info_from_list(self.__entity_id)

        # Store entity position for undo
        if not self.__executed:
            self.__old_position = entity_info.position

        # Get tile info
        tile_info = self.__game_state.get_game_tile_info(
            entity_info.position[0],
            entity_info.position[1],
        )

        # Find item on tile
        tile_item = None

        for item in tile_info.item_list:
            if item.lower() == self.__item_name.lower():
                tile_item = item
                break

        # Ensure item is on tile
        if tile_item is None:
            raise ValueError("Item not found on tile!")

        # Remove item from tile
        self.__removed_item = self.__game_state.remove_item_from_tile(
            entity_info.position[0],
            entity_info.position[1],
            tile_item,
        )

        # Ensure item was removed
        if self.__removed_item is None:
            raise ValueError("Item could not be removed from tile!")

        # Add item to backpack
        self.__game_state.add_item_to_backpack_based_on_info(
            self.__entity_id,
            self.__removed_item.name,
        )

        # Mark command as executed
        self.__executed = True

    # Undo
    # Returns the picked-up item to its original tile
    # Params: None
    # Returns: None
    def undo(self):
        if not self.__executed:
            raise ValueError("Item has not been picked up!")

        # Remove item from backpack
        self.__game_state.remove_item_from_backpack(
            self.__entity_id,
            self.__removed_item.name,
        )

        # Return item to original tile
        self.__game_state.add_item_to_tile(
            self.__old_position[0],
            self.__old_position[1],
            self.__removed_item.name,
        )

        # Mark command as no longer executed
        self.__executed = False

    # Redo
    # Picks up the item again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__executed:
            raise ValueError("Item has already been picked up!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Give Item Command extends from Command
class GiveItemCommand(Command):

    # Initialize Give Item Command
    def __init__(self, game_state, entity_id, item_name):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__item_name = item_name
        self.__name = "Give"
        self.__executed = False

    # Execute
    # Gives an item to the specified entity
    # Params: None
    # Returns: None
    def execute(self):
        # Add item to backpack
        self.__game_state.add_item_to_backpack_based_on_info(
            self.__entity_id, self.__item_name
        )

        # Mark command as executed
        self.__executed = True

    # Undo
    # Removes the given item from the entity's backpack
    # Params: None
    # Returns: None
    def undo(self):
        if not self.__executed:
            raise ValueError("Item has not been given!")

        # Remove item from backpack
        self.__game_state.remove_item_from_backpack(self.__entity_id, self.__item_name)

        # Mark command as no longer executed
        self.__executed = False

    # Redo
    # Gives the item again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__executed:
            raise ValueError("Item has already been given!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Drop Item Command extends from Command
class DropItemCommand(Command):

    # Initialize Drop Item Command
    def __init__(self, game_state, entity_id, item_name):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__item_name = item_name
        self.__name = "Drop"
        self.__old_position = None
        self.__dropped_item = None
        self.__executed = False

    # Execute
    # Drops an item from the entity's backpack onto its tile
    # Params: None
    # Returns: None
    def execute(self):
        # Get entity info
        entity_info = self.__game_state.get_entity_info_from_list(self.__entity_id)

        # Store entity position for undo
        if not self.__executed:
            self.__old_position = entity_info.position

        # Find item in backpack
        item = None

        for temp_item in entity_info.backpack:
            if self.__item_name.lower() == temp_item.name.lower():
                item = temp_item.name
                break

        # Ensure item is in backpack
        if item is None:
            raise ValueError("Item not found in backpack!")

        # Add item to tile
        self.__game_state.add_item_to_tile(
            self.__old_position[0],
            self.__old_position[1],
            item,
        )

        # Remove item from backpack
        self.__dropped_item = self.__game_state.remove_item_from_backpack_based_on_info(
            self.__entity_id, item
        )

        # Update inventory and entity stats
        self.__game_state.update_inventory_based_on_info(self.__entity_id)
        self.__game_state.update_entity(self.__entity_id)

        # Mark command as executed
        self.__executed = True

    # Undo
    # Returns the dropped item to the entity's backpack
    # Params: None
    # Returns: None
    def undo(self):
        if not self.__executed:
            raise ValueError("Item has not been dropped!")

        # Remove item from tile
        self.__game_state.remove_item_from_tile(
            self.__old_position[0],
            self.__old_position[1],
            self.__item_name,
        )

        # Return item to backpack
        self.__game_state.add_item_to_backpack_based_on_info(
            self.__entity_id, self.__item_name
        )

        # Update inventory and entity stats
        self.__game_state.update_inventory_based_on_info(self.__entity_id)
        self.__game_state.update_entity(self.__entity_id)

        # Mark command as no longer executed
        self.__executed = False

    # Redo
    # Drops the item again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__executed:
            raise ValueError("Item has already been dropped!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Swap Item Command extends from Command
class SwapItemCommand(Command):

    # Initialize Swap Item Command
    def __init__(self, game_state, entity_id, item_slot, item_name):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__item_slot = item_slot
        self.__item_name = item_name
        self.__name = "Swap"
        self.__old_item = None
        self.__executed = False

    # Execute
    # Swaps the equipped item with an item in the backpack
    # Params: None
    # Returns: None
    def execute(self):
        # Get entity info
        entity_info = self.__game_state.get_entity_info_from_list(self.__entity_id)

        # Find item in backpack
        item = None

        for temp_item in entity_info.backpack:
            if temp_item.name.lower() == self.__item_name.lower():
                item = temp_item
                break

        # Ensure item is in backpack
        if item is None:
            raise ValueError("Item not found in backpack!")

        # Get currently equipped item
        if not self.__executed:
            self.__old_item = self.__game_state.get_equipped_item_info(
                self.__entity_id, self.__item_slot
            )

        # Equip the selected item
        self.__game_state.equip_item_based_on_info(
            self.__entity_id, item.name, self.__item_slot
        )

        # Update entity stats
        self.__game_state.update_entity(self.__entity_id)

        # Mark command as executed
        self.__executed = True

    # Undo
    # Restores the previously equipped item
    # Params: None
    # Returns: None
    def undo(self):
        if not self.__executed:
            raise ValueError("Item has not been swapped!")

        # Restore previously equipped item
        self.__game_state.equip_item_based_on_info(
            self.__entity_id,
            self.__old_item.name,
            self.__item_slot,
        )

        # Update entity stats
        self.__game_state.update_entity(self.__entity_id)

        # Mark command as no longer executed
        self.__executed = False

    # Redo
    # Swaps the item again
    # Params: None
    # Returns: None
    def redo(self):
        if self.__executed:
            raise ValueError("Item has already been swapped!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets name of command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name


# Use Item Command extends from Command
class UseItemCommand(Command):
    # Initialize Use Item Command
    # Params:   game_state - GameState - Current game state
    #           entity_id - int - ID of entity using the item
    #           item_name - string - Name of consumable to use
    # Returns: None
    def __init__(self, game_state, entity_id, item_name):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__item_name = item_name
        self.__name = "Use"
        self.__old_state = None
        self.__executed = False

    # Execute
    # Uses the specified consumable
    # Params: None
    # Returns: None
    def execute(self):
        # Save original state before using the consumable
        if not self.__executed:
            self.__old_state = self.__game_state.create_memento()

        # Use consumable
        self.__game_state.use_consumable(self.__entity_id, self.__item_name)

        self.__executed = True

    # Undo
    # Restores the game state before the consumable was used
    # Params: None
    # Returns: None
    def undo(self):
        # Ensure command was executed
        if not self.__executed:
            raise ValueError("Item has not been used!")

        # Restore original state
        self.__game_state.restore_memento(self.__old_state)

        self.__executed = False

    # Redo
    # Uses the consumable again after undoing
    # Params: None
    # Returns: None
    def redo(self):
        # Ensure command was undone
        if self.__executed:
            raise ValueError("Item has already been used!")

        # Execute Command
        self.execute()

    # Get Name
    # Gets the command name
    # Params: None
    # Returns: string - Name of command
    def get_name(self):
        return self.__name


# Tick Command extends from Command
class TickCommand(Command):
    # Initialize Tick Command
    # Params:   game_state - GameState - Current game state
    # Returns: None
    def __init__(self, game_state):
        self.__game_state = game_state
        self.__name = "Tick"
        self.__old_state = None
        self.__executed = False

    # Execute
    # Advances the turn and updates all entity turn timers
    # Params: None
    # Returns: None
    def execute(self):
        # Save original state before ticking
        if not self.__executed:
            self.__old_state = self.__game_state.create_memento()

        # Update entity turn timers
        if self.__game_state.entities_exists():
            entities_to_remove = self.__game_state.process_tick_for_all_entities()

            # Remove entities that should leave the game
            if len(entities_to_remove) > 0:
                for entity_id in entities_to_remove:
                    self.__game_state.remove_entity_from_game(entity_id)

        # Mark game state as unsaved
        self.__game_state.mark_as_unsaved()

        # Advance turn
        self.__game_state.advance_turn()

        # Mark command as executed
        self.__executed = True

    # Undo
    # Restores the game state before the turn was advanced
    # Params: None
    # Returns: None
    def undo(self):
        # Ensure command was executed
        if not self.__executed:
            raise ValueError("Tick has not been executed!")

        # Restore original state
        self.__game_state.restore_memento(self.__old_state)

        # Mark command as undone
        self.__executed = False

    # Redo
    # Executes the tick again after undoing
    # Params: None
    # Returns: None
    def redo(self):
        # Ensure command was undone
        if self.__executed:
            raise ValueError("Tick has already been executed!")

        # Execute Command
        self.execute()

    # Get Name
    # Gets the command name
    # Params: None
    # Returns: string - Name of command
    def get_name(self):
        return self.__name


# Init Map Command extends Command
class InitCommand(Command):
    def __init__(self, game_state, width, height):
        self.__game_state = game_state
        self.__width = int(width)
        self.__height = int(height)
        self.__name = "Init Map"
        self.__old_state = None
        self.__executed = False

    # Execute
    # Creates a new map
    # Params: None
    # Returns: None
    def execute(self):
        # Save current state before initializing map
        if not self.__executed:
            self.__old_state = self.__game_state.create_memento()

        # Reset map if one already exists
        if self.__game_state.is_map_created():
            self.__game_state.reset_map()

        # Create new map
        self.__game_state.create_grid(self.__width, self.__height)

        # Mark command as executed
        self.__executed = True

    # Undo
    # Restores the game state before the map was initialized
    # Params: None
    # Returns: None
    def undo(self):
        # Command has not been executed
        if not self.__executed:
            raise ValueError("Map has not been initialized!")

        # Restore previous game state
        self.__game_state.restore_memento(self.__old_state)

        # Mark command as not executed
        self.__executed = False

    # Redo
    # Reinitializes the map
    # Params: None
    # Returns: None
    def redo(self):
        # Command has already been executed
        if self.__executed:
            raise ValueError("Map has already been initialized!")
        # Execute command again
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - string - Name of command
    def get_name(self):
        return self.__name


# Save Command extends Commad
class SaveCommand(Command):
    def __init__(self, game_state, game_state_manager, filename):
        self.__game_state = game_state
        self.__game_state_manager = game_state_manager
        self.__filename = filename
        self.__name = "Save"
        self.__executed = False

    # Execute
    # Saves the current game state to a file
    # Params: None
    # Returns: None
    def execute(self):
        # Save game state
        self.__game_state_manager.save_game(self.__game_state, self.__filename)

        # Mark command as executed
        self.__executed = True

    # Undo
    # Deletes the save file created by this command
    # Params: None
    # Returns: None
    def undo(self):
        # Command has not been executed
        if not self.__executed:
            raise ValueError("Game has not been saved!")

        # Delete save file
        self.__game_state_manager.delete_save(self.__filename)

        # Mark command as not executed
        self.__executed = False

    # Redo
    # Saves the game state again
    # Params: None
    # Returns: None
    def redo(self):
        # Command has already been executed
        if self.__executed:
            raise ValueError("Game has already been saved!")

        # Execute command again
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - string - Name of command
    def get_name(self):
        return self.__name


# Load Command extends Command
class LoadCommand(Command):
    def __init__(self, game_state, game_state_manager, filename):
        self.__game_state = game_state
        self.__game_state_manager = game_state_manager
        self.__filename = filename
        self.__name = "Load"
        self.__memento = None
        self.__executed = False

    # Execute Command
    # Loads the saved game state
    # Params: None
    # Returns: None
    def execute(self):
        # Save current game state before loading
        self.__memento = self.__game_state.create_memento()

        # Load saved game state
        self.__game_state_manager.load_game(self.__game_state, self.__filename)

        # Mark command as executed
        self.__executed = True

    # Undo Command
    # Restores game state from before loading
    # Params: None
    # Returns: None
    def undo(self):
        # Verify command was executed
        if not self.__executed:
            raise ValueError("Game has not been loaded!")

        # Restore previous game state
        self.__game_state.restore_memento(self.__memento)

        # Mark command as undone
        self.__executed = False

    # Redo Command
    # Loads the saved game state again
    # Params: None
    # Returns: None
    def redo(self):
        # Verify command was undone
        if self.__executed:
            raise ValueError("Game has already been loaded!")

        # Execute Command
        self.execute()

    # Get Name
    # Gets the command name
    # Params: None
    # Returns: string - command name
    def get_name(self):
        return self.__name


# Inspect Command extends from Command
class InspectCommand(Command):

    # Initialize Inspect Command
    def __init__(self, game_state, entity_id):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__name = "Inspect"

    # Execute
    # Displays information about the specified entity
    # Params: None
    # Returns: None
    def execute(self):
        entity_info = self.__game_state.get_entity_info_from_list(self.__entity_id)

        if entity_info is None:
            raise ValueError("Entity does not exist!")

        print(f"Id: {entity_info.id}")
        print(f"Type: {entity_info.e_type}")
        print(f"Position: {entity_info.position}")
        print(f"Health: {entity_info.health}/{entity_info.max_health}")
        print(f"Attack: {entity_info.attack}")
        print(f"Defence: {entity_info.defence}")
        print(f"Speed: {entity_info.speed}")
        print(f"Active Modifiers: {entity_info.active_modifiers}")

    # Undo
    # No action required because this command does not modify game state
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Re-executes the inspect command
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines whether the command should be added to undo history
    # Params: None
    # Returns: bool - False if command cant be undone
    def is_undoable(self):
        return False


# Inventory Command extends from Command
class InventoryCommand(Command):

    # Initialize Inventory Command
    def __init__(self, game_state, entity_id):
        self.__game_state = game_state
        self.__entity_id = int(entity_id)
        self.__name = "Inventory"

    # Execute
    # Displays the inventory of the specified entity
    # Params: None
    # Returns: None
    def execute(self):
        # Get entity information
        entity_info = self.__game_state.get_entity_info_from_list(self.__entity_id)

        # Get entity for is_alive check
        entity = self.__game_state.get_entity_from_list(self.__entity_id)

        # Check if entity exists
        if entity_info is None:
            raise ValueError("Player entity does not exist!")
        # Check if entity is alive
        elif not entity.is_alive():
            raise ValueError("Player entity is dead!")

        # Display equipped items
        print(f"Weapon: {entity_info.inventory[0]}")
        print(f"Armor: {entity_info.inventory[1]}")
        print(f"Accessory: {entity_info.inventory[2]}")

        # Display backpack slots
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

    # Undo
    # No action required because this command does not modify game state
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Re-executes the inventory command
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines whether the command should be added to undo history
    # Params: None
    # Returns: bool - False because inventory does not modify game state
    def is_undoable(self):
        return False


# Tile Command extends from Command
class TileCommand(Command):

    # Initialize Tile Command
    def __init__(self, game_state, x, y):
        self.__game_state = game_state
        self.__x = x
        self.__y = y
        self.__name = "Tile"

    # Execute
    # Displays information about the tile at the specified grid position
    # Params: None
    # Returns: None
    def execute(self):
        # Ensure map exists
        if not self.__game_state.is_map_created():
            raise ValueError("Map does not exist!")

        # Check if x and y are valid integers
        elif not are_valid_ints(self.__x, self.__y):
            raise ValueError("x and y are not valid integers!")

        # Check if x and y exceed grid bounds
        elif not self.__game_state.is_valid_grid_position(self.__x, self.__y):
            raise ValueError("x and y exceed current grid bounds!")

        # Display coordinates
        print(f"Coordinate: {self.__x}, {self.__y}")

        # Get tile information
        current_tile_info = self.__game_state.get_game_tile_info(
            int(self.__x), int(self.__y)
        )

        if current_tile_info is None:
            raise ValueError("No tile exists at this position!")

        # Display tile type
        # Special case with shallowwater for proper capitalization
        if current_tile_info.tile_type.lower() == "shallowwater":
            print("Type: ShallowWater")
        else:
            print(f"Type: {current_tile_info.tile_type.capitalize()}")

        # Display passable
        print(f"Passable: {current_tile_info.passable}")

        # Display occupants
        if len(current_tile_info.occupants) == 0:
            print("Occupants: None")
        else:
            print(f"Occupants: {current_tile_info.occupants[0]}")

    # Undo
    # No action required because this command does not modify game state
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Re-executes the tile command
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines whether the command should be added to undo history
    # Params: None
    # Returns: bool - False because this command does not modify game state
    def is_undoable(self):
        return False


# State Info Command extends from Command
class StateInfoCommand(Command):

    # Initialize State Info Command
    def __init__(self, game_state):
        self.__game_state = game_state
        self.__name = "State-Info"

    # Execute
    # Displays information about the current game state
    # Params: None
    # Returns: None
    def execute(self):
        # Check that game state exists and is active
        if not self.__game_state.game_state_is_active():
            raise ValueError(" Game State is not initialized!")

        else:
            # Get game state information
            try:
                game_state_info = self.__game_state.get_game_state_info()

                print(
                    f"ok: turn {game_state_info[0]}, entities: {game_state_info[1]}, saved: {str(game_state_info[2]).lower()}"
                )

            # Extensive error checking
            except (AttributeError, TypeError, ValueError) as error:
                raise error

    # Undo
    # No action required because this command does not modify game state
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Re-executes the state-info command
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Gets the name of the command
    # Params: None
    # Returns: name - String - command name
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines whether the command should be added to undo history
    # Params: None
    # Returns: bool - False because this command does not modify game state
    def is_undoable(self):
        return False


# History Command extends from Command
# Displays the number of commands in the undo and redo histories
class HistoryCommand(Command):

    # Initialize History Command
    # Params: command_manager - CommandManager - Command manager instance
    # Returns: None
    def __init__(self, command_manager):
        self.__command_manager = command_manager
        self.__name = "History"

    # Execute
    # Displays the undo and redo history counts
    # Params: None
    # Returns: None
    def execute(self):
        history_info = self.__command_manager.get_history_info()

        print(f"ok: undo_stack:{history_info[0]}, redo_stack:{history_info[1]}")

    # Undo
    # History is not an undoable command
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Re-displays the history information
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Returns name of command
    # Params: None
    # Returns: command name - String
    def get_name(self):
        return self.__name

    # Is Undoable
    # History is not an undoable command
    # Params: None
    # Returns: False
    def is_undoable(self):
        return False


# Undo Command extends from Command
# Reverses the last successfully executed command
class UndoCommand(Command):

    # Initialize Undo Command
    # Params: command_manager - CommandManager - Command manager instance
    # Returns: None
    def __init__(self, command_manager):
        self.__command_manager = command_manager
        self.__name = "Undo"

    # Execute
    # Reverses the last command in the undo history
    # Params: None
    # Returns: None
    def execute(self):
        is_undone, command_undone = self.__command_manager.undo_last_command()

        if is_undone:
            name = command_undone.get_name()
            print(f"ok: undone {name}!")
        else:
            print("error: undo_failed - No commands to undo!")

    # Undo
    # Undo commands cannot themselves be undone
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Repeats the undo operation
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Returns name of command
    # Params: None
    # Returns: command name - String
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines if it will be added to history
    # Params: None
    # Returns: False
    def is_undoable(self):
        return False


# Redo Command extends from Command
# Re-executes the most recently undone command
class RedoCommand(Command):

    # Initialize Redo Command
    # Params: command_manager - CommandManager - Command manager instance
    # Returns: None
    def __init__(self, command_manager):
        self.__command_manager = command_manager
        self.__name = "Redo"

    # Execute
    # Re-executes the last command in the redo history
    # Params: None
    # Returns: None
    def execute(self):
        is_redone, command_redone = self.__command_manager.redo_last_command()

        if is_redone:
            name = command_redone.get_name()
            print(f"ok: redone {name}!")
        else:
            print("error: redo_failed - No commands to redo!")

    # Undo
    # Redo commands cannot themselves be undone
    # Params: None
    # Returns: None
    def undo(self):
        pass

    # Redo
    # Repeats the redo operation
    # Params: None
    # Returns: None
    def redo(self):
        self.execute()

    # Get Name
    # Returns name of command
    # Params: None
    # Returns: command name - String
    def get_name(self):
        return self.__name

    # Is Undoable
    # Determines if it will be added to history
    # Params: None
    # Returns: False
    def is_undoable(self):
        return False
