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
from copy import deepcopy
import domain_library as dl
from equipment import Equipment, create_equipment
from dataclasses import dataclass


# Data class for entity stats
@dataclass
class EntityInfo:
    id: int
    e_type: str
    position: tuple
    health: int
    max_health: int
    attack: int
    defence: int
    speed: int
    inventory: tuple
    active_modifiers: tuple  # tuple of two dictionaries - flat and percent modifiers
    backpack: tuple
    attack_type: str
    temp_buffs: tuple


# Entity class with all methods needed for entities
class Entity:

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
        self.__id = id
        self.__e_type = e_type
        self.__position = deepcopy(position)
        self.__health = health
        self.__max_health = max_health
        self.__attack = attack
        self.__defence = defence
        self.__speed = speed
        self.__inventory = deepcopy(inventory)
        self.__active_modifiers = deepcopy(active_modifiers)
        self.__backpack = deepcopy(backpack)
        self.__attack_type = attack_type
        self.__temp_buffs = []  # temp buffs list of dictionarys

        # Temp Buffs Structure
        """
        {
            "Name": consumable.name,
            "Effects": consumable.over_time_effects,
            "Turns": consumable.duration,
        } x number of temp buffs
        """

    # Get Info
    # Gets all relevant info of the entity and returns them
    # Params: None
    # Returns: EntityInfo - all info for current entity
    def get_info(self):
        return EntityInfo(
            id=self.__id,
            e_type=self.__e_type,
            position=self.__position,
            health=self.__health,
            max_health=self.__max_health,
            attack=self.__attack,
            defence=self.__defence,
            speed=self.__speed,
            inventory=tuple(item.get_info() for item in self.__inventory),
            active_modifiers=tuple(
                (
                    (
                        "Flat_modifiers",
                        tuple(self.__active_modifiers["Flat_modifiers"].items()),
                    ),
                    (
                        "Percent_modifiers",
                        tuple(self.__active_modifiers["Percent_modifiers"].items()),
                    ),
                )
            ),
            backpack=tuple(item.get_info() for item in self.__backpack),
            attack_type=self.__attack_type,
            temp_buffs=tuple(
                (
                    ("Name", buff["Name"]),
                    (
                        "Effects",
                        (
                            (
                                "Flat_modifiers",
                                tuple(buff["Effects"]["Flat_modifiers"].items()),
                            ),
                            (
                                "Percent_modifiers",
                                tuple(buff["Effects"]["Percent_modifiers"].items()),
                            ),
                        ),
                    ),
                    ("Turns", buff["Turns"]),
                )
                for buff in self.__temp_buffs
            ),
        )

    # Get Stats End

    # Get Stat
    # Gets given stat value of entity
    # Only called on real objects within this file - editing the actual entity
    # Params:   stat - string - stat to get
    # Return:   value - int - stat value
    def get_stat(self, stat):
        match stat:
            case "Health":
                return self.__health

                """case "Max Health":
                return self.__max_health"""

            case "Attack":
                return self.__attack
            case "Defence":
                return self.__defence
            case "Speed":
                return self.__speed

    # Reset Stats Start
    # Resets entities stats to base values
    # Params: None
    # Return: None
    def reset_stats(self):
        self.__health = self.BASE_STATS["Health"]
        self.__max_health = self.BASE_STATS["Health"]
        self.__attack = self.BASE_STATS["Attack"]
        self.__defence = self.BASE_STATS["Defence"]
        self.__speed = self.BASE_STATS["Speed"]

    # Reset Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    # Params: game_state - game state instance - Current active game objects/features
    # Return: None
    def update_stats(self, game_state):
        # starting health - used to set health after reset
        starting_health = self.__health
        if hasattr(self, "Mana"):
            starting_mana = self.__mana
        # Clear active modifiers to avoid double counting of modifiers
        self.__active_modifiers["Flat_modifiers"] = {}
        self.__active_modifiers["Percent_modifiers"] = {}
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.__inventory:
            slot_info = slot.get_info()
            # Iterate through all stats modified within current slot
            for stat, modifier in slot_info.effects:
                # Ignore stats that only affect Mage class
                if (
                    stat == "Mana" or stat == "Spell_power"
                ) and self.__e_type.lower() != "mage":
                    continue
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)

        # Tile modifiers
        # Get entity grid position
        x = self.__position[0]
        y = self.__position[1]

        # Get current tile copy
        tile = game_state.get_game_tile_info(x, y)

        # Handle modifiers for tile - split due to way tile modifiers are setup - could be cleaned up later
        for stat, modifier in tile.modifiers:
            # Ignore stats that onlt affect Mage class
            if stat == "Mana" or stat == "Spell_power":
                continue

            self.handle_modifiers(stat, modifier)

        # Handle temp buffs
        for buff in self.__temp_buffs:
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
        # Set health and mana if applicable back to normal
        self.__health = starting_health
        if hasattr(self, "mana"):
            self.__mana = starting_mana
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
            if stat in self.__active_modifiers["Flat_modifiers"]:
                self.__active_modifiers["Flat_modifiers"][stat] += int(modifier)
            else:  # Stat is not already modified by a flat modifier
                self.__active_modifiers["Flat_modifiers"][stat] = int(modifier)

        else:  # Is a percent modifier
            # Percent modifier
            # If a stat is already being modified by a percent modifier
            if stat in self.__active_modifiers["Percent_modifiers"]:
                self.__active_modifiers["Percent_modifiers"][stat] += int(
                    modifier[: len(modifier) - 1]
                )
            else:  # Stat is not already being modified by a percent modifier
                self.__active_modifiers["Percent_modifiers"][stat] = int(
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
            if stat in self.__active_modifiers["Flat_modifiers"]:
                temp_value += self.__active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.__active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.__active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update max stats
            if stat == "Health":
                self.__max_health = temp_value

    # Calculate Final Stats Start
    # Handles stat calculation for entities and updates them
    # Params: None
    # Return: None
    def calculate_final_stats(self):
        # Stats to be checked
        stats = ("Health", "Attack", "Defence", "Speed")
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = self.get_stat(stat)
            # If flat values exist
            if stat in self.__active_modifiers["Flat_modifiers"]:
                temp_value += self.__active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.__active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.__active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            self.update_single_stat(stat.lower(), temp_value)

    # Calculate Final Stats End

    # Update Inventory
    # Updates inventory after backpack changes - ensures no phantom items exist
    # if dupes of an item exist, the dupe will remain equipped
    # Params: None
    # Returns:  None
    def update_inventory(self):
        # for item in inventory
        for item in self.__inventory.copy():  # copy to avoid skipping
            # if item is in backpack - continue
            if any(item == temp_item for temp_item in self.__backpack):
                continue
            elif item.name != "None":  # no real item matches found - Remove
                # self.__inventory.remove(item)
                match item.slot.lower():
                    case "weapon":
                        self.__inventory[0] = create_equipment("none_wep")
                    case "armor":
                        self.__inventory[1] = create_equipment("none_armor")
                    case "accessory":
                        self.__inventory[2] = create_equipment("none_acc")
                continue

    # Equip Item Start
    # Equips given item at given slot
    # Params: item - Equipment object - equipment to be equipped
    #           slot - string - slot to equip weapon to
    # Return: None
    def equip_item(self, item, slot):
        if not isinstance(item, Equipment):
            return
        # Get info
        item_info = item.get_info()
        """# Redundant code btw
        if slot != item_info.slot.lower():
            return"""
        # match statement for slot
        match item_info.slot.lower():
            # weapon case
            case "weapon":
                self.__inventory[0] = item
            # armor case
            case "armor":
                self.__inventory[1] = item
            # accessory case
            case "accessory":
                self.__inventory[2] = item

        # add to backpack
        # self.add_item_to_backpack(item)

    # Update Temp Buffs
    # Updates temp buffs with their duration due to CLI tick process
    # Params: None
    # Returns: buffs_to_be_removed - list - list of buff names to be removed
    def update_temp_buffs(self):
        # init to be removed list
        buffs_to_be_removed = []
        # check for empty temp_buffs
        if self.__temp_buffs == []:
            return buffs_to_be_removed

        for buff in self.__temp_buffs:
            # Process turn passing
            buff["Turns"] -= 1
            # Check for "Turns" = 0
            if buff["Turns"] == 0:
                # Mark for removal
                buffs_to_be_removed.append(buff["Name"])
        # Return list of buffs
        return buffs_to_be_removed

    # Remove Temp Buffs
    # Removes buffs from entity that are in list provided
    # List is checked beforehand and should be clean/valid
    # Params: to_be_removed - list - List of buff names to be removed
    # Returns: bool - bool - true if current entity should be removed from board
    def remove_temp_buffs(self, to_be_removed):

        # Iterate through list of names to be removed
        for buff_name in to_be_removed:
            # For each name iterate through list of temp buffs
            for buff in self.__temp_buffs:
                # If name matches one to be removed - remove it
                if buff_name == buff["Name"]:
                    # Check for dead status for special case handling
                    if buff["Name"] == "Dead":
                        return True

                    self.__temp_buffs.remove(buff)
                    print(f'Buff Removed: {buff["Name"]}!')
                    break
        return False

    # Process Tick on Entity
    # Processes turn tick on entity - temp buffs updates, ...
    # Only temp buffs right now, may need updates in future with new functionality
    # Params: None
    # Returns: bool - True if entity is to be removed
    def process_tick_on_entity(self):
        # Update the buffs of the entity
        buffs_to_remove = self.update_temp_buffs()

        # If there are buffs to remove
        if len(buffs_to_remove) > 0:
            # Remove them
            return self.remove_temp_buffs(buffs_to_remove)

        return False

    # Add Item To Backpack
    # Adds provided item to backpack
    # Size Handling responses TBD
    # Params: item - Equipment Object - item to be added to the backpack
    # Returns: None
    def add_item_to_backpack(self, item):
        self.__backpack.append(item)

    # Remove Item From Backpack
    # Removes provided item from the backpack
    # Size Handling responses TBD - CLI?
    # Params: item_name - str - name of the item to be removed from the backpack
    # Returns: None
    def remove_item_from_backpack(self, item_name):
        for item in self.__backpack:
            item_info = item.get_info()
            if item_info.name == item_name:
                self.__backpack.remove(item)
                break

    # Handle Death
    # Handles death of entity in combat
    # Params:   None
    # Returns:  None
    def handle_death(self):
        # self.__health = 0
        # Assign "Dead" to temp_buffs
        self.__temp_buffs.append(dl.DEAD_STATUS.copy())

    # Move To
    # Moves entity to given coordinates
    # Params:   x, y - ints - coordinates
    # Returns:  None
    def move_to(self, x, y):
        self.__position = [x, y]

    # Attack Entity
    # Current entity attacks given entity
    # Called after all variables and entities have been validated
    # Params:   self - Entity - One who is attacking
    #           target - Entity - One being attacked
    # Return:   damage - int - damage dealt to the defender
    def attack_entity(self, target):
        # Get damage dealt
        damage = max(1, (self.__attack - target.__defence))
        # Subtract health from defender with max at 0 - prevents underflow
        target.__health = max(0, (target.__health - damage))
        # Handle target death
        if target.__health == 0:
            target.handle_death()
        # return damage for success message
        return damage

    # Is Alive
    # Checks entity to see if they are alive
    # used for CLI command checks
    # Params: None
    # Retunrs: Bool - bool - True if entity is alive / False if entity is dead
    def is_alive(self):
        # check temp buffs for "Dead" status
        for buff in self.__temp_buffs:
            if buff["Name"] == "Dead":
                return False
        return True

    # Is Alive From Info
    # Checks entity info temp buffs to see if they are alive
    # Protects entity from being modified by CLI commands - is_alive still has use
    # in functions where entity is being modified and is not just being checked by CLI commands
    # Params: None
    # Retunrs: Bool - bool - True if entity is alive / False if entity is dead
    def is_alive_from_info(entity_info):
        # check temp buffs for "Dead" status
        for buff in entity_info.temp_buffs:
            buff_info = dict(buff)
            if buff_info["Name"] == "Dead":
                return False
        return True

    # Update Single Stat
    # Updates a single stat of the entity with given value
    # Params:   stat - string - stat to be updated
    #           value - int - value to be set to the stat
    # Return:   None
    def update_single_stat(self, stat, value):
        match stat.lower():
            case "health":
                self.__health = value
            case "max_health":
                self.__max_health = value
            case "attack":
                self.__attack = value
            case "defence":
                self.__defence = value
            case "speed":
                self.__speed = value

    # Add Temp Buff
    # Adds temp buff to entity
    # Params:   buff - dict - includes all buff attributes (name, effects, duration)
    # Return:   None
    def add_temp_buff(self, buff):
        self.__temp_buffs.append(buff)

    # Memento DataClass
    @dataclass(frozen=True)
    class Memento:
        entity_id: int
        e_type: str
        position: object
        health: int
        max_health: int
        attack: int
        defence: int
        speed: int
        inventory: object
        active_modifiers: object
        backpack: object
        attack_type: object
        temp_buffs: object

    # Create Memento
    # Create entity memento
    # Params:   None
    # Returns Entity Memento
    def create_memento(self):
        return Entity.Memento(
            entity_id=self.__id,
            e_type=self.__e_type,
            position=deepcopy(self.__position),
            health=self.__health,
            max_health=self.__max_health,
            attack=self.__attack,
            defence=self.__defence,
            speed=self.__speed,
            inventory=deepcopy(self.__inventory),
            active_modifiers=deepcopy(self.__active_modifiers),
            backpack=deepcopy(self.__backpack),
            attack_type=self.__attack_type,
            temp_buffs=deepcopy(self.__temp_buffs),
        )

    # Restore
    # Restores entity based on memento
    # Params: Memento - Memento - entity info pulled from save file
    # Returns: None
    def restore(self, memento):
        if not isinstance(memento, Entity.Memento):
            raise TypeError("Invalid Entity memento")

        self.__id = memento.entity_id
        self.__e_type = memento.e_type
        self.__position = list(memento.position)
        self.__health = memento.health
        self.__max_health = memento.max_health
        self.__attack = memento.attack
        self.__defence = memento.defence
        self.__speed = memento.speed
        self.__inventory = deepcopy(memento.inventory)
        self.__active_modifiers = deepcopy(memento.active_modifiers)
        self.__backpack = list(deepcopy(memento.backpack))
        self.__attack_type = memento.attack_type
        self.__temp_buffs = deepcopy(memento.temp_buffs)

    """# id
    # Solves issues with accessing if of mage which inherits from Entity
    # Params: None
    # Returns: id of entity
    @property
    def id(self):
        return self.__id"""


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


# Data class for Mage stats
@dataclass
class MageInfo:
    id: int
    e_type: str
    position: tuple
    health: int
    max_health: int
    mana: int
    max_mana: int
    spell_power: int
    attack: int
    defence: int
    speed: int
    active_modifiers: tuple  # tuple of two dictionaries - flat and percent modifiers
    backpack: tuple
    attack_type: str
    temp_buffs: tuple


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
        self.__mana = self.BASE_STATS["Mana"]
        self.__max_mana = self.BASE_STATS["Mana"]
        self.__spell_power = self.BASE_STATS["Spell_power"]
        # self.__temp_buffs = []  # temp buffs list of dictionarys

    # Get Info
    # Gets all relevant info of the entity and returns them
    # Params: None
    # Returns: MageStats - all info for current mage
    def get_info(self):
        entity_info = super().get_info()
        return MageInfo(
            id=entity_info.id,
            e_type=entity_info.e_type,
            position=entity_info.position,
            health=entity_info.health,
            max_health=entity_info.max_health,
            mana=self.__mana,
            max_mana=self.__max_mana,
            spell_power=self.__spell_power,
            attack=entity_info.attack,
            defence=entity_info.defence,
            speed=entity_info.speed,
            active_modifiers=entity_info.active_modifiers,
            backpack=entity_info.backpack,
            attack_type=entity_info.attack_type,
            temp_buffs=entity_info.temp_buffs,
        )

    # Mage Memento
    @dataclass(frozen=True)
    class Memento:
        entity_memento: Entity.Memento
        mana: int
        max_mana: int
        spell_power: int

    # Create Memento
    # Create mage memento
    # Params:   None
    # Returns Mage Memento
    def create_memento(self):
        return Mage.Memento(
            entity_memento=super().create_memento(),
            mana=self.__mana,
            max_mana=self.__max_mana,
            spell_power=self.__spell_power,
        )

    # Restore
    # Restores mage based on memento
    # Params: Memento - Memento - mage info pulled from save file
    # Returns: None
    def restore(self, memento):
        if not isinstance(memento, Mage.Memento):
            raise TypeError("Invalid Mage memento")

        # Restore inherited Entity state
        super().restore(memento.entity_memento)

        # Restore Mage-specific state
        self.__mana = memento.mana
        self.__max_mana = memento.max_mana
        self.__spell_power = memento.spell_power

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    # Params: None
    # Return: None
    def reset_stats(self):
        self.__health = self.BASE_STATS["Health"]
        self.__max_health = self.BASE_STATS["Health"]
        self.__attack = self.BASE_STATS["Attack"]
        self.__defence = self.BASE_STATS["Defence"]
        self.__speed = self.BASE_STATS["Speed"]
        self.__mana = self.BASE_STATS["Mana"]
        self.__max_mana = self.BASE_STATS["Mana"]
        self.__spell_power = self.BASE_STATS["Spell_power"]

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
            temp_value = self.get_stat(stat)
            # If flat values exist
            if stat in self._Entity__active_modifiers["Flat_modifiers"]:
                temp_value += self._Entity__active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self._Entity__active_modifiers["Percent_modifiers"]:
                temp_percent_value = self._Entity__active_modifiers[
                    "Percent_modifiers"
                ][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            self.update_single_stat(stat.lower(), temp_value)

    # Calculate Final Stats End

    # NEEDS CLEANER IMPLEMENTATIO WITHOUT NAME MANGLING
    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    # Params: game_state - Game state from cli - Current active game objects/features
    # Return: None
    def update_stats(self, game_state):
        super().update_stats(game_state)

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
            if stat in self._Entity__active_modifiers["Flat_modifiers"]:
                temp_value += self._Entity__active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self._Entity__active_modifiers["Percent_modifiers"]:
                temp_percent_value = self._Entity__active_modifiers[
                    "Percent_modifiers"
                ][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update max stats
            if stat == "Health":
                self.__max_health = temp_value

            elif stat == "Mana":
                self.__max_mana = temp_value

    # Update Single Stat
    # Updates a single stat of the entity with given value
    # Params:   stat - string - stat to be updated
    #           value - int - value to be set to the stat
    # Return:   None
    def update_single_stat(self, stat, value):
        match stat.lower():
            case "health":
                self.__health = value
            case "max_health":
                self.__max_health = value
            case "mana":
                self.__mana = value
            case "max_mana":
                self.__max_mana = value
            case "attack":
                self.__attack = value
            case "defence":
                self.__defence = value
            case "speed":
                self.__speed = value
            case "spell_power":
                self.__spell_power = value

    # Get Stat
    # Gets given stat value of entity
    # Only called on real objects within this file - editing the actual entity
    # Params:   stat - string - stat to get
    # Return:   value - int - stat value
    def get_stat(self, stat):
        match stat:
            case "Health":
                return self.__health

                """case "Max Health":
                return self.__max_health"""

            case "Mana":
                return self.__mana
            case "Spell_power":
                return self.__spell_power

            case "Attack":
                return self.__attack
            case "Defence":
                return self.__defence
            case "Speed":
                return self.__speed


# Entities Factory
# Create Entity
# Creates entity with base stats and values based on the entity
# Holds base stats for all of the entities
# Params:   e_type - str - Type of entity to create
#           x, y - int - Coordinates to spawn entity at
#           e_id - int - ID generated for entity
# Returns:  Entity instance of the specified type, or None if invalid
def create_entity(e_type, x, y, e_id):
    # Ensure correct typing
    try:
        e_type = str(e_type).lower()
        x = int(x)
        y = int(y)
    except (TypeError, ValueError):
        print(f"error: spawn_failed x ({x}) and/or y ({y}) are not integers!")
        return None

    # Create entity based on type
    match e_type:
        case "warrior":
            entity = Warrior(e_id, [x, y])

        case "mage":
            entity = Mage(e_id, [x, y])

        case "skeleton":
            entity = Skeleton(e_id, [x, y])

        case "goblin":
            entity = Goblin(e_id, [x, y])

        case _:
            # Invalid entity type
            return None

    # Correct entity information before returning to game state
    entity.__temp_buffs = []

    return entity
