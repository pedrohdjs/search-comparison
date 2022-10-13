from __future__ import annotations
from collections import namedtuple
import os
from collections import deque
from queue import PriorityQueue
import numpy as np
from time import sleep
from scipy.spatial.distance import cityblock as get_manhattan_distance
from IPython.display import clear_output

"""
Definição do labirinto a ser usado.

0 -> Espaço normal
1 -> Parede
2 -> Pacman (Ponto inicial)
3 -> Frutas
"""

DEFAULT_MAZE = [
    [0,0,0,0,0,0,0,0,1,1,0,0,3,0,0,0,0,0],
    [0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0],
    [0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0],
    [1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1],
    [1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1],
    [0,3,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
    [1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1],
    [1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1],
    [0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0],
    [0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,3,0,0,0],
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
    clear: function

    def __init__(self, on_terminal : bool = True) -> None:
        self._maze = DEFAULT_MAZE

        self.height = len(self._maze)
        self.width = len(self._maze[0])
        self.starting_pos = self._get_starting_position()
        self.current_pos = self.starting_pos
        self.fruits = self._get_fruits()
        self.done = False
        self.dfs_call_count = 0
        self.on_terminal = on_terminal


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

        if self.on_terminal == True:
            os.system("clear")
        else:
            clear_output(wait=True)

        for i in range(0,width+2):
            print(frame, end="")
        print()

        for i in range(0,height):
            print(frame, end="")
            for j in range(0,self.width):
                print(Maze.EMOJI_DICT[maze[i][j]],end="")
            print(frame)

        for i in range(0,width+2):
            print(frame, end="")
        print()

        print(additional_text)

        if self.on_terminal == True:
            input()
        else:
            sleep(0.24)


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


    def _get_distance (
        self, 
        distances : dict, 
        current_pos : tuple[int,int], 
        target_pos : tuple[int,int]
    ) -> int:
        '''
        Retorna a distância de Manhattan até o próximo alvo, 
        além de armazená-la no dicionário de distâncias.
        '''
        if current_pos not in distances:
            distances[current_pos] = get_manhattan_distance(current_pos, target_pos)
        return distances[current_pos]
    

    def _get_valid_positions (
        self, 
        visited : dict, 
        current_pos : tuple[int,int]
    ) -> tuple[int,int]:
        '''
        Retorna as posições possíveis a partir da posição atual.
        '''
        positions = deque([])
        for direction in Maze.DIRECTIONS:
            new_i = current_pos[0] + direction[0]
            new_j = current_pos[1] + direction[1]
            if self._is_valid(new_i, new_j) and not (new_i, new_j) in visited:
                positions.append((new_i, new_j))
        return tuple(positions)
                
    

    def start_a_star_search(self) -> None:
        '''
        Inicializa o algoritmo de busca A*, realizando impressão do 
        resultado a cada caminho calculado.
        '''
        # Para controle das frutas (objetivos)
        fruits = np.array(list(self.fruits))
        fruits_indexes = np.arange(0, fruits.shape[0])
        num_fruits = fruits.shape[0]
        non_collected_fruits = np.full(fruits.shape[0], True)
        num_collected_fruits = 0

        # Para controle de fluxo
        Node = namedtuple('Node', ['g_n', 'pos', 'parent'])

        # Para controle de posição
        current_position = self.current_pos

        # Itera ao longo das frutas
        while num_collected_fruits < num_fruits:

            # Posição inicial
            initial_position = (current_position[0], current_position[1])

            # Para controle de fluxo
            queue = PriorityQueue()
            parents = {}
            distances = {}
            visited = {}
            
            # Seleção da fruta mais próxima
            active_fruits = fruits[non_collected_fruits]
            active_indexes = fruits_indexes[non_collected_fruits]
            active_index = 0
            min_dist = get_manhattan_distance(active_fruits[0], current_position)
            for i in range(1, active_fruits.shape[0]):
                dist = get_manhattan_distance(active_fruits[i], current_position)
                if dist < min_dist:
                    min_dist = dist
                    active_index = i
            current_fruit = tuple(active_fruits[active_index])
            current_fruit_index = active_indexes[active_index]

            # Inicialização da busca
            parents[current_position] = initial_position
            adjacent_node = self._get_valid_positions(visited, current_position)
            for adjacent_position in adjacent_node:
                h_n = self._get_distance(distances, adjacent_position, current_fruit)
                f_n = 1 + h_n # f_n = g_n + h_n
                queue.put ((
                    f_n, 
                    Node(1, adjacent_position, current_position)
                ))
            
            # Enquanto não finalizar o objetivo atual
            while current_position != current_fruit and not queue.empty():
                
                # Obtenção do próximo nó
                current_node = queue.get()[1]
                current_position = current_node.pos
                parents[current_position] = current_node.parent
                visited[current_position] = True

                # Adição dos nós adjacentes à fila
                adjacent_node = self._get_valid_positions(visited, current_position)
                for adjacent_position in adjacent_node:
                    h_n = self._get_distance(distances, adjacent_position, current_fruit)
                    g_n = current_node.g_n + 1
                    f_n = g_n + h_n
                    queue.put ((
                        f_n, 
                        Node(g_n, adjacent_position, current_position)
                    ))
                
            # Atualização de objetivo
            num_collected_fruits += 1
            non_collected_fruits[current_fruit_index] = False

            # Impressão do resultado --- backtracking (construção do caminho)
            path = deque([])
            backtracking_position = (current_position[0], current_position[1])
            while backtracking_position != initial_position:
                path.append(backtracking_position)
                backtracking_position = parents[backtracking_position]

            # Impressão interativa
            while len(path) > 0:
                pos = path.pop()
                self._maze[pos[0]][pos[1]] = self.PACMAN
                self.print()
                self._maze[pos[0]][pos[1]] = self.VISITED
            self.print()
        
        # Finalização
        self.done = True
    

    def start_bfs(self) -> True:
        '''
        Inicializa o algoritmo de busca BFS, realizando impressão do 
        resultado a cada caminho calculado.
        '''
        # Para controle das frutas (objetivos)
        fruits = np.array(list(self.fruits))
        fruits_indexes = np.arange(0, fruits.shape[0])
        num_fruits = fruits.shape[0]
        non_collected_fruits = np.full(fruits.shape[0], True)
        num_collected_fruits = 0

        # Para controle de fluxo
        Node = namedtuple('Node', ['pos', 'parent'])

        # Para controle de posição
        current_position = self.current_pos

        # Itera ao longo das frutas
        while num_collected_fruits < num_fruits:

            # Posição inicial
            initial_position = (current_position[0], current_position[1])

            # Para controle de fluxo
            queue = deque([])
            parents = {}
            visited = {}
            
            # Seleção da fruta mais próxima
            active_fruits = fruits[non_collected_fruits]
            active_indexes = fruits_indexes[non_collected_fruits]
            active_index = 0
            min_dist = get_manhattan_distance(active_fruits[0], current_position)
            for i in range(1, active_fruits.shape[0]):
                dist = get_manhattan_distance(active_fruits[i], current_position)
                if dist < min_dist:
                    min_dist = dist
                    active_index = i
            current_fruit = tuple(active_fruits[active_index])
            current_fruit_index = active_indexes[active_index]

            # Inicialização da busca
            parents[current_position] = initial_position
            adjacent_node = self._get_valid_positions(visited, current_position)
            for adjacent_position in adjacent_node:
                queue.append(Node(adjacent_position, current_position))
            
            # Enquanto não finalizar o objetivo atual
            while current_position != current_fruit and len(queue) > 0:
                
                # Obtenção do próximo nó
                current_node = queue.pop()
                current_position = current_node.pos
                parents[current_position] = current_node.parent
                visited[current_position] = True

                # Impressão
                self._maze[current_position[0]][current_position[1]] = self.PACMAN
                self.print()
                self._maze[current_position[0]][current_position[1]] = self.VISITED

                # Adição dos nós adjacentes à fila
                adjacent_node = self._get_valid_positions(visited, current_position)
                for adjacent_position in adjacent_node:
                    queue.append(Node(adjacent_position, current_position))
                
            # Atualização de objetivo
            num_collected_fruits += 1
            non_collected_fruits[current_fruit_index] = False
        
        # Finalização
        self.done = True