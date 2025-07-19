import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Wall dimensions
wall_w, wall_h = 406.8, 268.6
spacing = 6.0  # Spacing between frames changed to 6.0 cm

# Frame sizes (width, height) - Specific dimensions as per your last working code
frames = {
    "A3": (30.0, 40.0),      # a
    "A4-1": (21.0, 29.7),    # b
    "A4-2": (21.0, 29.7),    # c
    "200x150-1": (20.0, 15.0), # d
    "200x150-2": (20.0, 15.0), # e
    "200x150-3": (20.0, 15.0), # f
    "127x178-1": (12.7, 17.8), # g
    "127x178-2": (12.7, 17.8), # h
    "A4-3": (20.0, 30.0),    # i
}

# Unique names for plotting labels
frame_display_names = {
    "A3": "a", "A4-1": "b", "A4-2": "c", "200x150-1": "d",
    "200x150-2": "e", "200x150-3": "f", "127x178-1": "g",
    "127x178-2": "h", "A4-3": "i",
}

# --- Frame Dimension Helper (to get placed dimensions based on "flip" logic) ---
def get_placed_dims(frame_label, original_dims):
    w_orig, h_orig = original_dims
    placed_w, placed_h = w_orig, h_orig

    if frame_label == "A3": # Placed vertically (short side vertical)
        placed_w, placed_h = h_orig, w_orig # 40x30
    elif frame_label in ["A4-3", "200x150-1", "200x150-2", "127x178-1", "127x178-2"]:
        # i, d, e, g, h are flipped horizontally (long side horizontal)
        placed_w, placed_h = h_orig, w_orig

    return placed_w, placed_h

# --- Layout Calculation ---
calculated_positions = {}
plotted_dims = {} # Store the (width, height) used for plotting each rectangle

# 1. Place 'a' (A3) in the center
a_w_placed, a_h_placed = get_placed_dims("A3", frames["A3"])
a_center_x = wall_w / 2
a_center_y = wall_h / 2
calculated_positions["A3"] = (a_center_x, a_center_y)
plotted_dims["A3"] = (a_w_placed, a_h_placed)

# Calculate 'a's boundaries for relative positioning
a_left = a_center_x - a_w_placed / 2
a_right = a_center_x + a_w_placed / 2
a_top = a_center_y + a_h_placed / 2
a_bottom = a_center_y - a_h_placed / 2

# 2. Place 'b' (A4-1) and 'c' (A4-2) aligned with 'a'
b_w, b_h = get_placed_dims("A4-1", frames["A4-1"])
c_w, c_h = get_placed_dims("A4-2", frames["A4-2"])

b_center_x = a_left - spacing - b_w / 2
b_center_y = a_center_y
calculated_positions["A4-1"] = (b_center_x, b_center_y)
plotted_dims["A4-1"] = (b_w, b_h)

c_center_x = a_right + spacing + c_w / 2
c_center_y = a_center_y
calculated_positions["A4-2"] = (c_center_x, c_center_y)
plotted_dims["A4-2"] = (c_w, c_h)

# Calculate b & c boundaries for relative positioning
b_left = b_center_x - b_w / 2
b_right = b_center_x + b_w / 2
b_top = b_center_y + b_h / 2
b_bottom = b_center_y - b_h / 2

c_left = c_center_x - c_w / 2
c_right = c_center_x + c_w / 2
c_top = c_center_y + c_h / 2
c_bottom = c_center_y - c_h / 2

# 3. Place 'i' (A4-3) on top of 'a', flipped
i_w_placed, i_h_placed = get_placed_dims("A4-3", frames["A4-3"])
i_center_x = a_center_x
i_center_y = a_top + spacing + i_h_placed / 2
calculated_positions["A4-3"] = (i_center_x, i_center_y)
plotted_dims["A4-3"] = (i_w_placed, i_h_placed)

# 4. Place 'd' (200x150-1) and 'e' (200x150-2), flipped
d_w_placed, d_h_placed = get_placed_dims("200x150-1", frames["200x150-1"])
e_w_placed, e_h_placed = get_placed_dims("200x150-2", frames["200x150-2"])

d_center_x = b_left - spacing - d_w_placed / 2
d_center_y = b_center_y
calculated_positions["200x150-1"] = (d_center_x, d_center_y)
plotted_dims["200x150-1"] = (d_w_placed, d_h_placed)

e_center_x = c_right + spacing + e_w_placed / 2
e_center_y = c_center_y
calculated_positions["200x150-2"] = (e_center_x, e_center_y)
plotted_dims["200x150-2"] = (e_w_placed, e_h_placed)

# Calculate d & e boundaries for relative positioning
d_left = d_center_x - d_w_placed / 2
d_right = d_center_x + d_w_placed / 2
d_top = d_center_y + d_h_placed / 2
d_bottom = d_center_y - d_h_placed / 2

e_left = e_center_x - e_w_placed / 2
e_right = e_center_x + e_w_placed / 2
e_top = e_center_y + e_h_placed / 2
e_bottom = e_center_y - e_h_placed / 2

