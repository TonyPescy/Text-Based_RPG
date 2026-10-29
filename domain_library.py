"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 3, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: domain_library.py
Purpose: Houses all private facing functions that will be used to run the game, setup, and complete all of the user inputted commands
"""

# Imports
import equipment
from enum import Enum

# Constants


# Enums for equipment slots
class EquipmentSlot(Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    ACCESSORY = "Accessory"


# Inventory slot indexes enum
class EquipmentSlotIndex(Enum):
    WEAPON = 0
    ARMOR = 1
    ACCESSORY = 2


# Attack Types Constants Enums
class AttackTypes(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"


# Attack Types Constants
MELEE_RANGE = 1
RANGED_RANGE = 3  # May want to restrict to be 2-3 only not 1-3 so it doesnt completely outclass melee


# Spell Type enums
class SpellTypes(Enum):
    OFFENSIVE = "Offensive"
    SUPPORT = "Support"
    CONTROL = "Control"


# Spell Effects enums - Easier to add spells here
class SpellEffects(Enum):
    FROSTBOLT = "Frostbolt"


# Base Invetory for all Entities
BASE_INVENTORY = [
    equipment.create_equipment("none_wep"),
    equipment.create_equipment("none_armor"),
    equipment.create_equipment("none_acc"),
]

# Dead Status for corpses of entities - used in Temp Buffs on entity
# Will need to be removed with revivals
DEAD_STATUS = {
    "Name": "Dead",
    "Effects": {"Flat_modifiers": {}, "Percent_modifiers": {}},
    "Turns": 3,
}


# Is Valid Entity
# Checks to see if input is a valid entity type
# Params:   entity_type - str - Entity name
# Returns:  bool
def is_valid_entity(entity_type):
    # Check if entity type is valid
    if not isinstance(entity_type, str):
        return False

    # Check if entity name is valid
    return entity_type.lower() in (
        "warrior",
        "mage",
        "skeleton",
        "goblin",
    )


# Is Valid Spell
# Checks if the given spell name is valid
# Params:   spell_name - str - Name of spell
# Returns:  bool
def is_valid_spell(spell_name):
    # Check if spell name is valid
    if not isinstance(spell_name, str):
        return False

    # Check if spell name exists
    return spell_name.lower() in (
        "fireball",
        "heal",
        "frostbolt",
    )


# Are Valid Ints
# Checks to see if x and y are valid ints
# Params: x/y - ints
# Returns: bool
def are_valid_ints(x, y):
    # Try except for width/height typing
    try:
        int(x)
        int(y)
    except:  # Return error for proper error message
        return False
    return True
