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
import domain_library as dl
from equipment import Equipment


# Entity class with all methods needed for entities
class Entity:
    """# Base Invetory for all Entities
    BASE_INVENTORY = [
        dl.create_equipment("none_wep"),
        dl.create_equipment("none_armor"),
        dl.create_equipment("none_acc"),
    ]"""

    # Base Modifiers for all Entities
    # BASE_MODIFIERS = {"Flat_modifiers": {}, "Percent_modifiers": {}}

    # Backpack Size
    BACKPACK_SIZE = 5

    # Initialize Entity Class with id, type, position, health, attack, defence, speed, inventory, active_modifiers
    def __init__(
        self,
        id,
        e_type,
        position,
        health,
        max_health,
        attack,
        defence,
        speed,
        inventory,
        active_modifiers,
        backpack,
        attack_type,
    ):
        self.id = id
        self.e_type = e_type
        self.position = position
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.inventory = inventory
        self.active_modifiers = active_modifiers
        self.backpack = backpack
        self.attack_type = attack_type
        self.temp_buffs = []  # temp buffs list of dictionarys

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
        self.max_health = self.BASE_STATS["Health"]
        self.attack = self.BASE_STATS["Attack"]
        self.defence = self.BASE_STATS["Defence"]
        self.speed = self.BASE_STATS["Speed"]

    # Reset Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    # Params: CLI - cli instance - Current active game objects/features
    # Return: None
    def update_stats(self, cli):  # UPDATE TEST
        # starting health - used to set health after reset
        # starting_health = self.health
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
        tile = cli.grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - could be cleaned up later
        for stat, modifier in tile.modifiers.items():
            # Ignore stats that onlt affect Mage class
            if stat == "Mana" or stat == "Spell_power":
                continue

            self.handle_modifiers(stat, modifier)

        # Handle temp buffs
        for buff in self.temp_buffs:
            for modifier_type, modifiers in buff["Effects"].items():
                for stat, amount in modifiers.items():

                    # Ignore stats that onlt affect Mage class
                    if stat == "Mana" or stat == "Spell_power":
                        continue
                    # Convert modifier into handle_modifiers format
                    elif modifier_type == "Flat_modifiers":
                        modifier = str(amount)

                    elif modifier_type == "Percent_modifiers":
                        modifier = str(amount) + "%"

                    else:
                        continue

                    self.handle_modifiers(stat, modifier)

        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()
        # Update max stats
        self.calculate_max_stats()

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
            modifier[len((modifier)) - 1] != "%"
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

    # Calculate Max Values
    # Calculates the max health and/or mana of entity
    # Params: None
    # Returns:  None
    def calculate_max_stats(self):
        # Stats to be checked
        stats = ["Health"]
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = self.BASE_STATS.get(stat, 0)
            # If flat values exist
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update max stats
            if stat == "Health":
                self.max_health = temp_value

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

    # Update Inventory
    # Updates inventory after backpack changes - ensures no phantom items exist
    # if dupes of an item exist, the dupe will remain equipped
    # Params: None
    # Returns:  None
    def update_inventory(self):
        # for item in inventory
        for item in self.inventory.copy():  # copy to avoid skipping
            # if item is in backpack - continue
            if any(item == temp_item for temp_item in self.backpack):
                continue
            elif item.name != "None":  # no real item matches found - Remove
                self.inventory.remove(item)
                continue

    """
    # Create Entity Start - NEEDS FIX/REFACTOR
    # Creates entity with base stats and values based on the entity
    # Holds base stats for all of the entities
    # Params: e_type - String - Type of entity to create
    #       x,y - int - Coordinates to spawn entity at
    #       id__to_use - int - id generated for entity based on current entity ID counter
    # Return: None
    def create_entity(e_type, x, y, id_to_use):
        # ensure correct typing
        x = int(x)
        y = int(y)
        # Case statement to match to every entity type in game
        match e_type:
            # Warrior
            case "warrior":
                # Create warrior entity
                temp_entity = Entity(
                    id_to_use,
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
                    id_to_use,
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
                    id_to_use,
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
                    id_to_use,
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

        # HANDLE INSIDE OF CLI
        # Increment entity_ids_issued to account for new entity
        Entity.entity_ids_issued += 1
        # Add new entity to entity list
        Entity.entity_list.append(temp_entity)
        # HANDLE INSIDE OF CLI
    """
    # Create Entity End

    # Equip Item Start
    # Equips given item at given slot
    # Params: item - Equipment object - equipment to be equipped
    #           slot - string - slot to equip weapon to
    # Return: None
    def equip_item(self, item, slot):
        if not isinstance(item, Equipment):
            return
        # Redundant code btw
        if slot != item.slot.lower():
            return
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

        # add to backpack
        self.add_item_to_backpack(item)

    # Add Item To Backpack
    # Adds provided item to backpack
    # Size Handling responses TBD
    # Params: item - Equipment Object - item to be added to the backpack
    # Returns: None
    def add_item_to_backpack(self, item):
        """HANDLE IN CLI
        # if backpack is full
        if len(self.backpack) > 5:
            print(f"error: pickup_failed - Backpack full!")
        """
        self.backpack.append(item)

    # Remove Item From Backpack
    # Removes provided item from the backpack
    # Size Handling responses TBD - CLI?
    # Params: item - Equipment Object - item to be removed from the backpack
    # Returns: None
    def remove_item_from_backpack(self, item):
        """HANDLE IN CLI
        # if backpack is full
        if len(self.backpack) > 5:
            print(f"error: pickup_failed - Backpack full!")
        """
        self.backpack.remove(item)

    # Attack Entity
    # Current entity attacks given entity
    # Called after all variables and entities have been validated
    # Params:   self - Entity - One who is attacking
    #           target - Entity - One being attacked
    # Return:   damage - int - damage dealt to the defender
    def attack_entity(self, target):
        # Get damage dealt
        damage = max(1, (self.attack - target.defence))
        # Subtract health from defender with max at 0 - prevents underflow
        target.health = max(0, (target.health - damage))
        # Handle target death DEATH NOT IMPLEMENTED YET!!!
        # HANDLE A KILL HERE
        # return damage for success message
        return damage


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
    def __init__(self, id, position, active_modifiers=None, backpack=None):
        if active_modifiers is None:
            active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        if backpack is None:
            backpack = []

        # Inherit init from Entity super class
        super().__init__(
            id,
            "warrior",
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            dl.BASE_INVENTORY,
            active_modifiers,
            backpack,
            dl.AttackTypes.MELEE,
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
    def __init__(self, id, position, active_modifiers=None, backpack=None):
        if active_modifiers is None:
            active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        if backpack is None:
            backpack = []
        # Inherit init from Entity super class
        super().__init__(
            id,
            "skeleton",
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            dl.BASE_INVENTORY,
            active_modifiers,
            backpack,
            dl.AttackTypes.RANGED,
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
    def __init__(self, id, position, active_modifiers=None, backpack=None):
        if active_modifiers is None:
            active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        if backpack is None:
            backpack = []

        # Inherit init from Entity super class
        super().__init__(
            id,
            "goblin",
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            dl.BASE_INVENTORY,
            active_modifiers,
            backpack,
            dl.AttackTypes.MELEE,
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
    def __init__(self, id, position, active_modifiers=None, backpack=None):
        if active_modifiers is None:
            active_modifiers = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        if backpack is None:
            backpack = []
        # Inherit init from Entity super class
        super().__init__(
            id,
            "mage",
            position,
            self.BASE_STATS["Health"],
            self.BASE_STATS["Health"],
            self.BASE_STATS["Attack"],
            self.BASE_STATS["Defence"],
            self.BASE_STATS["Speed"],
            dl.BASE_INVENTORY,
            active_modifiers,
            backpack,
            dl.AttackTypes.MELEE,  # When not using spells using staff to attack physically
        )
        # New attributes
        self.mana = self.BASE_STATS["Mana"]
        self.max_mana = self.BASE_STATS["Mana"]
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
        self.max_health = self.BASE_STATS["Health"]
        self.attack = self.BASE_STATS["Attack"]
        self.defence = self.BASE_STATS["Defence"]
        self.speed = self.BASE_STATS["Speed"]
        self.mana = self.BASE_STATS["Mana"]
        self.max_mana = self.BASE_STATS["Mana"]
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
    # Params: CLI - cli instance - Current active game objects/features
    # Return: None
    def update_stats(self, cli):  # UPDATE TESTS
        # starting health - used to set health after reset
        # starting_health = self.health
        # starting mana - used to set mana after reset
        # starting_mana = self.mana
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
        tile = cli.grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - FIX?
        for stat, modifier in tile.modifiers.items():
            self.handle_modifiers(stat, modifier)

        # Handle temp buffs
        for buff in self.temp_buffs:
            for modifier_type, modifiers in buff["Effects"].items():
                for stat, amount in modifiers.items():

                    # Convert modifier into handle_modifiers format
                    if modifier_type == "Flat_modifiers":
                        modifier = str(amount)

                    elif modifier_type == "Percent_modifiers":
                        modifier = str(amount) + "%"

                    else:
                        continue

                    self.handle_modifiers(stat, modifier)

        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()
        # Update max stats
        self.calculate_max_stats()

        # Update Stats End

    # Calculate Max Values
    # Calculates the max health and/or mana of entity
    # Params: cli - cli instance - Current active game objects/features
    # Returns:  None
    def calculate_max_stats(self):
        # Stats to be checked
        stats = ["Health", "Mana"]
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = self.BASE_STATS.get(stat, 0)
            # If flat values exist
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update max stats
            if stat == "Health":
                self.max_health = temp_value

            elif stat == "Mana":
                self.max_mana = temp_value


# Entities Factory
# Create Entity Start
# Creates entity with base stats and values based on the entity
# Holds base stats for all of the entities
# Params: e_type - String - Type of entity to create
#       x,y - int - Coordinates to spawn entity at
#       e_id - int - id generated for entity based on current entity ID counter
# Returns: Entity instance of the specified type
def create_entity(e_type, x, y, e_id):
    # ensure correct typing
    try:
        # Convert to enum
        e_type = dl.EntityType(str(e_type).capitalize())
        x = int(x)
        y = int(y)
    except:
        print(f"error: spawn_failed x ({x}) and/or y ({y}) are not integers!")

    match e_type:  # MATCH WITH ENUMS UPON THAT UPDATE
        case dl.EntityType.WARRIOR:
            return Warrior(e_id, [x, y])

        case dl.EntityType.MAGE:
            return Mage(e_id, [x, y])

        case dl.EntityType.SKELETON:
            return Skeleton(e_id, [x, y])

        case dl.EntityType.GOBLIN:
            return Goblin(e_id, [x, y])
