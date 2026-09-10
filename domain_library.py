# Create Methods - Used to create instances of the classes above
# Create Entity Start
# Creates entity with base stats and values based on the entity
# Holds base stats for all of the entities
# Params: e_type - String - Type of entity to create
#       x,y - int - Coordinates to spawn entity at
def create_entity(e_type, x, y):
    # Case statement to match to every entity type in game
    match e_type:
        # Warrior
        case Entity.ENTITY_TYPES(0):
            # Create warrior entity
            temp_entity = Entity(
                Entity.entity_ids_issued,
                Entity.ENTITY_TYPES(0),
                [x, y],
                Entity.WARRIOR_BASE_STATS["Health"],
                Entity.WARRIOR_BASE_STATS["Attack"],
                Entity.WARRIOR_BASE_STATS["Defence"],
                Entity.WARRIOR_BASE_STATS["Speed"],
                Equipment.BASE_INVENTORY,
                {"Flat_modifiers": {}, "Percent_modifiers": {}},  # Empty dictionaries
            )
        # Mage
        case Entity.ENTITY_TYPES(1):
            # Create mage entity
            temp_entity = Entity.Mage(
                Entity.entity_ids_issued,
                Entity.ENTITY_TYPES(1),
                [x, y],
                Entity.Mage.MAGE_BASE_STATS["Health"],
                Entity.Mage.MAGE_BASE_STATS["Attack"],
                Entity.Mage.MAGE_BASE_STATS["Defence"],
                Entity.Mage.MAGE_BASE_STATS["Speed"],
                Equipment.BASE_INVENTORY,
                {"Flat_modifiers": {}, "Percent_modifiers": {}},  # Empty dictionaries
                Entity.Mage.MAGE_BASE_STATS["Mana"],
                Entity.Mage.MAGE_BASE_STATS["Spell_power"],
            )
        # Skeleton
        case Entity.ENTITY_TYPES(2):
            # Create skeleton entity
            temp_entity = Entity(
                Entity.entity_ids_issued,
                Entity.ENTITY_TYPES(2),
                [x, y],
                Entity.SKELETON_BASE_STATS["Health"],
                Entity.SKELETON_BASE_STATS["Attack"],
                Entity.SKELETON_BASE_STATS["Defence"],
                Entity.SKELETON_BASE_STATS["Speed"],
                Equipment.BASE_INVENTORY,
                {"Flat_modifiers": {}, "Percent_modifiers": {}},  # Empty dictionaries
            )
        # Goblin
        case Entity.ENTITY_TYPES(3):
            # Create goblin entity
            temp_entity = Entity(
                Entity.entity_ids_issued,
                Entity.ENTITY_TYPES(3),
                [x, y],
                Entity.GOBLIN_BASE_STATS["Health"],
                Entity.GOBLIN_BASE_STATS["Attack"],
                Entity.GOBLIN_BASE_STATS["Defence"],
                Entity.GOBLIN_BASE_STATS["Speed"],
                Equipment.BASE_INVENTORY,
                {"Flat_modifiers": {}, "Percent_modifiers": {}},  # Empty dictionaries
            )
        case _:  # Error no matching entity type found - May be redundant
            print(
                f"Error: Invalid entity type '{e_type}'. "
                f"Expected one of: {Entity.ENTITY_TYPES}."
            )

    # Increment entity_ids_issued to account for new entity
    Entity.entity_ids_issued += 1
    # Add new entity to entity list
    Entity.entity_list.append(temp_entity)


# Create Entity End


# Create Equipment Start
# Creates equipment with base stats and values based on the equipment
# Holds base stats for all of the equipment
# Params: e_type - String - Equipment to create
def create_equipment(e_type):
    # Match to equipment name
    match e_type:
        # Iron Sword
        case Equipment.VALID_ITEMS(1):
            # Create Iron Sword
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(1), Equipment.VALID_SLOTS(0), {"Attack": "+10"}
            )
        # Cursed Dagger
        case Equipment.VALID_ITEMS(2):
            # Create cursed dagger
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(2),
                Equipment.VALID_SLOTS(0),
                {"Attack": "+18", "Defence": "-5"},
            )
        # Mage Staff
        case Equipment.VALID_ITEMS(3):
            # Create Mage Staff
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(3),
                Equipment.VALID_SLOTS(0),
                {"Spell Power": "+5"},
            )
        # Iron chestplate
        case Equipment.VALID_ITEMS(4):
            # Create iron chestplate
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(4),
                Equipment.VALID_SLOTS(1),
                {"Defence": "+15", "Speed": "-2"},
            )
        # Leather Tunic
        case Equipment.VALID_ITEMS(5):
            # Create leather tunic
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(5), Equipment.VALID_SLOTS(1), {"Defence": "+5"}
            )
        # Scout Armor
        case Equipment.VALID_ITEMS(6):
            # Create scout armor
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(6),
                Equipment.VALID_SLOTS(1),
                {"Defence": "+3", "Speed": "+10%"},
            )
        # Ring of the Sorcerer
        case Equipment.VALID_ITEMS(7):
            # Create Ring of the Sorcerer
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(7),
                Equipment.VALID_SLOTS(2),
                {"Spell_power": "+5", "Mana": "+15%"},
            )
        # Amulet of vitality
        case Equipment.VALID_ITEMS(8):
            # Create Amulet of vitality
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(8),
                Equipment.VALID_SLOTS(2),
                {"Health": "+10%", "Defence": "+3"},
            )
        # Ring of Haste
        case Equipment.VALID_ITEMS(8):
            # Create Ring of Haste
            temp_equipment = Equipment(
                Equipment.VALID_ITEMS(9),
                Equipment.VALID_SLOTS(2),
                {"Speed": "+2"},
            )
    return temp_equipment


