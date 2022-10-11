from __future__ import annotations
import os
from time import sleep

"""
Definição do labirinto a ser usado.

0 -> Espaço normal
1 -> Parede
2 -> Pacman (Ponto inicial)
3 -> Frutas
"""

DEFAULT_MAZE = [
    [0,0,0,0,0,0,0,0,1,1,0,0,3,0,0,3,0,0],
    [0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0],
    [0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0],
    [1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1],
    [1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1],
    [0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
    [1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1],
    [1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1],
    [0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0],
    [0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
]

class Maze:
    """
    Representa o labirinto
    """

    # Constants
    PATH = 0
    WALL = 1
    PACMAN = 2
    FRUIT = 3
    VISITED = 4
    EMOJI_DICT = {
        0: "  ",
        1: "🟦",
        2: "🤔",
        3: "🍒",
        4: "🔶"
    }
    FRAME = "⬜"

    DIRECTIONS = [
        (-1, 0),
        ( 0, 1),
        ( 1, 0),
        ( 0,-1)
    ]

    # Attributes
    _maze: list[list[int]]
    width: int
    height: int
    starting_pos: tuple[int,int]
    current_pos: tuple[int,int]
    fruits: set[tuple[int,int]]
    done: bool
    dfs_call_count: int

    def __init__(self) -> None:
        self._maze = DEFAULT_MAZE

        self.height = len(self._maze)
        self.width = len(self._maze[0])
        self.starting_pos = self._get_starting_position()
        self.current_pos = self.starting_pos
        self.fruits = self._get_fruits()
        self.done = False
        self.dfs_call_count = 0

    def _get_starting_position(self) -> tuple[int,int]:
        """
        Obtém a posição inicial especificada como uma tupla.
        """

        maze = self._maze
        width = self.width
        height = self.height

        for i in range(0,height):
            for j in range(0, width):
                if(maze[i][j] == 2):
                    return (i,j)

        raise Exception("Posição inicial não especificada")


    def _get_fruits(self) -> set[tuple[int,int]]:
        """
        Obtém a posição inicial especificada como uma tupla.
        """

        maze = self._maze
        width = self.width
        height = self.height
        fruits = set()

        for i in range(0,height):
            for j in range(0, width):
                if(maze[i][j] == Maze.FRUIT):
                    fruits.add((i,j))
        
        return fruits

    def print(self, additional_text="") -> None:
        """
        Limpa o console e imprime o labirinto, formatado com emojis
        """

        frame = Maze.FRAME
        height = self.height
        width = self.width
        maze = self._maze

        os.system("clear")

        for i in range(0,width+2):
            print(frame,end="")
        print()

        for i in range(0,height):
            print(frame, end="")
            for j in range(0,self.width):
                print(Maze.EMOJI_DICT[maze[i][j]],end="")
            print(frame)

        for i in range(0,width+2):
            print(frame,end="")
        print()

        print(additional_text)

        input()


        
    def start_dfs(self) -> None:
        current_pos = self.current_pos
        current_i = current_pos[0]
        current_j = current_pos[1]

        self.dfs(current_i,current_j)

    def dfs(self, i: int, j: int) -> True:
        additional_text = ""
        self.dfs_call_count += 1
        
        if self._is_goal(i,j):
            self.fruits.remove((i,j))
            additional_text = "Fruta encontrada!"
            
            # Não há mais frutas, finalizar
            if(len(self.fruits) == 0):
                self.print(additional_text=f"Resposta encontrada com {self.dfs_call_count} chamadas à DFS!")
                self.done = True
                return True

        self.print(additional_text=additional_text)

        current_pos = self.current_pos
        current_i = current_pos[0]
        current_j = current_pos[1]
        

        for direction in Maze.DIRECTIONS:

            new_position = (current_i + direction[0], current_j + direction[1])
            new_i = new_position[0]
            new_j = new_position[1]
                        
            if self._is_valid(new_i, new_j) and not self._is_visited(new_i, new_j):
                self._mark_visited(current_i,current_j)

                self._set_position(new_i, new_j)
                success = self.dfs(new_i, new_j)
        
                self._set_position(current_i, current_j)

                self._mark_not_visited(current_i,current_j)
                if not self.done:
                    self.print() #Mostrar backtracking

                if success:
                    return True

  

    def _set_position(self, i:int, j:int) -> None:
        new_pos = (i,j)
        current_pos = self.current_pos

        if (self._maze[current_pos[0]][current_pos[1]] == Maze.PACMAN):
            self._maze[current_pos[0]][current_pos[1]] = Maze.PATH

        self.current_pos = new_pos
        self._maze[new_pos[0]][new_pos[1]] = Maze.PACMAN
        

    def _is_valid(self, i: int, j: int) -> bool:
        if i<0 or j<0:
            return False
        elif i >= self.height or j >= self.width:
            return False
        elif self._maze[i][j] == Maze.WALL:
            return False
        else:
            return True

    def _is_goal(self, i: int, j: int) -> bool:
        return (i,j) in self.fruits

    def _is_visited(self, i: int, j: int) -> bool:
        return self._maze[i][j] == Maze.VISITED

    def _mark_visited(self, i: int, j: int) -> None:
        self._maze[i][j] = Maze.VISITED

    def _mark_not_visited(self, i: int, j: int) -> None:
        self._maze[i][j] == Maze.WALL