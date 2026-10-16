"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 12, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: game_state.py
Purpose: Record game state stats.
"""

# Imports
from grid import Grid
from equipment import Consumable
from spell import Spell, get_spell
import domain_library as dl


# GamesState Class to handle game state stats
class GameState:

    # Init with necessary variables
    def __init__(self):
        self.__grid = None
        self.__entity_list = []  # List of real entity objects, not copies
        self.__entity_ids_issued = 1
        self.__map_created = False
        self.__turn_number = 1
        self.__is_saved = True

    # Is Map Created
    # True/False if map is created
    # Params: None
    # Returns Bool - True if map created
    def is_map_created(self):
        return self.__map_created

    # Reset Entity List Start
    # resets entity list back to empty to prevent errors with testing
    # Params: None
    # Return: None
    def reset_entity_list(self):
        self.__entity_list = []

    # Reset ID Issuer Tracker Start
    # resets entity id issues number back to 1 to prevent errors with testing
    # Params: None
    # Return: None
    def reset_id_issuer_tracker(self):
        self.__entity_ids_issued = 1

    # Reset Turn Number Start
    # resets turn back to 1 to prevent errors with testing
    # Params: None
    # Return: None
    def reset_turn_number(self):
        self.__turn_number = 1

    # Advance Turn Start
    # Advances turn by one
    # Params: None
    # Return: None
    def advance_turn(self):
        self.__turn_number += 1
        print(f"ok: advanced to turn {self.__turn_number}!")

    # Mark As Unsaved Start
    # Sets is saved to False
    # Params: None
    # Return: None
    def mark_as_unsaved(self):
        self.__is_saved = False

    # Mark As Saved Start
    # Sets is saved to True
    # Params: None
    # Return: None
    def mark_as_saved(self):
        self.__is_saved = True

    # Mark Map Created
    # Marks map created as True
    # Params: None
    # Returns: None
    def mark_map_created(self):
        self.__map_created = True

    # Create grid
    # Creates grid for the game state
    # Params: width/height - ints - grid bounds
    # Returns: None
    def create_grid(self, width, height):
        # params checked before calling of emthod
        # Assign/Create grid
        self.__grid = Grid(width, height)
        # reset entity id counter
        self.__entity_ids_issued = 1
        # Set map created to True
        self.mark_map_created()

    # Reset Map
    # Resets map and all associated variables
    # Params: None
    # Returns: None
    def reset_map(self):
        # Reset Grid
        self.__grid = None
        # reset entity id counter
        self.__entity_ids_issued = 1
        # reset map created
        self.__map_created = False
        # Reset entity list
        self.__entity_list = []

    # Set Game Grid Tile
    # Sets tile in active game grid
    # Params:   x/y - ints - tile position
    #           tile_type - string - Type of tile to set
    # Returns: None
    def set_game_grid_tile(self, x, y, tile_type):
        self.__grid.set_tile(int(x), int(y), tile_type)

    # Is Grid Tile Occupied
    # Returns t/f if tile is occupied
    # Params: x/y - ints - tile position
    # Returns: bool - if tile is occupied > True
    def is_grid_tile_occupied(self, x, y):
        return self.__grid.is_occupied(int(x), int(y))

    # Is Tile Passable
    # Returns t/f is tile is passable
    # Params: x/y - ints - tile position
    # Returns: Bool - True if tile is passable, else False
    def is_tile_passable(self, x, y):
        return self.__grid.is_passable(int(x), int(y))

    # Get Game Tile Info
    # Returns tile in game grid
    # Params: x,y - ints - tile position
    # Returns: TileInfo - all info about the current tile
    def get_game_tile_info(self, x, y):
        return self.__grid.get_tile_info(int(x), int(y))

    # Is Within Range
    # Returns bool if tile is within range
    # Params:   start_x/start_y - ints - starting tile position
    #           target_x/target_y - ints - target tile position
    #           Range - int - range from tile
    # Returns:  Bool - True if within range, else False
    def is_within_range(self, start_x, start_y, target_x, target_y, range):
        return self.__grid.is_within_range(
            [start_x, start_y], [target_x, target_y], range
        )

    # Get entity id from tile
    # Gets the entity id from the tile
    # Params: x/y - ints - tile position
    # Returns: id - int - entity id
    def get_entity_id_from_tile(self, x, y):
        # Get tile info
        tile_info = self.__grid.get_tile_info(int(x), int(y))
        return tile_info.occupants[0]

    # REDO UPON RESTRUCTURE OF ENTITY - HERE
    # Get entity from list
    # Gets real entity from entity list
    # Params: id - int - entity ID
    # Returns: entity if it exists - immutable copy of entity, else None
    def get_entity_from_list(self, id):
        for entity in self.__entity_list:
            # Get entity info
            entity_info = entity.get_info()
            # temp_entity = entity
            if int(entity_info.id) == int(id):
                return entity
        return None

    # Get entity info from list
    # Gets entity info from entity list
    # Params: id - int - entity ID
    # Returns: entity info if it exists - immutable copy of entity, else None
    def get_entity_info_from_list(self, id):
        for entity in self.__entity_list:
            # Get entity info
            entity_info = entity.get_info()
            try:
                if int(entity_info.id) == int(id):
                    return entity_info
            except:
                return None

    # Process Tick For All Entities
    # Processes tick for all currnet entities
    # Params: None
    # Returns: List - entities ids to remove
    def process_tick_for_all_entities(self):
        entities_to_remove = []
        for entity in self.__entity_list:
            temp_bool = entity.process_tick_on_entity()
            # Check for removal of entity
            if temp_bool:
                entity_id = (entity.get_info()).id
                # Remove if true
                entities_to_remove.append(entity_id)
        return entities_to_remove

    # Remove Entity From Game
    # Removes given entity from the game
    # Params: entity_id - Entity.id - id of entity to remove
    # Returns: None
    def remove_entity_from_game(self, entity_id):
        # Get entity info
        entity_info = self.get_entity_info_from_list(entity_id)
        # Get grid position of entity
        entity_x = entity_info.position[0]
        entity_y = entity_info.position[1]
        # Clear tile
        self.__grid.clear_occupant(entity_x, entity_y, entity_info.id)
        # Remove
        for temp_entity in self.__entity_list:
            temp_entity_info = temp_entity.get_info()
            if temp_entity_info.id == entity_info.id:
                self.__entity_list.remove(temp_entity)
                break

    # Update Entity
    # Updates the matching entity
    # Params: id - int - entity ID
    # Returns: None
    def update_entity(self, id):
        entity = self.get_entity_from_list(id)
        if entity == None:
            pass
        else:
            entity.update_stats(self)

    """    # Update Entity From Info
    # Updates the matching entity from entity info
    # Params: entity_info - EntityInfo - entity info to update entity with
    # Returns: None
    def update_entity_from_info(self, entity_info):
        self.update_entity(entity_info.id)"""

    # Is Valid Grid Position
    # Returns t/f is grid positon is valid
    # Params: x/y - ints - grid position
    # Returns: Bool - t/f - true if position is valid
    def is_valid_grid_position(self, x, y):
        # Get grid info
        grid_info = self.__grid.get_info()
        return Grid.is_valid_grid_position(grid_info, int(x), int(y))

    # Spawn Entity
    # Spawns entity for game grid
    # Params:   x/y - ints - positions on grid
    #           entity_type - String - type of entity to spawn
    # Returns: None
    def spawn_entity(self, x, y, entity_type):
        # Spawned entity should be a immutable copy of the entity spawned, so that it can be updated without affecting the original entity
        spawned_entity = self.__grid.spawn_entity(
            int(x), int(y), entity_type, self.__entity_ids_issued
        )
        # Increment entity_ids_issued to account for new entity
        self.__entity_ids_issued += 1
        # Add to list
        self.__entity_list.append(
            spawned_entity
        )  # append real entity object to list, not copy
        # Update Entity
        self.update_entity(self.__entity_ids_issued - 1)

    # Spawn Loot
    # Spawns loot on game grid
    # Params:   x/y - ints - grid position
    #           Item_name - string - name of item to spawn
    # Returns: None
    def spawn_loot(self, x, y, item_name):
        self.__grid.add_item_to_tile_item_list(int(x), int(y), item_name)

    # Entities Exist
    # Returns t/f if entities exist
    # Params: None
    # Return: Bool - True if entites exist else False
    def entities_exists(self):
        if len(self.__entity_list) > 0:
            return True
        else:
            return False

    # Remove Item From Tile
    # Removes item from tiles item list
    # Params:   x/y - ints - tile position
    #           item_name - Item - name of item to remove
    # Returns: item removed from tile
    def remove_item_from_tile(self, x, y, item_name):
        return self.__grid.remove_item_from_tile_item_list(int(x), int(y), item_name)

    # Add Item From Tile
    # Adds item from tiles item list
    # Params:   x/y - ints - tile position
    #           item_name - Item - name of item to add
    # Returns: None
    def add_item_to_tile(self, x, y, item_name):

        self.__grid.add_item_to_tile_item_list(int(x), int(y), item_name)

    # Add Item From Backpack From Info
    # Adds provided item to the backpack based on entity info
    # Params: entity_id - int - id of entity whose backpack to add item to
    #           item_name - str - name of item to add to backpack
    # Returns: None
    def add_item_to_backpack_based_on_info(self, entity_id, item_name):
        entity = self.get_entity_from_list(entity_id)
        # get Item from item name
        item = dl.create_equipment(item_name.lower())
        entity.add_item_to_backpack(item)

    # Remove Item From Backpack From Info
    # Removes provided item from the backpack based on entity info
    # Params: entity_id - int - id of entity whose backpack to remove item from
    #           item - Item - item to remove from backpack
    # Returns: None
    def remove_item_from_backpack_based_on_info(self, entity_id, item_name):
        entity = self.get_entity_from_list(entity_id)
        entity.remove_item_from_backpack(item_name)

    # Update Inventory Based on Info
    # Updates the inventory based on entity info
    # Params: entity_id - int - id of entity whose inventory to update
    # Returns: None
    def update_inventory_based_on_info(self, entity_id):
        entity = self.get_entity_from_list(entity_id)
        entity.update_inventory()

    # Equip Item Based on Info
    # Equips provided item based on entity info
    # Params: entity_id - int - id of entity whose inventory to update
    #           item_name - str - name of item to equip
    #           slot - str - slot to equip item in
    # Returns: None
    def equip_item_based_on_info(self, entity_id, item_name, slot):
        entity = self.get_entity_from_list(entity_id)
        # get Item from item name
        item = dl.create_equipment(item_name.lower())
        entity.equip_item(item, slot)
        # Update entity stats
        self.update_entity(entity_id)

    # Use Consumable
    # Uses provided consumable based on entity info
    # Params: entity_id - int - id of entity whose inventory to update
    #           item_name - str - name of item to use
    # Returns: None
    def use_consumable(self, entity_id, item_name):
        entity = self.get_entity_from_list(entity_id)
        # get Item from item name
        item = dl.create_equipment(item_name.lower())
        Consumable.use_consumable(item, entity, self)
        # Remove item from backpack
        entity.remove_item_from_backpack(item_name)

    # Move Entity
    # Moves entity to x, y
    # Params:   entity_id - Entity.id - id of entity to move
    #           x,y - ints - target tile position
    # Returns: None
    def move_entity(self, entity_id, x, y):
        # Needs entity object and read only object
        entity = self.get_entity_from_list(entity_id)
        entity_info = entity.get_info()
        self.__grid.occupy(x, y, entity_info.id)
        self.__grid.clear_occupant(
            entity_info.position[0], entity_info.position[1], entity_info.id
        )
        entity.move_to(x, y)
        # Update entity stats after move
        entity.update_stats(self)

    # Attack Entity
    # Attacks entity with another entity
    # Params:   attacker_id - Entity.id - id of entity to attack with
    #           defender_id - Entity.id - id of entity to attack
    # Returns: None
    def attack_entity(self, attacker_id, defender_id):
        # Needs entity object
        attacker = self.get_entity_from_list(attacker_id)
        defender = self.get_entity_from_list(defender_id)
        # Attack
        damage = attacker.attack_entity(defender)
        return damage

    # Cast Spell
    # Casts spell from entity to another entity
    # Params:   caster_id - Entity.id - id of entity to cast spell with
    #           target_id - Entity.id - id of entity to cast spell on
    #          spell_name - String - name of spell to cast
    # Returns: None
    def cast_spell(self, caster_id, target_id, spell_name):
        # Needs entity object
        caster = self.get_entity_from_list(caster_id)
        target = self.get_entity_from_list(target_id)
        # Get Spell Object
        spell = get_spell(spell_name.lower())
        # Cast Spell
        effect = spell.cast_spell(caster, target, self)
        return effect

    # Update Single Entity Stat
    # Updates single entity stat based on entity info
    # Params:   entity_id - Entity.id - id of entity to update
    #           stat - String - stat to update
    #           value - int - value to update stat to
    # Returns: None
    def update_single_entity_stat(self, entity_id, stat, value):
        entity = self.get_entity_from_list(entity_id)
        entity.update_single_stat(stat, value)

    # Add Temp Buff To Entity
    # Adds temp buff to entity based on entity info
    # Params:   entity_id - Entity.id - id of entity to add buff to
    #           buff - dict - includes all buff attributes (name, effects, duration)
    # Returns: None
    def add_temp_buff_to_entity(self, entity_id, buff):
        entity = self.get_entity_from_list(entity_id)
        entity.add_temp_buff(buff)

    # Get Spell Info
    # Gets spellinfo from spell name
    # Params:   spell_name - string - name of spell\
    # Returns:  SpellInfo - All needed spell info
    def get_spell_info(self, spell_name):
        spell = get_spell(spell_name)
        return spell.get_info()

    # Create Momento
    # Creates momento of the game state
    # Params: None
    # Returns: Momento of the game state
    def create_momento():
        pass

    # Restore Momento
    # Restores momento of the game state
    # Params: momento - Momento - Contains all info for the game state to be restored
    # Returns: None
    def restore(momento):
        pass
