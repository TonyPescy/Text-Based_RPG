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

# from equipment import Equipment

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
}
# Valid Equipment Slots
VALID_SLOTS = ("Weapon", "Armor", "Accessory")

# Entity Types Constant
# Entity Constants
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


# Entities Factories
"""     THIS IS AN EXAMPLE OF THE FACTORY
def create_entity(e_type, x, y):

    match e_type:
        case "warrior":
            return Warrior(x, y)

        case "mage":
            return Mage(x, y)

        case "skeleton":
            return Skeleton(x, y)

        case "goblin":
            return Goblin(x, y)
"""
