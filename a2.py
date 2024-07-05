# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# Name: Connor Ilic
# Student Number: s48839341
# ----------------

# Write your classes and functions here

# Model Classes
class Tile():
    def __init__(self) -> None:
        """Initialize a new instance for this class."""
        self._symbol: str = TILE_SYMBOL
        self._name: str = TILE_NAME
        self._block: bool = False
    
    def __repr__(self) -> str:
        """Returns a string representation of the instance.

        The string is an expression that can be used to recreate
        the object with the same attributes.
        """
        return "{}()".format(self._name)
    
    def __str__(self) -> str:
        """Returns a readable string that represents the instance."""
        return self._symbol

    def get_tile_name(self) -> str:
        """Returns the tile name."""
        return self._name
    
    def is_blocking(self) -> bool:
        """Returns True if tile is blocking else False.
        
        A blocked tile prevents entities from standing on it.
        """
        return self._block

class Ground(Tile):
    def __init__(self) -> None:
        super().__init__()
        self._symbol: str = GROUND_SYMBOL
        self._name: str = GROUND_NAME

class Mountain(Tile):
    def __init__(self) -> None:
        super().__init__()
        self._symbol: str = MOUNTAIN_SYMBOL
        self._name: str = MOUNTAIN_NAME
        self._block: bool = True

class Building(Tile):
    def __init__(self, initial_health: int) -> None:
        """Initialize a new instance for this class.
        
        Args:
            initial_health: The health as an integer the building instance
                has when initiated.
        """
        super().__init__()
        self._health: int = initial_health
        self._name: str = BUILDING_NAME
        self._argument: str = self._symbol
    
    def __repr__(self) -> str:
        return "{}({})".format(self._name, self._health)

    def __str__(self) -> str:
        return str(self._health)

    def get_health(self) -> int:
        """Returns the health of the instance as an integer."""
        return self._health
    
    def is_destroyed(self) -> bool:
        """Returns True if health is 0 else False"""
        return not bool(self._health)
    
    def is_blocking(self) -> bool:
        return not self.is_destroyed()
    
    def damage(self, damage: int) -> None:
        """Changes the health of the instance by the damage integer.
        
        If damage is positive then health decreases, if negative then health
        increases. No matter the damage, health will stay between 0 and 9.
        """
        if not self.is_destroyed():
            self._health = max(0, min(self._health - damage, 9))

class Board():
    def __init__(self, board: list[list[str]]) -> None:
        """Initialize a new instance for this class.
        
        Args:
            board: Each list inside the board list represents a row, and
                each character inside the row list represents a tile
                instance by its string representation. Rows are sorted
                from top to bottom and columns are sorted from left to right.
        """
        newboard: list[list[str]] = []
        i: int = 0

        for row in board:
            newboard.append([])

            for column in row:
                tile_string: list = column
                tile: Tile = None

                if tile_string.isnumeric():
                    tile = Building(int(tile_string))
                elif tile_string == GROUND_SYMBOL:
                    tile = Ground()
                elif tile_string == MOUNTAIN_SYMBOL:
                    tile = Mountain()
                else:
                    tile = Tile()
                
                newboard[i].append(tile)
            
            i += 1
        
        self._board: list[list[str]] = newboard

    
    def __str__(self) -> str:
        """Returns a readable string that represents the instance.
        
        Returns:
            Each line of the string represents a row and each character
            in that line represents a tile as its string representation.
        """
        string: str = ""

        for row in self._board:

            for column in row:
                string += str(column)
            string += "\n"
        
        string = string[:-1]
        return string

    def __repr__(self) -> str:
        """Returns a string representation of the instance.

        The string is an expression that can be used to recreate
        the object with the same attributes.
        """
        string: str = "["

        for row in self._board:
            string += "["

            for column in row:
                string += f"'{column}', "

            string = string[:-2] + "], "

        string = string[:-2] + "]"
        return f"Board({string})"

    def get_dimensions(self) -> tuple[int, int]:
        """Returns the dimension of the board as (#row, #column)."""
        return (len(self._board), len(self._board[0]))
    
    def get_tile(self, position: tuple[int, int]) -> Tile:
        """Returns the instance of a tile at position.
        
        Args:
            position: The coordinate as an integer tuple of (row, column).
        """
        y, x = position
        return self._board[y][x]
    
    def get_buildings(self) ->  dict[tuple[int, int], Building]:
        """Returns a dictionary of buildings on the board.
        
        Returns:
            A dictionary where the keys are coordinates as an integer tuple
            of (row, column) and the value is the building instance at that
            coordinate.
        """
        dictionary: dict = {}
        
        row_num, column_num = self.get_dimensions()
        for row in range(0, row_num):

            for column in range(0, column_num):

                tile: Tile = self.get_tile((row,column))
                if str(tile).isdigit():
                    dictionary[(row,column)] = tile

        return dictionary

