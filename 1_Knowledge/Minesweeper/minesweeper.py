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
        # any time the number of cells is equal to the count, we know that all of that sentence’s cells must be mines.
        if len(self.cells) == self.count:
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # any time we have a sentence whose count is 0, we know that all of that sentence’s cells must be safe.
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # removing one mine cell from total set would decrease the count of mine by one
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)
            return 1
        else:
            return 0

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # removing a safe cell from total set would not affect the count of mine
        if cell in self.cells:
            self.cells.remove(cell)
            return 1
        else:
            return 0


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
               use subset method i.e. set2 - set1 = count2 - count1
        """
        # Marks the cell as a move
        self.moves_made.add(cell)

        # Marks the cell as safe
        self.mark_safe(cell)

        # create a set of neighbors
        neighbors = set()

        # Loop over all cells within one row and column
        for i in range(max(cell[0] - 1, 0), min(cell[0] + 2, self.height)):
            for j in range(max(cell[1] - 1, 0), min(cell[1] + 2, self.width)):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # include all the neighbors
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) not in self.moves_made:
                    neighbors.add((i, j))

        # add neighbors and count to sentence and then to knowledge
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        self.update_sentences()

        inferences = self.new_inferences()

        while inferences:
            for sentence in inferences:
                self.knowledge.append(sentence)

            self.update_sentences()

            inferences = self.new_inferences()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for possible_moves in self.safes:
            if possible_moves not in self.moves_made and possible_moves not in self.mines:
                return possible_moves

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set(itertools.product(range(0, self.height), range(0, self.width)))
        possible_moves = all_moves - self.mines - self.moves_made

        if possible_moves:
            return random.choice(tuple(possible_moves))
        else:
            return None

    def new_inferences(self):
        inferences = []
        removals = []
        for sentence1 in self.knowledge:
            if sentence1.cells == set():
                removals.append(sentence1)
                continue

            for sentence2 in self.knowledge:
                if sentence2.cells == set():
                    removals.append(sentence2)

                if sentence1 != sentence2:

                    # draw new inference from existing knowledge use subset method
                    if sentence2.cells.issubset(sentence1.cells):
                        diff_cells = sentence1.cells.difference(sentence2.cells)
                        diff_count = sentence1.count - sentence2.count
                        new_inference = Sentence(diff_cells, diff_count)
                        if new_inference not in self.knowledge:
                            inferences.append(new_inference)

        self.knowledge = [x for x in self.knowledge if x not in removals]
        return inferences

    def update_sentences(self):
        counter = 1
        while counter:
            counter = 0
            for sentence in self.knowledge:
                for cell in sentence.known_safes():
                    self.mark_safe(cell)
                    counter += 1
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
                    counter += 1
            for cell in self.safes:
                self.mark_safe(cell)
            for cell in self.mines:
                self.mark_mine(cell)