# Create Equipment End


# Create all Equipment Start
# Creates an instance of each equipment item and returns the list
# Returns: equipment_list - list - Contains instances of all equipment
def create_all_equipment():
    # Init list
    equipment_list = []
    for item in Equipment.VALID_ITEMS:
        # Skip over None item as it does not do anything
        if item == "None":
            continue
        else:
            # create item and add to list
            equipment_list.append(create_equipment(item.name))
    # Return completed list
    return equipment_list


# Create all Equipment End


# Create Tile Start
# Creates an empty tile based on the tile type adn returns it - Tiles occupied later
# Params: t_type - string - Type of tile to create
# Returns: Tile - Tile based on tile type provided
def create_tile(t_type):
    # Match case for each type of tile
    match t_type:
        # Floor tile
        case Grid.Tile.VALID_TYPES(0):
            # create and return floor tile
            return Grid.Tile(t_type, True, Grid.EMPTY_TILE)
        # Wall tile
        case Grid.Tile.VALID_TYPES(1):
            # create and return Wall tile
            return Grid.Tile(t_type, False, Grid.EMPTY_TILE)
        # ShallowWater tile
        case Grid.Tile.VALID_TYPES(2):
            # create and return ShallowWater tile
            return Grid.Tile(t_type, True, Grid.EMPTY_TILE)


# Grid class with all methods needed for manipulating the grid
class Grid:
    # Constants - SOME MAY CHANGE
    EMPTY_TILE = -1
    MIN_BOUNDS = 5
    MAX_BOUNDS = 50

    # Initialize Grid with height, width
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []  # To be filed with Tiles

        # Generate grid based on height and width and fill with OPEN spaces
        for col in range(width):  # for each col based on width of grid
            temp_col = []

            # For each row in that column
            for row in range(height):
                # If tile is on the edge of the grid - First/last row/column
                if (row == 0 or row == height - 1) or (col == 0 or col == width - 1):
                    # Add wall tile to grid
                    temp_col.append(self.Tile("Wall", False, self.EMPTY_TILE))
                else:  # Any tile not on the edge
                    # Add floor tile to grid
                    temp_col.append(self.Tile("Floor", True, self.EMPTY_TILE))
                # Each cell is initialized with an OPEN space

            # After row was completed add row to grid
            self.grid.append(temp_col)

    # Is Occupied Start
    # Checks grid location at given x,y to see if it is occupied
    # Params: x,y - int - grid position to check
    # Returns: Bool - if grid tile is occupied T/F
    def is_occupied(self, x, y):
        return self.grid[x][y].occupants == self.EMPTY_TILE

    # Is Occupied End

    # Occupy Start
    # Sets grid location to given entity's ID, marking it as occupied
    # only called after tile is known to be unoccupied
    # Params: x,y - int - grid position to occupy
    #       e_ID - int - entity ID value
    def occupy(self, x, y, e_ID):
        self.grid[x][y].occupants.append(e_ID)

    # Occupy End

    # Clear Occupant Start
    # Removes occupant from grid location at given x,y
    # Params: x,y - int - tile position to clear occupant from
    #       e_ID - int - id number of occupant to remove at given tile
    def clear_occupant(self, x, y, e_ID):
        for occupant in self.grid[x][y].occupants:
            if occupant == e_ID:
                self.grid[x][y].occupants.remove(occupant)

    # Clear Occupant End

    # Is Passable Start
    # Sets grid location at given x,y to open
    # Params: x,y - int - grid position to clear
    # Returns: Bool - if tile is passable
    def is_passable(self, x, y):
        return self.grid[x][y].passable

    # Is Passable End

    # Get Stats Start
    # Gets all relevant stats of the tile at designated position and returns them
    # Params: x,y - int - position of tile
    # Returns tuple - Contains all stats needed for Command Line Interface commands
    #       (int x coord, int y coord, str t_type, bool passable, list occupants)
    def get_stats(self, x, y):
        stat_tuple = (
            x,
            y,
            self.grid[x][y].t_type,
            self.grid[x][y].passable,
            self.grid[x][y].occupants,
        )
        return stat_tuple

    # Get Stats End

    # Create Tile class because the grid will be made up of Tiles
    class Tile:
        # Constants
        VALID_TYPES = ("Floor", "Wall", "ShallowWater")

        # Initialize Tile with t_type, passable, occupant
        def __init__(self, t_type, passable, occupants):
            self.t_type = t_type
            self.passable = passable
            self.occupants = occupants