class Entity():
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        """Initialize a new instance for this class.
        
        Args:
            position: The coordinate of the entity instance
                as an integer tuple of (row, column).
            initial_health: The health as an integer the entity instance
                has when initiated.
            speed: An integer which effects how many tiles an entity can
                move in a turn.
            strength: An integer which effects how much health from a
                building or entity is lost/gained when this entity attacks
                it.
        """
        self._yposition, self._xposition = position
        self._health: int = initial_health
        self._speed: int = speed
        self._strength: int = strength
        self._name: str = ENTITY_NAME
        self._symbol: str = ENTITY_SYMBOL
        self._icon: str = 'E'
        self._friendly: bool = False
    
    def __repr__(self) -> str:
        """Returns a string representation of the instance.

        The string is an expression that can be used to recreate
        the object with the same attributes.
        """
        return "{}(({}, {}), {}, {}, {})".format(
            self._name,
            self._yposition,
            self._xposition,
            self._health,
            self._speed,
            self._strength
        )
    
    def __str__(self) -> str:
        """Returns a readable string that represents the instance."""
        return "{},{},{},{},{},{}".format(
            self._symbol,
            self._yposition,
            self._xposition,
            self._health,
            self._speed,
            self._strength
        )
    
    def get_symbol(self) -> str:
        """Returns the symbol of the entity as a string."""
        return self._symbol
    
    def get_name(self) -> str:
        """Returns the name of the entity as a string."""
        return self._name
    
    def get_position(self) -> tuple[int, int]:
        """Returns the position of the entity as an integer tuple."""
        return (self._yposition, self._xposition)
    
    def set_position(self, position: tuple[int, int]) -> None:
        """Sets the position of the entity.
        
        Args:
            position: an integer tuple of coordinates in the form,
                (row, column).
        """
        self._yposition, self._xposition = position
    
    def get_health(self) -> int:
        """Returns the health as an integer of the entity."""
        return self._health
    
    def get_speed(self) -> int:
        """Returns the speed as an integer of the entity."""
        return self._speed
    
    def get_strength(self) -> int:
        """Returns the strength as an integer of the entity."""
        return self._strength
    
    def is_alive(self) -> bool:
        """Returns False if health is 0 else True"""
        return bool(self._health)

    def damage(self, damage: int) -> None:
        """Decreases the health of the entity by the damage integer.
        
        Args:
            damage: An integer which dictates how much health is changed.
                A positive integer will decrease the health while
                a negative integer will increase it.
        """
        if not self.is_alive():
            return
        
        self._health = max(0, self._health - damage)
    
    def is_friendly(self) -> bool:
        """Returns True."""
        return self._friendly
    
    def get_targets(self) -> list[tuple[int, int]]:
        """Returns a list of integer tuples of coordinates in (row, column).
        
        Returns:
            A list of integer tuples of coordinates in (row, column) of which
            the entity will attack any other entities 
            or buildings in those coordinates.
        """
        targets: list = []
        targets.append((self._yposition, self._xposition + 1))
        targets.append((self._yposition, self._xposition - 1))
        targets.append((self._yposition + 1, self._xposition))
        targets.append((self._yposition - 1, self._xposition))
        return targets

    def attack(self, entity: "Entity") -> None:
        """Attacks the passed entity based on this entities strength.
        
        Args:
            entity: An entity instance which will be attacked by this entity
                based on its strength.
        """
        entity.damage(self.get_strength())
    
    def get_icon(self) -> str:
        """Returns the icon to be displayed on the view."""
        return self._icon

class Mech(Entity):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name: str = MECH_NAME
        self._symbol: str = MECH_SYMBOL
        self._friendly: bool = True
        self._active: bool = True
        self._xprev_pos, self._yprev_pos = position
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._xprev_pos = self._xposition
        self._yprev_pos = self._yposition
        super().set_position(position)

    def enable(self) -> None:
        """Sets the active booleon to True."""
        self._active = True
    
    def disable(self) -> None:
        """Sets the active booleon to False."""
        self._active = False
    
    def is_active(self) -> bool:
        """Returns the active booleon."""
        return self._active

