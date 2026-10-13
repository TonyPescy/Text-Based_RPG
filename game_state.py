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


# GamesState Class to handle game state stats
class GameState:

    # Init with necessary variables
    def __init__(self):
        self.__grid = None
        self.__entity_list = []
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

    # Get Game Tile
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
        self.__grid.is_within_range([start_x, start_y], [target_x, target_y], range)

    # Get entity id from tile
    # GEts the entity id from the tile
    # Params: x/y - ints - tile position
    # Returns: id - int - entity id
    def get_entity_id_from_tile(self, x, y):
        return self.__grid.grid[int(x)][int(y)].occupants[0].id

    # Get entity from list
    # Gets entity from entity list
    # Params: id - int - entity ID
    # Returns: entity if it exists
    def get_entity_from_list(self, id):
        for entity in self.__entity_list:
            if int(entity.id) == int(id):
                return entity
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
                # Remove if true
                entities_to_remove.append(entity.id)
        return entities_to_remove

    # Remove Entity From Game
    # Removes given entity from the game
    # Params: entity_id - Entity.id - id of entity to remove
    # Returns: None
    def remove_entity_from_game(self, entity_id):
        # Get entity
        entity = self.get_entity_from_list(entity_id)
        # Get grid position of entity
        entity_x = entity.position[0]
        entity_y = entity.position[1]
        # Clear tile
        self.__grid.clear_occupant(entity_x, entity_y, entity.id)
        # Remove
        self.__entity_list.remove(entity)

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

    # Is Valid Grid Position
    # Returns t/f is grid positon is valid
    # Params: x/y - ints - grid position
    # Returns: Bool - t/f - true if position is valid
    def is_valid_grid_position(self, x, y):
        return Grid.is_valid_grid_position(self.__grid, int(x), int(y))

    # Spawn Entity
    # Spawns entity for game grid
    # Params:   x/y - ints - positions on grid
    #           entity_type - String - type of entity to spawn
    # Returns: None
    def spawn_entity(self, x, y, entity_type):
        spawned_entity = self.__grid.spawn_entity(
            int(x), int(y), entity_type, self.__entity_ids_issued
        )
        # Increment entity_ids_issued to account for new entity
        self.__entity_ids_issued += 1
        # Add to list
        self.__entity_list.append(spawned_entity)
        # Stat adjustmesnt based on classes and more
        if (
            spawned_entity.e_type.lower() == "mage"
        ):  # spanws in with full health and mana
            spawned_entity.max_health = spawned_entity.health
            spawned_entity.max_mana = spawned_entity.mana
        else:  # Not a mage - spawns with max/full hp
            spawned_entity.max_health = spawned_entity.health
        # Add temp buffs for entity
        spawned_entity.temp_buffs = []
        # Update Entity
        self.update_entity(spawned_entity.id)

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
    def add_item_from_tile(self, x, y, item_name):
        self.__grid.add_item_to_tile_item_list(int(x), int(y), item_name)

    # Move Entity
    # Moves entity to x, y
    # Params: x,y - ints - target tile position
    # Returns: None
    def move_entity(self, entity, x, y):
        self.__grid.occupy(x, y, entity.id)
        self.__grid.clear_occupant(entity.position[0], entity.position[1], entity.id)
        entity.position = [x, y]

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
