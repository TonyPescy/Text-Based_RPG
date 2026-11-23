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
from enum import Enum
from command import Command
from command_manager import CommandManager
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
    #           command_manager
    # Returns:  None
    def save_game(self, game_state, filename, command_manager):
        # Create a snapshot of the current game
        memento = game_state.create_memento(command_manager)

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
    #           command_manager
    # Returns:  None
    def load_game(self, game_state, filename, command_manager):
        # Get file path to given file name
        file_path = self.create_filepath(filename)

        # Read the save file
        save_data = self.read_save_file(file_path)

        # Validate the saved data
        self.validate_save_data(save_data)

        # Reconstruct a Memento from the saved data
        memento = self.data_to_memento(save_data)

        # Restore the game from the reconstructed Memento
        game_state.restore(memento, command_manager, self)

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
        grid_memento = memento.grid_memento
        grid_data = None

        # Convert grid Memento
        if grid_memento is not None:
            tiles_data = []

            # Grid stores columns first, then rows
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

                    # Convert tile item mementos
                    for item_memento in tile_memento.item_list:
                        tile_data["items"].append(
                            self.equipment_memento_to_data(item_memento)
                        )

                    column_data.append(tile_data)

                tiles_data.append(column_data)

            grid_data = {
                "width": grid_memento.width,
                "height": grid_memento.height,
                "tiles": tiles_data,
            }

        # Convert entity Mementos
        entities_data = []

        for entity_memento in memento.entity_mementos:
            # Mage's Memento wraps its Entity Memento
            base_memento = entity_memento

            if hasattr(entity_memento, "entity_memento"):
                base_memento = entity_memento.entity_memento

            entity_data = {
                "id": base_memento.entity_id,
                "type": base_memento.e_type,
                "position": list(base_memento.position.data),
                "health": base_memento.health,
                "max_health": base_memento.max_health,
                "attack": base_memento.attack,
                "defence": base_memento.defence,
                "speed": base_memento.speed,
                "inventory": {},
                "active_modifiers": copy.deepcopy(base_memento.active_modifiers.data),
                "backpack": [],
                "attack_type": (
                    base_memento.attack_type.value
                    if isinstance(base_memento.attack_type, AttackTypes)
                    else base_memento.attack_type
                ),
                "temp_buffs": copy.deepcopy(base_memento.temp_buffs.data),
                "state_manager": {"state_name": base_memento.state_manager.state_name},
            }

            # Convert equipped inventory mementos
            slots = ["Weapon", "Armor", "Accessory"]

            for slot, item_memento in zip(slots, base_memento.inventory.data):
                entity_data["inventory"][slot] = self.equipment_memento_to_data(
                    item_memento
                )

            # Convert backpack item mementos
            for item_memento in base_memento.backpack.items:
                entity_data["backpack"].append(
                    self.equipment_memento_to_data(item_memento)
                )

            # Save Mage-specific fields
            if hasattr(entity_memento, "mana"):
                entity_data["mana"] = entity_memento.mana
                entity_data["max_mana"] = entity_memento.max_mana
                entity_data["spell_power"] = entity_memento.spell_power

            entities_data.append(entity_data)

        # Construct complete save data
        save_data = {
            "game_state": {
                "turn_number": memento.turn_number,
                "entity_ids_issued": memento.entity_ids_issued,
                "map_created": memento.map_created,
            },
            "command_manager": self.command_manager_memento_to_data(
                memento.command_manager_memento
            ),
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
        command_manager_data = save_data.get("command_manager")
        grid_memento = None

        if grid_data is not None:
            tile_columns = []

            for column_data in grid_data["tiles"]:
                tile_column = []

                for tile_data in column_data:
                    # Reconstruct tile item mementos
                    tile_items = []

                    for item_data in tile_data["items"]:
                        tile_items.append(self.data_to_equipment_memento(item_data))

                    # Reconstruct Tile Memento
                    tile_memento = Tile.Memento(
                        t_type=tile_data["tile_type"],
                        passable=tile_data["passable"],
                        occupants=tuple(tile_data["occupants"]),
                        modifiers=copy.deepcopy(tile_data["modifiers"]),
                        item_list=tuple(tile_items),
                    )

                    # Add tile memento to column
                    tile_column.append(tile_memento)

                # Add completed column
                tile_columns.append(tuple(tile_column))

            # Reconstruct Grid Memento
            grid_memento = Grid.Memento(
                width=grid_data["width"],
                height=grid_data["height"],
                tiles=tuple(tile_columns),
            )

        entity_mementos = []

        for entity_data in save_data["entities"]:
            entity_type = entity_data["type"].lower()

            # Reconstruct equipped inventory mementos
            inventory_items = []

            for slot in ["Weapon", "Armor", "Accessory"]:
                item_data = entity_data["inventory"].get(slot)

                # Reconstruct item memento
                item_memento = self.data_to_equipment_memento(item_data)

                inventory_items.append(item_memento)

            # Reconstruct backpack item mementos
            backpack_items = []

            for item_data in entity_data["backpack"]:
                item_memento = self.data_to_equipment_memento(item_data)

                backpack_items.append(item_memento)

            state_manager_data = entity_data.get("state_manager") or {}

            # Reconstruct the base Entity Memento.
            entity_memento = Entity.Memento(
                entity_id=entity_data["id"],
                e_type=entity_data["type"],
                position=Entity.PositionMemento(data=tuple(entity_data["position"])),
                health=entity_data["health"],
                max_health=entity_data["max_health"],
                attack=entity_data["attack"],
                defence=entity_data["defence"],
                speed=entity_data["speed"],
                inventory=Entity.InventoryMemento(data=tuple(inventory_items)),
                active_modifiers=Entity.ActiveModifiersMemento(
                    data=copy.deepcopy(entity_data["active_modifiers"])
                ),
                backpack=Entity.BackpackMemento(items=tuple(backpack_items)),
                attack_type=AttackTypes(entity_data["attack_type"]),
                temp_buffs=Entity.TempBuffsMemento(
                    data=copy.deepcopy(entity_data["temp_buffs"])
                ),
                state_manager=Entity.StateManagerMemento(
                    state_name=state_manager_data.get(
                        "state_name",
                        (
                            "Defending"
                            if entity_type in ("goblin", "skeleton", "ogre")
                            else None
                        ),
                    )
                ),
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

        # Command manager memento
        command_manager_memento = self.data_to_command_manager_memento(
            command_manager_data
        )

        return GameState.Memento(
            grid_memento=grid_memento,
            entity_mementos=tuple(entity_mementos),
            entity_ids_issued=game_data["entity_ids_issued"],
            map_created=game_data["map_created"],
            turn_number=game_data["turn_number"],
            is_saved=True,
            command_manager_memento=command_manager_memento,
        )

    # Delete Save
    # Deletes file with the given name
    # Params:   filename - string - file name associated with current save
    # Returns:  None
    def delete_save(self, filename):
        # Create file path
        filepath = self.create_filepath(filename)
        # Delete save file
        os.remove(filepath)

    # Command Manager Memento to Data
    # Converts a CommandManager Memento into JSON-compatible data
    # Params: memento - CommandManager.Memento
    # Returns: dict
    def command_manager_memento_to_data(self, memento):
        if memento is None:
            return None

        undo_history = []
        redo_history = []

        # Convert undo history
        for command_memento in memento.undo_history:
            undo_history.append(self.command_memento_to_data(command_memento))

        # Convert redo history
        for command_memento in memento.redo_history:
            redo_history.append(self.command_memento_to_data(command_memento))

        return {
            "undo_history": undo_history,
            "redo_history": redo_history,
        }

    # Command Memento to Data
    # Converts a Command Memento into JSON-compatible data
    # Params: memento - Command.Memento
    # Returns: dict
    def command_memento_to_data(self, memento):
        return {
            "command_type": memento.command_type,
            "data": self.command_data_to_data(memento.data),
        }

    # Command Data to Data
    # Recursively converts command data into JSON-compatible data
    # Params: data - object to convert
    # Returns: JSON-compatible object
    def command_data_to_data(self, data):

        # Convert nested GameState Mementos
        if isinstance(data, GameState.Memento):
            return self.memento_to_data(data)

        # Convert nested CommandManager Mementos
        elif hasattr(data, "undo_history") and hasattr(data, "redo_history"):
            return self.command_manager_memento_to_data(data)

        # Convert nested Command Mementos
        elif hasattr(data, "command_type") and hasattr(data, "data"):
            return self.command_memento_to_data(data)

        # Convert dictionaries
        elif isinstance(data, dict):
            converted_data = {}

            for key, value in data.items():
                converted_data[key] = self.command_data_to_data(value)

            return converted_data

        # Convert tuples and lists
        elif isinstance(data, (tuple, list)):
            converted_data = []

            for value in data:
                converted_data.append(self.command_data_to_data(value))

            return converted_data

        # Convert enums
        elif isinstance(data, Enum):
            return data.value

        # JSON-compatible primitive values
        elif data is None or isinstance(data, (str, int, float, bool)):
            return data

        else:
            raise TypeError(
                f"Cannot convert {type(data).__name__} into JSON-compatible data!"
            )

    # Data to Command Manager Memento
    # Converts JSON-compatible data into a CommandManager Memento
    # Params: command_manager_data - dict
    # Returns: CommandManager.Memento
    def data_to_command_manager_memento(self, command_manager_data):

        if command_manager_data is None:
            return None

        undo_history = []
        redo_history = []

        # Reconstruct undo history
        for command_data in command_manager_data["undo_history"]:
            undo_history.append(self.data_to_command_memento(command_data))

        # Reconstruct redo history
        for command_data in command_manager_data["redo_history"]:
            redo_history.append(self.data_to_command_memento(command_data))

        return CommandManager.Memento(
            undo_history=tuple(undo_history),
            redo_history=tuple(redo_history),
        )

    # Data to Command Memento
    # Converts JSON-compatible data into a Command Memento
    # Params: command_data - dict
    # Returns: Command.Memento
    def data_to_command_memento(self, command_data):

        return Command.Memento(
            command_type=command_data["command_type"],
            data=self.command_data_to_data(command_data["data"]),
        )

    # Create Command Memento
    # Creates a basic Command Memento for testing.
    # Params: None
    # Returns: Command.Memento
    def create_command_memento(self):
        return Command.Memento(
            command_type="TestCommand",
            data={
                "entity_id": 1,
                "x": 5,
                "y": 10,
            },
        )

    # Equipment Memento to Data
    # Converts equipment and consumable mementos into JSON-compatible data
    # Params: item_memento - EquipmentMemento or ConsumableMemento
    # Returns: dict or None
    def equipment_memento_to_data(self, item_memento):
        if item_memento is None:
            return None

        # Convert consumable memento
        if isinstance(item_memento, equipment.ConsumableMemento):
            base_memento = item_memento.equipment_memento

            return {
                "item_type": "Consumable",
                "name": base_memento.name,
                "slot": base_memento.slot,
                "rarity": base_memento.rarity,
                "rolled_effects": dict(base_memento.rolled_effects),
                "instant_effects": {
                    effect_type: dict(effects)
                    for effect_type, effects in item_memento.instant_effects
                },
                "over_time_effects": {
                    effect_type: dict(effects)
                    for effect_type, effects in item_memento.over_time_effects
                },
                "duration": item_memento.duration,
            }

        # Convert regular equipment memento
        if isinstance(item_memento, equipment.EquipmentMemento):
            return {
                "item_type": "Equipment",
                "name": item_memento.name,
                "slot": item_memento.slot,
                "rarity": item_memento.rarity,
                "rolled_effects": dict(item_memento.rolled_effects),
            }

        raise TypeError(f"Invalid equipment memento: {type(item_memento).__name__}")

    # Data to Equipment Memento
    # Reconstructs equipment or consumable mementos from saved data
    # Params: item_data - dict or None
    # Returns: EquipmentMemento, ConsumableMemento, or None
    def data_to_equipment_memento(self, item_data):
        if item_data is None:
            return None

        # Reconstruct regular equipment memento
        base_memento = equipment.EquipmentMemento(
            name=item_data["name"],
            slot=item_data["slot"],
            rarity=item_data["rarity"],
            rolled_effects=tuple(item_data["rolled_effects"].items()),
        )

        # Reconstruct consumable memento
        if item_data["item_type"] == "Consumable":
            return equipment.ConsumableMemento(
                equipment_memento=base_memento,
                instant_effects=tuple(
                    (effect_type, tuple(effects.items()))
                    for effect_type, effects in item_data["instant_effects"].items()
                ),
                over_time_effects=tuple(
                    (effect_type, tuple(effects.items()))
                    for effect_type, effects in item_data["over_time_effects"].items()
                ),
                duration=item_data["duration"],
            )

        # Return regular equipment memento
        if item_data["item_type"] == "Equipment":
            return base_memento

        raise ValueError(f"Unknown item type: {item_data['item_type']}")