class TankMech(Mech):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name: str = TANK_NAME
        self._symbol: str = TANK_SYMBOL
        self._icon: str = TANK_DISPLAY
    
    def get_targets(self) -> list[tuple[int, int]]:
        targets: list = []

        for i in range(1,6):
            targets.append((self._yposition, self._xposition + i))
            targets.append((self._yposition, self._xposition -i))
        
        return targets

class HealMech(Mech):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name: str = HEAL_NAME
        self._symbol: str = HEAL_SYMBOL
        self._icon: str = HEAL_DISPLAY
    
    def get_strength(self) -> int:
        """Returns the strength of this entity as a negative integer."""
        return -self._strength
    
    def attack(self, entity: Entity) -> None:
        """Heals the passed Mech/Building based on this entities strength.
        
        Args:
            entity: An entity instance which will be healed by this entity
                based on its strength.
        """
        if str(entity).isdigit():
            super().attack(entity)
            return
        
        if entity.is_friendly():
            super().attack(entity)

class Enemy(Entity):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name: str = ENEMY_NAME
        self._symbol: str = ENEMY_SYMBOL
        self._yobjective, self._xobjective = position
    
    def get_objective(self) -> tuple[int, int]:
        """Returns the coordinate as an integer tuple of (row, column).
        
        Returns:
            The coordinate as an integer tuple of (row, column) of which
            the enemy will move closer to at the end of each turn.
        """
        return (self._yobjective, self._xobjective)
    
    def update_objective(
            self,
            entities: list[Entity],
            buildings: dict[tuple[int, int], Building]
    ) -> None:
        """Updates the objective to be the enemies position.
        
        Args:
            entities: A list of entities.
            buildings: A dictionary where the keys are coordinates
                as an integer tuple of (row, column) and the value
                is the building instance at that coordinate.
        """
        self._yobjective = self._yposition
        self._xobjective = self._xposition

class Scorpion(Enemy):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name: str = SCORPION_NAME
        self._symbol: str = SCORPION_SYMBOL
        self._icon: str = SCORPION_DISPLAY
    
    def get_targets(self) -> list[tuple[int, int]]:
        targets: list = []
        for i in range(1,3):
            targets.append((self._yposition, self._xposition + i))
            targets.append((self._yposition, self._xposition - i))
            targets.append((self._yposition + i, self._xposition))
            targets.append((self._yposition - i, self._xposition))
        
        return targets
    
    def update_objective(
            self,
            entities: list[Entity],
            buildings: dict[tuple[int, int], Building]
    ) -> None:
        """Updates the objective to be the position of the healthiest mech.
        
        The healthiest mech is a mech with the most health, if there are
        multiple healthiest mechs than, the highest priority mech is
        made as the objective.

        Args:
            entities: A list of entities.
            buildings: A dictionary where the keys are coordinates
                as an integer tuple of (row, column) and the value
                is the building instance at that coordinate.
        """
        mechs = [entity for entity in entities if entity.is_friendly()]
        try:
            healthiest_mech = mechs[0]
        except:
            return super().update_objective(entities, buildings)
        
        for mech in mechs:
            if mech.get_health() > healthiest_mech.get_health():
                healthiest_mech = mech
            
        self._yobjective, self._xobjective = healthiest_mech.get_position()

