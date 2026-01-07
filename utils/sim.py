import os
import shutil
from utils.viz import extract_camera_image


def print_agent_status(event):
    """Shows general info and agent status"""
    print("-----------------------------------------------")
    print(f"sceneName: {event.metadata['sceneName']}")
    print(f"lastAction: {event.metadata['lastAction']}")
    print(f"agent cameraHorizon: {event.metadata['agent']['cameraHorizon']}")
    print(f"agent isStanding: {event.metadata['agent']['isStanding']}")
    print(f"agent position: {event.metadata['agent']['position']}")
    print(f"agent rotation: {event.metadata['agent']['rotation']}")
    print("-----------------------------------------------\n")


def is_object_on_scene(event, object_name):
    """Check if an object is on the scene. Useful for OGAMUS"""
    print("-----------------------------------------------")
    for obj in event.metadata["objects"]:
        if obj["name"].lower().find(object_name) != -1:
            print(f"{object_name} exists in the scene")
    print("-----------------------------------------------\n")


def print_object_status(event, object_meta):
    """Shows full state of an object"""
    print("-----------------------------------------------")
    for obj in event.metadata["objects"]:
        if obj["objectId"] == object_meta["objectId"]:
            for key, value in obj.items():
                if key not in ["axisAlignedBoundingBox", "objectOrientedBoundingBox"]:
                    print(f"{key}: {value}")
    print("-----------------------------------------------\n")


def print_last_action_status(event):
    """Shows info of the last action executed"""
    print("-----------------------------------------------")
    print(f"lastAction: {event.metadata['lastAction']}")
    print(f"lastActionSuccess: {event.metadata['lastActionSuccess']}")
    if event.metadata["errorMessage"]:
        print(f"Error: {event.metadata['errorMessage']}")
    print("-----------------------------------------------\n")


def create_camera(controller):
    """Creates a camera and calls extract_camera_image() to save an image"""
    event = controller.step("Done")
    center = event.metadata["sceneBounds"]["center"]
    center["y"] = event.metadata["sceneBounds"]["cornerPoints"][0][1]
    camera_loc = center

    event = controller.step(
        action="AddThirdPartyCamera",
        position=camera_loc,
        rotation=dict(x=90, y=0, z=0),
        fieldOfView=110,
    )
    extract_camera_image(event.third_party_camera_frames[0], "scene")


def remove_result_folders():
    """Cleans and ensures existence of result folders mentioned below"""
    dirs = ["./pddl/problems/", "./pddl/outputs/", "./images/", "./results/"]

    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            continue

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
