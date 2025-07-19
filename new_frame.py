import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Wall dimensions
wall_w, wall_h = 406.8, 268.6
spacing = 4.0  # max allowed space between frames

# Frame sizes (width, height) - UPDATED FOR A3 AND A4-3
frames = {
    "A3": (30.0, 40.0), # a - CHANGED from (29.7, 42.0)
    "A4-1": (21.0, 29.7), # b
    "A4-2": (21.0, 29.7), # c
    "200x150-1": (20.0, 15.0), # d
    "200x150-2": (20.0, 15.0), # e
    "200x150-3": (20.0, 15.0), # f: remains (20.0, 15.0)
    "127x178-1": (12.7, 17.8), # g: original dimensions, will be rotated visually
    "127x178-2": (12.7, 17.8), # h
    "A4-3": (20.0, 30.0), # i - CHANGED from (21.0, 29.7)
}

# Unique names for plotting labels
frame_display_names = {
    "A3": "a",
    "A4-1": "b",
    "A4-2": "c",
    "200x150-1": "d",
    "200x150-2": "e",
    "200x150-3": "f",
    "127x178-1": "g",
    "127x178-2": "h",
    "A4-3": "i",
}

# Center of the 'a' frame (shifted up by 2)
original_a3_w, original_a3_h = frames["A3"]

# For placement, swap 'a's width and height to align the short side vertically
a3_w_placed = original_a3_h # Will be 40.0
a3_h_placed = original_a3_w # Will be 30.0

a3_center_x = wall_w / 2
a3_center_y = wall_h / 2 + 2

# Calculate corners of the 'a' frame based on its PLACED dimensions
a3_left = a3_center_x - a3_w_placed / 2
a3_right = a3_center_x + a3_w_placed / 2
a3_top = a3_center_y + a3_h_placed / 2
a3_bottom = a3_center_y - a3_h_placed / 2

# Frame positions (center x, y) - build this dictionary carefully based on dependencies
positions = {
    "A3": (a3_center_x, a3_center_y), # a
    "A4-1": (a3_left - spacing - frames["A4-1"][0]/2, a3_center_y + frames["A4-1"][1]/2), # b
    "A4-2": (a3_right + spacing + frames["A4-2"][0]/2, a3_center_y - frames["A4-2"][1]/2), # c
}

# Frame 'd' (200x150-1): Left edge aligns with 'a's left edge
# Its vertical position remains 4 above 'a'
positions["200x150-1"] = (a3_left + frames["200x150-1"][0]/2, a3_top + spacing + frames["200x150-1"][1]/2) # d

# Frame 'h' (127x178-2): Right edge aligns with 'a's right edge
positions["127x178-2"] = (a3_right - frames["127x178-2"][0]/2, a3_top + spacing + frames["127x178-2"][1]/2) # h

# Frame 'f' (200x150-3): 4 above 'c', centers align horizontally (NO ROTATION for f)
# First, get 'c's current properties (A4-2)
c_cx, c_cy = positions["A4-2"]
c_w, c_h = frames["A4-2"]
c_top = c_cy + c_h / 2
# Now define 'f's position using original dimensions (20.0, 15.0)
positions["200x150-3"] = (c_cx, c_top + spacing + frames["200x150-3"][1]/2) # f

# Frame 'e' (200x150-2): 4 below 'b', centers align horizontally
# First, get 'b's current properties (A4-1)
b_cx, b_cy = positions["A4-1"]
b_w, b_h = frames["A4-1"]
b_bottom = b_cy - b_h / 2
# Now define 'e's position
positions["200x150-2"] = (b_cx, b_bottom - spacing - frames["200x150-2"][1]/2) # e

# Frame 'g' (127x178-1): Rotated (17.8 wide, 12.7 high), 4 cm above 'f', horizontally centered with 'f'
g_original_w, g_original_h = frames["127x178-1"] # (12.7, 17.8)
# Rotation for 'g': 17.8 cm aligned horizontally, so width is 17.8, height is 12.7
g_w_placed = g_original_h # 17.8
g_h_placed = g_original_w # 12.7

# Get 'f's current properties
f_cx, f_cy = positions["200x150-3"]
f_w, f_h = frames["200x150-3"] # Using f's original w,h as per assumption
f_top = f_cy + f_h / 2

# Now define 'g's position
positions["127x178-1"] = (f_cx, f_top + spacing + g_h_placed / 2) # g

# Frame 'i' (A4-3): Flipped to its side (now based on 20x30),
# horizontal center aligned with 'a', and 4 cm below 'a'
i_original_w, i_original_h = frames["A4-3"] # Now pulls (20.0, 30.0)
i_w_placed = i_original_h # 30.0 (long side horizontal)
i_h_placed = i_original_w # 20.0

positions["A4-3"] = (a3_center_x, a3_bottom - spacing - i_h_placed / 2) # i


# Plotting
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, wall_w)
ax.set_ylim(0, wall_h)
ax.set_aspect('equal')
ax.set_title("Adjusted Layout with New Frame Sizes and In-Frame Text") # Title updated for clarity

# Draw wall
wall = patches.Rectangle((0, 0), wall_w, wall_h, edgecolor='gray', facecolor='whitesmoke')
ax.add_patch(wall)

# Draw frames
for label, (w, h) in frames.items():
    cx, cy = positions[label]

    plot_w, plot_h = w, h
    # Apply special dimensions if frame is "placed" rotated
    if label == "A3": # 'a' - uses a3_w_placed, a3_h_placed
        plot_w, plot_h = a3_w_placed, a3_h_placed
    elif label == "127x178-1": # 'g' - ROTATED to (17.8, 12.7) for plotting
        plot_w, plot_h = g_original_h, g_original_w # (17.8, 12.7)
    elif label == "A4-3": # 'i' - ROTATED to (30.0, 20.0) for plotting
        plot_w, plot_h = i_original_h, i_original_w # (30.0, 20.0)

    rect = patches.Rectangle((cx - plot_w/2, cy - plot_h/2), plot_w, plot_h, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)

    display_name = frame_display_names.get(label, label)
    # Text is centered at (cx, cy). Reducing fontsize to help it fit small frames.
    ax.text(cx, cy, f"{display_name}\n{w:.1f}x{h:.1f}", ha='center', va='center', fontsize=6, fontweight='bold', color='black')

# Remove axes, save and open
ax.axis('off')
plt.tight_layout()
image_path = "adjusted_layout_new_sizes.png" # NOT CHANGING FILENAME THIS TIME
plt.savefig(image_path, dpi=150)
plt.close()
print(f"Layout saved to {image_path}")