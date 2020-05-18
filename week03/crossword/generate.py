import sys

from crossword import *


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
        for var in self.domains:
            word_len = var.length
            for word in self.crossword.words:
                if len(word) != word_len:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        ret = False
        overlaps = self.crossword.overlaps
        
        for overlap, value in overlaps.items():
            if overlap == (x, y):
                words_cp = self.domains[x].copy()
                for x_word in words_cp:
                    delete = True
                    for y_word in self.domains[y]:
                        if x_word[value[0]] == y_word[value[1]]:
                            delete = False
                    # If a revision was made to the domain of x, remove the value from the domain 
                    if delete:
                        ret = True
                        self.domains[x].remove(x_word)
        return ret

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is None, start with all of the arcs
        if not arcs:
            arcs = []
            vars = self.crossword.variables
            for var in vars:
                neighbors = self.crossword.neighbors(var)
                if len(neighbors):
                    for neighbor in neighbors:
                        if not (var, neighbor) in arcs:
                            arcs.append((var, neighbor))
        # While queue is not empty, revise each arc
        while len(arcs):
            arc = arcs.pop(0)
            if self.revise(arc[0], arc[1]):   
                neighbors = self.crossword.neighbors(arc[0])
                if len(neighbors):
                    for neighbor in neighbors:
                        # If domain was changed, add affected arc again to arc
                        arcs.append((neighbor, arc[0]))
        for value in self.domains.values():
            if not len(value):
                return False
        return True
        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False
            if not assignment[var] in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if every value is the correct lenght 
        for var_x in assignment:
            word_x = assignment[var_x]
            if word_x:
                if var_x.length != len(word_x):
                    return False
            # Check if values are distinct
            for var_y in assignment:
                word_y = assignment[var_y]
                if var_x != var_y:
                    if word_x == word_y:
                        return False
                    # Check if there are no conflicts between neighboring variables
                    overlap = self.crossword.overlaps[var_x, var_y]
                    if overlap and word_x and word_y:
                        if word_x[overlap[0]] != word_y[overlap[1]]:
                            return False
        return True
        
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        neighbors.difference_update(set(assignment))
        output = {}
        # For every value compute the number possible choices to be eleminated for neighboring variables
        for word_x in self.domains[var]:
            eliminated = 0
            for neighbor in neighbors:
                for word_y in self.domains[neighbor]:
                    overlaps = self.crossword.overlaps[var, neighbor]
                    if overlaps:
                        if word_x[overlaps[0]] != word_y[overlaps[1]]:
                            eliminated += 1
            output[word_x] = eliminated
        sort_output = sorted(output.items(), key=lambda x: x[1])
        return [val[0] for val in sort_output]                   

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        output = {}
        for var in self.crossword.variables:
            if not var in assignment:
                ret = var
                # For every variable assign number of remaining values in its domain
                # and number of neighbors
                output[var] = (len(self.domains[var]), len(self.crossword.neighbors(var)))
        if output:
            sort_output = sorted(output.items(), key=lambda x: (x[1][0], -x[1][1]))
            return sort_output[0][0]
        return ret

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: return assignment if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        # Take not used variable and check if assignment is complete
        for value in self.order_domain_values(var, assignment):
            if var:
                assignment[var] = value
                if self.consistent(assignment):
                    res = self.backtrack(assignment)
                    if not res:
                        assignment[var] = None
                    else:
                        return res
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
