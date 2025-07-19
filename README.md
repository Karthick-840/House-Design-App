# House Design App

A Python toolkit for modeling walls and designing houses, with 2D image generation for visualizing layouts.

## Features

- Define walls and rooms using Python classes
- Generate 2D PNG images of house layouts
- Easily extendable for future 3D design features

## Requirements

- Python 3.x
- Pillow

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage

1. Edit or run `src/design/image2d.py` to define your house layout.
2. The script will generate a PNG image (`house_2d.png`) showing the walls and rooms.

Example:
```sh
python src/design/image2d.py
```

## Project Structure

```
src/design/house.py      # Wall and House classes
src/design/image2d.py    # 2D image generation
```

## Author

Karthick Jayaraman