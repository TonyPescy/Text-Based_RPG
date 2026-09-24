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
