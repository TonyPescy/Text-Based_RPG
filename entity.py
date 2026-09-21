"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 19, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: entity.py
Purpose: Houses all functions necessary for proper entity handling and logic in the game
"""

# imports
import domain_library as d_Lib


# Entity class with all methods needed for entities
class Entity:

    # Base Invetory for all Entities
    BASE_INVENTORY = (
        d_Lib.create_equipment("none_wep"),
        d_Lib.create_equipment("none_armor"),
        d_Lib.create_equipment("none_acc"),
    )

    # Initialize Entity Class with id, type, position, health, attack, defence, speed, inventory, active_modifiers
    def __init__(
        self,
        id,
        e_type,
        position,
        health,
        attack,
        defence,
        speed,
        inventory,
        active_modifiers,
    ):
        self.id = id
        self.e_type = e_type
        self.position = position
        self.health = health
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.inventory = inventory
        self.active_modifiers = active_modifiers

    # START MOVE TO CLI?
    # Entity List for tracking entities
    entity_list = []
    # Value to count what ID to give the next entity
    entity_ids_issued = 0
    # END MOVE TO CLI

    # Base Entity Methods

    # Reset ID Issuer Tracker Start
    # resets entity id issues number back to 0 to prevent errors with testing
    # Params: None
    # Return: None
    def reset_id_issuer_tracker():
        Entity.entity_ids_issued = 0

    # Reset Entity List Start
    # resets entity list back to empty to prevent errors with testing
    # Params: None
    # Return: None
    def reset_entity_list():
        Entity.entity_list = []

    # Get Stats Start
    # Gets all relevant stats of the entity and returns them
    # Params: None
    # Returns dictionary - Contains all stats needed for Command Line Interface commands
    #       (int id, str e_type, tuple x/y coords, int health, int attack, int defence, int speed, list of two dictionaries active_modifiers)
    def get_stats(self):
        stat_dict = {
            "Id": self.id,
            "Type": self.e_type,
            "Position": self.position,
            "Health": self.health,
            "Attack": self.attack,
            "Defence": self.defence,
            "Speed": self.speed,
            "Active_modifiers": self.active_modifiers,
        }
        return stat_dict

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    # Params: None
    # Return: None
    def reset_stats(self):
        self.health = self.BASE_STATS["Health"]
        self.attack = self.BASE_STATS["Attack"]
        self.defence = self.BASE_STATS["Defence"]
        self.speed = self.BASE_STATS["Speed"]

    # Reset Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    # Params: active_grid - Grid - Current grid used by the CLI
    def update_stats(self, active_grid):
        # Clear active modifiers to avoid double counting of modifiers
        self.active_modifiers["Flat_modifiers"] = {}
        self.active_modifiers["Percent_modifiers"] = {}
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.inventory:
            # Iterate through all stats modified within current slot
            for stat, modifier in slot.effects.items():
                # Ignore stats that onlt affect Mage class
                if stat == "Mana" or stat == "Spell_power":
                    continue
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)

        # Tile modifiers
        # Get entity grid position
        x = self.position[0]
        y = self.position[1]

        # Get current tile
        tile = active_grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - could be cleaned up later
        for stat, modifier in tile.modifiers["Flat_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        for stat, modifier in tile.modifiers["Percent_modifiers"].items():
            self.handle_modifiers(stat, modifier)

        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()

    # Update Stats End

    # Handle Modifiers Start
    # Handles the flat and percent modifier split for the update_stats method
    # Updates active modifier of current unit
    # Params: stat - string - Stat that is to be modified
    #           modifier - string - modifier to be parsed and applied to given stat
    # Return: None
    def handle_modifiers(self, stat, modifier):
        # Determine if the modifier is percent based or a flat modifier and add it active modifiers accordingly
        if (
            modifier[len(modifier) - 1] != "%"
        ):  # All percent based modifiers will end with "%"
            # Flat modifier
            # If a stat is already being modified by a flat modifier
            if stat in self.active_modifiers["Flat_modifiers"]:
                self.active_modifiers["Flat_modifiers"][stat] += int(modifier)
            else:  # Stat is not already modified by a flat modifier
                self.active_modifiers["Flat_modifiers"][stat] = int(modifier)

        else:  # Is a percent modifier
            # Percent modifier
            # If a stat is already being modified by a percent modifier
            if stat in self.active_modifiers["Percent_modifiers"]:
                self.active_modifiers["Percent_modifiers"][stat] += int(
                    modifier[: len(modifier) - 1]
                )
            else:  # Stat is not already being modified by a percent modifier
                self.active_modifiers["Percent_modifiers"][stat] = int(
                    modifier[: len(modifier) - 1]
                )

    # Handle Modifiers End

    # Calculate Final Stats Start
    # Handles stat calculation for entities and updates them
    # Params: None
    # Return: None
    def calculate_final_stats(self):
        # Stats to be checked
        stats = ("Health", "Attack", "Defence", "Speed")
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = getattr(self, stat.lower())
            # If flat values exist
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            setattr(self, stat.lower(), temp_value)

    # Calculate Final Stats End

    # Is Valid Entity Start
    # Checks to see input is a valid entity type
    # Params: entity_type - string - entity name
    # Returns: Bool
    def is_valid_entity(entity_type):
        if entity_type in [entity.lower() for entity in d_Lib.ENTITY_TYPES]:
            return True
        else:
            print("error: Tile Type added is not a valid tile type!")
            return False

    # Create Entity Start - NEEDS FIX
    # Creates entity with base stats and values based on the entity
    # Holds base stats for all of the entities
    # Params: e_type - String - Type of entity to create
    #       x,y - int - Coordinates to spawn entity at
    # Return: None
    def create_entity(e_type, x, y):
        # ensure correct typing
        x = int(x)
        y = int(y)
        # Case statement to match to every entity type in game
        match e_type:
            # Warrior
            case "warrior":
                # Create warrior entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "warrior",
                    [x, y],
                    Entity.WARRIOR_BASE_STATS["Health"],
                    Entity.WARRIOR_BASE_STATS["Attack"],
                    Entity.WARRIOR_BASE_STATS["Defence"],
                    Entity.WARRIOR_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            # Mage
            case "mage":
                # Create mage entity
                temp_entity = Mage(
                    Entity.entity_ids_issued,
                    "mage",
                    [x, y],
                    Mage.MAGE_BASE_STATS["Health"],
                    Mage.MAGE_BASE_STATS["Attack"],
                    Mage.MAGE_BASE_STATS["Defence"],
                    Mage.MAGE_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                    Mage.MAGE_BASE_STATS["Mana"],
                    Mage.MAGE_BASE_STATS["Spell_power"],
                )
            # Skeleton
            case "skeleton":
                # Create skeleton entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "skeleton",
                    [x, y],
                    Entity.SKELETON_BASE_STATS["Health"],
                    Entity.SKELETON_BASE_STATS["Attack"],
                    Entity.SKELETON_BASE_STATS["Defence"],
                    Entity.SKELETON_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            # Goblin
            case "goblin":
                # Create goblin entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "goblin",
                    [x, y],
                    Entity.GOBLIN_BASE_STATS["Health"],
                    Entity.GOBLIN_BASE_STATS["Attack"],
                    Entity.GOBLIN_BASE_STATS["Defence"],
                    Entity.GOBLIN_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            case _:  # error no matching entity type found - May be redundant
                print(
                    f"error: Invalid entity type '{e_type}'. "
                    f"Expected one of: {Entity.ENTITY_TYPES}."
                )

        # Increment entity_ids_issued to account for new entity
        Entity.entity_ids_issued += 1
        # Add new entity to entity list
        Entity.entity_list.append(temp_entity)

    # Create Entity End

    # Equip Item Start
    # Equips given item at given slot
    # Params: None
    # Return: None
    def equip_item(self, item, slot):
        # match statement for slot
        match slot:
            # weapon case
            case "weapon":
                self.inventory[0] = item
            # armor case
            case "armor":
                self.inventory[1] = item
            # accessory case
            case "accessory":
                self.inventory[2] = item


# Warrior Class extend from Entity class
# Uses all functions without any changes
class Warrior(Entity):

    # Warrior Constants
    BASE_STATS = {
        "Health": 120,
        "Attack": 15,
        "Defence": 10,
        "Speed": 5,
    }

    # Initialize warrior class with entity class attributes
    def __init__(
        self,
        id,
        e_type,
        position,
        active_modifiers,
    ):
        # Inherit init from Entity super class
        super().__init__(
            id,
            e_type,
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            self.BASE_INVENTORY,
            active_modifiers,
        )


# Skeleton Class extend from Entity class
# Uses all functions without any changes
class Skeleton(Entity):

    # Skeleton Constants
    BASE_STATS = {
        "Health": 60,
        "Attack": 10,
        "Defence": 8,
        "Speed": 4,
    }

    # Initialize skeleton class with entity class attributes
    def __init__(
        self,
        id,
        e_type,
        position,
        active_modifiers,
    ):
        # Inherit init from Entity super class
        super().__init__(
            id,
            e_type,
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            self.BASE_INVENTORY,
            active_modifiers,
        )


# Goblin Class extend from Entity class
# Uses all functions without any changes
class Goblin(Entity):

    # Goblin Constants
    BASE_STATS = {
        "Health": 45,
        "Attack": 12,
        "Defence": 3,
        "Speed": 6,
    }

    # Initialize goblin class with entity class attributes
    def __init__(
        self,
        id,
        e_type,
        position,
        active_modifiers,
    ):
        # Inherit init from Entity super class
        super().__init__(
            id,
            e_type,
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            self.BASE_INVENTORY,
            active_modifiers,
        )


# Mage Class extend from Entity class
class Mage(Entity):
    # Mage Constants
    BASE_STATS = {
        "Health": 70,
        "Attack": 8,
        "Defence": 4,
        "Speed": 5,
        "Mana": 100,
        "Spell_power": 25,
    }

    # Initialize mage class with entity class attributes + new ones: mana and spell power
    def __init__(
        self,
        id,
        e_type,
        position,
        active_modifiers,
    ):

        # Inherit init from Entity super class
        super().__init__(
            id,
            e_type,
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            self.BASE_INVENTORY,
            active_modifiers,
        )
        # New attributes
        self.mana = self.BASE_STATS["Mana"]
        self.spell_power = self.BASE_STATS["Spell_power"]

    # Get Stats Start
    # Gets all relevant stats of the entity and returns them
    # Params: None
    # Returns dictionary - Contains all stats needed for Command Line Interface commands
    #       (int id, str e_type, tuple x/y coords, int health, int mana, int attack, int defence, int speed, list of two dictionaries active_modifiers)
    def get_stats(self):
        stat_dict = {
            "Id": self.id,
            "Type": self.e_type,
            "Position": self.position,
            "Health": self.health,
            "Mana": self.mana,
            "Attack": self.attack,
            "Defence": self.defence,
            "Speed": self.speed,
            "Active_modifiers": self.active_modifiers,
        }
        return stat_dict

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    # Params: None
    # Return: None
    def reset_stats(self):
        self.health = self.BASE_STATS["Health"]
        self.attack = self.BASE_STATS["Attack"]
        self.defence = self.BASE_STATS["Defence"]
        self.speed = self.BASE_STATS["Speed"]
        self.mana = self.BASE_STATS["Mana"]
        self.spell_power = self.BASE_STATS["Spell_power"]

    # Reset Stats End

    # Calculate Final Stats Start
    # Handles stat calculation for entities and updates them
    # Params: None
    # Return: None
    def calculate_final_stats(self):
        # Stats to be checked
        stats = ("Health", "Attack", "Defence", "Speed", "Mana", "Spell_power")
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = getattr(self, stat.lower())
            # If flat values exist
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            setattr(self, stat.lower(), temp_value)

    # Calculate Final Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    # Params: None
    # Return: None
    def update_stats(self, active_grid):
        # Clear active modifiers to avoid double counting of modifiers
        self.active_modifiers["Flat_modifiers"] = {}
        self.active_modifiers["Percent_modifiers"] = {}
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.inventory:
            # Iterate through all stats modified within current slot
            for stat, modifier in slot.effects.items():
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)

        # Tile modifiers
        # Get entity grid position
        x = self.position[0]
        y = self.position[1]

        # Get current tile
        tile = active_grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - FIX
        for stat, modifier in tile.modifiers["Flat_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        for stat, modifier in tile.modifiers["Percent_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()

        # Update Stats End