# 5. Place 'f' (200x150-3) below 'a', not flipped
f_w, f_h = get_placed_dims("200x150-3", frames["200x150-3"])
f_center_x = a_center_x
f_center_y = a_bottom - spacing - f_h / 2
calculated_positions["200x150-3"] = (f_center_x, f_center_y)
plotted_dims["200x150-3"] = (f_w, f_h)

# 6. Place 'h' (127x178-2) and 'g' (127x178-1), flipped
h_w_placed, h_h_placed = get_placed_dims("127x178-2", frames["127x178-2"])
g_w_placed, g_h_placed = get_placed_dims("127x178-1", frames["127x178-1"])

h_center_x = d_left - spacing - h_w_placed / 2
h_center_y = d_center_y
calculated_positions["127x178-2"] = (h_center_x, h_center_y)
plotted_dims["127x178-2"] = (h_w_placed, h_h_placed)

g_center_x = e_right + spacing + g_w_placed / 2
g_center_y = e_center_y
calculated_positions["127x178-1"] = (g_center_x, g_center_y)
plotted_dims["127x178-1"] = (g_w_placed, g_h_placed)


# --- Plotting ---
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, wall_w)
ax.set_ylim(0, wall_h)
ax.set_aspect('equal')
ax.set_title("Frame Layout with Arrowed Guide Lines and Snake Plant")

# Draw wall
wall = patches.Rectangle((0, 0), wall_w, wall_h, edgecolor='gray', facecolor='whitesmoke')
ax.add_patch(wall)

# Draw frames
for label in frames.keys():
    cx, cy = calculated_positions[label]
    plot_w, plot_h = plotted_dims[label]

    rect = patches.Rectangle((cx - plot_w/2, cy - plot_h/2), plot_w, plot_h, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)

    display_name = frame_display_names.get(label, label)
    original_w, original_h = frames[label]
    ax.text(cx, cy, f"{display_name}\n{original_w:.1f}x{original_h:.1f}",
            ha='center', va='center', fontsize=6, fontweight='bold', color='black')

# --- Add Snake Plant Visualization ---
plant_height = 40.0
plant_width = 15.0
pot_height = 10.0
pot_width = 18.0
margin = 5.0

pot_x = margin
pot_y = margin
plant_x = pot_x + (pot_width - plant_width) / 2
plant_y = pot_y + pot_height

pot = patches.Rectangle((pot_x, pot_y), pot_width, pot_height, edgecolor='brown', facecolor='sienna', linewidth=1)
ax.add_patch(pot)
ax.text(pot_x + pot_width/2, pot_y + pot_height/2, "Pot", ha='center', va='center', fontsize=6, color='white')

snake_plant = patches.Rectangle((plant_x, plant_y), plant_width, plant_height, edgecolor='darkgreen', facecolor='olivedrab', linewidth=1)
ax.add_patch(snake_plant)
ax.text(plant_x + plant_width/2, plant_y + plant_height/2, "Snake Plant", ha='center', va='center', fontsize=6, color='white')

# --- Add Guide Lines ---
# Diagonal lines (red, dotted, faded)
ax.plot([0, wall_w], [0, wall_h], 'r:', alpha=0.3, linewidth=0.8) # Bottom-left to top-right
ax.plot([0, wall_w], [wall_h, 0], 'r:', alpha=0.3, linewidth=0.8) # Top-left to bottom-right

# Central vertical line (black, dotted, faded)
ax.axvline(x=wall_w / 2, color='k', linestyle=':', alpha=0.3, linewidth=0.8)

# Top horizontal line (black, dotted, faded) - this acts as a reference for measurements
ax.axhline(y=wall_h, color='k', linestyle=':', alpha=0.3, linewidth=0.8)


# --- Add Vertical Guide Lines from Top to Frames with Measurements ---
# Iterate through each frame to draw its guide line and measurement
for label in frames.keys():
    cx, cy = calculated_positions[label] # Center of the frame
    plot_w, plot_h = plotted_dims[label] # Actual plotted dimensions

    # Calculate the top-center point of the frame
    frame_top_center_x = cx
    frame_top_center_y = cy + plot_h / 2

    # Draw the dotted line from the top of the wall to the frame's top-center
    # Using ax.annotate for lines with arrows - FIX: Added text=''
    ax.annotate(text='', xy=(frame_top_center_x, frame_top_center_y),
                xytext=(frame_top_center_x, wall_h),
                arrowprops=dict(arrowstyle='->', color='blue', linestyle=':', alpha=0.6, linewidth=0.7))

    # Calculate the measurement (distance from top of wall to top of frame)
    measurement_cm = wall_h - frame_top_center_y

    # Place the measurement text
    # Position the text slightly above the frame's top edge, horizontally centered
    text_y_position = frame_top_center_y + 1.5 # Offset slightly above the frame
    ax.text(frame_top_center_x, text_y_position, f"{measurement_cm:.1f} cm",
            ha='center', va='bottom', fontsize=6, color='blue', fontweight='bold')


# Remove axes, save and open
ax.axis('off')
plt.tight_layout()
image_path = "adjusted_layout_new_sizes.png" # NOT CHANGING FILENAME
plt.savefig(image_path, dpi=150)
plt.close()
print(f"Layout saved to {image_path}")