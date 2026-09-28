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
# Equipment Types Dictionary
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

    return equipment_type()  # Return initialized item


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


# Use Consumable
# Uses the current consumable - Inputs cleaned in CLI - MAKE SURE ITEM IN BACKPACK
# Params: consumable - Consumable instance - Consumable to be used
#         entity - Entity instance - entity using the item
# Return: None
def use_consumable(
    consumable,
    entity,
):
    # Apply instant effects
    for modifier_type, modifiers in consumable.instant_effects.items():

        # Flat modifiers
        if modifier_type == "Flat_modifiers":
            for stat, amount in modifiers.items():

                # Convert modifier amount to int
                amount = int(amount)
                # Get current stat
                current_value = getattr(entity, stat.lower())
                # Calculate new stat
                new_value = current_value + amount

                # Prevent oveflow of health/mana
                # max
                max_stat = None
                if stat == "Health":
                    max_stat = entity.max_health
                elif stat == "Mana" and hasattr(entity, "max_mana"):
                    max_stat = entity.max_mana
                # Prevent overflow
                if max_stat is not None:
                    new_value = min(new_value, max_stat)

                # Apply the new value
                setattr(entity, stat.lower(), new_value)

        # Percent modifiers
        elif modifier_type == "Percent_modifiers":
            for stat, amount in modifiers.items():

                # Convert percentage to int
                amount = int(amount)
                # Get current stat
                current_value = getattr(entity, stat.lower())
                # Calculate percentage change
                modifier = current_value * (amount / 100)
                # Calculate new stat
                new_value = int(current_value + modifier)

                # Prevent overflow of health/mana
                # max
                max_stat = None
                if stat == "Health":
                    max_stat = entity.max_health

                elif stat == "Mana" and hasattr(entity, "max_mana"):
                    max_stat = entity.max_mana

                # Prevent stat from exceeding its maximum
                if max_stat is not None:
                    new_value = min(new_value, max_stat)

                # Apply the new value
                setattr(entity, stat.lower(), new_value)

        # Add over time effects as a temp buff
        if consumable.over_time_effects and consumable.duration > 0:
            # Store temp buff
            entity.temp_buffs.append(
                {
                    "Name": consumable.name,
                    "Effects": consumable.over_time_effects,
                    "Turns": consumable.duration,
                }
            )


# NO TIME ADDED YET, SO THIS IS  A PLACEHOLDER - WILL NEED TESTS WHEN TIME IS ADDED AS WELL
# Process temp buffs
# Processes the temp buffs on the entity
# Params: entity - Entity instance - entity whose buffs are being processed
#         cli - current cli instance - houses entity max stats and entity temp buffs
# Return: None
def process_temp_buffs(entity, cli):

    # Get temporary buffs for entity
    temp_buffs = cli.entity_temp_buffs.get(entity.id, [])

    # Get max stats for entity
    max_stats = cli.entity_max_stats.get(entity.id, {})

    # Process temp buffS
    for buff in temp_buffs:

        # Get effects from buff
        effects = buff["Effects"]

        # Process each modifier type
        for modifier_type, modifiers in effects.items():

            # Process each stat modifier
            for stat, amount in modifiers.items():

                # Convert to int
                amount = int(amount)
                # Get current stat
                current_value = getattr(entity, stat)

                # Flat modifiers
                if modifier_type == "Flat_modifiers":

                    # Calculate new stat
                    new_value = current_value + amount

                # Percent modifiers
                elif modifier_type == "Percent_modifiers":

                    # Calculate percentage change
                    modifier = current_value * (amount / 100)
                    # Calculate new stat
                    new_value = int(current_value + modifier)

                else:
                    continue

                # Prevent stat from exceeding its maximum
                if stat in max_stats:
                    new_value = min(new_value, max_stats[stat])

                # Apply modifier
                setattr(entity, stat, new_value)

        # Reduce remaining duration
        buff["Turns"] -= 1

    # Remove expired buffs
    cli.entity_temp_buffs[entity.id] = [
        buff for buff in temp_buffs if buff["Turns"] > 0
    ]