# Entity class with all methods needed for entities
class Entity:
    # Entity Constants
    ENTITY_TYPES = ("Warrior", "Mage", "Skeleton", "Goblin")
    # Entity base Stats
    WARRIOR_BASE_STATS = {"Health": 120, "Attack": 15, "Defence": 10, "Speed": 5}
    SKELETON_BASE_STATS = {"Health": 60, "Attack": 10, "Defence": 8, "Speed": 4}
    GOBLIN_BASE_STATS = {"Health": 45, "Attack": 12, "Defence": 3, "Speed": 6}

    # Initialize Entity Class with id, type, position, health, attack, defence, speed, inventory, active_modifiers
    def __init__(
        self,
        id,
        e_type,
        position,
        health,
        attack,
        defence,
        speed,
        inventory,
        active_modifiers,
    ):
        self.id = id
        self.e_type = e_type
        self.position = position
        self.health = health
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.inventory = inventory
        self.active_modifiers = active_modifiers

    # Entity List for tracking entities
    entity_list = []
    # Value to count what ID to give the next entity
    entity_ids_issued = 0
    # Base Entity Methods

    # Get Stats Start
    # Gets all relevant stats of the entity and returns them
    # Returns tuple - Contains all stats needed for Command Line Interface commands
    #       (int id, str e_type, tuple x/y coords, int health, int attack, int defence, int speed, list of two dictionaries active_modifiers)
    def get_stats(self):
        stat_tuple = (
            self.id,
            self.e_type,
            self.position,
            self.health,
            self.attack,
            self.defence,
            self.speed,
            self.active_modifiers,
        )
        return stat_tuple

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    def reset_stats(self):
        # Match case to entity type
        match self.e_type:
            # Warrior case
            case self.ENTITY_TYPES(0):
                self.health = Entity.WARRIOR_BASE_STATS["Health"]
                self.attack = Entity.WARRIOR_BASE_STATS["Attack"]
                self.defence = Entity.WARRIOR_BASE_STATS["Defence"]
                self.speed = Entity.WARRIOR_BASE_STATS["Speed"]
            # Skeleton Case
            case self.ENTITY_TYPES(2):
                self.health = Entity.SKELETON_BASE_STATS["Health"]
                self.attack = Entity.SKELETON_BASE_STATS["Attack"]
                self.defence = Entity.SKELETON_BASE_STATS["Defence"]
                self.speed = Entity.SKELETON_BASE_STATS["Speed"]
            # Goblin Case
            case self.ENTITY_TYPES(3):
                self.health = Entity.GOBLIN_BASE_STATS["Health"]
                self.attack = Entity.GOBLIN_BASE_STATS["Attack"]
                self.defence = Entity.GOBLIN_BASE_STATS["Defence"]
                self.speed = Entity.GOBLIN_BASE_STATS["Speed"]

    # Reset Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    def update_stats(self):
        # Clear active modifiers to avoid double counting of modifiers
        self.active_modifiers.clear()
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.inventory:
            # Iterate through all stats modified within current slot
            for stat, modifier in slot.items():
                # Ignore stats that onlt affect Mage class
                if stat == "Mana" or stat == "Spell_power":
                    continue
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)
        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()

    # Update Stats End

    # Handle Modifiers Start
    # Handles the flat and percent modifier split for the update_stats method
    # Updates active modifier of current unit
    def handle_modifiers(self, stat, modifier):
        # Determine if the modifier is percent based or a flat modifier and add it active modifiers accordingly
        if (
            modifier[len(modifier) - 1] != "%"
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

    # Calculate Final Stats Start
    # Handles stat calculation for entities and updates them
    def calculate_final_stats(self):
        # Stats to be checked
        stats = ("Health", "Attack", "Defence", "Speed")
        # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
        for stat in stats:
            temp_value = getattr(self, stat.lower())
            # If flat values exist
            if self.active_modifiers["Flat_modifiers"][stat]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            setattr(self, stat.lower(), temp_value)

    # Calculate Final Stats End

    # Mage Class extend from Entity class
    class Mage:
        # Mage Constants
        MAGE_BASE_STATS = {
            "Health": 70,
            "Attack": 8,
            "Defence": 4,
            "Speed": 5,
            "Mana": 100,
            "Spell_power": 25,
        }

        # Initialize mage class with entity class attributes + new ones: mana and spell power
        def __init__(
            self,
            id,
            e_type,
            position,
            health,
            attack,
            defence,
            speed,
            inventory,
            active_modifiers,
            mana,
            spell_power,
        ):

            # Inherit init from Entity super class
            super.__init__(
                id,
                e_type,
                position,
                health,
                attack,
                defence,
                speed,
                inventory,
                active_modifiers,
            )
            # New attributes
            self.mana = mana
            self.spell_power = spell_power

        # Get Stats Start
        # Gets all relevant stats of the entity and returns them
        # Returns tuple - Contains all stats needed for Command Line Interface commands
        #       (int id, str e_type, tuple x/y coords, int health, int mana, int attack, int defence, int speed, list of two dictionaries active_modifiers)
        def get_stats(self):
            stat_tuple = (
                self.id,
                self.e_type,
                self.position,
                self.health,
                self.mana,
                self.attack,
                self.defence,
                self.speed,
                self.active_modifiers,
            )
            return stat_tuple

        # Get Stats End

        # Reset Stats Start
        # Resets entities stats to base values
        def reset_stats(self):
            # Match case to entity type
            match self.e_type:
                # Mage case
                case self.ENTITY_TYPES(1):
                    self.health = Entity.Mage.MAGE_BASE_STATS["Health"]
                    self.attack = Entity.Mage.MAGE_BASE_STATS["Attack"]
                    self.defence = Entity.Mage.MAGE_BASE_STATS["Defence"]
                    self.speed = Entity.Mage.MAGE_BASE_STATS["Speed"]
                    self.mana = Entity.Mage.MAGE_BASE_STATS["Mana"]
                    self.spell_power = Entity.Mage.MAGE_BASE_STATS["Spell_power"]

        # Reset Stats End

        # Calculate Final Stats Start
        # Handles stat calculation for entities and updates them
        def calculate_final_stats(self):
            # Stats to be checked
            stats = ("Health", "Attack", "Defence", "Speed", "Mana", "Spell_power")
            # Iterate through all stats and add flat modifiers first, then calculate multiplicative modifiers
            for stat in stats:
                temp_value = getattr(self, stat.lower())
                # If flat values exist
                if self.active_modifiers["Flat_modifiers"][stat]:
                    temp_value += self.active_modifiers["Flat_modifiers"][stat]
                # If percent modifiers exist
                if stat in self.active_modifiers["Percent_modifiers"]:
                    temp_percent_value = self.active_modifiers["Percent_modifiers"][
                        stat
                    ]
                    temp_value += temp_value * (temp_percent_value / 100)
                # Update entities stats with new stat before continuing to next stat
                setattr(self, stat.lower(), temp_value)

        # Calculate Final Stats End

        # Update Stats Start
        # Calculates final stats and updates entities stats based on their bases and modifiers
        # Called when inventory is changed or if unit is positioned on a tile that modifies stats
        def update_stats(self):
            # Clear active modifiers to avoid double counting of modifiers
            self.active_modifiers.clear()
            # Stats to be checked
            # stats = ("Health", "Attack", "Defence", "Speed")
            # Check all inventory slots for modifiers to add to active_modifiers of entity
            for slot in self.inventory:
                # Iterate through all stats modified within current slot
                for stat, modifier in slot.items():
                    # Ignore stats that onlt affect Mage class
                    if stat == "Mana" or stat == "Spell_power":
                        continue
                    # Handle modifiers split between flat and percent
                    self.handle_modifiers(stat, modifier)
            # Since stats will be changed and overwritten, we need the entity stats set to their bases
            self.reset_stats()
            # Calculate the entities final stats
            self.calculate_final_stats()

            # Update Stats End


# Equipment class with all methods needed for equipment
class Equipment:
    # Constants
    VALID_ITEMS = (
        "None",
        "IronSword",
        "CursedDagger",
        "MageStaff",
        "IronChestplate",
        "LeatherTunic",
        "ScoutArmor",
        "RingOfTheSorceror",
        "AmuletOfVitality",
        "RingOfHaste",
    )
    VALID_SLOTS = ("Weapon", "Armor", "Accessory")
    BASE_INVENTORY = ["None", "None", "None"]
    ALL_EQUIPMENT = create_all_equipment()

    # Initilize Equipment class with name, slot, effects
    def __init__(self, name, slot, effects):
        self.name = name
        self.slot = slot
        self.effects = effects

    # Get Stats Start
    # Gets necessary stats about equipment and returns them
    # Returns: name - string - equipments name
    def get_stats(self):
        return self.name

    # Get Stats End
