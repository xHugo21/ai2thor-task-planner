from PIL import Image as im


def extractActionImage(event, name):
    """Extracts an image using event"""
    data = im.fromarray(event.frame)
    data.save("./images/" + name + ".png")


def extractCameraImage(nparray, name):
    """Extracts an image using a nparray"""
    data = im.fromarray(nparray)
    data.save("./images/" + name + ".png")
