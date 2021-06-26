from PIL import Image, ImageDraw, ImageFont
from global_variables import GeneralSettings
import enum


class Position(enum.Enum):
    TopLeft = 0
    TopCenter = 1
    TopRight = 2
    CenterLeft = 3
    Center = 4
    CenterRight = 5
    BottomLeft = 6
    BottomCenter = 7
    BottomRight = 8


class ImageProcessor:

    font = ImageFont.truetype(GeneralSettings.font_path, GeneralSettings.font_size)

    def __init__(self, dir: str, name: str, overwrite: bool = False):
        self.image = Image.open(dir + name)
        self.width, self.height = self.image.size
        self.draw = ImageDraw.Draw(self.image)
        self.directory = dir
        self.file_name = (name.split("."))[-2]
        self.overwrite = overwrite

    def place(self, text: str, pos_x: int, pos_y: int):
        if self.overwrite:
            new_name = self.file_name + ".jpg"
            new_path = "{}{}".format(self.directory, new_name)
        else:
            new_name = self.file_name + "-Watermarked.jpg"
            new_path = "{}{}".format(self.directory, new_name)

        text_width, text_height = self.draw.textsize(text, self.font)
        self.draw.rectangle((pos_x - 10,
                             pos_y - 10,
                             pos_x + text_width + 20,
                             pos_y + text_height + 20), fill="black")
        self.draw.text((pos_x, pos_y), text, font=self.font)
        self.image.save(new_path)

        return new_path

    def place_at(self, text: str, pos: Position, margin: int):
        text_width, text_height = self.draw.textsize(text, self.font)

        xL = margin
        xC = (self.width / 2) - (text_width / 2)
        xR = self.width - text_width - margin
        yT = margin
        yC = (self.height / 2) - (text_height / 2)
        yB = self.height - text_height - margin

        if pos is Position.TopLeft:
            return self.place(text, xL, yT)
        elif pos is Position.TopCenter:
            return self.place(text, xC, yT)
        elif pos is Position.TopRight:
            return self.place(text, xR, yT)
        elif pos is Position.CenterLeft:
            return self.place(text, xL, yC)
        elif pos is Position.Center:
            return self.place(text, xC, yC)
        elif pos is Position.CenterRight:
            return self.place(text, xR, yC)
        elif pos is Position.BottomLeft:
            return self.place(text, xL, yB)
        elif pos is Position.BottomCenter:
            return self.place(text, xC, yB)
        elif pos is Position.BottomRight:
            return self.place(text, xR, yB)