class Firefly(Enemy):
    def __init__(
            self,
            position: tuple[int, int],
            initial_health: int,
            speed: int,
            strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._name = FIREFLY_NAME
        self._symbol = FIREFLY_SYMBOL
        self._icon = FIREFLY_DISPLAY
    
    def get_targets(self) -> list[tuple[int, int]]:
        targets = []
        for i in range(1,6):            
            targets.append((self._yposition + i, self._xposition))
            targets.append((self._yposition - i, self._xposition))
        return targets
    
    def update_objective(
            self,
            entities: list[Entity],
            buildings: dict[tuple[int, int], Building]
    ) -> None:
        """Updates the objective to be the position of the weakest building.
        
        The weakest building is a building with the least health, if there are
        multiple weakest buildings than, the building in the top most and left
        most row and coloumn respectively is made as the objective.

        Args:
            entities: A list of entities.
            buildings: A dictionary where the keys are coordinates
                as an integer tuple of (row, column) and the value
                is the building instance at that coordinate.
        """
        try:
            weakest_key = list(buildings.keys())[0]
        except:
            return super().update_objective(entities, buildings)
        
        for key in buildings.keys():
            weakest_building = buildings[weakest_key]
            if (
                buildings[key].get_health() < weakest_building.get_health()
                and not buildings[key].is_destroyed()
            ):
                weakest_key = key
        self._yobjective, self._xobjective = weakest_key

class BreachModel():
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """Initialize a new instance for this class.
        
        Args:
            board: A Board instance.
            entities: A list of Entity instances.
        """
        self._board: Board = board
        self._entities: list[Entity] = entities
    
    def __str__(self) -> str:
        """Returns a readable string that represents the instance.
        
        Returns:
            A string representation of the board, a blank line,
            then a line of an entity string representation for
            each entity in the entities list.
        """
        string: str = ""
        string += str(self._board) + "\n\n"

        for entity in self._entities:
            string += str(entity) + "\n"
        
        return string[:-1]
    
    def get_board(self) -> Board:
        """Returns the board instance."""
        return self._board
    
    def get_entities(self) -> list[Entity]:
        """Returns the list of entities."""
        return self._entities
    
    def get_win_conditions(self) -> tuple[bool, bool, bool]:
        """Returns a booleon tuple.
        
        Returns:
            The first value returns True if there is at least one mech
            in the entities list else False. The second value returns
            True if there is at least one enemy in the entities list
            else Flase. The third value returns True if there is at least
            one building that isn't destroyed on the board.
        """
        has_mech: bool = False
        has_enemy: bool = False
        has_building: bool = False

        for entity in self._entities:
            if not entity.is_alive():
                continue

            if entity.is_friendly() and not has_mech:
                has_mech = True
            
            if not (entity.is_friendly() or has_enemy):
                has_enemy = True
        
        for building in self._board.get_buildings().values():
            if not (building.is_destroyed() or has_building):
                has_building = True
        
        return has_mech, has_enemy, has_building

    def has_won(self) -> bool:
        """Returns True if the win conditions are met else False.
        
        The win conditions are met when there is at least one mech
        and no enemies in the entities board and at least one building
        isn't destroyed.
        """
        has_mech, has_enemy, has_building = self.get_win_conditions()

        if has_mech and has_building and not has_enemy:
            return True
        
        return False
    
    def has_lost(self) -> bool:
        """Returns True if the lost conditions are met else False.
        
        The lost conditions are met when there are either no mechs
        in the entities list or all buildings are destroyed.
        """
        has_mech, _, has_building = self.get_win_conditions()

        if has_mech and has_building:
            return False
        
        return True
    
    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """Returns a dictionary of entities on the board.
        
        Returns:
            A dictionary where the keys are coordinates as an integer tuple
            of (row, column) and the value is the entity instance at that
            coordinate.
        """
        dictionary: dict = {}

        for entity in self._entities:
            dictionary[entity.get_position()] = entity
        
        return dictionary
    
    def get_valid_movement_positions(
            self,
            entity: Entity
    ) -> list[tuple[int, int]]:
        """Gets the valid positions the passed entity can move to.
        
        Valid positions are the entity's speed integer many
        position away from its origin position.

        Args:
            entity: An Entity instance.
        
        Returns:
            A list of positions as an integer tuple of (row, column) that the
            passed entity can move to in one turn.
        """
        positions: list = []
        origin: tuple[int, int] = entity.get_position()
        row_num, column_num = self._board.get_dimensions()

        for row in range(0, row_num):

            for column in range(0, column_num):
                distance = get_distance(self, origin, (row, column))

                if distance > 0 and distance <= entity.get_speed():
                    positions.append((row, column))
        
        return positions
    
    def attempt_move(
            self,
            entity: Entity,
            position: tuple[int, int]
    ) -> None:
        """Attempts to move the passed entity to the passed position.
        
        The entity will not move if its an enemy, entity's active is False
        and the passed position is not a valid position. If move is successful
        than the entity is disabled.

        Args:
            entity: An entity instance to be moved.
            position: The position as an integer tuple of (row, column)
                that the entity will attempt to move to.
        """
        if not entity.is_friendly():
            return
        
        if (
            entity.is_active()
            and position in self.get_valid_movement_positions(entity)
        ):
            entity.set_position(position)
            entity.disable()
    
    def ready_to_save(self) -> bool:
        """Returns True if all mechs' active are True else False."""
        for entity in self._entities:
            if not entity.is_friendly():
                continue

            if not entity.is_active():
                return False
        
        return True
    
    def assign_objectives(self) -> None:
        """Updates the objective of all enemies in the entities list."""
        for entity in self._entities:
            if entity.is_friendly():
                continue

            entity.update_objective(
                self._entities,
                self._board.get_buildings()
            )
    
    def move_enemies(self) -> None:
        """Moves all enemies closer to its objective."""
        self.assign_objectives()

        for entity in self._entities:
            if entity.is_friendly() or not entity.is_alive():
                continue
            
            valid_tiles_pos = self.get_valid_movement_positions(entity)
            distances: dict = {}

            if len(valid_tiles_pos) == 0:
                continue
            
            for i in range(0, len(valid_tiles_pos)):
                distance = get_distance(
                    self,
                    entity.get_objective(),
                    valid_tiles_pos[i]
                )
                distances[valid_tiles_pos[i]] = distance
            
            valid_tiles_pos: list[tuple[int, int]] = distances.keys()
            discard_keys: list[tuple[int, int]] = [
                pos for pos in valid_tiles_pos if distances[pos] == -1
            ]

            for key in discard_keys:
                distances.pop(key)
            
            valid_tiles_pos: list[tuple[int, int]] = list(distances.keys())

            if len(valid_tiles_pos) == 0:
                continue

            distances: list[int] = list(distances.values())
            
            valid_tiles_pos.reverse()
            distances.reverse()
            
            position: tuple[int, int] = valid_tiles_pos[
                distances.index(min(distances))
            ]

            entity.set_position(position)
    
    def make_attack(self, entity: Entity) -> None:
        """Makes the passed entity attack its targetted positions.
        
        The passed entity will only attack entities and buildings if its an 
        enemy or a tank mech. If the entity is a heal mech then it will heal
        other mechs and buildings.

        Args:
            entity: An Entity instance that will be attacking its targetted
                positions.
        """
        if not entity.is_alive():
            return
        
        entities = self.entity_positions()
        buildings = self._board.get_buildings()

        for target in entity.get_targets():
            targeted_entity: Entity = entities.get(target)
            targeted_building: Building = buildings.get(target)

            if targeted_entity:
                entity.attack(targeted_entity)

            if targeted_building:
                entity.attack(targeted_building)
    
    def end_turn(self) -> None:
        """Ends the turn.
        
        Makes all entities attack, enables all mechs, deletes any
        dead entities from the entities list then moves all the
        enemies.
        """
        for entity in self._entities:
            self.make_attack(entity)

            if entity.is_friendly():
                entity.enable()
        
        self._entities = [
            entity for entity in self._entities if entity.is_alive()
        ]
        self.move_enemies()
        

# View Classes
class GameGrid(AbstractGrid):
    def __init__(
        self,
        master: Union[tk.Tk, tk.Widget],
        dimensions: tuple[int, int],
        size: tuple[int, int]
    ) -> None:
        super().__init__(master, dimensions, size)
        self.yposition, self.xposition = 0, 0
        self.pack(side=tk.RIGHT)

    def redraw(
            self,
            board: Board,
            entities: list[Entity],
            highlighted: list[tuple[int, int]] = None,
            movement: bool = False
    ) -> None:
        """Redraws the game grid according to the board and entities.
        
        Args:
            board: A board instance.
            entities: A list of Entity Instances.
            highlighted: A list of coordinates as an integer tuples of
                (row, column) that is to be highlighted.
            movement: A booleon that dictates the colour the highlighted
                rectangles are.
        """
        self._dimensions = board.get_dimensions()
        row_num, column_num = self._dimensions
        colour = ""
        self.clear()

        #Highlights
        if highlighted == None:
            highlighted: list[tuple[int, int]] = []
        
        if movement:
            colour: str = MOVE_COLOR
        else:
            colour: str = ATTACK_COLOR
        
        for coordinate in highlighted:
            self.color_cell(coordinate, colour)
        
        #Buildings
        buildings = board.get_buildings()

        for coordinate in buildings.keys():
            if coordinate in highlighted:
                continue

            building = buildings[coordinate]
            if building.is_destroyed():
                self.color_cell(coordinate, DESTROYED_COLOR)
            else:
                self.color_cell(coordinate, BUILDING_COLOR)
                self.annotate_position(
                    coordinate,
                    str(building.get_health()),
                    ENTITY_FONT
                )
        
        #Tiles
        for row in range(0, row_num):
            for column in range(0, column_num):
                if (row, column) in highlighted:
                    continue

                tile = board.get_tile((row, column))
                if str(tile) == " ":
                    colour = GROUND_COLOR
                elif str(tile) == "M":
                    colour = MOUNTAIN_COLOR
                else:
                    continue
                
                self.color_cell((row, column), colour)

        #Entities
        for entity in entities:
            self.annotate_position(
                entity.get_position(),
                entity.get_icon(),
                ENTITY_FONT
            )
        
    def click_callback(
            self,
            event,
            click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """A function to be binded to mouse clicks on the game grid.
        
        Args:
            click_callback: A function with an integer tuple of (row, column)
                as an argument that is to be called on every mouse click.
        """
        self.yposition, self.xposition = event.y, event.x
        click_callback(self.pixel_to_cell(self.xposition, self.yposition))

    def bind_click_callback(
            self,
            click_callback: Callable[[tuple[int, int]], None]
        ) -> None:
        """Binds the click_callback function to mouse clicks on the game grid.
        
        Args:
            click_callback: A function with an integer tuple of (row, column)
                as an argument that is to be called on every mouse click.
        """
        self.bind(
            "<Button-1>",
            lambda x: self.click_callback(x, click_callback),
            True
        )
        self.bind(
            "<Button-2>",
            lambda x: self.click_callback(x, click_callback),
            True
        )  

class SideBar(AbstractGrid):
    def __init__(
            self,
            master: tk.Widget,
            dimensions: tuple[int, int],
            size: tuple[int, int]
    ) -> None:
        super().__init__(master, dimensions, size)
        self.pack(side=tk.RIGHT)
    
    def display(self, entities: list[Entity]) -> None:
        """Redraws the side bar according to the entities.
        
        Args:
            entities: A list of Entity Instances.
        """
        self.set_dimensions((len(entities) + 1, 4))
        self.clear()

        #Header
        headertxt: list[str] = ["Unit", "Coord", "Hp", "Dmg"]
        for i in range(0, len(headertxt)):
            self.annotate_position(
                (0, i),
                headertxt[i],
                SIDEBAR_FONT
            )

        #Contents
        for i in range(1, len(entities) + 1):
            entity = entities[i-1]

            entity_elements = [
                entity.get_icon(),
                entity.get_position(),
                entity.get_health(),
                entity.get_strength()
            ]

            entity_elements = [str(element) for element in entity_elements]

            for j in range(0, len(entity_elements)):
                self.annotate_position(
                    (i, j),
                    entity_elements[j],
                    SIDEBAR_FONT
                )
        
class ControlBar(tk.Frame):
    def __init__(
            self,
            master: tk.Widget,
            save_callback: Optional[Callable[[], None]] = None,
            load_callback: Optional[Callable[[], None]] = None,
            turn_callback: Optional[Callable[[], None]] = None,
            **kwargs ) -> None:
        """Initialize a new control bar.
        
        Args:
            master: A tkinter window that this control bar will appear in.
            save_callback: A function binded to the save button.
            load_callback: A function binded to the load button.
            turn_callback: A function binded to the end turn button.
        """
        super().__init__(master)

        save_btn = tk.Button(
            self,
            text="Save Game",
            command=save_callback
        ).grid(row=0,column=0)
        load_btn = tk.Button(
            self,
            text="Load Game",
            command=load_callback
        ).grid(row=0,column=1)
        end_btn = tk.Button(
            self,
            text="End Turn",
            command=turn_callback
        ).grid(row=0,column=2)

        for i in range(0, 3):
            self.rowconfigure(0, weight=1)
            self.columnconfigure(i, weight=1)
        
        self.pack(fill=tk.X, side=tk.BOTTOM)

class BreachView():
    def __init__(
            self,
            root: tk.Tk,
            board_dims: tuple[int, int],
            save_callback: Optional[Callable[[], None]] = None,
            load_callback: Optional[Callable[[], None]] = None,
            turn_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """Initialize a view that contains a game grid, side and control bar.
        
        Args:
            root: A tkinter window that this view will appear in.
            save_callback: A function binded to the save button.
            load_callback: A function binded to the load button.
            turn_callback: A function binded to the end turn button.
        """
        self._root: tk.Tk = root
        self._root.wm_title("Into The Breach")
        self._root.wm_resizable(False, False)

        self._banner = tk.Label(
            self._root,
            text="Into The Breach",
            font=BANNER_FONT
        )
        self._banner.pack(fill=tk.X, side=tk.TOP)

        self._ControlBar = ControlBar(
            self._root,
            save_callback,
            load_callback,
            turn_callback
        )
        self._SideBar = SideBar(
            self._root,
            (0, 4),
            (SIDEBAR_WIDTH, GRID_SIZE)
        )

        self._GameGrid = GameGrid(
            self._root,
            board_dims,
            (GRID_SIZE, GRID_SIZE)
        )
        
    def get_game_grid(self) -> GameGrid:
        """Returns the game grid instance."""
        return self._GameGrid

    def bind_click_callback(
            self,
            click_callback: Callable[[tuple[int, int]], None]
    ) -> None:
        """Binds the click_callback function to mouse clicks on the game grid.
        
        Args:
            click_callback: A function with an integer tuple of (row, column)
                as an argument that is to be called on every mouse click.
        """
        self._GameGrid.bind_click_callback(click_callback)

    def redraw(
            self,
            board: Board,
            entities: list[Entity],
            highlighted: list[tuple[int, int]] = None,
            movement: bool = False
    ) -> None:
        """Redraws the view according to the board and entities.
        
        Args:
            board: A board instance.
            entities: A list of Entity Instances.
            highlighted: A list of coordinates as an integer tuples of
                (row, column) that is to be highlighted.
            movement: A booleon that dictates the colour the highlighted
                rectangles are.
        """
        self._SideBar.display(entities)
        self._GameGrid.redraw(board, entities, highlighted, movement)
        
def read_file(file_path: str) -> tuple[Board, list[Entity]]:
    """Reads a text file and returns a Board and a list of Entities.
    
    Args:
        file_path: A string that is the directory to the text file.

    Returns:
        A tuple of a Board instance and a list of Entity instances that
        was read from the text file at the passed file path.
    """
    with open(file_path) as file:
        boardtxt: list[str] = []
        entitytxt: list[str] = []
        section:int = 0

        for line in file:
            if line == '\n':
                section += 1
                continue

            if section == 0:
                boardtxt.append(line[:-1])
            if section == 1:
                entitytxt.append(line[:-1])
        
        board: list[list[str]] = []
        entities: list[Entity] = []

        for line in boardtxt:
            row: list[str] = []

            for char in line:
                row.append(char)
            board.append(row)
        
        for line in entitytxt:
            #en is short for entity elements
            en: list[str] = line.split(',')
            symbol = en[0]
            en: list[int] = [int(x) for x in en[1:]]
            if symbol == SCORPION_SYMBOL:
                entity = Scorpion((en[0], en[1]), en[2], en[3], en[4])
            elif symbol == FIREFLY_SYMBOL:
                entity = Firefly((en[0], en[1]), en[2], en[3], en[4])
            elif symbol == TANK_SYMBOL:
                entity = TankMech((en[0], en[1]), en[2], en[3], en[4])
            elif symbol == HEAL_SYMBOL:
                entity = HealMech((en[0], en[1]), en[2], en[3], en[4])
            
            entities.append(entity)
        
        return Board(board), entities

class IntotheBreach():
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """Initializes the game with a tkinter window and text file.
        
        Arguments:
            root: The tkinter window the view will appear in.
            game_file: The file path as a string where the game will be loaded
                from.
        """
        self._game_file: str = game_file
        self._board, self._entities = read_file(self._game_file)

        self._root: tk.Tk = root

        self._model: BreachModel = BreachModel(self._board, self._entities)
        self._view: BreachView = BreachView(
            self._root,
            self._board.get_dimensions(),
            self._save_game,
            self._load_game,
            self._end_turn
        )

        self._view.redraw(self._model.get_board(), self._model.get_entities())
        self._view.bind_click_callback(self._handle_click)

        self._focussed_entity = None
    
    def get_model(self) -> BreachModel:
        """Returns the game model."""
        return self._model()
    
    def get_view(self) -> BreachView:
        """Returns the game view."""
        return self._view()

    def get_highlighted(
            self,
            entity: Entity
    ) -> tuple[list[tuple[int, int]], bool]:
        """Returns the positions to be highlighted and the movement booleon.
        
        Args:
            entity: The Entity instance that will be used to get its
                highlighted positions.
        
        Returns:
            A list of coordinates as an integer tuple of (row, column) that
            are the positions to be highlighted and a booleon, True if the
            entity is ready to be moved or False if its waiting to attack.
        """
        if not entity.is_friendly():
            return entity.get_targets(), False
        
        if entity.is_active():
            return self._model.get_valid_movement_positions(entity), True
        else:
            return entity.get_targets(), False

    def redraw(self) -> None:
        """Redraws the view according to the model."""
        highlited = None
        movement = None

        if self._focussed_entity:
            highlited, movement = self.get_highlighted(self._focussed_entity)
            
        self._view.redraw(
            self._model.get_board(),
            self._model.get_entities(),
            highlited, movement
        )
        
    def set_focussed_entity(self, entity: Optional[Entity]) -> None:
        """Set the focus entity
        
        The focus entity is set to the passed entity or is set to None if
        the focus entity is the same as the passed entity.

        Args:
            entity: An Entity instance or None.
        """
        if self._focussed_entity == entity:
            self._focussed_entity = None
        else:
            self._focussed_entity = entity
    
    def make_move(self, position: tuple[int, int]) -> None:
        """Attemps to move the focussed entity to the passed position.
        
        Args:
            position: An integer tuple of (row, column) that the focussed
                entity will attempt to move to.
        """
        self._model.attempt_move(self._focussed_entity, position)
        self._focussed_entity = None
        self.redraw()
    
    def load_model(self, file_path: str) -> None:
        """Loads the model from the text file.
        
        Args:
            file_path: A string that is the directory to the text file.
        """
        try:
            read_file(file_path)
        except:
            messagebox.showerror(IO_ERROR_TITLE, IO_ERROR_MESSAGE + f'{file_path}')
    
    def _save_game(self) -> None:
        """Saves the game to a text file chosen by the user."""
        if not self._model.ready_to_save:
            messagebox.showerror(INVALID_SAVE_TITLE, INVALID_SAVE_MESSAGE)
            return
        file_name = filedialog.asksaveasfilename(
            initialdir="levels/",
            initialfile="untitled.txt",
            filetypes=[("Text files", "*.txt")],
            defaultextension=".txt"
        )
        if file_name:
            with open(file_name, "w") as file:
                string = str(self._model) + "\n"
                file.write(string)
    
    def _load_game(self) -> None:
        """Loads the game from a text file chosen by the user."""
        file_name = filedialog.askopenfilename(
            initialdir="levels/"
        )
        if file_name:
            self._game_file = file_name
            board, entities = read_file(self._game_file)
            self._model = BreachModel(board, entities)
            self.set_focussed_entity(None)
            self.redraw()
    
    def _end_turn(self) -> None:
        """Ends the turn then checks if the user won or lost."""
        self._model.end_turn()
        self.set_focussed_entity(None)
        self.redraw()

        has_won = self._model.has_won()
        has_lost = self._model.has_lost()

        if not (has_won or has_lost):
            return
        
        if has_won:
            play_again = messagebox.askyesno(
                "You Win!",
                "You Win! " + PLAY_AGAIN_TEXT
            )
        if has_lost:
            play_again = messagebox.askyesno(
                "You Lost!",
                "You Lost! " + PLAY_AGAIN_TEXT
            )

        if play_again:
            board, entities = read_file(self._game_file)
            self._model = BreachModel(board, entities)
            self.redraw()
        else:
            self._root.destroy()
        
    def _handle_click(self, position: tuple[int, int]) -> None:
        """Handles the behavior of the model and view at a mouse click.
        
        Args:
            position: The position of the mouse click as an integer tuple
                of (row, column).
        """
        row, column = position
        entity_positions = self._model.entity_positions()
        entity = entity_positions.get((row, column))

        if entity:
            self.set_focussed_entity(entity)
            self.redraw()
            return
        
        if not self._focussed_entity:
            return
        
        if not self._focussed_entity.is_friendly():
            self.set_focussed_entity(None)
            self.redraw()
            return
        
        valid_tiles = self._model.get_valid_movement_positions(
            self._focussed_entity
        )

        if position in valid_tiles:
            self.make_move(position)
        else:
            self.set_focussed_entity(None)
            self.redraw()
            

def play_game(root: tk.Tk, file_path: str) -> None:
    """Creates the game with a tkinter window and file path.

    Args:
        root: A tkinter window the view will appear in.
        file_path: The file path as a string where the game will be loaded
                from.
    """
    controller = IntotheBreach(root, file_path)
    root.mainloop()

def main() -> None:
    """The main function"""
    root = tk.Tk()
    play_game(root, 'levels/level1.txt')
    

if __name__ == "__main__":
    main()
