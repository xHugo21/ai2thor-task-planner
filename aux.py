# Auxiliary functions
# Imports
from PIL import Image as im
import os
import shutil


def printAgentStatus(event):
    """Shows general info and agent status"""
    print("-----------------------------------------------")
    print(f"sceneName: {event.metadata['sceneName']}")
    print(f"lastAction: {event.metadata['lastAction']}")
    print(f"agent cameraHorizon: {event.metadata['agent']['cameraHorizon']}")
    print(f"agent isStanding: {event.metadata['agent']['isStanding']}")
    print(f"agent position: {event.metadata['agent']['position']}")
    print(f"agent rotation: {event.metadata['agent']['rotation']}")
    print("-----------------------------------------------\n")


def isObjectOnScene(event, object):
    """Check if an object is on the scene. Useful for OGAMUS"""
    print("-----------------------------------------------")
    for obj in event.metadata["objects"]:
        if obj["name"].lower().find(object) != -1:
            print(f"{object} existe en la escena")
    print("-----------------------------------------------\n")


def printObjectStatus(event, object):
    """Shows full state of an object"""
    print("-----------------------------------------------")
    for obj in event.metadata["objects"]:
        if obj["objectId"] == object["objectId"]:
            for key, value in obj.items():
                if (
                    key != "axisAlignedBoundingBox"
                    and key != "objectOrientedBoundingBox"
                ):
                    print(f"{key}: {value}")
    print("-----------------------------------------------\n")


def printLastActionStatus(event):
    """Shows info of the last action executed"""
    print("-----------------------------------------------")
    print(f"lastAction: {event.metadata['lastAction']}")
    print(f"lastActionSuccess: {event.metadata['lastActionSuccess']}")
    if event.metadata["errorMessage"]:
        print(f"Error: {event.metadata['errorMessage']}")
    print("-----------------------------------------------\n")


def extractActionImage(event, name):
    """Extracts an image using event"""
    data = im.fromarray(event.frame)
    data.save("./images/" + name + ".png")


def createCamera(controller):
    """Creates a camera and calls extractCameraImage() to save an image"""
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
    extractCameraImage(event.third_party_camera_frames[0], "scene")


def extractCameraImage(nparray, name):
    """Extracts an image using a nparray"""
    data = im.fromarray(nparray)
    data.save("./images/" + name + ".png")


def removeResultFolders():
    """Cleans and ensures existence of result folders mentioned below"""
    dirs = ["./pddl/problems/", "./pddl/outputs/", "./images/", "./Results/"]

    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
            continue

        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))
