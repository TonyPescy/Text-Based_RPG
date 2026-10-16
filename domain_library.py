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
"""# Equipment Types Dictionary - CHANGE TO MATCH SPELL NAMES
EQUIPMENT_TYPES = {
    "ironsword": equipment.IronSword,
    "curseddagger": equipment.CursedDagger,
    "magestaff": equipment.MageStaff,
    "ironchestplate": equipment.IronChestplate,
    "leathertunic": equipment.LeatherTunic,
    "scoutarmor": equipment.ScoutArmor,
    "ringofthesorcerer": equipment.RingOfTheSorcerer,
    "amuletofvitality": equipment.AmuletOfVitality,
    "ringofhaste": equipment.RingOfHaste,
    "none_wep": equipment.NoneWeapon,
    "none_armor": equipment.NoneArmor,
    "none_acc": equipment.NoneAccessory,
    "smallhealthpotion": equipment.SmallHealthPotion,
    "greaterhealthpotion": equipment.GreaterHealthPotion,
    "superiorhealthpotion": equipment.SuperiorHealthPotion,
    "manapotion": equipment.ManaPotion,
    "turtlemasterpotion": equipment.TurtleMasterPotion,
}

"""


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


# Valid consumables Enums
class ConsumableType(Enum):
    SMALL_HEALTH_POTION = "smallhealthpotion"
    GREATER_HEALTH_POTION = "greaterhealthpotion"
    SUPERIOR_HEALTH_POTION = "superiorhealthpotion"
    MANA_POTION = "manapotion"
    TURTLE_MASTER_POTION = "turtlemasterpotion"


# Entity Types Constant
# Entity Constants enum
class EntityType(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    SKELETON = "Skeleton"
    GOBLIN = "Goblin"


# Attack Types Constants Enums
class AttackTypes(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"


# Attack Types Constants
MELEE_RANGE = 1
RANGED_RANGE = 3  # May want to restrict to be 2-3 only not 1-3 so it doesnt completely outclass melee


# Spell name enums
class SpellNames(Enum):
    FIREBALL = "Fireball"
    HEAL = "Heal"
    FROSTBOLT = "Frostbolt"


# Spell Type enums
class SpellTypes(Enum):
    OFFENSIVE = "Offensive"
    SUPPORT = "Support"
    CONTROL = "Control"


"""# Equipment Factory Start
# Used to create all of the equipment based on item_name provided
# Params: item_name - string - name of item to be created
# Returns: Initialized matching item
def create_equipment(item_name):
    # Get item from equipment types dictionary
    equipment_type = EQUIPMENT_TYPES.get(item_name)

    # Check for error finding item with given name
    if equipment_type is None:
        return None  # Handle error on other end

    return equipment_type()  # Return initialized item"""


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


# Is Valid Entity Start # MOVE TO D_LIB
# Checks to see input is a valid entity type
# Params: entity_type - string - entity name
# Returns: Bool
def is_valid_entity(entity_type):
    if entity_type.lower() in [e_type.value.lower() for e_type in EntityType]:
        return True
    else:
        # print("error: Entity Type added is not a valid entity type!")
        return False


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
