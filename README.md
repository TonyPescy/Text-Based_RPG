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
The test suite only tests the public facing functions as they will call and use the other private facing functions. This means that these private facing functions will also be tested in tandem.

### Command Line Interface
