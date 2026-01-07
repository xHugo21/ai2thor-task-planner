from PIL import Image as im


def extract_action_image(event, name):
    """Extracts an image using event"""
    data = im.fromarray(event.frame)
    data.save("./images/" + name + ".png")


def extract_camera_image(nparray, name):
    """Extracts an image using a nparray"""
    data = im.fromarray(nparray)
    data.save("./images/" + name + ".png")
