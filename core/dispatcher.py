from utils.sim import printObjectStatus, printLastActionStatus
from utils.viz import extractActionImage


class ExecOgamus:
    """This class executes the action asked by the user after OGAMUS has found the objective"""

    def __init__(self, controller, problem, objective, iteration):
        self.controller = controller
        self.problem = problem
        self.objective = objective

        # An image is extracted with the current state
        extractActionImage(self.controller.last_event, f"problem{iteration}_0")

        # We call get_object_id() to get object id
        self.get_object_id()

        # Depending on the problem we execute an action or another. get_close_to action is ignored because there isn't more actions that the simulator has to trigger
        if self.problem == "pickup":
            self.controller.step(
                action="PickupObject", objectId=self.final_objective["objectId"]
            )
            self.controller.step(
                action="MoveHeldObjectUp", moveMagnitude=0.3, forceVisible=False
            )

        elif self.problem == "open":
            self.controller.step(
                action="OpenObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "close":
            self.controller.step(
                action="CloseObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "break":
            self.controller.step(
                action="BreakObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "cook":
            self.controller.step(
                action="CookObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "slice":
            self.controller.step(
                action="SliceObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "toggleon":
            self.controller.step(
                action="ToggleObjectOn", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "toggleoff":
            self.controller.step(
                action="ToggleObjectOff", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "dirty":
            self.controller.step(
                action="DirtyObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "clean":
            self.controller.step(
                action="CleanObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "fill":
            self.controller.step(
                action="FillObjectWithLiquid",
                objectId=self.final_objective["objectId"],
                fillLiquid="water",
            )

        elif self.problem == "empty":
            self.controller.step(
                action="EmptyLiquidFromObject",
                objectId=self.final_objective["objectId"],
            )

        elif self.problem == "useup":
            self.controller.step(
                action="UseUpObject", objectId=self.final_objective["objectId"]
            )

        elif self.problem == "drop":
            self.controller.step(action="DropHandObject")

        elif self.problem == "put":
            self.controller.step(
                action="PutObject",
                objectId=self.final_objective["objectId"],
                placeStationary=True,
            )

        # Show the object status via CLI
        printObjectStatus(self.controller.last_event, self.final_objective)
        printLastActionStatus(self.controller.last_event)

        # Extract last state image
        self.controller.step("Pass")
        extractActionImage(self.controller.last_event, f"problem{iteration}_1")

    def get_object_id(self):
        """Method that extracts the object id corresponding to the object found in OGAMUS"""
        for obj in self.controller.last_event.metadata["objects"]:
            aux = obj["objectId"].upper().find(self.objective.upper())
            if aux != -1:
                if obj["objectId"][aux + len(self.objective)] == "|":
                    print(obj["objectId"])
                    self.final_objective = obj
