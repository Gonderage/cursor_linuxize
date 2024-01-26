# Separate the frames of each cursor icon from each .png file that is
# extracted from the .gif files of SnooAh's Hololive EN Promise cursors,
# because SnooAh hasn't responded to my inquiry about making cursors for Linux yet. :(
# Currently, I've extracted the .png files with ezgif.com/split and placed them in frames/
# TODO: Figure out how to do split .gif files with PIL.Image.GIFImagePlugin

import os

from PIL import Image, ImageDraw, GifImagePlugin

input_path = "input"
output_dir = "output"
frames_amount = 11
icon_size = 340
icon_spacing = icon_size + 10
margin_left = 30
margin_top = 290


class Icon:
    """Icon with a name and box coordinates on the image."""

    def __init__(self, name: str, coordinates: tuple[int]):
        self.name: str = name
        self.coordinates: tuple[int] = coordinates


icons: list[Icon] = []
icon_names: list[str] = [
    "normal_select",
    "help_selection",
    "working_in_background",
    "busy",
    "text_select",
    "unavailable",
    "vertical_resize",
    "horizontal_resize",
    "diagonal_resize1",
    "diagonal_resize2",
    "move",
    "alternate_selection",
    "link_selection"]


def generate_all_icon_coordinates() -> tuple[tuple[int]]:
    """Generate a tuple of tuple-4s representing an icon's box coordinates."""

    def generate_icon_coordinates(
            row: int, column: int,
            left_edge: int = margin_left,
            top_edge: int = margin_top) -> tuple[int]:
        """Generates an icon's box coordinates for Image.crop()"""
        left = left_edge + (row * icon_spacing)
        top = top_edge + (column * icon_spacing)
        return tuple([
            left, top,
            left + icon_size,
            top + icon_size])

    # First two rows
    for j in [0, 1]:
        for i in [0, 1, 2, 3, 4]:
            yield generate_icon_coordinates(i, j)
    # Last row is offset by one icon spacing
    for i in [0, 1, 2]:
        yield generate_icon_coordinates(
            i, 2, margin_left + icon_spacing)


def setup_icons() -> None:
    coordinates_list = tuple(generate_all_icon_coordinates())
    for i, coordinates in enumerate(coordinates_list):
        icons.append(Icon(icon_names[i], coordinates))


def generate_icon_images(_icon: Icon) -> tuple[Image.Image]:
    """Generate a tuple of all frames of one icon."""
    for frame in range(0, frames_amount):
        # TODO: Use a more robust way of getting image filename
        frame_path = os.path.join(input_path, f"{frame}.png")
        # Image processing
        with Image.open(frame_path).convert('RGBA') as frame_image:
            frame_image = frame_image.crop(_icon.coordinates)
            # Transparency
            ImageDraw.floodfill(frame_image, [0, 0], (0, 0, 0, 0))
            yield frame_image


def save_icon_frames(_icon: Icon) -> None:
    """Save one icon's frames into its own directory.
    If the directory doesn't exist, one will be created."""
    icon_path = os.path.join(output_dir, _icon.name)
    if os.path.exists(icon_path):
        return
    else:
        os.mkdir(icon_path)

    # Save the images to output directory
    images_list = list(generate_icon_images(_icon))
    for frame, image in enumerate(images_list):
        # Image file should look like "icons/busy/busy_0.png"
        image_name = f"{_icon.name}_{frame}.png"
        output_path = os.path.join(icon_path, image_name)
        image.save(output_path)


def setup() -> None:
    assert os.path.isdir(input_path), NotADirectoryError("bro wtf that's not a directory.")

    global output_dir # bro you're already a global variable ????
    if output_dir == "":
        output_dir = "output"
        os.mkdir(output_dir)
    elif not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    print(f"Saving to path {output_dir}")


if __name__ == '__main__':
    setup_icons()
    output_dir = input(
        "Where would you like to store the icons?\n"
        "Leave blank for an automatic output directory\n")
    input_path = input(
        "Insert path to either a sequence of PNGs.\n")
    setup()

    # Percentage completion
    count = len(icons)
    iterator = 0

    for icon in icons:
        percentage = str(iterator * 100 / count)[:4]
        print(f"Completion: {percentage}%")
        iterator += 1

        save_icon_frames(icon)

    print("Done :D")
