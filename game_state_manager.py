"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: October 12, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: game_state_manager.py
Purpose: Handles momento/save handling and validation.
"""

# Imports
import copy
import json
import os
import tempfile
from game_state import GameState
from grid import Tile, Grid
from entity import Entity, Mage
from domain_library import AttackTypes
import equipment


# Game State Manager Class
class GameStateManager:

    # Initialize the GameStateManager
    def __init__(self):
        self.__save_directory = "save_files"
        os.makedirs(self.__save_directory, exist_ok=True)

    # Create Filepath
    # Creates and returns filepath based on filename given
    # Params: filename - string - name of file in path
    # Returns: filepath - string - path to given file
    def create_filepath(self, filename):
        # Add json extension if needed
        if not filename.endswith(".json"):
            # Add it
            filename += ".json"
        # Create and return full file path
        return os.path.join(self.__save_directory, filename)

    # Save Game
    # Save the current game state to a file
    # Params:   game state - Game State - Current game state to save
    #           filename - string - file name to save to
    # Returns:  None
    def save_game(self, game_state, filename):
        # Create a snapshot of the current game
        memento = game_state.create_memento()

        for entity_memento in memento.entity_mementos:
            if hasattr(entity_memento, "entity_memento"):
                entity_memento = entity_memento.entity_memento

            print(
                f"Saving entity {entity_memento.entity_id}: "
                f"health={entity_memento.health}"
            )

        # Convert the Memento into JSON-compatible data
        save_data = self.memento_to_data(memento)

        # Validate the data before saving
        self.validate_save_data(save_data)

        # Create file path
        file_path = self.create_filepath(filename)

        # Write the save data to the file
        self.write_save_file(save_data, file_path)

    # Load Game
    # Load the current game state from a file and restore
    # Params:   game state - Game State - Current game state to load into
    #           filename - string - file name to load from
    # Returns:  None
    def load_game(self, game_state, filename):
        # Get file path to given file name
        file_path = self.create_filepath(filename)

        # Read the save file
        save_data = self.read_save_file(file_path)

        # Validate the saved data
        self.validate_save_data(save_data)

        # Reconstruct a Memento from the saved data
        memento = self.data_to_memento(save_data)

        # Restore the game from the reconstructed Memento
        game_state.restore(memento)

    # Validate Save Data
    # Validate the saved from the file
    # Params:   save_data - dict - Current saved data
    # Returns:  None
    def validate_save_data(self, save_data):
        # More validation will be added here
        if not isinstance(save_data, dict):
            raise ValueError("Save data must be a dictionary.")

    # Write Save File
    # Writes save data to a JSON file
    # Params:   save_data - dict - Saved game data
    #           file_path - string - file path to save file to
    # Returns: None
    def write_save_file(self, save_data, file_path):
        # Create the destination directory if needed
        directory = os.path.dirname(os.path.abspath(file_path))
        os.makedirs(directory, exist_ok=True)

        temp_path = None

        try:
            # Write to a temporary file first
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=directory,
                delete=False,
            ) as save_file:
                temp_path = save_file.name

                json.dump(
                    save_data,
                    save_file,
                    indent=4,
                )

            # Replace the destination after writing succeeds
            os.replace(temp_path, file_path)

        finally:
            # Clean up a temporary file if writing failed
            if temp_path is not None and os.path.exists(temp_path):
                os.remove(temp_path)

    # Read Save File
    # Read save data from a JSON file
    # Params: file_path - string - file path to get save data from
    # Returns: None
    def read_save_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as save_file:
                return json.load(save_file)

        except FileNotFoundError:
            raise FileNotFoundError(f"Save file not found: {file_path}") from None

        except json.JSONDecodeError:
            raise ValueError("Save file contains invalid JSON.") from None

    # Momento to Data
    # Convert a Memento into JSON-compatible data
    # Params: memento - Momento - Memento to write into JSON data
    # Returns: None
    def memento_to_data(self, memento):
        # Convert a GameState Memento into JSON-compatible data.

        grid_memento = memento.grid_memento

        grid_data = None

        if grid_memento is not None:
            tiles_data = []

            # Grid stores columns first, then rows.
            for column in grid_memento.tiles:
                column_data = []

                for tile_memento in column:
                    tile_data = {
                        "tile_type": tile_memento.t_type,
                        "passable": tile_memento.passable,
                        "occupants": list(tile_memento.occupants),
                        "modifiers": copy.deepcopy(tile_memento.modifiers),
                        "items": [],
                    }

                    # Store equipment by its name, not as an object.
                    for item in tile_memento.item_list:
                        if item is None:
                            column_data_item = None
                        elif isinstance(item, str):
                            column_data_item = item
                        else:
                            item_info = item.get_info()
                            column_data_item = item_info.name
                        tile_data["items"].append(column_data_item)

                    column_data.append(tile_data)

                tiles_data.append(column_data)

            grid_data = {
                "width": grid_memento.width,
                "height": grid_memento.height,
                "tiles": tiles_data,
            }

        entities_data = []

        for entity_memento in memento.entity_mementos:
            # Mage's Memento wraps its Entity Memento.
            base_memento = entity_memento

            if hasattr(entity_memento, "entity_memento"):
                base_memento = entity_memento.entity_memento

            entity_data = {
                "id": base_memento.entity_id,
                "type": base_memento.e_type,
                "position": list(base_memento.position),
                "health": base_memento.health,
                "max_health": base_memento.max_health,
                "attack": base_memento.attack,
                "defence": base_memento.defence,
                "speed": base_memento.speed,
                "inventory": {},
                "active_modifiers": copy.deepcopy(base_memento.active_modifiers),
                "backpack": [],
                "attack_type": (
                    base_memento.attack_type.value
                    if isinstance(base_memento.attack_type, AttackTypes)
                    else base_memento.attack_type
                ),
                "temp_buffs": copy.deepcopy(base_memento.temp_buffs),
            }

            # Counts
            inv_count = 0
            # back_count = 0

            # Convert equipped items to names.
            for item in base_memento.inventory:
                # Set slot based on count
                match inv_count:
                    case 0:
                        slot = "Weapon"
                    case 1:
                        slot = "Armor"
                    case 2:
                        slot = "Accessory"
                # Increase count after assignment
                inv_count += 1
                # Assign accordingly
                if item is None:
                    entity_data["inventory"][slot] = None
                elif isinstance(item, str):
                    entity_data["inventory"][slot] = item
                else:
                    entity_data["inventory"][slot] = item.get_info().name

            # Convert backpack items to names.
            for item in base_memento.backpack:
                if item is None:
                    entity_data["backpack"].append(None)
                elif isinstance(item, str):
                    entity_data["backpack"].append(item)
                else:
                    entity_data["backpack"].append(item.get_info().name)

            # Save Mage-specific fields.
            if hasattr(entity_memento, "mana"):
                entity_data["mana"] = entity_memento.mana
                entity_data["max_mana"] = entity_memento.max_mana
                entity_data["spell_power"] = entity_memento.spell_power

            entities_data.append(entity_data)

        save_data = {
            "game_state": {
                "turn_number": memento.turn_number,
                "entity_ids_issued": memento.entity_ids_issued,
                "map_created": memento.map_created,
            },
            "grid": grid_data,
            "entities": entities_data,
        }

        return save_data

    # Data to Memento
    # Create a Memento from saved JSON data
    # Params: save_data - dict - Contains all data to save to a file
    # Returns: None
    def data_to_memento(self, save_data):
        game_data = save_data["game_state"]
        grid_data = save_data["grid"]

        grid_memento = None

        if grid_data is not None:
            tile_columns = []

            for column_data in grid_data["tiles"]:
                tile_column = []

                for tile_data in column_data:
                    tile_memento = Tile.Memento(
                        t_type=tile_data["tile_type"],
                        passable=tile_data["passable"],
                        occupants=tuple(tile_data["occupants"]),
                        modifiers=copy.deepcopy(tile_data["modifiers"]),
                        item_list=tuple(tile_data["items"]),
                    )

                    tile_column.append(tile_memento)

                tile_columns.append(tuple(tile_column))

            grid_memento = Grid.Memento(
                width=grid_data["width"],
                height=grid_data["height"],
                tiles=tuple(tile_columns),
            )

        entity_mementos = []

        for entity_data in save_data["entities"]:
            entity_type = entity_data["type"].lower()

            # Reconstruct equipped items as equipment objects.
            inventory_items = []

            for slot, default_item in [
                ("Weapon", "none_wep"),
                ("Armor", "none_armor"),
                ("Accessory", "none_acc"),
            ]:
                item_name = entity_data["inventory"].get(slot)

                # Empty slots may have been saved as None or "None".
                if item_name is None or (
                    isinstance(item_name, str) and item_name.lower() == "none"
                ):
                    item_name = default_item

                # Reconstruct the equipment object.
                item = equipment.create_equipment(item_name)

                # Fail here with a useful message instead of crashing later.
                if item is None:
                    raise ValueError(
                        f"Could not reconstruct {slot} item {item_name!r} "
                        f"for entity {entity_data['id']}. "
                        "Check the saved equipment name and factory key."
                    )

                inventory_items.append(item)

            # Reconstruct the base Entity Memento.
            entity_memento = Entity.Memento(
                entity_id=entity_data["id"],
                e_type=entity_data["type"],
                position=tuple(entity_data["position"]),
                health=entity_data["health"],
                max_health=entity_data["max_health"],
                attack=entity_data["attack"],
                defence=entity_data["defence"],
                speed=entity_data["speed"],
                inventory=tuple(inventory_items),
                active_modifiers=copy.deepcopy(entity_data["active_modifiers"]),
                backpack=tuple(entity_data["backpack"]),
                attack_type=AttackTypes(entity_data["attack_type"]),
                temp_buffs=copy.deepcopy(entity_data["temp_buffs"]),
            )

            # Mage's Memento contains its base Entity Memento.
            if entity_type == "mage":
                entity_memento = Mage.Memento(
                    entity_memento=entity_memento,
                    mana=entity_data["mana"],
                    max_mana=entity_data["max_mana"],
                    spell_power=entity_data["spell_power"],
                )

            entity_mementos.append(entity_memento)

        return GameState.Memento(
            grid_memento=grid_memento,
            entity_mementos=tuple(entity_mementos),
            entity_ids_issued=game_data["entity_ids_issued"],
            map_created=game_data["map_created"],
            turn_number=game_data["turn_number"],
            is_saved=True,
        )
