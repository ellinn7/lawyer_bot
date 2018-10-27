import sys
import os
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

def generateOverlayFileName(full_path):
#
  base_name = os.path.basename(full_path)
  name = os.path.splitext(base_name)[0]
  return full_path.replace(name, name + "_overlay")
#

def highlight(image_paths, highlights):
#
  overlay_image_paths = []

  for i in range(0, len(image_paths)):
    image = Image.open(image_paths[i])

    draw = ImageDraw.Draw(image, 'RGBA')
    draw.rectangle([highlights[i].starting_coordinate.x,
                    highlights[i].starting_coordinate.y,
                    highlights[i].rectangle_dimensions.width,
                    highlights[i].rectangle_dimensions.height],
                    fill = (highlights[i].color.r,
                            highlights[i].color.g,
                            highlights[i].color.b,
                            highlights[i].color.a))

    new_name = generateOverlayFileName(image_paths[i])
    image.save(new_name)
    overlay_image_paths.append(new_name)

  del draw
  return overlay_image_paths
#

#grey = Color(50, 50, 50, 64)
#images = ["d:/hack/test/image1.jpg",
#          "d:/hack/test/image2.jpg"]
#highlights = [Highlight(0, StartingCoordinate(100, 200), RectangleDimensions(250, 50), grey),
#              Highlight(1, StartingCoordinate(40, 80), RectangleDimensions(95, 160), grey)]
#
#overlay_images = highlight(images, highlights)

#for im in overlay_images:
#  print(im)

def generateJpegPath(tiff_path, page_number):
#
  base_name = os.path.basename(tiff_path)
  name = os.path.splitext(base_name)[0]

  tiff_template = name + '.tiff'
  jpeg_template = str(page_number) + "_" + name + '.jpeg'
  
  return tiff_path.replace(tiff_template, jpeg_template)
#

def tiffToJpg(tiff_path):
#
  image_paths = []
  
  image = Image.open(tiff_path)
  for i in range(0, image.n_frames):
    image.seek(i)
    out = image.convert("RGB")
    jpeg_path = generateJpegPath(tiff_path, i+1)
    out.save(jpeg_path, "JPEG", quality=90)
    
    image_paths.append(jpeg_path)

  return image_paths
#

#tiff_path = 'd:/hack/tifftojpg/contract2.tiff'
#result = tiffToJpg(tiff_path)
#
#print("result:")
#for j in result:
#  print(j)
