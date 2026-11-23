# Text-Based_RPG
## Description
Test-based RPG where a grid of tiles is occupied by players, monsters, and items. Playing the game is done through the Command Line Interface

## Author
Tony Pescatore

## Table of Contents
[Running The Game](#running-the-game)

[Entities](#entities)

[Equipment](#equipment)

[Tiles](#tiles)

[Spells](#spells)

[Command Line Interface Guide](#command-line-interface-guide)

[Design Decisions](#design-decisions)

[Game Commands](#game-commands)

## Running The Game
[Table of Contents](#table-of-contents)

Run the game by entering the following command in your terminal:

```
python main.py
```

Exit the game by using the keyboard interrupt or by entering "quit" as a command.


## Entities
[Table of Contents](#table-of-contents)

### Player Entities
- **Warrior**

| Stat         | Base Value |
| ------------- |:-------------:|
| Health         | 120 |
| Attack      |  15    |
| Defence      | 10 |
| Speed        | 5 |
| Attack Type | Melee |

- **Mage**

| Stat         | Base Value |
| ------------- |:-------------:|
| Health         | 70 |
|  Mana  |  100  |
|  Spell Power  |  25  |
| Attack      |  8    |
| Defence      | 4 |
| Speed        | 5 |
| Attack Type | Melee / Caster |


### Non-player Entities
- **Goblin**

| Stat         | Base Value |
| ------------- |:-------------:|
| Health         | 45 |
| Attack      |  12    |
| Defence      | 3 |
| Speed        | 6 |
| Attack Type | Melee |

- **Skeleton**

| Stat         | Base Value |
| ------------- |:-------------:|
| Health         | 60 |
| Attack      |  10    |
| Defence      | 8 |
| Speed        | 4 |
| Attack Type | Ranged |

- **Ogre**

| Stat         | Base Value |
| ------------- |:-------------:|
| Health         | 150 |
| Attack      |  20    |
| Defence      | 1 |
| Speed        | 2 |
| Attack Type | Melee |

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
| Forest        | Tile that grants the entity +5 defence and a speed debuff of -2 |

## Spells
[Table of Contents](#table-of-contents)

| Spells         | Desciption |
| ------------- |:-------------:|
| Fireball         | Deals high damage |
| Heal      |  Heals the targets health    |
| Frostbolt      | Deals lower damage and applies -2 speed debuff |

## Command Line Interface Guide
[Table of Contents](#table-of-contents)

**Description:** This is a guide to the Command Line Interface to be used to play the game. It will outline and define the commands that are currently supported within the game.

### Init Map
**Description:** Will create a map with the provided width and height.

**Called as:** init map [width] [height]

**Contraints:** Width and height are integers between 5 and 50 inclusive.

**Undoable/Redoable:** True

### Set Tile
**Description:** Will set the tile at a given grid position to be the provided tile type.

**Called as:** set tile [x] [y] [tile_type]

**Contraints:** tile_type must be within list of valid tile types, (x,y) must be integers within the current grid bounds, and map must have been created.

**Undoable/Redoable:** True

### Spawn
**Description:** Will spawn specified entity or item at given grid position

**Called as:** 
- spawn [entity_type] [x] [y] -> Spawns entity at given coordinates
- spawn loot [item_name] [x] [y] -> Spawns loot at given coordinates

**Contraints:**  (x,y) must be integers within current grid bounds and map must have been created.
- **Spawn Entity:** entity_type must be within list of valid entity types and there must not be any other entity already present at the given grid position.
- **Spawn Loot:** item_name must be within list of valid equipment types.

**Undoable/Redoable:** True

### Swap
**Description:** Will equip provided item in the given, or determined, inventory slot to a "player".

**Called as:** swap [id] [slot] [item_name]

**Contraints:** item must be within the list of valid items. id must be an integer within the current entity list and slot must be within valid slots.

**Undoable/Redoable:** True

### Inventory
**Description:** Will display the current inventory of provided entity.

**Called as:** inventory [id]

**Contraints:** An entity with a matching id must exist.

**Undoable/Redoable:** False

### Inspect
**Description:** Will display the stats of an entity given its id.

**Called as:** inspect [id]

**Contraints:** The id must be an integer that corresponds to a valid entity within the entity list.

**Undoable/Redoable:** False

### Tile
**Description:** Will display a description of the tile at the given grid position.

**Called as:** tile [x] [y]

**Contraints:** (x,y) must be integers within the current grid bounds and the map must have been created.

**Undoable/Redoable:** False

### Pickup
**Description:** Will pickup the item with the given name at the given entity's current location, if it is present.

**Called as:** pickup [id] [item_name]

**Contraints:** id must be an integer within the current entity list, the item with the same name must be located at the same tile as the entity, and the entity must have space in their backpack for the item.

**Undoable/Redoable:** True

### Drop
**Description:** Will drop the item with the given name at the given entity's current location.

**Called as:** drop [id] [item_name]

**Contraints:** id must be an integer within the current entity list and an item with the same name must be within the entity's backpack.

**Undoable/Redoable:** True

### Give
**Description:** Will give the item with the given name to the matching entity.

**Called as:** give [id] [item_name]

**Contraints:** id must be an integer within the current entity list and the item must be a valid item.

**Undoable/Redoable:** True

### Use
**Description:** Will use the item with the given name on the matching entity.

**Called as:** use [id] [item_name]

**Contraints:** id must be an integer within the current entity list and the item must be a valid consumable within the given entity's inventory.

**Undoable/Redoable:** True

### Move
**Description:** Will move the given entity to the grid position if they are within range and a valid.

**Called as:** move [id] [x] [y]

**Contraints:** id must be an integer within the current entity list and the x,y must correspond to a valid grid position for the entity to occupy.

**Undoable/Redoable:** True

### Attack
**Description:** First entity will attack the second entity with damage being calculated as attack vs defence. When an defender's health reaches zero they will die and receive the "Dead" status.

**Called as:** attack [attacker_id] [defender_id]

**Contraints:** ids must be an integer within the current entity list and the defender must be within the attack range of the attacker. 

**Undoable/Redoable:** True

### Cast
**Description:** First entity will cast a spell on the other entity. This can do damage using the spell power and the spell damage modifier against the targets defence, it can heal them, and it can apply an effect on them. When a targets health reaches zero they will die and receive the "Dead" status.

**Called as:** cast [caster_id] [target_id] [spell_name]

**Contraints:** ids must be an integer within the current entity list and the defender must be within the spell range of the caster. The spell must also exist in the valid spell list

**Undoable/Redoable:** True

### Tick
**Description:** Adavances to the next turn. Turns start at 1 and increase by 1 when tick is called.

**Called as:** tick

**Contraints:** Map must be created.

**Undoable/Redoable:** True

### Save
**Description:** Captures the snapshot of the game state via the memento pattern and converts it to JSON through GameStateManager. Then writes save data to given file name, and updates save status.

**Called as:** save [filename]

**Contraints:** Game state must be created and active.

**Undoable/Redoable:** True

### Load
**Description:** Reads the specified file, parses the save data, restores the game state, and resets the sessions save status.

**Called as:** load [filename]

**Contraints:** File must exist that matches given file name.

**Undoable/Redoable:** True

### State-Info
**Description:** Displays metadata about the current session (Turn Count, Active Entities, Save Status etc).

**Called as:** state-info

**Contraints:** Game state must be created and active.

**Undoable/Redoable:** False

### Undo
**Description:** Undos the most recent command if it is able to be undone.

**Called as:** undo

**Contraints:** An undo-able command must be within the undo stack.

**Undoable/Redoable:** False

### Redo
**Description:** Redos the most recently undone command if it is able to be redone.

**Called as:** redo

**Contraints:** An redo-able command must be within the redo stack.

**Undoable/Redoable:** False

### History
**Description:** Summarizes the list of recent commands in the undo and redo stacks.

**Called as:** history

**Contraints:** None

**Undoable/Redoable:** False

### State
**Description:** Gets current state of specified entity.

**Called as:** state [id]

**Contraints:** id must be a valid integer, entity id, and correspond to a non-player entity.

**Undoable/Redoable:** False

### Simulate
**Description:** Executes the specified entities current state.

**Called as:** simulate [id]

**Contraints:** id must be a valid integer, entity id, and correspond to a non-player entity.

**Undoable/Redoable:** True

### Force
**Description:** Forces an entity into a specific state for testing and debugging.

**Called as:** force [id] [state_name]

**Contraints:** id must be a valid integer, entity id, and correspond to a non-player entity. state name must be a valid state for the corresponding entity id.

**Undoable/Redoable:** True

## Design Decisions
[Table of Contents](#table-of-contents)

**Description:** The following design decisions will provide an overview of each section of the project as well as a breif explanation of why and how some mechanics are implemented the way that they are. Each section was split using bullet points to avoid a large convulated block of text forming when new features or designs are added to the project.

### Grid 
- The grid is used as the worlds coordinate system that will track entity positions, tile states, and occupancy across the multiple tile types within the game. The grid is represented by a 2D matrix of Tiles. 
- This grid can range from 5x5 to a max of 50x50 Tiles. It is initialized in such a way that all tiles are passable and open floor tiles. 
- It has a get_stats function which is used to get the stats of the tile at the designated grid position.
- It has is_passable, within_bounds, is_valid_grid_position, etc. helper functions which help to verify the values that interact with the grid, especially in the CLI.
- Grid distances will be calculating using Manhattan Distance.
- When using A* pathing, entities will not block their tiles. So you will be able to move through entities but will not be able to end on the same tile as an entity.
- Creates and resotres its own memento to follow Single Responsibility Principle.

### Tiles
- Tiles are what make up the grid. Each Tile has its typing, a boolean determining whether they are passable or not for collision/movement restrictions, and a list of occupants. 
- Each tile can have more than 1 occupant, which will be represented by a list of entity IDs, or if there are no occupants it will be instead be filled with the empty tile constant value. 
- Each tile also has an item_list for loot that can be picked up, dropped, or spawned at the tile location.
- Impassable tiles also block Line of sight for ranged/magic attacks.
- There are only 4 valid tile types, which are: Floor, Wall, ShallowWater, and Forest. 
    - **Floor Tiles:** Act as open tiles which are passable and will not impede movement in anyway. 
    - **Wall Tiles:** Impassable tiles that will be used to enforce spatial boundaries and colision. 
    - **ShallowWater Tiles:** Passable tiles that apply a negative modifier that will impede the movement of its occupant(s).
    - **Forest Tiles:** Passable tiles that apply positive modifier to entity defence as well as impeding their movement slightly.

### Spells
- Spells are their own class each with their own spell attack ranges, spell damage modifiers, and spell effects.
- Three types of spells exist:
    - **Offensive:** Purely damage based magic.
    - **Support:** Supports the targetted entity with healing.
    - **Control:** Deals lower damage but applies debuffs to targets.
- Standard healing spells cannot revive characters from the dead, adn these specialized spells must revive the entity before it disappears completely, similar to death saves in Dungeon and Dragons 5e.

### Attacks
- Currently there are two types of attacks that can be made, excluding spellcasting. The only difference currently is their attack ranges.
    - **Melee:** Physical attacks made within 1 tile.
    - **Ranged:** Physical attacks made within 3 tiles.

### Entities
- Entities include both player and monster classes which use base stats and conditional modifiers to get their final stat values. Entities have the following stats: id, type, position, health, attack, defence, speed, inventory, and active_modifiers. These can be added to in some cases, such as with the player Mage class which adds mana and spell power. 
- Max Health and Max Mana is tracked to allow for consumables to refill health and mana, it also prevents any overflow errors with those consumables. They also allow for percentages to be accurately used based on max health/mana of an entity instead of on their current health and for easier tracking of damage during combat. 
- The entity's inventory will be filled with 3 pieces of equipment with only 1 of each type being allowed to be eqipped at a time. 
- Entities will have a dictionary of active modifiers which will contain two keys, Flat_modifiers and Percent_modifiers, which will make it significantly easier to calculate the entities final stats with these modifiers taken into account.
- Entities will have 5 spaces open for their backpack, this is where they store their items in their inventory as well as any backup items and consumables.
- When an entity dies they will remain on the map for 3 turns, for looting purposes, and will be given the "Dead" status as a temporary buff. This will prevent them from making any actions or being targetted, but will keep them present on the map.
- After 3 turns on the map, the "Dead" entity will be removed from the game completely.
- Creates and resotres its own memento to follow Single Responsibility Principle.

### Equipment
- The equipment class represents items that will be held within an entity's inventory. There are only 3 types, weapon, armor, and accessory, all of which can only have 1 equipped in a single slot at a time. These items will have modifiers that will be to calculate the final stat values for the entity that they are equipped to. 
- The items themselves will inherit the Equipment class then add their own stats to it so make getting the stats from each item simpler.
- New items consumables will inherit the Equipment class but expand on it with two types of effects: over time effects and instant effects. This allows for them to be consumed (consumables), while other item cannot be consumed, and for their effects to effect the entity stats. Over time effects duration are reduced by 1 per tick of the in game ticker. They will be removed when the duration reaches 0.

### Test Suite 
- The test suite tests the public facing methods as they will call and use the other private facing methods. This means that these private facing methods will also be tested in tandem. It incldues verbose tests includings tests on the boundary values, the validity of inputs, and ensures that all public facing methods and private methods are working as intended. 
- All other aspects of the project are tested within this suite including the Command Line Interface, Equipment, Entities, Grid, Game State, Game State Manager, Spells, Tiles, Command, and Command Manager.
- Each suite has a set of helper functions to reduce the amount of code needed, but does not detract from the readability of the code.

### Command Line Interface
- The command line interface is where the game in played. Running the command line interface will allow the user to input commands, which will be handled accordingly by the command line interfaces process_command method. This will return descriptive error messages so that users will know what was wrong with their inputs. 
- Houses the game state variable through which interaction between files and objects are handled.
- It also contains the main function that will prompt for the commands in the terminal, the player can exit at any time by entering 'quit'.
- Allows for files to be piped/redirected in for inputs and will account for end of file errors.
- Finally is used so that goodbye message is always sent.


### Game State
- Manages time passing in game through ticks.
- The game state will house the current game grid of tiles, a list of the current entities, an entity id tracker, a boolean to determine if the map was already created, a turn tracker, and a boolean to determine the save status.
- Interacts with the other files and classes for the command line interface to protect sensitive information.
- Creates and resotres its own memento to follow Single Responsibility Principle.

### Game State Manager
- Gathers all immutable read-only mementos that are required for saving, Game State, Entities within active entity list, active Equipment Grid, and Tiles, by using their classes create_memento methods. Then utilizes JSON to save them to a file that will be used to load them.
- Handles loading mementos from files and uses the respective class method, restore, to restore to a game-ready object.
- Classes that have stats that change such as entity, grid, and game state will need the momentos created, other than that new instances will be created for static valued instances (Example: Items will always have the same stat so they will be recreated when loading a save). These static instances can be created from their name so where they are saved will just be a name to recreate them.
- Cleans and validates save data before calling restore functions to ensure game state is restored correctly and completely.
- Handles loading and saving from files as well as conversion to JSON from mementos. Calls other classes to create and to restore their own memento to follow Single Responsibility Principle.

### Command
- Commands are created as objects which allow for them to be run using .execute().
- Many commands, those that change gamestate or change files (for example, save), can be undone or redone using .undo() or .redo() respectively.
- Other commands that cannot be undone or redone will simply be passed on when it comes to undo/redo commands and history.
- Game state verification checks are done prior to the execution of the commands being undone or redone, so the reverification is redundant here. Before they are added to history all of the relevant variables are checked and preserved so that undoing or redoing can be done without errors.
- Few commands cannot be redone as they either do not change the game state or files, or they are either undo/redo.

### Command Manager
- Houses all universal functions that are useful when running commands.
- Manages command history allowing for undo and redo to function accurately to their proper history.
- Redos are cleared when undoable commands are executed to prevent issues with redoing something after it has already been used to manipulate something else.

### Entity State
- Houses all state classes and methods.
- Currently three states for entities:
    - **Defending** - Entity is waiting for player to come into range.
    - **Attacking** - Entity is attempting to chase and attack player.
    - **Fleeing** - Entity is attempting to run away and escape player.
    - **Raging** - Entity will gain an attack buff and keeping attacking the player.
- Triggers for the states are:
    - **Defending** - Player out of speed range of entity.
    - **Attacking** - Player is within speed range of entity.
    - **Fleeing** - Entity has less than 25% of their max health remaining.
    - **Raging** - Entity has less than 50% and can become enraged.
- Each state is responsible to tell the manager when it is time to transition.
- Attacking and Fleeing AI movement use A* pathfinding.
- Currently moving and attacking are considered seperate actions, therefore an entity cannot move towards the player and attack on the same tick/turn.
- Entities that can become enraged:
    - Ogre

### Entity State Manager
- Houses all functions needed for entity state management.
- Transistions to new entity states, updates current state, and gets current state.
- Listens to the state to determine when to transition.
- Tick will evaluate environment and trigger the transistions based on findings.


### Other
- Values for entities, tiles, spells, equipment, grids, and game state are marked as private (__varname). To access this information x.getinfo() will return a immutable copy to prevent any of that private data from being public and able to be modified. When these do need to be changed, such as an entity losing health, it is handled within its own class.
- Mementos are snapshots of the current game state and include the information that is necessary to rebuild the object in its current state. These are immutable and do not expose the private fields as they use a dataclass that will then have the information copied into its fields.

### Known Issues
- Game saves can become extremely large, especially if many commands are performed and the UNDO history is never reset. Could be recursion issue somewhere in the save/memento logic.
    - Largest game save with fuzz based testing was ~2.35 GB