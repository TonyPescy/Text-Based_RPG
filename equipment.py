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


# Equipment class with all methods needed for equipment
class Equipment:
    # Initilize Equipment class with name, slot, effects
    def __init__(self, name, slot, effects):
        self.name = name
        self.slot = slot
        self.effects = effects


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

        self.instant_effects = instant_effects
        self.over_time_effects = over_time_effects
        self.duration = duration


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
