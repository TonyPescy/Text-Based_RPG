# Grid class with all methods needed for manipulating the grid
class Grid:
    # Constants
    MIN_BOUNDS = 5
    MAX_BOUNDS = 50

    # Initialize Grid with height, width
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []  # To be filed with Tiles

        if Grid.are_valid_ints(width, height) and Grid.within_bounds(width, height):
            # Generate grid based on height and width and fill with OPEN spaces
            for col in range(int(width)):  # for each col based on width of grid
                temp_col = []

                # For each row in that column
                for row in range(int(height)):
                    # Each cell is initialized with an empty space
                    temp_col.append(Tile("Floor", True, []))

                # After row was completed add row to grid
                self.grid.append(temp_col)

    # Is Occupied Start
    # Checks grid location at given x,y to see if it is occupied
    # Params: x,y - int - grid position to check
    # Returns: Bool - if grid tile is occupied T/F
    def is_occupied(self, x, y):
        # typing fix
        x = int(x)
        y = int(y)
        if len(self.grid[x][y].occupants) == 0:  # empty list of occupants
            return False
        else:
            return True

    # Is Occupied End

    # Occupy Start
    # Sets grid location to given entity's ID, marking it as occupied
    # only called after tile is known to be unoccupied
    # Params: x,y - int - grid position to occupy
    #       e_ID - int - entity ID value
    def occupy(self, x, y, e_ID):
        # typing fix
        x = int(x)
        y = int(y)
        self.grid[x][y].occupants.append(e_ID)

    # Occupy End

    # Clear Occupant Start
    # Removes occupant from grid location at given x,y
    # Params: x,y - int - tile position to clear occupant from
    #       e_ID - int - id number of occupant to remove at given tile
    def clear_occupant(self, x, y, e_ID):
        # typing fix
        x = int(x)
        y = int(y)
        for occupant in self.grid[x][y].occupants:
            if occupant == e_ID:
                self.grid[x][y].occupants.remove(occupant)

    # Clear Occupant End

    # Is Passable Start
    # Sets grid location at given x,y to open
    # Params: x,y - int - grid position to clear
    # Returns: Bool - if tile is passable
    def is_passable(self, x, y):
        # typing fix
        x = int(x)
        y = int(y)
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

    # Within Bounds start
    # checks to see if width and height are within bounds - only runs if they are valid ints
    # Params: width/height - ints
    # Returns: bool
    def within_bounds(width, height):
        if (
            Grid.MIN_BOUNDS <= int(width) <= Grid.MAX_BOUNDS
            and Grid.MIN_BOUNDS <= int(height) <= Grid.MAX_BOUNDS
        ):
            return True
        else:
            return False

    # Is Valid Grid Position
    # checks to see if x and y are valid in current grid
    # Params: x/y - ints - grid positon
    # Returns: Bool
    def is_valid_grid_position(self, x, y):
        if int(self.width) > int(x) >= 0 and int(self.height) > int(y) >= 0:
            return True
        else:
            return False

    # Set Tile Start
    # Sets tile at given grid position
    # Params: x/y - ints - grid position
    #       tile_type - string - Type of tile to set
    def set_tile(self, x, y, tile_type):
        # Create tile to be placed
        temp_tile = Tile.create_tile(tile_type)
        # cast to int
        x = int(x)
        y = int(y)
        # update temp_tile to have correct occupants
        for occupant in self.grid[x][y].occupants:
            temp_tile.occupants.append(occupant)
        # set tile on grid
        self.grid[x][y] = temp_tile

    # Spawn Entity start
    # Spawns entity at given grid position
    # Params: x/y - ints - grid position
    #       entity_type - string - Type of entity to spawn
    # Returns: new_entity - Entity - spawned in entity
    def spawn_entity(self, x, y, entity_type):
        # typing fix
        x = int(x)
        y = int(y)
        # spawn entity
        Entity.create_entity(entity_type, x, y)
        # get entity - NEW entity is at end of the list
        new_entity = Entity.entity_list[-1]

        # occupy position on map
        self.occupy(x, y, new_entity.id)

        # return updated grid
        return new_entity

    # Reset Grid start
    def reset_grid():
        # reset grid stats
        Grid.width = 0
        Grid.height = 0
        Grid.grid = []
        # return grid to CLI
        return Grid.grid


