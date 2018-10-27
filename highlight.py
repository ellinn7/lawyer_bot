import sys
from PIL import Image, ImageDraw

#im = Image.open("out1-1.jpg")

#draw = ImageDraw.Draw(im, 'RGBA')
#draw.rectangle([100, 20, 500, 300], fill = (50, 50, 50, 64))
#draw.line((0, im.size[1], im.size[0], 0), fill=128)
#del draw

#im.show()

class StartingCoordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class RectangleDimensions:
  def __init__(self, width, height):
    self.width = width
    self.height = height

class Color:
  def __init__(self, r, g, b, a):
    self.r = r
    self.g = g
    self.b = b
    self.a = a

class Highlight:
  def __init__(self, page_number, starting_coordinate, rectangle_dimensions, color):
    self.page_number = page_number
    self.starting_coordinate = starting_coordinate
    self.rectangle_dimensions = rectangle_dimensions
    self.color = color
    
def highlight(images, highlights):
#
  print("start highlight")

  for i in range(0, len(images)):
    image = Image.open(images[i])

    draw = ImageDraw.Draw(image, 'RGBA')
    #draw.rectangle([100, 20, 500, 300], fill = (50, 50, 50, 64))
    #TODO: учесть page_number
    draw.rectangle([highlights[i].starting_coordinate.x, highlights[i].starting_coordinate.y, highlights[i].rectangle_dimensions.width, highlights[i].rectangle_dimensions.height],
                   fill = (highlights[i].color.r, highlights[i].color.g, highlights[i].color.b, highlights[i].color.a))
    del draw
    image.show()

  print("stop highlight")
#
grey = Color(50, 50, 50, 64)

images = ["d:/hack/test/image1.jpg",
          "d:/hack/test/image2.jpg"]
#highlights = [[page_num, (x, y), (width, height), color], ...]
#highlights = [[0, (100, 200), (250, 50), "color1"], [1, (40, 80), (95, 160), "color2"]]
highlights = [Highlight(0, StartingCoordinate(100, 200), RectangleDimensions(250, 50), grey),
              Highlight(1, StartingCoordinate(40, 80), RectangleDimensions(95, 160), grey)]

highlight(images, highlights)
