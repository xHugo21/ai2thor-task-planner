# File that contains the class which calls the planner
import os


class Planner:
    """Class that contains the methods to call the planner and manage generated plans"""

    def __init__(
        self,
        problem_path,
        output_path,
        problem,
        search_algorithm,
        heuristic,
        print=False,
        ogamus=False,
    ):
        # Selects domain depending on the method selected
        self.domain_path = "./pddl/domain_input.pddl"
        if not ogamus:
            self.domain_path = f"./pddl/domain_{problem}.pddl"
        self.problem_path = problem_path
        self.output_path = output_path

        self.search_algorithm = search_algorithm
        self.heuristic = heuristic

        # Runs plan using cbp_roller planner
        self.run_plan_cbp()

        # If print arg is true -> print plan via CLI
        if print:
            self.print_plan()

    def run_plan_cbp(self):
        """Method that executes cbp_roller using argument paths"""
        try:
            os.system(
                f"ff -o {self.domain_path} -f {self.problem_path} > {self.output_path}"
            )
        except Exception as e:
            raise Exception(f"Error executing planner: {e}\n")

    def print_plan(self):
        """Method that prints plan via CLI"""
        with open(self.output_path, "r") as f:
            print(f.read())

    def get_plan(self):
        """Method which saves and returns the plan inside a variable"""
        with open(self.output_path, "r") as f:
            raw_plan = f.read()
        return raw_plan
