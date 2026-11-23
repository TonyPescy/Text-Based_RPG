"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: equipment.py
Purpose: Houses all functions necessary for proper equipment handling and logic in the game
"""

# Imports
from dataclasses import dataclass


# Data Classes for equipment and all equipment classes
@dataclass
class EquipmentInfo:
    name: str
    slot: str
    rarity: str
    effects: dict


@dataclass
class ConsumableInfo:
    name: str
    rarity: str
    instant_effects: tuple
    over_time_effects: tuple
    duration: int


# Equipment Memento Data Class
@dataclass
class EquipmentMemento:
    name: str
    slot: str
    rarity: str
    rolled_effects: tuple[
        tuple[str, int], ...
    ]  # Tuple of tuples: [ [stat_effected, effect_value] ]


# Equipment class with all methods needed for equipment
class Equipment:
    # Initilize Equipment class with name, slot, effects
    def __init__(self, name, slot, effects):
        self.__name = name
        self.__slot = slot
        self.__effects = effects

        # Default rarity and rolled effects - PLACEHOLDERS UNTIL PROPER RARITY IMPLEMENTATION
        self.__rarity = "Common"
        self.__rolled_effects = {}

    # Get Info
    # Returns a EquipmentInfo object of the equipment's information
    # Params: None
    # Returns: EquipmentInfo - Equipment information
    def get_info(self):
        return EquipmentInfo(
            name=self.__name,
            slot=self.__slot,
            effects=tuple(self.__effects.items()),
            rarity=self.__rarity,
        )

    # Name
    # Solves issues with accessing name of consumble which inherits from equipment
    # Params: None
    # Returns: name of consumble/equipment
    @property
    def name(self):
        return self.__name

    # Slot
    # Solves issues with accessing slot of consumble which inherits from equipment
    # Params: None
    # Returns: slot of consumble/equipment
    @property
    def slot(self):
        return self.__slot

    # Effects
    # Solves issues with accessing effects of consumble which inherits from equipment
    # Params: None
    # Returns: effect of consumble/equipment
    @property
    def effects(self):
        return self.__effects

    # Create Memento
    # Creates equipment memento from equipment
    # Params: None
    # Returns: equipment_memento - EquipmentMemento
    def create_memento(self):
        return EquipmentMemento(
            name=self.__name,
            slot=self.__slot,
            rarity=self.__rarity,
            rolled_effects=tuple(self.__rolled_effects.items()),
        )

    # Restore Memento
    # Restores equipment state from a memento
    # Params: memento - EquipmentMemento
    # Returns: None
    def restore(self, memento):
        if not isinstance(memento, EquipmentMemento):
            raise TypeError("Invalid Equipment Memento")

        self.__name = memento.name
        self.__rarity = memento.rarity
        self.__rolled_effects = dict(memento.rolled_effects)


# None Equipment Classes
# None Weapon Class - Inherits from equipment
class NoneWeapon(Equipment):
    # Initialize with "base" stats
    def __init__(self):
        super().__init__("None", "Weapon", {})


# None Weapon Class - Inherits from equipment
class NoneArmor(Equipment):
    # Initialize with "base" stats
    def __init__(self):
        super().__init__("None", "Armor", {})


# None Weapon Class - Inherits from equipment
class NoneAccessory(Equipment):
    # Initialize with "base" stats
    def __init__(self):
        super().__init__("None", "Accessory", {})


# Weapon Classes
# Iron Sword Class - inherits from equipment
class IronSword(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "IronSword",
            "Weapon",
            {"Attack": "+12"},
        )


# Cursed Dagger Class - inherits from equipment
class CursedDagger(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "CursedDagger",
            "Weapon",
            {"Attack": "+18", "Defence": "-5"},
        )


# Mage Staff Class - inherits from equipment
class MageStaff(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "MageStaff",
            "Weapon",
            {"Spell_power": "+5"},
        )


# Armor Classes
# Iron Chestplate Class - inherits from equipment
class IronChestplate(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "IronChestplate",
            "Armor",
            {"Defence": "+15", "Speed": "-2"},
        )


# Leather Tunic Class - inherits from equipment
class LeatherTunic(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "LeatherTunic",
            "Armor",
            {"Defence": "+5"},
        )


# Scout Armor Class - inherits from equipment
class ScoutArmor(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "ScoutArmor",
            "Armor",
            {"Defence": "+3", "Speed": "+10%"},
        )


# Accessory Classes
# Ring of the Sorcerer Class - inherits from equipment
class RingOfTheSorcerer(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "RingOfTheSorcerer",
            "Accessory",
            {"Spell_power": "+5", "Mana": "+15%"},
        )


# Amulet of Vitality Class - inherits from equipment
class AmuletOfVitality(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "AmuletOfVitality",
            "Accessory",
            {"Health": "+10%", "Defence": "+3"},
        )


# Ring of Haste Class - inherits from equipment
class RingOfHaste(Equipment):
    # Initialize with base stats
    def __init__(self):
        super().__init__(
            "RingOfHaste",
            "Accessory",
            {"Speed": "+2"},
        )


# Consumable Memento Data Class
@dataclass(frozen=True)
class ConsumableMemento:
    equipment_memento: EquipmentMemento
    instant_effects: tuple[
        tuple[str, tuple[tuple[str, int | float], ...]], ...
    ]  # Tuples cubed:  [ flat_effects: [stat_effected, effect_value], percent_effects: [stat_effected, effect_value] ]
    over_time_effects: tuple[
        tuple[str, tuple[tuple[str, int | float], ...]], ...
    ]  # Tuples cubed:  [ flat_effects: [stat_effected, effect_value], percent_effects: [stat_effected, effect_value] ]
    duration: int


# Consumable Class - Inherits from Equipment
# Has different effect types - instant/over_time as well as percent/flat modifiers
class Consumable(Equipment):
    def __init__(self, name, instant_effects=None, over_time_effects=None, duration=0):
        super().__init__(name, "Consumable", {})
        # effect types
        if instant_effects is None:
            instant_effects = {"Flat_modifiers": {}, "Percent_modifiers": {}}
        if over_time_effects is None:
            over_time_effects = {"Flat_modifiers": {}, "Percent_modifiers": {}}

        self.__instant_effects = instant_effects
        self.__over_time_effects = over_time_effects
        self.__duration = duration

    # Get Info
    # Returns a ConsumableInfo object of the consumable's information
    # Params: None
    # Returns: ConsumableInfo - Consumable information
    def get_info(self):
        equipment_info = super().get_info()
        consumable_rarity = equipment_info.rarity
        return ConsumableInfo(
            name=self.name,
            rarity=consumable_rarity,
            instant_effects=(
                (
                    "Flat_modifiers",
                    tuple(self.__instant_effects["Flat_modifiers"].items()),
                ),
                (
                    "Percent_modifiers",
                    tuple(self.__instant_effects["Percent_modifiers"].items()),
                ),
            ),
            over_time_effects=(
                (
                    "Flat_modifiers",
                    tuple(self.__over_time_effects["Flat_modifiers"].items()),
                ),
                (
                    "Percent_modifiers",
                    tuple(self.__over_time_effects["Percent_modifiers"].items()),
                ),
            ),
            duration=self.__duration,
        )

    # Use Consumable
    # Uses the current consumable - Inputs cleaned in CLI - MAKE SURE ITEM IN BACKPACK
    # Params:   consumable - Consumable instance - Consumable to be used
    #           entity - Entity instance - entity using the item
    #           game_state - GameState instance - current game state for entity and item management
    # Return: None
    def use_consumable(
        consumable,
        entity,
        game_state,
    ):
        entity_info = entity.get_info()
        # Apply instant effects
        for modifier_type, modifiers in consumable.__instant_effects.items():

            # Flat modifiers
            if modifier_type == "Flat_modifiers":
                for stat, amount in modifiers.items():
                    stat = stat.lower()
                    # Convert modifier amount to int
                    amount = int(amount)
                    print(amount)
                    # Check if entity has the stat
                    if not hasattr(entity_info, stat.lower()):
                        continue
                    # Get current stat
                    current_value = getattr(entity_info, stat.lower())
                    # Calculate new stat
                    new_value = current_value + amount
                    # Debug health values
                    print(f"DEBUG - Current health: {entity_info.health}")
                    print(f"DEBUG - Potion amount: {amount}")
                    print(f"DEBUG - Calculated health: {new_value}")
                    # Prevent oveflow of health/mana
                    # max
                    max_stat = None
                    if stat == "health":
                        max_stat = entity_info.max_health
                    elif stat == "mana":
                        max_stat = getattr(entity_info, "max_mana", None)
                    # Prevent overflow
                    if max_stat is not None:
                        new_value = min(new_value, max_stat)

                    # Apply the new value
                    game_state.update_single_entity_stat(
                        entity_info.id, stat.lower(), new_value
                    )

            # Percent modifiers
            elif modifier_type == "Percent_modifiers":
                for stat, amount in modifiers.items():
                    stat = stat.lower()
                    # Convert percentage to int
                    amount = int(amount)
                    print(amount)
                    # Get current stat
                    current_value = getattr(entity_info, stat.lower())
                    # Calculate percentage change
                    modifier = current_value * (amount / 100)
                    # Calculate new stat
                    new_value = int(current_value + modifier)
                    # Debug health values
                    print(f"DEBUG - Current health: {entity_info.health}")
                    print(f"DEBUG - Potion amount: {amount}")
                    print(f"DEBUG - Calculated health: {new_value}")
                    # Prevent overflow of health/mana
                    # max
                    max_stat = None
                    if stat == "health":
                        max_stat = entity_info.max_health

                    elif stat == "mana":
                        max_stat = getattr(entity_info, "max_mana", None)
                    # Prevent stat from exceeding its maximum
                    if max_stat is not None:
                        new_value = min(new_value, max_stat)

                    # Apply the new value
                    game_state.update_single_entity_stat(
                        entity_info.id, stat.lower(), new_value
                    )
            entity_info = entity.get_info()
            print(f"DEBUG - Updated health: {entity_info.health}")

            # Add over time effects as a temp buff
            if consumable.__over_time_effects and consumable.__duration > 0:
                # Create formatted buff
                buff = {
                    "Name": consumable.name,
                    "Effects": consumable.__over_time_effects,
                    "Turns": consumable.__duration,
                }
                # Store temp buff
                game_state.add_temp_buff_to_entity(entity_info.id, buff)
                """entity.__temp_buffs.append(
                    {
                        "Name": consumable.__name,
                        "Effects": consumable.__over_time_effects,
                        "Turns": consumable.__duration,
                    }
                )"""

    # Create Consumable Memento
    # Saves the current consumable state
    # Params: None
    # Returns: ConsumableMemento
    def create_memento(self):
        return ConsumableMemento(
            equipment_memento=super().create_memento(),
            instant_effects=(
                (
                    "Flat_modifiers",
                    tuple(self.__instant_effects["Flat_modifiers"].items()),
                ),
                (
                    "Percent_modifiers",
                    tuple(self.__instant_effects["Percent_modifiers"].items()),
                ),
            ),
            over_time_effects=(
                (
                    "Flat_modifiers",
                    tuple(self.__over_time_effects["Flat_modifiers"].items()),
                ),
                (
                    "Percent_modifiers",
                    tuple(self.__over_time_effects["Percent_modifiers"].items()),
                ),
            ),
            duration=self.__duration,
        )

    # Restore Consumable Memento
    # Restores consumable state from a memento
    # Params: memento - ConsumableMemento
    # Returns: None
    def restore(self, memento):
        # Restore inherited equipment state
        super().restore(memento.equipment_memento)

        # Restore instant effects
        self.__instant_effects = {
            effect_type: dict(effects)
            for effect_type, effects in memento.instant_effects
        }

        # Restore over time effects
        self.__over_time_effects = {
            effect_type: dict(effects)
            for effect_type, effects in memento.over_time_effects
        }

        # Restore duration
        self.__duration = memento.duration


# Small Health Potion Class - Inherits from Consumable Class
class SmallHealthPotion(Consumable):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "SmallHealthPotion",
            instant_effects={
                "Flat_modifiers": {"Health": "20"},
                "Percent_modifiers": {},
            },
        )


# Greater Health Potion Class - Inherits from Consumable Class
class GreaterHealthPotion(Consumable):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "GreaterHealthPotion",
            instant_effects={
                "Flat_modifiers": {"Health": "50"},
                "Percent_modifiers": {},
            },
        )


# Greater Health Potion Class - Inherits from Consumable Class
class SuperiorHealthPotion(Consumable):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "SuperiorHealthPotion",
            instant_effects={
                "Flat_modifiers": {"Health": "100"},
                "Percent_modifiers": {},
            },
        )


# Mana Potion Class - Inherits from Consumable Class
class ManaPotion(Consumable):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "ManaPotion",
            instant_effects={
                "Flat_modifiers": {"Mana": "50"},
                "Percent_modifiers": {},
            },
        )


# Greater Health Potion Class - Inherits from Consumable Class
class TurtleMasterPotion(Consumable):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "TurtleMasterPotion",
            instant_effects={
                "Flat_modifiers": {},
                "Percent_modifiers": {"Health": "10"},
            },
            over_time_effects={
                "Flat_modifiers": {"Speed": "-3", "Defence": "10"},
                "Percent_modifiers": {"Health": "10", "Defence": "20"},
            },
            duration=5,
        )


# Create Equipment
# Creates an equipment object based on the given equipment name
# Params:   equipment_name - str - Name of equipment to create
# Returns:  Equipment object if valid, otherwise None
def create_equipment(equipment_name):
    # Normalize equipment name
    equipment_name = equipment_name.lower()

    # Create equipment based on name
    if equipment_name == "ironsword":
        return IronSword()
    elif equipment_name == "curseddagger":
        return CursedDagger()
    elif equipment_name == "magestaff":
        return MageStaff()
    elif equipment_name == "ironchestplate":
        return IronChestplate()
    elif equipment_name == "leathertunic":
        return LeatherTunic()
    elif equipment_name == "scoutarmor":
        return ScoutArmor()
    elif equipment_name == "ringofthesorcerer":
        return RingOfTheSorcerer()
    elif equipment_name == "amuletofvitality":
        return AmuletOfVitality()
    elif equipment_name == "ringofhaste":
        return RingOfHaste()
    elif equipment_name == "none_wep":
        return NoneWeapon()
    elif equipment_name == "none_armor":
        return NoneArmor()
    elif equipment_name == "none_acc":
        return NoneAccessory()
    elif equipment_name == "smallhealthpotion":
        return SmallHealthPotion()
    elif equipment_name == "greaterhealthpotion":
        return GreaterHealthPotion()
    elif equipment_name == "superiorhealthpotion":
        return SuperiorHealthPotion()
    elif equipment_name == "manapotion":
        return ManaPotion()
    elif equipment_name == "turtlemasterpotion":
        return TurtleMasterPotion()

    # Invalid equipment name
    return None


# Get Equipment Names
# Gets all valid equipment names
# Params: None
# Returns: tuple - All valid equipment names
def get_equipment_names():
    return (
        "ironsword",
        "curseddagger",
        "magestaff",
        "ironchestplate",
        "leathertunic",
        "scoutarmor",
        "ringofthesorcerer",
        "amuletofvitality",
        "ringofhaste",
        "none_wep",
        "none_armor",
        "none_acc",
        "smallhealthpotion",
        "greaterhealthpotion",
        "superiorhealthpotion",
        "manapotion",
        "turtlemasterpotion",
    )
