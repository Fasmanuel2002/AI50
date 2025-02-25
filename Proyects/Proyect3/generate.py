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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
      
        #this means making sure that every value in a variable’s domain 
        # has the same number of letters as the variable’s length.
        # si la palabra no es del tamano de los cuadros del puzzle, borrar posibilidad
        
        for var in self.domains:
            variable_length = var.length
            to_remove = [word for word in self.domains[var] if len(word) != variable_length]
            for word in to_remove:
                self.domains[var].remove(word)
                
            
            
        

    def revise(self, x, y):
        overlap = self.crossword.overlaps.get((x, y))
        revise = False

        if overlap is not None:
            i, j = overlap
            to_remove = []

           
            for wordx in self.domains[x]:
                if not any(wordy[j] == wordx[i] for wordy in self.domains[y]):
                    to_remove.append(wordx)
            for word in to_remove:
                self.domains[x].remove(word)
                revise = True

        return revise

            
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        return 1

    def ac3(self, arcs=None):
        if arcs is None:
           queue = [(x, y) for x in self.domains for y in self.crossword.neighbors(x)]
        else:
            queue = arcs[:]
            
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z,x))
        return True
        
        
        
        
                    
                
            
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

    def assignment_complete(self, assignment):
        required_variables = set(self.crossword.variables)
        assigned_variables = set(assignment.keys())
        return required_variables == assigned_variables

    def consistent(self, assignment):
        #if (len_Variables == variables) and (self.crossword.variables != assignment.keys()) and (overlap is not None):
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
            
        for (var1,var2) in self.crossword.overlaps:
            overlap = self.crossword.overlaps.get((var1,var2))
            if overlap is not None and var1 in assignment and var2 in assignment:
                i,j = overlap
            
                if assignment[var1][i] != assignment[var2][j]:
                    return False
            
       
                
        return True    
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, ordered by
        the number of values they rule out for neighboring variables.
        The first value in the list should be the one that rules out the fewest
        values among the neighbors of `var`.
        """
        def count_conflicts(value):
            conflicts = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps.get((var, neighbor))
                    if overlap:
                        i, j = overlap
                        conflicts += sum(
                            1 for neighbor_value in self.domains[neighbor]
                            if neighbor_value[j] != value[i]
                        )
            return conflicts

        return sorted(self.domains[var], key=count_conflicts)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree (most neighbors). If there is still a tie, any tied variable
        can be returned.
        """
        unassigned = [var for var in self.crossword.variables if var not in assignment]

        # Sort by minimum remaining values (smallest domain first)
        # Tie-break by highest degree (most neighbors)
        return min(
            unassigned,
            key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var)))
        )

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment is complete, return the assignment
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Try each value in the domain of the variable
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value

            # If the assignment is consistent, proceed
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            # If not consistent, remove the assignment
            assignment.pop(var)

        # If no valid assignment is found, return None
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
