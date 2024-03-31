from ortools.sat.python import cp_model

def SANTA_CLAUS_XMAS():
    """Solve the cryptarithmic puzzle SANTA-CLAUS=XMAS."""
    model = cp_model.CpModel()

    # Create variables.
    # Since s is a leading digit, it can't be 0.
    s = model.NewIntVar(1, 9, "s")
    a = model.NewIntVar(0, 9, "a")
    n = model.NewIntVar(0, 9, "n")
    t = model.NewIntVar(0, 9, "t")
    #a

    # Since c is a leading digit, it can't be 0.
    c = model.NewIntVar(1, 9, "c")
    l = model.NewIntVar(0, 9, "l")
    #a
    u = model.NewIntVar(0, 9, "u")
    #s

    # Since x is a leading digit, it can't be 0.
    x = model.NewIntVar(1, 9, "x")
    m = model.NewIntVar(0, 9, "m")
    #a
    #s

    #borrows
    b0 = model.NewBoolVar("b0")
    b1 = model.NewBoolVar("b1")
    b2 = model.NewBoolVar("b2")
    b3 = model.NewBoolVar("b3")

    # Force all letters to take on different values.
    model.AddAllDifferent(s, a, n, t, c, l, u, x, m)

    # Column 0:
    model.Add(s-c-b0 == 0)

    # Column 1:
    model.Add(10*b0 + a - l- b1 == x)

    # Column 2:
    model.Add(10*b1 + n - a - b2 == m)

    # Column 3:
    model.Add(10*b2 + t - u - b3 == a)

    # Column 4:
    model.Add(10*b3 + a - s == s)

    # Solve model./
    solver = cp_model.CpSolver()
    if solver.Solve(model) == cp_model.OPTIMAL:
        print("Optimal solution found!")
    solver.parameters.enumerate_all_solutions = True

    solution_printer = VarArraySolutionPrinter([s,a,n,t,c,l,u,x,m])
    status = solver.Solve(model, solution_printer)
    print(f"Number of solutions found: {solution_printer.solution_count()}")

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"{self.__solution_count:>2d}) ", end="")
        for v in self.__variables:
            print(f"{v}={self.Value(v)}", end=" ")
        print()

    def solution_count(self):
        return self.__solution_count
SANTA_CLAUS_XMAS()