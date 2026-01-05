# File that contains the class which translates plans into actions and executes them
from ai2thor.controller import Controller
from utils.viz import extractActionImage


class ParserPDDLAI2THOR:
    """Class which contains methods needed to translate plans into actions and execute them"""

    def __init__(self, raw_plan, controller, iteration, liquid):
        self.actions = []
        self.executable_actions = []
        self.controller = controller
        self.objects = self.controller.last_event.metadata["objects"]

        # Extracts each action from the plan and stores them as an array in self.actions
        self.extract_plan(raw_plan)

        print("*EXECUTING PLAN*\n")

        # Parse each action
        self.parse_actions(iteration, liquid)

        print("*PLAN SUCCESSFULLY EXECUTED*\n")

    def extract_plan(self, raw_plan):
        """Method that extracts each action from the plan and stores them as an array in self.actions"""
        start_index = raw_plan.find("0:")
        end_index = raw_plan.find("time")

        plan = raw_plan[start_index:end_index]  # Extracts raw plan

        plan = plan.splitlines()  # Splits each line into an array

        # Removes blank spaces
        for act in plan:
            if (act.find(":") == -1) or (not act):
                plan.remove(act)
            index = act.find(":")
            act = act[:index].replace(" ", "") + act[index:]
            self.actions.append(act)

        # Removes last position if empty
        if self.actions and self.actions[-1] == " ":
            self.actions.pop()

        if not self.actions:
            print(
                "WARNING: No actions found in the plan. Check if the planner found a solution."
            )

    def parse_actions(self, iteration, liquid):
        """Method that identifies and executes each line of the plan. It also extracts images of the states"""
        # Extracts an image of the initial state
        extractActionImage(self.controller.last_event, f"iter{iteration}_0")
        n_image = 1

        # Find and execute the corresponding action
        for act in self.actions:
            if act.find("ROTATE-LEFT") != -1:
                self.controller.step("RotateLeft")

            elif act.find("ROTATE-RIGHT") != -1:
                self.controller.step("RotateRight")

            elif (
                (act.find("MOVE-AHEAD-0") != -1)
                or (act.find("MOVE-AHEAD-90") != -1)
                or (act.find("MOVE-AHEAD-180") != -1)
                or (act.find("MOVE-AHEAD-270") != -1)
            ):
                self.controller.step(action="MoveAhead")

            elif act.find("LOOKUP") != -1:
                self.controller.step(action="LookUp", degrees=30)

            elif act.find("LOOKDOWN") != -1:
                self.controller.step(action="LookDown", degrees=30)

            elif act.find("STANDUP") != -1:
                self.controller.step("Stand")

            elif act.find("CROUCH") != -1:
                self.controller.step("Crouch")

            elif act.find("PICKUP") != -1:
                self.object_state_action(act, "PICKUP", 7, "PickupObject")

            elif act.find("OPEN") != -1:
                self.object_state_action(act, "OPEN", 5, "OpenObject")

            elif act.find("CLOSE") != -1:
                self.object_state_action(act, "CLOSE", 6, "CloseObject")

            elif act.find("BREAK") != -1:
                self.object_state_action(act, "BREAK", 6, "BreakObject")

            elif act.find("COOK") != -1:
                self.object_state_action(act, "COOK", 5, "CookObject")

            elif act.find("SLICE") != -1:
                self.object_state_action(act, "SLICE", 6, "SliceObject")

            elif act.find("TOGGLEON") != -1:
                self.object_state_action(act, "TOGGLEON", 9, "ToggleObjectOn")

            elif act.find("TOGGLEOFF") != -1:
                self.object_state_action(act, "TOGGLEOFF", 10, "ToggleObjectOff")

            elif act.find("DIRTY") != -1:
                self.object_state_action(act, "DIRTY", 6, "DirtyObject")

            elif act.find("CLEAN") != -1:
                self.object_state_action(act, "CLEAN", 6, "CleanObject")

            elif act.find("FILL") != -1:
                self.object_state_action(act, "FILL", 5, "FillObjectWithLiquid", liquid)

            elif act.find("EMPTY") != -1:
                self.object_state_action(act, "EMPTY", 6, "EmptyLiquidFromObject")

            elif act.find("USEUP") != -1:
                self.object_state_action(act, "USEUP", 6, "UseUpObject")

            elif act.find("PUT") != -1:
                start_index = act.find("PUT ")
                end_index1 = act.find(" ", start_index + 4)
                end_index2 = act.find(" ", end_index1)
                print(end_index2)
                obj_name = act[start_index + 4 : end_index2]
                for obj in self.objects:
                    if (obj["name"].upper() == obj_name) and ("PUT" != "FILL"):
                        self.controller.step(
                            action="PutObject", objectId=obj["objectId"]
                        )

            # If there has been an error -> print via CLI and exit
            if self.controller.last_event.metadata["errorMessage"]:
                print(f"Error: {self.controller.last_event.metadata['errorMessage']}")
                print("Restart the program and try with another action\n")
                exit()

            # Extract image of the final state
            extractActionImage(self.controller.last_event, f"iter{iteration}_{n_image}")
            n_image += 1

    def object_state_action(
        self, act, action_name_domain, plus_index, action_name_ai2thor, liquid="coffee"
    ):
        """Method that executes similar iTHOR actions with info extracted from the plan"""
        start_index = act.find(action_name_domain)
        end_index = act.find(" POSE")
        obj_name = act[start_index + plus_index : end_index]
        for obj in self.objects:
            if (obj["name"].upper() == obj_name) and (action_name_domain != "FILL"):
                self.controller.step(
                    action=action_name_ai2thor, objectId=obj["objectId"]
                )
            elif (obj["name"].upper() == obj_name) and (action_name_domain == "FILL"):
                self.controller.step(
                    action=action_name_ai2thor,
                    objectId=obj["objectId"],
                    fillLiquid=liquid,
                )