# Create Tile class because the grid will be made up of Tiles
class Tile:
    # Constants
    VALID_TYPES = ("Floor", "Wall", "ShallowWater")

    # Initialize Tile with t_type, passable, occupant
    def __init__(self, t_type, passable, occupants, modifiers=None):
        self.t_type = t_type
        self.passable = passable
        self.occupants = occupants

        if modifiers is None:
            modifiers = {
                "Flat_modifiers": {},
                "Percent_modifiers": {},
            }

        self.modifiers = modifiers

    # Is Valid Tile Start
    # Checks to see input is a valid tile type
    # Params: tile_type - string - tile name
    # Returns: Bool
    def is_valid_tile(tile_type):
        if tile_type in [t_type.lower() for t_type in Tile.VALID_TYPES]:
            return True
        else:
            return False

    # Create Tile Start
    # Creates an empty tile based on the tile type adn returns it - Tiles occupied later
    # Params: t_type - string - Type of tile to create
    # Returns: Tile - Tile based on tile type provided
    def create_tile(t_type):
        # Match case for each type of tile
        match t_type:
            # Floor tile
            case "floor":
                # create and return floor tile
                return Tile(t_type, True, [])
            # Wall tile
            case "wall":
                # create and return Wall tile
                return Tile(t_type, False, [])
            # ShallowWater tile
            case "shallowwater":
                # create and return ShallowWater tile
                return Tile(
                    t_type,
                    True,
                    [],
                    {"Flat_modifiers": {"Speed": "-2"}, "Percent_modifiers": {}},
                )


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

    def reset_id_issuer_tracker():
        Entity.entity_ids_issued = 0

    def reset_entity_list():
        Entity.entity_list = []

    # Get Stats Start
    # Gets all relevant stats of the entity and returns them
    # Returns dictionary - Contains all stats needed for Command Line Interface commands
    #       (int id, str e_type, tuple x/y coords, int health, int attack, int defence, int speed, list of two dictionaries active_modifiers)
    def get_stats(self):
        stat_dict = {
            "Id": self.id,
            "Type": self.e_type,
            "Position": self.position,
            "Health": self.health,
            "Attack": self.attack,
            "Defence": self.defence,
            "Speed": self.speed,
            "Active_modifiers": self.active_modifiers,
        }
        return stat_dict

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    def reset_stats(self):
        # Match case to entity type
        match self.e_type:
            # Warrior case
            case "warrior":
                self.health = Entity.WARRIOR_BASE_STATS["Health"]
                self.attack = Entity.WARRIOR_BASE_STATS["Attack"]
                self.defence = Entity.WARRIOR_BASE_STATS["Defence"]
                self.speed = Entity.WARRIOR_BASE_STATS["Speed"]
            # Skeleton Case
            case "skeleton":
                self.health = Entity.SKELETON_BASE_STATS["Health"]
                self.attack = Entity.SKELETON_BASE_STATS["Attack"]
                self.defence = Entity.SKELETON_BASE_STATS["Defence"]
                self.speed = Entity.SKELETON_BASE_STATS["Speed"]
            # Goblin Case
            case "goblin":
                self.health = Entity.GOBLIN_BASE_STATS["Health"]
                self.attack = Entity.GOBLIN_BASE_STATS["Attack"]
                self.defence = Entity.GOBLIN_BASE_STATS["Defence"]
                self.speed = Entity.GOBLIN_BASE_STATS["Speed"]

    # Reset Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    def update_stats(self, active_grid):
        # Clear active modifiers to avoid double counting of modifiers
        self.active_modifiers["Flat_modifiers"] = {}
        self.active_modifiers["Percent_modifiers"] = {}
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.inventory:
            # Iterate through all stats modified within current slot
            for stat, modifier in slot.effects.items():
                # Ignore stats that onlt affect Mage class
                if stat == "Mana" or stat == "Spell_power":
                    continue
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)

        # Tile modifiers
        # Get entity grid position
        x = self.position[0]
        y = self.position[1]

        # Get current tile
        tile = active_grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - could be cleaned up later
        for stat, modifier in tile.modifiers["Flat_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        for stat, modifier in tile.modifiers["Percent_modifiers"].items():
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
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            setattr(self, stat.lower(), temp_value)

    # Calculate Final Stats End

    # Is Valid Entity Start
    # Checks to see input is a valid entity type
    # Params: entity_type - string - entity name
    # Returns: Bool
    def is_valid_entity(entity_type):
        if entity_type in [entity.lower() for entity in Entity.ENTITY_TYPES]:
            return True
        else:
            print("error: Tile Type added is not a valid tile type!")
            return False

    # Create Entity Start
    # Creates entity with base stats and values based on the entity
    # Holds base stats for all of the entities
    # Params: e_type - String - Type of entity to create
    #       x,y - int - Coordinates to spawn entity at
    def create_entity(e_type, x, y):
        # ensure correct typing
        x = int(x)
        y = int(y)
        # Case statement to match to every entity type in game
        match e_type:
            # Warrior
            case "warrior":
                # Create warrior entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "warrior",
                    [x, y],
                    Entity.WARRIOR_BASE_STATS["Health"],
                    Entity.WARRIOR_BASE_STATS["Attack"],
                    Entity.WARRIOR_BASE_STATS["Defence"],
                    Entity.WARRIOR_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            # Mage
            case "mage":
                # Create mage entity
                temp_entity = Mage(
                    Entity.entity_ids_issued,
                    "mage",
                    [x, y],
                    Mage.MAGE_BASE_STATS["Health"],
                    Mage.MAGE_BASE_STATS["Attack"],
                    Mage.MAGE_BASE_STATS["Defence"],
                    Mage.MAGE_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                    Mage.MAGE_BASE_STATS["Mana"],
                    Mage.MAGE_BASE_STATS["Spell_power"],
                )
            # Skeleton
            case "skeleton":
                # Create skeleton entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "skeleton",
                    [x, y],
                    Entity.SKELETON_BASE_STATS["Health"],
                    Entity.SKELETON_BASE_STATS["Attack"],
                    Entity.SKELETON_BASE_STATS["Defence"],
                    Entity.SKELETON_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            # Goblin
            case "goblin":
                # Create goblin entity
                temp_entity = Entity(
                    Entity.entity_ids_issued,
                    "goblin",
                    [x, y],
                    Entity.GOBLIN_BASE_STATS["Health"],
                    Entity.GOBLIN_BASE_STATS["Attack"],
                    Entity.GOBLIN_BASE_STATS["Defence"],
                    Entity.GOBLIN_BASE_STATS["Speed"],
                    BASE_INVENTORY.copy(),
                    {
                        "Flat_modifiers": {},
                        "Percent_modifiers": {},
                    },  # Empty dictionaries
                )
            case _:  # error no matching entity type found - May be redundant
                print(
                    f"error: Invalid entity type '{e_type}'. "
                    f"Expected one of: {Entity.ENTITY_TYPES}."
                )

        # Increment entity_ids_issued to account for new entity
        Entity.entity_ids_issued += 1
        # Add new entity to entity list
        Entity.entity_list.append(temp_entity)

    # Create Entity End

    # Equip Item Start
    # Equips given item at given slot
    def equip_item(self, item, slot):
        # match statement for slot
        match slot:
            # weapon case
            case "weapon":
                self.inventory[0] = item
            # armor case
            case "armor":
                self.inventory[1] = item
            # accessory case
            case "accessory":
                self.inventory[2] = item


# Mage Class extend from Entity class
class Mage(Entity):
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
        super().__init__(
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
    # Returns dictionary - Contains all stats needed for Command Line Interface commands
    #       (int id, str e_type, tuple x/y coords, int health, int mana, int attack, int defence, int speed, list of two dictionaries active_modifiers)
    def get_stats(self):
        stat_dict = {
            "Id": self.id,
            "Type": self.e_type,
            "Position": self.position,
            "Health": self.health,
            "Mana": self.mana,
            "Attack": self.attack,
            "Defence": self.defence,
            "Speed": self.speed,
            "Active_modifiers": self.active_modifiers,
        }
        return stat_dict

    # Get Stats End

    # Reset Stats Start
    # Resets entities stats to base values
    def reset_stats(self):
        # Match case to entity type
        match self.e_type:
            # Mage case
            case "mage":
                self.health = Mage.MAGE_BASE_STATS["Health"]
                self.attack = Mage.MAGE_BASE_STATS["Attack"]
                self.defence = Mage.MAGE_BASE_STATS["Defence"]
                self.speed = Mage.MAGE_BASE_STATS["Speed"]
                self.mana = Mage.MAGE_BASE_STATS["Mana"]
                self.spell_power = Mage.MAGE_BASE_STATS["Spell_power"]

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
            if stat in self.active_modifiers["Flat_modifiers"]:
                temp_value += self.active_modifiers["Flat_modifiers"][stat]
            # If percent modifiers exist
            if stat in self.active_modifiers["Percent_modifiers"]:
                temp_percent_value = self.active_modifiers["Percent_modifiers"][stat]
                temp_value += temp_value * (temp_percent_value / 100)
            # Update entities stats with new stat before continuing to next stat
            setattr(self, stat.lower(), temp_value)

    # Calculate Final Stats End

    # Update Stats Start
    # Calculates final stats and updates entities stats based on their bases and modifiers
    # Called when inventory is changed or if unit is positioned on a tile that modifies stats
    def update_stats(self, active_grid):
        # Clear active modifiers to avoid double counting of modifiers
        self.active_modifiers["Flat_modifiers"] = {}
        self.active_modifiers["Percent_modifiers"] = {}
        # Stats to be checked
        # stats = ("Health", "Attack", "Defence", "Speed")
        # Check all inventory slots for modifiers to add to active_modifiers of entity
        for slot in self.inventory:
            # Iterate through all stats modified within current slot
            for stat, modifier in slot.effects.items():
                # Handle modifiers split between flat and percent
                self.handle_modifiers(stat, modifier)

        # Tile modifiers
        # Get entity grid position
        x = self.position[0]
        y = self.position[1]

        # Get current tile
        tile = active_grid.grid[x][y]

        # Handle modifiers for tile - split due to way tile modifiers are setup - FIX
        for stat, modifier in tile.modifiers["Flat_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        for stat, modifier in tile.modifiers["Percent_modifiers"].items():
            self.handle_modifiers(stat, modifier)
        # Since stats will be changed and overwritten, we need the entity stats set to their bases
        self.reset_stats()
        # Calculate the entities final stats
        self.calculate_final_stats()

        # Update Stats End


# Create all Equipment End


# Equipment class with all methods needed for equipment
class Equipment:
    # Initilize Equipment class with name, slot, effects
    def __init__(self, name, slot, effects):
        self.name = name
        self.slot = slot
        self.effects = effects

    # Create functions
    # Create Equipment Start
    # Creates equipment with base stats and values based on the equipment
    # Holds base stats for all of the equipment
    # Params: e_type - String - Equipment to create
    def create_equipment(e_type):
        # Match to equipment name
        match e_type:
            # Iron Sword
            case "ironsword":
                # Create Iron Sword
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[1],
                    Equipment.VALID_SLOTS[0],
                    {"Attack": "+12"},
                )

            # Cursed Dagger
            case "curseddagger":
                # Create cursed dagger
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[2],
                    Equipment.VALID_SLOTS[0],
                    {"Attack": "+18", "Defence": "-5"},
                )

            # Mage Staff
            case "magestaff":
                # Create Mage Staff
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[3],
                    Equipment.VALID_SLOTS[0],
                    {"Spell Power": "+5"},
                )

            # Iron chestplate
            case "ironchestplate":
                # Create iron chestplate
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[4],
                    Equipment.VALID_SLOTS[1],
                    {"Defence": "+15", "Speed": "-2"},
                )

            # Leather Tunic
            case "leathertunic":
                # Create leather tunic
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[5],
                    Equipment.VALID_SLOTS[1],
                    {"Defence": "+5"},
                )

            # Scout Armor
            case "scoutarmor":
                # Create scout armor
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[6],
                    Equipment.VALID_SLOTS[1],
                    {"Defence": "+3", "Speed": "+10%"},
                )

            # Ring of the Sorcerer
            case "ringofthesorcerer":
                # Create Ring of the Sorcerer
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[7],
                    Equipment.VALID_SLOTS[2],
                    {"Spell_power": "+5", "Mana": "+15%"},
                )

            # Amulet of vitality
            case "amuletofvitality":
                # Create Amulet of vitality
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[8],
                    Equipment.VALID_SLOTS[2],
                    {"Health": "+10%", "Defence": "+3"},
                )

            # Ring of Haste
            case "ringofhaste":
                # Create Ring of Haste
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[9],
                    Equipment.VALID_SLOTS[2],
                    {"Speed": "+2"},
                )
            # none cases for default inventory
            case "none_armor":
                # create none
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[0],
                    Equipment.VALID_SLOTS[1],
                    {},
                )
            case "none_wep":
                # create none
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[0],
                    Equipment.VALID_SLOTS[0],
                    {},
                )
            case "none_acc":
                # create none
                temp_equipment = Equipment(
                    Equipment.VALID_ITEMS[0],
                    Equipment.VALID_SLOTS[2],
                    {},
                )
        return temp_equipment

        # Create Equipment End

    # Constants
    VALID_ITEMS = (
        "None",
        "IronSword",
        "CursedDagger",
        "MageStaff",
        "IronChestplate",
        "LeatherTunic",
        "ScoutArmor",
        "RingOfTheSorcerer",
        "AmuletOfVitality",
        "RingOfHaste",
    )
    VALID_SLOTS = ("Weapon", "Armor", "Accessory")


BASE_INVENTORY = [
    Equipment.create_equipment("none_wep"),
    Equipment.create_equipment("none_armor"),
    Equipment.create_equipment("none_acc"),
]

"""# Get Stats Start
# Gets necessary stats about equipment and returns them
# Returns: name - string - equipments name
def get_stats(self):
    return self.name

# Get Stats End"""
