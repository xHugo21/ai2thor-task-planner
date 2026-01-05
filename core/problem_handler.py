# File that manages input data between the program and the user

# Imports
import os
from core.planning.planner import Planner


class ProblemDefinition:
    """Class that contains all methods to manage input data"""

    def __init__(self):
        self.problem_list = []
        self.objective_list = []

    def method_selection(self):
        """Method that allows selecting execution type:
        1. METADATA: Uses data returned by simulator to locate objects and agent positions
        2. OGAMUS: Uses OGAMUS algorithm to scan scenes using pretrained neural networks"""
        loop = True
        while loop:
            print("----METHOD----")
            print("[1] - METADATA")
            print("[2] - OGAMUS")
            print("--------------")
            self.method = int(input("Select the method used to solve the problem: "))
            print("")
            if 1 <= self.method <= 2:
                loop = False
                self.method = str(self.method)
            else:
                print("Please, input a valid option\n")

        return self.method

    def scene_selection(self):
        """Method that allows selection of the scene"""
        loop = True
        while loop:
            print("----SCENE----")
            print("[1-30] - Kitchens")
            print("[201-230] - Living Rooms")
            print("[301-330] - Bedrooms")
            print("[401-430] - Bathrooms")
            print("---------------")
            self.scene_number = int(input("Select a scene: "))
            print("")
            if (
                (1 <= self.scene_number <= 30)
                or (201 <= self.scene_number <= 230)
                or (301 <= self.scene_number <= 330)
                or (401 <= self.scene_number <= 430)
            ):
                loop = False
                self.scene_number = str(self.scene_number)
            else:
                print("Please, input a valid scene\n")

        return self.scene_number

    def paths_selection(self, iteracion):
        """Method that specifies problem and output paths"""
        self.problem_path = f"./pddl/problems/problem{iteracion}.pddl"
        self.output_path = f"./pddl/outputs/problem{iteracion}.txt"

        return self.problem_path, self.output_path

    def problem_selection(self, event):
        """Method that allows selecting problems and objectives"""
        self.liquid = "coffee"
        self.event = event
        loop = True
        holding = False
        while loop:
            print("----ACTION----")
            print("[1] - Move Agent")
            print("[2] - Pickup Object")
            print("[3] - Open Object")
            print("[4] - Close Object")
            print("[5] - Break Object")
            print("[6] - Cook Object")
            print("[7] - Slice Object")
            print("[8] - Toggle On Object")
            print("[9] - Toggle Off Object")
            print("[10] - Dirty Object")
            print("[11] - Clean Object")
            print("[12] - Fill Object")
            print("[13] - Empty Object")
            print("[14] - Use Up Object")
            print("[15] - Drop Object (Requires holding an object)")
            print("[16] - Put Object (Requires holding an object)")
            print("----------------")
            aux = input("Select an action: ")
            print("")
            for obj in event.metadata["objects"]:
                if obj["isPickedUp"]:
                    holding = True
            if 1 <= int(aux) <= 14:
                loop = False
            elif (15 <= int(aux) <= 16) and holding:
                loop = False
            else:
                print("Please, input a valid action\n")

        # Establecer parámetros en caso de que se seleccione problema de movimiento
        if str(aux) == "1":
            self.problem = "move"
            print("----OBJECTIVE----")
            positions = event.metadata["actionReturn"]
            i = 0
            for pos in positions:
                print(f"[{i}] - {pos}")
                i += 1
            print("----------------")
            aux2 = input("Select the goal position: ")
            self.objective = positions[int(aux2)]
            print("")
            print(f"Selected goal position is: {self.objective}")

        # Establecer parámetros en caso de que se seleccione problema de pickup
        if str(aux) == "2":
            self.object_selection("pickup", "pickupable", "isPickedUp", False)

        if str(aux) == "3":
            self.object_selection("open", "openable", "isOpen", False)

        if str(aux) == "4":
            self.object_selection("close", "openable", "isOpen", True)

        if str(aux) == "5":
            self.object_selection("break", "breakable", "isBroken", False)

        if str(aux) == "6":
            self.object_selection("cook", "cookable", "isCooked", False)

        if str(aux) == "7":
            self.object_selection("slice", "sliceable", "isSliced", False)

        if str(aux) == "8":
            self.object_selection("toggleon", "toggleable", "isToggled", False)

        if str(aux) == "9":
            self.object_selection("toggleoff", "toggleable", "isToggled", True)

        if str(aux) == "10":
            self.object_selection("dirty", "dirtyable", "isDirty", False)

        if str(aux) == "11":
            self.object_selection("clean", "dirtyable", "isDirty", True)

        if str(aux) == "12":
            self.object_selection(
                "fill", "canFillWithLiquid", "isFilledWithLiquid", False, True
            )

        if str(aux) == "13":
            self.object_selection(
                "empty", "canFillWithLiquid", "isFilledWithLiquid", True
            )

        if str(aux) == "14":
            self.object_selection("useup", "canBeUsedUp", "isUsedUp", False)

        if str(aux) == "15":
            self.object_selection("drop", "pickupable", "isPickedUp", True)

        if str(aux) == "16":
            self.object_selection("put", "receptacle", "receptacle", True)

        return self.problem, self.objective, self.liquid

    def object_selection(
        self, problem_type, condition1, condition2, condition2_res, select_liquid=False
    ):
        """Method that contains the objective selection of most of the problems"""
        self.problem = problem_type
        posible_objects = []
        for obj in self.event.metadata["objects"]:
            if (obj[condition1] == True) and (obj[condition2] == condition2_res):
                posible_objects.append(obj)
        if not posible_objects:
            print(
                "There aren't any objectives for this action. Select another or switch the scene\n"
            )
            return self.problem_selection(self.event)
        print("----OBJECTIVE----")
        i = 0
        for obj in posible_objects:
            print(f"[{i}] - {obj['objectId']}")
            i += 1
        print("----------------")
        aux2 = input("Select the objective: ")
        self.objective = posible_objects[int(aux2)]
        print("")
        print(
            f"Selected objective is: {self.objective['objectId']} {self.objective['name']}\n"
        )

        if select_liquid:
            print("----LIQUID----")
            print("[1] - Coffee")
            print("[2] - Wine")
            print("[3] - Water")
            print("----------------")
            inp = input(f"Select liquid to fill objective with: ")

            if str(inp) == "1":
                self.liquid = "coffee"
            elif str(inp) == "2":
                self.liquid = "wine"
            elif str(inp) == "3":
                self.liquid = "water"

    def problem_selection_ogamus(self):
        """Method that allows user to select problems to be solved with OGAMUS"""
        loop = True
        while loop:
            print("----ACTION----")
            print("[1] - Get Close To Object")
            print("[2] - Pickup Object")
            print("[3] - Open Object")
            print("[4] - Close Object")
            print("[5] - Break Object")
            print("[6] - Cook Object")
            print("[7] - Slice Object")
            print("[8] - Toggle On Object")
            print("[9] - Toggle Off Object")
            print("[10] - Dirty Object")
            print("[11] - Clean Object")
            print("[12] - Fill Object")
            print("[13] - Empty Object")
            print("[14] - Use Up Object")
            print("[15] - Drop Object (Requires holding an object)")
            print("[16] - Put Object (Requires holding an object)")
            print("----------------")
            aux = input("Select an action: ")
            print("")
            if 1 <= int(aux) <= 16:
                loop = False
            else:
                print("Please, input a valid action\n")

        problemas_ogamus = [
            "get_close_to",
            "pickup",
            "open",
            "close",
            "break",
            "cook",
            "slice",
            "toggleon",
            "toggleoff",
            "dirty",
            "clean",
            "fill",
            "empty",
            "useup",
            "drop",
            "put",
        ]
        self.problem = problemas_ogamus[int(aux) - 1]
        self.problem_list.append(self.problem)

        self.object_selection_ogamus()

        print("")
        condition = input(
            "Do you want to execute more actions in this environment? [Y/n]: "
        )
        print("")
        if condition == "Y":
            self.problem_selection_ogamus()

        return self.problem_list, self.objective_list

    def object_selection_ogamus(self):
        """Method that allows selecting the objective of OGAMUS problem"""
        if self.problem == "get_close_to":
            possible_objects = [
                "alarmclock",
                "aluminumfoil",
                "apple",
                "baseballbat",
                "book",
                "boots",
                "basketball",
                "bottle",
                "bowl",
                "box",
                "bread",
                "butterknife",
                "candle",
                "cd",
                "cellphone",
                "peppershaker",
                "cloth",
                "creditcard",
                "cup",
                "dishsponge",
                "dumbbell",
                "egg",
                "fork",
                "handtowel",
                "kettle",
                "keychain",
                "knife",
                "ladle",
                "laptop",
                "lettuce",
                "mug",
                "newspaper",
                "pan",
                "papertowel",
                "papertowelroll",
                "pen",
                "pencil",
                "papershaker",
                "pillow",
                "plate",
                "plunger",
                "pot",
                "potato",
                "remotecontrol",
                "saltshaker",
                "scrubbrush",
                "soapbar",
                "soapbottle",
                "spatula",
                "spoon",
                "spraybottle",
                "statue",
                "tabletopdecor",
                "teddybear",
                "tennisracket",
                "tissuebox",
                "toiletpaper",
                "tomato",
                "towel",
                "vase",
                "watch",
                "wateringcan",
                "winebottle",
                "armchair",
                "bathtub",
                "bathtubbasin",
                "bed",
                "bowl",
                "box",
                "cabinet",
                "coffeemachine",
                "coffeetable",
                "countertop",
                "desk",
                "diningtable",
                "drawer",
                "fridge",
                "garbagecan",
                "handtowelholder",
                "laundryhamper",
                "microwave",
                "mug",
                "ottoman",
                "pan",
                "plate",
                "pot",
                "safe",
                "shelf",
                "sidetable",
                "sinkbasin",
                "sofa",
                "toaster",
                "toilet",
                "toiletpaperhanger",
                "towelholder",
                "tvstand",
                "stoveburner",
                "blinds",
                "book",
                "box",
                "cabinet",
                "drawer",
                "fridge",
                "kettle",
                "laptop",
                "microwave",
                "safe",
                "showercurtain",
                "showerdoor",
                "toilet",
            ]

        elif self.problem == "pickup" or self.problem == "drop":
            possible_objects = [
                "alarmclock",
                "aluminumfoil",
                "apple",
                "baseballbat",
                "book",
                "boots",
                "basketball",
                "bottle",
                "bowl",
                "box",
                "bread",
                "butterknife",
                "candle",
                "cd",
                "cellphone",
                "peppershaker",
                "cloth",
                "creditcard",
                "cup",
                "dishsponge",
                "dumbbell",
                "egg",
                "fork",
                "handtowel",
                "kettle",
                "keychain",
                "knife",
                "ladle",
                "laptop",
                "lettuce",
                "mug",
                "newspaper",
                "pan",
                "papertowel",
                "papertowelroll",
                "pen",
                "pencil",
                "papershaker",
                "pillow",
                "plate",
                "plunger",
                "pot",
                "potato",
                "remotecontrol",
                "saltshaker",
                "scrubbrush",
                "soapbar",
                "soapbottle",
                "spatula",
                "spoon",
                "spraybottle",
                "statue",
                "tabletopdecor",
                "teddybear",
                "tennisracket",
                "tissuebox",
                "toiletpaper",
                "tomato",
                "towel",
                "vase",
                "watch",
                "wateringcan",
                "winebottle",
            ]

        elif self.problem == "open" or self.problem == "close":
            possible_objects = [
                "blinds",
                "book",
                "box",
                "cabinet",
                "drawer",
                "fridge",
                "kettle",
                "laptop",
                "microwave",
                "safe",
                "showercurtain",
                "showerdoor",
                "toilet",
            ]

        elif self.problem == "put":
            possible_objects = [
                "armchair",
                "bathtub",
                "bathtubbasin",
                "bed",
                "bowl",
                "box",
                "cabinet",
                "coffeemachine",
                "coffeetable",
                "countertop",
                "desk",
                "diningtable",
                "drawer",
                "fridge",
                "garbagecan",
                "handtowelholder",
                "laundryhamper",
                "microwave",
                "mug",
                "ottoman",
                "pan",
                "plate",
                "pot",
                "safe",
                "shelf",
                "sidetable",
                "sinkbasin",
                "sofa",
                "toaster",
                "toilet",
                "toiletpaperhanger",
                "towelholder",
                "tvstand",
                "stoveburner",
            ]

        elif self.problem == "break":
            possible_objects = [
                "bottle",
                "bowl",
                "cellphone",
                "cup",
                "egg",
                "laptop",
                "television",
                "mirror",
                "mug",
                "plate",
                "showerdoor",
                "statue",
                "vase",
                "window",
                "winebottle",
            ]

        elif self.problem == "cook":
            possible_objects = ["breadsliced", "eggcracked", "potato", "potatosliced"]

        elif self.problem == "slice":
            possible_objects = ["apple", "bread", "egg", "lettuce", "potato", "tomato"]

        elif self.problem == "toggleon" or self.problem == "toggleoff":
            possible_objects = [
                "candle",
                "cellphone",
                "coffeemachine",
                "desklamp",
                "faucet",
                "floorlamp",
                "laptop",
                "lightswitch",
                "microwave",
                "showerhead",
                "stoveburner",
                "stoveknob",
                "television",
                "toaster",
            ]

        elif self.problem == "dirty" or self.problem == "clean":
            possible_objects = [
                "bed",
                "bowl",
                "cloth",
                "cup",
                "mirror",
                "mug",
                "pan",
                "plate",
                "pot",
            ]

        elif self.problem == "fill" or self.problem == "empty":
            possible_objects = [
                "bottle",
                "bowl",
                "cup",
                "houseplant",
                "kettle",
                "mug",
                "pot",
                "wateringcan",
                "winebottle",
            ]

        elif self.problem == "useup":
            possible_objects = [
                "papertowelroll",
                "soapbottle",
                "tissuebox",
                "toiletpaper",
            ]

        print("----OBJECTIVE----")
        i = 0
        for obj in possible_objects:
            print(f"[{i}] - {obj}")
            i += 1
        print("----------------")
        aux2 = input("Select the objective: ")
        self.objective = possible_objects[int(aux2)]
        self.objective_list.append(self.objective)

    def problem_selection_ogamus_input(self, input):
        """Method that executes and reads PDDL input files for OGAMUS"""
        # We call the planner and save the input in /pddl/outputs/input_plan.txt
        planificador = Planner(
            input, "./pddl/outputs/input_plan.txt", "pickup", 1, 3, True, True
        )

        # Extract the plan
        raw_plan = planificador.get_plan()
        start_index = raw_plan.find("0:")
        end_index = raw_plan.find("time")

        # Get actions split by lines
        plan = raw_plan[start_index:end_index]
        plan = plan.splitlines()

        list_plan = []

        # Remove blank spaces
        for act in plan:
            if (act.find(":") == -1) or (not act):
                plan.remove(act)
            index = act.find(":")
            act = act[:index].replace(" ", "") + act[index:]
            list_plan.append(act)

        # Remove last position if empty
        if list_plan[-1] == " ":
            list_plan.pop()

        # Cycle through each action and parse it to add problems and objectives to arrays
        for act in list_plan:
            if act.find("BASICACTION") != -1:
                start_index = act.find("(") + 15
                act2 = act[start_index:]
                end_index = act2.find(" ")
                problem_name = act2[:end_index]
                end_index2 = act2.find(")")
                objective_name = act2[end_index + 1 : end_index2]

                self.problem_list.append(problem_name.lower())
                self.objective_list.append(objective_name.lower())

        print(" ")
        print(self.problem_list)
        print(self.objective_list)
        print(" ")

        return self.problem_list, self.objective_list
