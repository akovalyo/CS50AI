import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) <= self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()    

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            subtract = self.count - 1
            self.count = 0 if subtract < 0 else subtract

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbors(self, cell):
        """
        Returns 8 neighbors of cell
        """
        neighbors = set()
        row = cell[0]
        col = cell[1]
        if row > 0:
            neighbors.add((row - 1, col))
        if row < self.height - 1:
            neighbors.add((row + 1, col))
        if col > 0:
            neighbors.add((row, col - 1))
        if col < self.width - 1:
            neighbors.add((row, col + 1))
        if (row > 0) and (col > 0):
            neighbors.add((row - 1, col - 1))
        if (row > 0) and (col < self.width - 1):
            neighbors.add((row - 1, col + 1))
        if (row < self.height - 1) and (col > 0):
            neighbors.add((row + 1, col - 1))
        if (row < self.height - 1) and (col < self.width - 1):
            neighbors.add((row + 1, col + 1))
        return neighbors

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1-2
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        # 3
        neighbors = self.get_neighbors(cell)
        to_remove = set()
        for neighbor in neighbors:
            if neighbor in self.moves_made or neighbor in self.safes:
                to_remove.add(neighbor)
        
        neighbors.difference_update(to_remove)
        self.knowledge.append(Sentence(neighbors, count))

        # 4
        for sent in self.knowledge:
            safes = sent.known_safes()
            for safe in safes:
                self.mark_safe(safe)

        for sent in self.knowledge:
            mines = sent.known_mines()    
            for mine in mines:
                self.mark_mine(mine)

        # 5
        for i, kn1 in enumerate(self.knowledge):
            for j, kn2 in enumerate(self.knowledge):
                if i >= j:
                    continue      
                if kn1.cells.issubset(kn2.cells):   
                    if kn1.count == kn2.count:
                        kn1.cells.union(kn2.cells)
                        kn1.cells = set()
                    elif kn1.count != 0 and kn2.count != 0:    
                        kn2.cells = kn2.cells - kn1.cells
                        subtract = kn2.count - kn1.count
                        kn2.count = 0 if subtract < 0 else subtract
                elif kn2.cells.issubset(kn1.cells):
                    if kn2.count == kn1.count:
                        kn2.cells.union(kn1.cells)
                        kn2.cells = set()
                    elif kn1.count != 0 and kn2.count != 0:
                        kn1.cells = kn1.cells - kn2.cells
                        subtract = kn1.count - kn2.count
                        kn1.count = 0 if subtract < 0 else subtract
        
        for sen in self.knowledge:
            if len(sen.cells) == 0:
                self.knowledge.remove(sen)
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safes:            
            next_moves = []
            for cell in self.safes:    
                if cell not in self.moves_made and cell not in self.mines:
                    next_moves.append(cell)
            if next_moves:
                return random.choice(next_moves)     
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        grid = [(col, row) for col in range(self.width) for row in range(self.height)] 
        next_moves = []
        for cell in grid:
            if cell not in self.moves_made and cell not in self.mines:
                next_moves.append(cell)
        return random.choice(next_moves) if next_moves else None