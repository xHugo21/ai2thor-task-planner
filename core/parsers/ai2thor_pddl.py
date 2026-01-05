# File that parses iTHOR state to PDDL problem file


class ParserAI2THORPDDL:
    """Class which contains all the methods needed to parse iTHOR state to PDDL problem file"""

    def __init__(self, event, problem_path, problem, objective, controller):
        self.event = event
        self.metadata = self.event.metadata
        self.problem_path = problem_path
        self.objective = objective
        self.controller = controller

        # General problem parsing (common to all types of problems)
        self.parse_general(problem)

        # Goal condition depending on type of problem
        if problem == "move":
            self.parse_move_problem()
        # elif problem == "drop":
        #     self.parse_drop_problem()

        # Interactable poses added if problem needs to interact with an object
        else:
            self.parse_interactable_poses()

        # Rest of goal conditions depending on type of problem
        if problem == "pickup":
            self.parse_general_problem("holding")
        elif problem == "open":
            self.parse_general_problem("opened")
        elif problem == "close":
            self.parse_general_problem("closed")
        elif problem == "break":
            self.parse_general_problem("broken")
        elif problem == "cook":
            self.parse_general_problem("cooked")
        elif problem == "slice":
            self.parse_general_problem("sliced")
        elif problem == "toggleon":
            self.parse_general_problem("toggledon")
        elif problem == "toggleoff":
            self.parse_general_problem("toggledoff")
        elif problem == "dirty":
            self.parse_general_problem("dirty")
        elif problem == "clean":
            self.parse_general_problem("cleaned")
        elif problem == "fill":
            self.parse_general_problem("filled")
        elif problem == "empty":
            self.parse_general_problem("emptied")
        elif problem == "useup":
            self.parse_general_problem("usedup")
        elif problem == "put":
            self.parse_put_problem()

        # When problem has been parsed, write it to a PDDL file
        self.write_parsed_problem()

    def parse_general(self, problem):
        """Method that transforms general environment data into PDDL problem file"""

        # Agent data extraction
        agent_location = self.metadata["agent"]["position"]  # Initial agent position
        positions = self.metadata[
            "actionReturn"
        ]  # Reachable positions by agent. Return of action GetReachablePositions
        agent_facing = self.metadata[
            "agent"
        ][
            "rotation"
        ][
            "y"
        ]  # Agent orientation. Posible values: 0, 90, 180, 270. Depending on its value, MoveAhead moves in a specific direction
        agent_inclination = self.metadata["agent"][
            "cameraHorizon"
        ]  # Vertical inclination of the agent. Possible values: 60, 30, 0, -30, -60

        # Object data extraction
        self.objects = self.metadata[
            "objects"
        ]  # Contiene todos los objetos del entorno

        # CREATING PDDL FILE
        self.problem = "(define (problem problem1)\n"
        self.problem += f"\t(:domain domain_{problem})\n"

        # Positions and objects definition
        self.problem += "\t(:objects\n"
        i = 0
        for pos in positions:
            self.problem += f"\t\tpos{i} - position\n"
            i += 1
        if self.objective.get("objectId") != None:
            for obj in self.objects:
                if (obj["objectId"] == self.objective["objectId"]) or (
                    obj["isPickedUp"]
                ):
                    self.problem += f"\t\t{obj['name']} - object\n"
        self.problem += "\t)\n\n"

        # State definition
        self.problem += "\t(:init\n"

        # Agent related predicates
        self.problem += f"\t\t(= (facing) {agent_facing})\n\n"
        self.problem += f"\t\t(= (inclination) {agent_inclination})\n\n"
        self.problem += f"\t\t(= (agent-at-x) {agent_location['x']})\n"
        self.problem += f"\t\t(= (agent-at-z) {agent_location['z']})\n\n"

        # Agent posible positions predicates
        i = 0
        for pos in positions:
            self.problem += f"\t\t(= (posiblepos-x pos{i}) {pos['x']})\n"
            self.problem += f"\t\t(= (posiblepos-z pos{i}) {pos['z']})\n\n"
            i += 1

        # Object being held predicates
        for obj in self.objects:
            if obj["isPickedUp"]:
                self.held_obj = obj
                self.problem += f"\t\t(holding {obj['name']})\n\n"

        self.problem += "\t)\n\n"

    def parse_move_problem(self):
        """Method that parses the goal of a move problem"""
        self.problem += "\t(:goal (and\n"
        self.problem += f"\t\t(= (agent-at-x) {self.objective['x']})"
        self.problem += f"\t\t(= (agent-at-z) {self.objective['z']})"
        self.problem += "\t))\n"
        self.problem += ")\n"

    def parse_interactable_poses(self):
        """Method that parses interactable poses of the objective"""

        # Add interactable poses. If there isn't any interactable poses, increase the horizons (agent inclinations)
        event2 = self.controller.step(
            action="GetInteractablePoses",
            objectId=self.objective["objectId"],
            standings=[True],
            horizons=[0],
        )
        interactable_poses = event2.metadata["actionReturn"]
        print(f"Interactable poses: {interactable_poses}")
        if not interactable_poses:
            event2 = self.controller.step(
                action="GetInteractablePoses",
                objectId=self.objective["objectId"],
                standings=[True],
                horizons=[0, 30],
            )
            interactable_poses = event2.metadata["actionReturn"]
            print(f"Interactable poses: {interactable_poses}")
            if not interactable_poses:
                event2 = self.controller.step(
                    action="GetInteractablePoses",
                    objectId=self.objective["objectId"],
                    standings=[True],
                    horizons=[0, 30, 60],
                )
                interactable_poses = event2.metadata["actionReturn"]
                print(f"Interactable poses: {interactable_poses}")
                if not interactable_poses:
                    event2 = self.controller.step(
                        action="GetInteractablePoses",
                        objectId=self.objective["objectId"],
                        standings=[True],
                    )
                    interactable_poses = event2.metadata["actionReturn"]
                    if not interactable_poses:
                        print("Error. The object is not accessible to the agent\n")
                        print("Restart the program and try with another action\n")
                        exit()

        # Write interactable poses predicates
        subproblem = ""
        i = 0
        if interactable_poses:
            for pose in interactable_poses:
                subproblem += f"\t\t(= (interactablepose-x pose{i} {self.objective['name']}) {pose['x']})\n"
                subproblem += f"\t\t(= (interactablepose-z pose{i} {self.objective['name']}) {pose['z']})\n"
                subproblem += f"\t\t(= (interactablepose-facing pose{i} {self.objective['name']}) {pose['rotation']})\n"
                subproblem += f"\t\t(= (interactablepose-inclination pose{i} {self.objective['name']}) {pose['horizon']})\n\n"
                i += 1
        start_index = self.problem.find("(:init\n")
        end_index = self.problem.find("\t\t(= (facing)")
        self.problem = (
            self.problem[: start_index + 8] + subproblem + self.problem[end_index:]
        )

        # Add poses as objects
        subproblem = ""
        for j in range(0, i):
            subproblem += f"\t\tpose{j} - position\n"
        start_index = self.problem.find("(:objects\n")
        end_index = self.problem.find("\t\tpos0")
        self.problem = (
            self.problem[: start_index + 11] + subproblem + self.problem[end_index:]
        )

    def parse_general_problem(self, act):
        """Parse most of actions goal state"""
        self.problem += "\t(:goal (and\n"
        self.problem += f"\t\t({act} {self.objective['name']})"
        self.problem += "\t))\n"
        self.problem += ")\n"

    # def parse_drop_problem(self):
    #     '''Parse drop problem goal state'''
    #     self.problem += "\t(:goal (and\n"
    #     self.problem += f"\t\t(not (holding {self.objective['name']}))\n"
    #     self.problem += "\t))\n"
    #     self.problem += ")\n"

    def parse_put_problem(self):
        """Parse put problem goal state"""
        self.problem += "\t(:goal (and\n"
        self.problem += f"\t\t(put {self.held_obj['name']} {self.objective['name']})\n"
        self.problem += "\t))\n"
        self.problem += ")\n"

    def write_parsed_problem(self):
        """Write full parsed problem into PDDL problem file located in problem_path"""
        with open(self.problem_path, "w") as f:
            f.write(self.problem)
