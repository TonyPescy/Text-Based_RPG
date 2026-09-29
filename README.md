# Text-Based_RPG
## Description
Test-based RPG where a grid of tiles is occupied by players, monsters, and items. Playing the game is done through the Command Line Interface

## Author
Tony Pescatore

## Table of Contents
[Entities](#Entities)

[Equipment](#Equipment)

[Tiles](#Tiles)

[Command Line Interface Guide](#Command-Line-Interface-Guide)

[Design Decisions](#Design-Decisions)

[Game Commands](#Game-Commands)

## Entities
[Table of Contents](#table-of-contents)

- Warrior
- Mage
- Goblin
- Skeleton

## Equipment
[Table of Contents](#table-of-contents)

- None
- IronSword
- CursedDagger
- MageStaff
- IronChestplate
- LeatherTunic
- ScoutArmor
- RingOfTheSorcerer
- AmuletOfVitality
- RingOfHaste

### Consumables

- SmallHealthPotion
- GreaterHealthPotion
- SuperiorHealthPotion
- ManaPotion
- TurtleMasterPotion

## Tiles
[Table of Contents](#table-of-contents)


| Tiles         | Desciption |
| ------------- |:-------------:|
| Floor         | Standard tile |
| Wall      |  An impassable tile     |
| ShallowWater      | Tile that imposes a speed debuff of -2 on the player |
| Forest        | Tile that grants the entity +5 defence and a debuff of -2 |

## Command Line Interface Guide
[Table of Contents](#table-of-contents)

**Description:** This is a guide to the Command Line Interface to be used to play the game. It will outline and define the commands that are currently supported within the game.

### Init Map
**Description:** Will create a map with the provided width and height.

**Called as:** init map width height

**Contraints:** Width and height are integers between 5 and 50 inclusive.

### Set Tile
**Description:** Will set the tile at a given grid position to be the provided tile type.

**Called as:** set tile x y tile_type

**Contraints:** tile_type must be within list of valid tile types, (x,y) must be integers within the current grid bounds, and map must have been created.

### Spawn
**Description:** Will spawn specified entity or item at given grid position

**Called as:** 
- spawn entity_type x y -> Spawns entity at given coordinates
- spawn loot item_name x y -> Spawns loot at given coordinates

**Contraints:**  (x,y) must be integers within current grid bounds and map must have been created.
- **Spawn Entity:** entity_type must be within list of valid entity types and there must not be any other entity already present at the given grid position.
- **Spawn Loot:** item_name must be within list of valid equipment types.
### Swap
**Description:** Will equip provided item in the given, or determined, inventory slot to a "player".

**Called as:** swap id slot item_name

**Contraints:** item must be within the list of valid items. id must be an integer within the current entity list and slot must be within valid slots.

### Inventory
**Description:** Will display the current inventory of provided entity.

**Called as:** inventory id

**Contraints:** An entity with a matching id must exist.

### Inspect
**Description:** Will display the stats of an entity given its id.

**Called as:** inspect id

**Contraints:** The id must be an integer that corresponds to a valid entity within the entity list.

### Tile
**Description:** Will display a description of the tile at the given grid position.

**Called as:** tile x y

**Contraints:** (x,y) must be integers within the current grid bounds and the map must have been created.

### Pickup
**Description:** Will pickup the item with the given name at the given entity's current location, if it is present.

**Called as:** pickup id item_name

**Contraints:** id must be an integer within the current entity list, the item with the same name must be located at the same tile as the entity, and the entity must have space in their backpack for the item.

### Drop
**Description:** Will drop the item with the given name at the given entity's current location.

**Called as:** drop id item_name

**Contraints:** id must be an integer within the current entity list and an item with the same name must be within the entity's backpack.

### Give
**Description:** Will give the item with the given name to the matching entity.

**Called as:** give id item_name

**Contraints:** id must be an integer within the current entity list and the item must be a valid item.

### Use
**Description:** Will use the item with the given name on the matching entity.

**Called as:** use id item_name

**Contraints:** id must be an integer within the current entity list and the item must be a valid consumable within the given entity's inventory.

### Move
**Description:** Will move the given entity to the grid position if they are within range and a valid.

**Called as:** move id x y

**Contraints:** id must be an integer within the current entity list and the x,y must correspond to a valid grid position for the entity to occupy.

## Design Decisions
[Table of Contents](#table-of-contents)

**Description:** The following design decisions will provide an overview of each section of the project as well as a breif explanation of why and how some mechanics are implemented the way that they are. Each section was split  using bullet points to avoid a large convulated block of text forming when new features or designs are added to the project.

### Grid 
- The grid is used as the worlds coordinate system that will track entity positions, tile states, and occupancy across the multiple tile types within the game. The grid is represented by a 2D matrix of Tiles. 
- This grid can range from 5x5 to a max of 50x50 Tiles. It is initialized in such a way that all tiles are passable and open floor tiles. 
- It has a get_stats function which is used to get the stats of the tile at the designated grid position.
- It has is_passable, within_bounds, is_valid_grid_position, etc. helper functions which help to verify the values that interact with the grid, especially in the CLI.
- Grid distances will be calculating using Manhattan Distance.
- When using A* pathing, entities will not block their tiles. So you will be able to move through entities but will not be able to end on the same tile as an entity.

### Tiles - ToDo: Reduce future cyclomatic complexity - Will need readme update as well
- Tiles are what make up the grid. Each Tile has its typing, a boolean determining whether they are passable or not for collision/movement restrictions, and a list of occupants. 
- Each tile can have more than 1 occupant, which will be represented by a list of entity IDs, or if there are no occupants it will be instead be filled with the empty tile constant value. 
- Each tile also has an item_list for loot that can be picked up, dropped, or spawned at the tile location.
- Impassable tiles also block Line of sight for ranged/magic attacks.
- There are only 4 valid tile types, which are: Floor, Wall, and ShallowWater. 
    - **Floor Tiles:** Act as open tiles which are passable and will not impede movement in anyway. 
    - **Wall Tiles:** Impassable tiles that will be used to enforce spatial boundaries and colision. 
    - **ShallowWater Tiles:** Passable tiles that apply a negative modifier that will impede the movement of its occupant(s).
    - **Forest Tiles:** Passable tiles that apply positive modifier to entity defence as well as impeding their movement slightly.

### Entities
- Entities include both player and monster classes which use base stats and conditional modifiers to get their final stat values. Entities have the following stats: id, type, position, health, attack, defence, speed, inventory, and active_modifiers. These can be added to in some cases, such as with the player Mage class which adds mana and spell power. 
- Max Health and Max Mana is tracked to allow for consumables to refill health and mana, it also prevents any overflow errors with those consumables. They also allow for percentages to be accurately used based on max health/mana of an entity instead of on their current health and for easier tracking of damage during combat. 
- The entity's inventory will be filled with 3 pieces of equipment with only 1 of each type being allowed to be eqipped at a time. 
- Entities will have a dictionary of active modifiers which will contain two keys, Flat_modifiers and Percent_modifiers, which will make it significantly easier to calculate the entities final stats with these modifiers taken into account.
- Entities will have 5 spaces open for their backpack, this is where they store their items in their inventory as well as any backup items and consumables.

### Equipment
- The equipment class represents items that will be held within an entity's inventory. There are only 3 types, weapon, armor, and accessory, all of which can only have 1 equipped in a single slot at a time. These items will have modifiers that will be to calculate the final stat values for the entity that they are equipped to. 
- The items themselves will inherit the Equipment class then add their own stats to it so make getting the stats from each item simpler.
- New items consumables will inherit the Equipment class but expand on it with two types of effects: over time effects and instant effects. This allows for them to be consumed (consumables), while other item cannot be consumed, and for their effects to effect the entity stats. Over time effects are waiting for time to be added (turns?) before their functionality is fully figured out.

### Test Suite NEEDS REFACTOR WITH TEST FUNCTIONS TO REDUCE LINES/REDUNDANCY
- The test suite tests the public facing methods as they will call and use the other private facing methods. This means that these private facing methods will also be tested in tandem. It incldues verbose tests includings tests on the boundary values, the validity of inputs, and ensures that all public facing methods and private methods are working as intended. 
- All other aspects of the project are tested within this suite including the Command Line Interface, Equipment, Entities, Grid, and Tiles.

### Command Line Interface
- The command line interface is where the game in played. Running the command line interface will allow the user to input commands, which will be handled accordingly by the command line interfaces process_command method. This will return descriptive error messages so that users will know what was wrong with their inputs. 
- The command line interface will house the current game grid of tiles, a list of the current entities, and a boolean to determine if the map was already created. It also contains the main function that will prompt for the commands in the terminal, the player can exit at any time by entering 'quit'.