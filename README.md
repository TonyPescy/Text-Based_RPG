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

## Equipment
[Table of Contents](#table-of-contents)

## Tiles
[Table of Contents](#table-of-contents)

## Command Line Interface Guide
[Table of Contents](#table-of-contents)
This is a guide to the Command Line Interface to be used to play the game. It will outline and define the commands that are currently supported within the game.

## Design Decisions
[Table of Contents](#table-of-contents)

### Grid 
The grid is used as the worlds coordinate system that will track entity positions, tile states, and occupancy across the multiple tile types within the game. The grid is represented by a 2D matrix of Tiles. This grid can range from 5x5 to a max of 50x50 Tiles. It is initialized in such a way that all tiles are passable and open floor tiles. It has a get_stats function which is used to get the stats of the tile at the designated grid position.

### Tiles
Tiles are what make up the grid. Each Tile has its typing, a boolean whether they are passable or not for collision/movement restrictions, and a list of occupants. Each tile can have more than 1 occupant, which will be represented by a list of entity IDs, or if there are no occupants it will be instead be filled with the empty tile constant value. Currently there are only 3 valid tile types, which are: Floor, Wall, and ShallowWater. Floor tiles act as open floor tiles which are passable and will not impede movement in anyway. Wall tiles are impassable tiles that will be used to enforce spatial boundaries and colision. ShallowWater tiles are passable tiles that apply a negative modifier that will impede the movement of its occupant(s).

### Entities
Entities include both player and monster classes which use base stats and conditional modifiers to get their final stat values. Entities have the following stats: id, type, position, health, attack, defence, speed, inventory, and active_modifiers. These can be added to in some cases, such as with the player Mage class which adds mana and spell power. The entity's inventory will be filled with 3 pieces of equipment with only 1 of each type being allowed to be eqipped at a time. Entities will have a dictionary of active modifiers which will contain two keys, Flat_modifiers and Percent_modifiers, which will make it significantly easier to calculate the entities final stats with these modifiers taken into account.

### Equipment
The equipment class represents items that will be held within an entity's inventory. There are only 3 types, weapon, armor, and accessory, all of which can only have 1 equipped in a single slot at a time. These items will have modifiers that will be to calculate the final stat values for the entity that they are equipped to. 

### Test Suite
The test suite only tests the public facing methods as they will call and use the other private facing methods. This means that these private facing methods will also be tested in tandem. It incldues verbose tests includings tests on the boundary values, the validity of inputs, and ensures that all public facing methods and private methods are working as intended.

### Command Line Interface
The command line interface is where the game in played. Running the command line interface will allow the user to input commands, which will be handled accordingly by the command line interfaces process_command method. This will return descriptive error messages so that users will know what was wrong with their inputs. The command line interface also will house the current game grid of tiles, a list of the current entities, and a boolean to determine if the map was already created.

## Game Commands
[Table of Contents](#table-of-contents)

#### Description
Commands that are currently supported in-game as well as how to use them.

### Init Map
**Description:** Will create a map with the provided width and height.
**Called as:** init map width height
**Contraints:** Width and height are integers between 5 and 50 inclusive.

### Set Tile
**Description:** Will set the tile at a given grid position to be the provided tile type.
**Called as:** set tile x y tile_type
**Contraints:** tile_type must be within list of valid tile types, (x,y) must be integers within the current grid bounds, and map must have been created.

### Spawn
**Description:** Will create an entity of the given type and spawn it at the provided grid position.
**Called as:** spawn entity_type x y
**Contraints:** entity_type must be within list of valid entity types, (x,y) must be integers within current grid bounds, there must not be any other entity already present at the given grid position, and map must have been created.

### Equip
**Description:** Will equip provided item in the given, or determined, inventory slot to a "player".
**Called as:** equip item slot*
**Contraints:** slot is an optional argument and can be skipped. However, if slot is provided it needs to be within list of valid slots and correspond to the items slot. item must be within the list of valid items. A "player" entity must have been created.

### Inventory
**Description:** Will display the current inventory of the "player".
**Called as:** inventory
**Contraints:** A "player" entity must exist.

### Inspect
**Description:** Will display the stats of an entity given its id.
**Called as:** inspect id
**Contraints:** The id must be an integer that corresponds to a valid entity within the entity list.

### Tile
**Description:** Will display a description of the tile at the given grid position.
**Called as:** tile x y
**Contraints:** (x,y) must be integers within the current grid bounds and the map must have been created.