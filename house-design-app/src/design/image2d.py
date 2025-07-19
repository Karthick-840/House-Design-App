from PIL import Image, ImageDraw
from house import House, Wall

def generate_2d_image(house, img_size=(800, 600)):
    image = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(image)
    for room in house.rooms:
        render_room(draw, room)
    for wall in house.walls:
        render_wall(draw, wall)
    return image

def render_wall(draw, wall):
    # wall: Wall object
    x, y, w, h = wall.x, wall.y, wall.width, wall.height
    draw.rectangle([x, y, x + w, y + h], outline="black", width=4)

def render_room(draw, room):
    # room: dict with x, y, width, height, color
    x = room.get('x', 0)
    y = room.get('y', 0)
    w = room.get('width', 100)
    h = room.get('height', 100)
    color = room.get('color', 'lightgray')
    draw.rectangle([x, y, x + w, y + h], fill=color, outline="gray", width=2)

def save_image(image, filename):
    image.save(filename, "PNG")

# Example usage
if __name__ == "__main__":
    house = House()
    house.add_wall(Wall(100, 100, 600, 10))
    house.add_wall(Wall(100, 100, 10, 400))
    house.add_wall(Wall(100, 500, 600, 10))
    house.add_wall(Wall(700, 100, 10, 410))

    house.add_room({'x': 120, 'y': 120, 'width': 200, 'height': 180, 'color': 'lightblue'})
    house.add_room({'x': 340, 'y': 120, 'width': 320, 'height': 180, 'color': 'lightgreen'})
    house.add_room({'x': 120, 'y': 320, 'width': 540, 'height': 170, 'color': 'lightyellow'})

    img = generate_2d_image(house)
    save_image(img, "house_2d.png")