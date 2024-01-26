from PIL import Image, ImageSequence
import os


if __name__ == '__main__':
    input_path = input("Please give the path to a GIF file to extract frames.\n")
    output_path = input("Please give a path to output GIF frame.\n")

    # Input validation
    if not os.path.exists(input_path):
        raise FileExistsError("wtf bro there is no file at " + input_path)
    elif not input_path.endswith('.gif'):
        raise TypeError("wtf bro that's not a gif")

    # Output validation
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    gif = Image.open(input_path)
    # save_sequence(generate_sequence_from_gif(gif))
    frame = 0
    sequence = ImageSequence.Iterator(gif)
    while True:
        try:
            filename = os.path.join(output_path, str(frame) + '.png')
            sequence[frame].save(filename)
            frame += 1
        except IndexError:
            break

    print(f"All frames from {gif} are extracted to {output_path}")
