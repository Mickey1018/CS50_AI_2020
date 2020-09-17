import sys

from crossword import *
import copy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # loop over all the variables
        for var in self.domains:

            # initialize a set for removing node-inconsistent variable
            remove = set()

            # if length of variable is not equal to the length of values
            # in its domain, remove the value
            for val in self.domains[var]:
                if var.length != len(val):
                    remove.add(val)

            for val in remove:
                self.domains[var].remove(val)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # return false if there is no overlapping between variable x and variable y
        if not self.crossword.overlaps[x, y]:
            return False

        # if there is overlap
        else:
            # get the index i fro variable x and index j for variable y if x and y can be overlapped
            i, j = self.crossword.overlaps[x, y]

            revise = False
            remove = set()

            # loop around all the possible strings from the domain of variable x
            for word_x in self.domains[x]:
                possible_x = word_x[i]

                # list out all the possible strings from the domain of variable y
                possible_y = set()
                for word_y in self.domains[y]:
                    possible_y.add(word_y[j])

                # where there is no possible corresponding value for 'y',
                # remove values from `self.domains[x]`
                if possible_x not in possible_y:
                    remove.add(word_x)
                    revise = True

            for word in remove:
                self.domains[x].remove(word)

            return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # where arcs is None, add all pairs of variables and their neighbors
        if arcs is None:
            arcs = []
            for var_x in self.crossword.variables:
                for var_y in self.crossword.neighbors(var_x):
                    arcs.append(tuple([var_x, var_y]))

        while arcs:
            x, y = arcs.pop(0)

            # if revision is made
            if self.revise(x, y):

                # if there is variable that has empty domain, return false
                if self.domains[x] is None:
                    return False

                for z in (self.crossword.neighbors(x) - {y}):
                    arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # loop around all variables
        for var in self.crossword.variables:

            # check if all variables have to be assigned
            if var not in assignment.keys():
                return False

            # check if there is value in variables
            if assignment[var] is None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check the uniqueness
        if len(assignment.values()) != len(set(assignment.values())):
            return False

        for var, val in assignment.items():
            # check if the length is consistent
            if len(val) != var.length:
                return False

            # loop for all neighbors in 'assignment'
            for neighbor in (self.crossword.neighbors(var)):
                if neighbor in assignment.keys():

                    # if there is overlap, get index
                    if self.crossword.overlaps[var, neighbor]:
                        i, j = self.crossword.overlaps[var, neighbor]

                        # check if there is any conflict
                        if assignment[var][i] != assignment[neighbor][j]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # initialize a counter for rule out values of neighboring variables
        eliminate_counts = dict()

        # for each value in 'var'
        for val in self.domains[var]:

            # keep tracking of the eliminate count
            eliminate_counts[val] = 0

            # loop for unassigned neighbour of 'var'
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment.keys():

                    # get the index of overlap between 'var' and it's neighbour
                    i, j = self.crossword.overlaps[var, neighbor]

                    # for each value in 'var''s neighbor
                    for val_neighbor in self.domains[neighbor]:

                        # when there is conflict, we can eliminate neighbors.
                        # also update the counter
                        if val[i] != val_neighbor[j]:
                            eliminate_counts[val] += 1

        # sort the values of variable 'var' in ascending number of neighbours they can ruled out
        rule_out_list = sorted(eliminate_counts.items(), key=lambda x: x[1])

        # return the value that it rules out the least number of neighbors
        return [x[0] for x in rule_out_list]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # find unassigned variables
        var_unassigned = self.crossword.variables - assignment.keys()

        # counting the number of values in domain of unassigned variables
        # with the use of dictionary
        domain_count = {}
        for var in var_unassigned:
            domain_count[var] = len(self.domains[var])

        # sort the unassigned variables in ascending order of number of values
        # in their domain
        sorted_domain_count = sorted(domain_count.items(), key=lambda x: x[1])

        # if the followings
        # 1. one and only one unassigned variable OR
        # 2. not tie,
        # return the variable
        if len(sorted_domain_count) == 1 or sorted_domain_count[0][1] < sorted_domain_count[1][1]:
            return sorted_domain_count[0][0]

        # if tie, sort by the the degree (i.e. the number of neighbors)
        else:
            degree_count = {}
            for var in var_unassigned:

                # just keep the unassigned variables with the minimum number of
                # values in their domain
                if len(self.domains[var]) == sorted_domain_count[0][1]:
                    degree_count[var] = len(self.crossword.neighbors(var))

            # sort from the highest degree to the lowest degree
            sorted_degree_count = sorted(degree_count.items(), key=lambda x: x[1], reverse=True)
            return sorted_degree_count[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # just return the whole assignment if it is already finished
        if self.assignment_complete(assignment):
            return assignment

        # select a unassigned variable
        var_unassigned = self.select_unassigned_variable(assignment)

        # loop for the variables in the order of lowest number of values
        # in their domain
        for val in self.order_domain_values(var_unassigned, assignment):

            # test the consistency
            test_assignment = copy.deepcopy(assignment)
            test_assignment[var_unassigned] = val
            if self.consistent(test_assignment):

                # add a key-value pair to assignment if consistent
                assignment[var_unassigned] = val

                # repeat but using the updated assignment, if there is
                # a result, return this result
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            # remove key-value pair and inferences from assignment
            assignment.pop(var_unassigned, None)

        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()