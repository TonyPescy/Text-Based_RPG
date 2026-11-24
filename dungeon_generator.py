"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: November 23, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: dungeon_generator.py
Purpose: Houses all dungeon generation logic and methods.
"""

# Note: Will utilize the Cellular Automata method for more natural caverns

# Imports
import random
from collections import deque
from dungeon_floor import DungeonFloor
from grid import Grid, Tile


# Dungeon Generator Class
class DungeonGenerator:
    # Constants
    # Add new passable terrain names here
    SPECIAL_TILES = ["ShallowWater", "Forest"]
    SPECIAL_TILE_PERCENT_MAX = int(100 / len(SPECIAL_TILES))
    SMOOTHING_ITERATIONS = 1  # 1 Smoothing chosen for more rough/irregular caverns

    # Init
    # Initializes Dungeon Generator instance
    # Params:   wall_chance - initial chance of a wall
    # Returns: None
    def __init__(self, wall_chance=0.45):
        # Ensure valid wall chance
        if not 0 <= wall_chance <= 1:
            raise ValueError("wall_chance must be between 0 and 1")
        # Assign variables
        self.__wall_chance = wall_chance
        self.__rng = random.Random()
        self.__last_terrain_percentages = None

    # Get Terrain Percentages
    # Get the terrain chances generated for the most recent floor
    # Params: None
    # Returns: None
    def get_terrain_percentages(self):
        return (
            dict(self.__last_terrain_percentages)
            # Checks thats the floor was generated
            if self.__last_terrain_percentages is not None
            else None
        )

    # Roll Terrain Percentages
    # Roll new terrain percentages based on number of terrains - save remainder for Floor tiles
    # Params:   None
    # Return:   None
    def __roll_terrain_percentages(self):
        # Inital variables
        percentages = {}
        remaining = 100
        # For every terrain tile verify valid tile and generate spawn chance based on total numbers of terrain
        for name in self.SPECIAL_TILES:
            # Checks that tiles are "special" terrain tiles
            if not Tile.is_valid_tile(name) or name.lower() in ("floor", "wall"):
                raise ValueError(f"Unsupported special tile: {name}")
            # Checks for non-passable tiles
            elif not Tile.create_tile(name).get_info().passable:
                raise ValueError(f"Special tile must be passable: {name}")
            # Prevents duped tiles
            elif name in percentages:
                raise ValueError(f"Duplicate special tile: {name}")

            # Cap at remaining percent so future additions cannot exceed 100
            chance = self.__rng.randint(
                0, min(self.SPECIAL_TILE_PERCENT_MAX, remaining)
            )
            # Assign percent to tile name
            percentages[name] = chance
            # Reduce total remaining percent to assign
            remaining -= chance
        # Set remainder to Floor tiles
        percentages["Floor"] = remaining
        # Return list of all terrain percents
        return percentages

    # Smooth
    # Apply exactly 8-neighbor Cellular Automata smoothing iteration - Map border will always be walls
    # Params:   walls - list where True = Wall and False = Floor
    #           width/height - ints - Grid dimensions
    # Returms: result - Grid of True and False
    def __smooth(self, walls, width, height):
        # Creates grid of False
        result = [[False for _ in range(height)] for _ in range(width)]
        # Iterate over grid
        for x in range(width):
            for y in range(height):
                # If border tile -> assign Wall
                if x in (0, width - 1) or y in (0, height - 1):
                    result[x][y] = True
                    continue

                wall_neighbors = 0
                # Check surrounding tiles - 3x3 square of tiles
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        # If current tile
                        if dx == 0 and dy == 0:
                            continue
                        # Get new tiles x and y coordinates
                        nx, ny = x + dx, y + dy
                        # Check for new tile is within grid OR if it is a wall
                        if not (0 <= nx < width and 0 <= ny < height) or walls[nx][ny]:
                            wall_neighbors += 1
                # Becomes True (Wall) if wall_neighbors >= 5 or False if wall_neighbors < 5
                result[x][y] = wall_neighbors >= 5
        return result

    # Find Open Regions
    # Finds all disconnected groups of walkable tiles using BFS
    # Params: walls - list where True = Wall and False = Floor
    #         width/height - ints - Grid dimensions
    # Returns: regions - list of coordinates - list of Coordinates of each connected open region
    def __find_open_regions(self, walls, width, height):
        # Track all checked tiles
        visited = set()
        # Store all open regions that will be connected
        regions = []

        # Iterate over all tiles except border walls
        for x in range(1, width - 1):
            for y in range(1, height - 1):

                # Skip walls and previously visited tiles
                if walls[x][y] or (x, y) in visited:
                    continue

                # Create a new region starting at the current tile
                region = {(x, y)}

                # Mark the starting tile as checked/visited
                visited.add((x, y))

                # Create a queue for BFS
                queue = deque([(x, y)])

                # Loop until all connected tiles have been checked
                while queue:

                    # Get the next tile from the queue
                    cx, cy = queue.popleft()

                    # Check the four directly adjacent tiles
                    for nx, ny in (
                        (cx + 1, cy),
                        (cx - 1, cy),
                        (cx, cy + 1),
                        (cx, cy - 1),
                    ):

                        # Check if the neighboring tile is within boundaries (except border wall), not a wall, and not checked
                        if (
                            1 <= nx < width - 1
                            and 1 <= ny < height - 1
                            and not walls[nx][ny]
                            and (nx, ny) not in visited
                        ):

                            # Mark the tile as visited
                            visited.add((nx, ny))

                            # Add the tile to the current region
                            region.add((nx, ny))

                            # Add the tile to the queue for further exploration
                            queue.append((nx, ny))

                # Add the completed region to the list
                regions.append(region)

        # Return all connected open regions
        return regions

    # Carve Corridor
    # Creates a corridor between two positions
    # Params: walls - list where True = Wall and False = Floor
    #         start/end - tuples - Starting and ending coordinates
    # Returns: None
    def __carve_corridor(self, walls, start, end):

        # Get starting and ending coordinates
        x1, y1 = start
        x2, y2 = end

        # Randomly choose horizontal or vertical first - Less predictable generation
        horizontal_first = self.__rng.choice([True, False])

        if horizontal_first:

            # Carve a horizontal hallway
            for x in range(min(x1, x2), max(x1, x2) + 1):
                walls[x][y1] = False

            # Carve a vertical hallway
            for y in range(min(y1, y2), max(y1, y2) + 1):
                walls[x2][y] = False

        else:

            # Carve a vertical hallway
            for y in range(min(y1, y2), max(y1, y2) + 1):
                walls[x1][y] = False

            # Carve a horizontal hallway
            for x in range(min(x1, x2), max(x1, x2) + 1):
                walls[x][y2] = False

    # Connect Regions
    # Connects all disconnected open regions using L-shaped corridors
    # Params: walls - 2D list where True = Wall and False = Floor
    #         width/height - ints - Grid dimensions
    # Returns: None
    def __connect_regions(self, walls, width, height):

        # Loop connecting regions until all are connected
        while True:

            # Find the current disconnected open regions
            regions = self.__find_open_regions(walls, width, height)

            # Stop when all open tiles are connected
            if len(regions) <= 1:
                return

            # Start with the largest region
            regions.sort(key=len, reverse=True)
            connected = regions[0]

            # Find the closest tile pair between the largest region and any other disconnected region
            closest_start = None
            closest_end = None
            shortest_distance = float("inf")

            for region in regions[1:]:
                for start in connected:
                    for end in region:

                        # Calculate Manhattan distance
                        distance = abs(start[0] - end[0]) + abs(start[1] - end[1])

                        # Update the closest connection found
                        if distance < shortest_distance:
                            shortest_distance = distance
                            closest_start = start
                            closest_end = end

            # Connect the two regions with a hallway
            self.__carve_corridor(walls, closest_start, closest_end)

    # Farthest
    # Find the most distant reachable position from a starting point
    # Params:   start - tuple - starting grid coordinates
    #           open_tiles - set - Coordinates of all walkable tiles
    # Returns:  farthest - tuple - farthest grid position from starting point
    def __farthest(self, start, open_tiles):
        # Create queue with starting position
        queue = deque([start])
        # Track distance from start to each tile - starts at 0
        distances = {start: 0}
        # Set starting farthest as start tile
        farthest = start

        # Loop through all tiles
        while queue:
            # Get next position from queue
            x, y = queue.popleft()

            # If new tile is farther - update faethest
            if distances[(x, y)] > distances[farthest]:
                farthest = (x, y)

            # Check cardinally neighboring tiles
            for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                # Check if they are walkable and have not been visited
                if neighbor in open_tiles and neighbor not in distances:
                    # Record each neighbors distance from starting position
                    distances[neighbor] = distances[(x, y)] + 1
                    # Add neighboring tile to queue to continue search
                    queue.append(neighbor)

        # Return the farthest reachable position from start
        return farthest

    # Generate
    # Generate a connected DungeonFloor with walls, terrain, entrance, and exit
    # Params:   floor_number - int - Number of the current floor
    #           width/height - ints - grid dimensions
    # Returns: floor - DungeonFloor - Generated dungeon floor
    def generate(self, floor_number, width, height):
        # Validate dungeon dimesnions
        if (
            not isinstance(width, int)
            or isinstance(width, bool)
            or not isinstance(height, int)
            or isinstance(height, bool)
            or not Grid.within_bounds(width, height)
        ):
            raise ValueError("Invalid dungeon dimensions")

        elif (
            not isinstance(floor_number, int)
            or isinstance(floor_number, bool)
            or floor_number < 1
        ):
            raise ValueError("Floor number must be a positive integer")

        # Generate the wall layout - True = Wall and False = Floor
        walls = [
            [
                (
                    # Border tiles are always walls
                    x in (0, width - 1)
                    or y in (0, height - 1)
                    # Random chance to be walls - interior tiles
                    or self.__rng.random() < self.__wall_chance
                )
                for y in range(height)
            ]
            for x in range(width)
        ]

        # Smooth walls with Cellular Automata
        for _ in range(self.SMOOTHING_ITERATIONS):
            walls = self.__smooth(walls, width, height)

        # Find all walkable tiles in boudnaries
        open_tiles = {
            (x, y)
            for x in range(1, width - 1)
            for y in range(1, height - 1)
            if not walls[x][y]
        }

        # Ensure there are enough tiles for both entrance and exit - If not convert interior to all floor as emergency fix
        if len(open_tiles) < 2:
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    walls[x][y] = False

        # Connect all disconnected open regions using corridors
        self.__connect_regions(walls, width, height)

        # Recalculate open tiles with corridors added
        open_tiles = {
            (x, y)
            for x in range(1, width - 1)
            for y in range(1, height - 1)
            if not walls[x][y]
        }

        # Create new dungeon floor and its grid
        floor = DungeonFloor(floor_number, width, height)
        grid = floor.get_grid()
        # Calculate percentages for terrains
        percentages = self.__roll_terrain_percentages()

        # Loop through every tile on floor
        for x in range(width):
            for y in range(height):

                # Set all non-walkablem tiles to Walls
                if (x, y) not in open_tiles:
                    grid.set_tile(x, y, "Wall")
                    continue

                # RNG for terrain type
                roll = self.__rng.randint(1, 100)
                cumulative = 0

                # Default tile of Floor
                tile_type = "Floor"
                # Check each terrain against the percentage roll
                for name, chance in percentages.items():
                    # Chance of tile total
                    cumulative += chance
                    # If terrain type falls within tile chance
                    if roll <= cumulative:
                        tile_type = name
                        break

                # Assign tile type at current position
                grid.set_tile(x, y, tile_type)

        # Select distant entrance and exit points from the connected region.
        start = min(open_tiles)
        # Find far position for entrance
        entrance = self.__farthest(start, open_tiles)
        # Find farthest position from the entrance for the exit - Could make random for more variety/Randomness in gameplay
        exit_position = self.__farthest(entrance, open_tiles)
        # Set positions to dungeon floor
        floor.set_entrance(*entrance)
        floor.set_exit(*exit_position)
        # Store terrain percentages for later use
        self.__last_terrain_percentages = percentages

        # Return dungeon floor
        return floor
