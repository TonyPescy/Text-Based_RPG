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

# Constants
# Equipment Types Dictionary
EQUIPMENT_TYPES = {
    "ironsword": equipment.IronSword(),
    "curseddagger": equipment.CursedDagger(),
    "magestaff": equipment.MageStaff(),
    "ironchestplate": equipment.IronChestplate(),
    "leathertunic": equipment.LeatherTunic(),
    "scoutarmor": equipment.ScoutArmor(),
    "ringofthesorcerer": equipment.RingOfTheSorcerer(),
    "amuletofvitality": equipment.AmuletOfVitality(),
    "ringofhaste": equipment.RingOfHaste(),
    "none_wep": equipment.NoneWeapon(),
    "none_armor": equipment.NoneArmor(),
    "none_acc": equipment.NoneAccessory(),
    "smallhealthpotion": equipment.SmallHealthPotion(),
    "greaterhealthpotion": equipment.GreaterHealthPotion(),
    "superiorhealthpotion": equipment.SuperiorHealthPotion(),
    "manapotion": equipment.ManaPotion(),
    "turtlemasterpotion": equipment.TurtleMasterPotion(),
}
# Valid Equipment Slots MAKE INTO AN ENUM
VALID_SLOTS = ("Weapon", "Armor", "Accessory")

# Entity Types Constant
# Entity Constants MAKE INTO AN ENUM
ENTITY_TYPES = ("Warrior", "Mage", "Skeleton", "Goblin")


# Equipment Factory Start
# Used to create all of the equipment based on item_name provided
# Params: item_name - string - name of item to be created
# Returns: Initialized matching item
def create_equipment(item_name):
    # Get item from equipment types dictionary
    equipment_type = EQUIPMENT_TYPES.get(item_name)

    # Check for error finding item with given name
    if equipment_type is None:
        return None  # Handle error on other end

    return equipment_type  # Return initialized item


# Base Invetory for all Entities
BASE_INVENTORY = [
    create_equipment("none_wep"),
    create_equipment("none_armor"),
    create_equipment("none_acc"),
]


# Is Valid Entity Start # MOVE TO D_LIB
# Checks to see input is a valid entity type
# Params: entity_type - string - entity name
# Returns: Bool
def is_valid_entity(entity_type):
    if entity_type in [e_type.lower() for e_type in ENTITY_TYPES]:
        return True
    else:
        print("error: Tile Type added is not a valid tile type!")
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
