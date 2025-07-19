import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Wall dimensions
wall_w, wall_h = 87.4, 267.5

# Frame sizes (width, height) - specific dimensions
frames_original_dims = {
    "small_frame": (13.0, 18.0),   # 13x18 cm
    "medium_frame": (21.0, 29.7), # 21x29.7 cm
    "large_frame": (30.0, 40.0),   # 30x40 cm
}

# Unique names for plotting labels
frame_display_names = {
    "small_frame": "13x18",
    "medium_frame": "21x29.7",
    "large_frame": "30x40",
}

# --- Frame Dimension Helper (ensuring long side is height) ---
def get_placed_dims_long_side_as_height(original_dims):
    w_orig, h_orig = original_dims
    if w_orig > h_orig: # If width is greater than height, swap them for vertical placement
        return h_orig, w_orig
    return w_orig, h_orig # Otherwise, keep as is

# Calculate placed dimensions for all frames
frames_placed_dims = {}
for label, dims in frames_original_dims.items():
    frames_placed_dims[label] = get_placed_dims_long_side_as_height(dims)

# Get widths and heights for calculation
w_small, h_small = frames_placed_dims["small_frame"]
w_medium, h_medium = frames_placed_dims["medium_frame"]
w_large, h_large = frames_placed_dims["large_frame"]

# --- Fixed Spacing ---
fixed_spacing = 4.5 # Specified as 4.5 cm

# --- Layout Calculation ---
calculated_positions = {}
plotted_dims = {}

# Total width occupied by frames
total_frames_width = w_small + w_medium + w_large

# Total width occupied by the fixed gaps (2 internal gaps)
total_gap_width = 2 * fixed_spacing

# Remaining width for the two margins
remaining_width_for_margins = wall_w - total_frames_width - total_gap_width

# Each margin is half of the remaining width
left_right_margin = remaining_width_for_margins / 2

if left_right_margin < 0:
    print("Warning: Frames and specified spacing are too wide for the wall. Adjusting margins to 0.")
    left_right_margin = 0 # Prevent negative margins


# --- Vertical Alignment Logic ---
# 1. Smallest frame's horizontal axis (center) aligns with wall's horizontal axis
small_frame_center_y = wall_h / 2
small_frame_bottom_y = small_frame_center_y - h_small / 2

# This bottom_y will be the reference for other frames' bottom edges
common_bottom_edge_y = small_frame_bottom_y

# --- Calculate positions horizontally based on fixed spacing and margins ---
# Small Frame (Horizontally Centered, Vertically centered on wall)
current_x = left_right_margin + w_small / 2
calculated_positions["small_frame"] = (current_x, small_frame_center_y)
plotted_dims["small_frame"] = frames_placed_dims["small_frame"]

# Medium Frame (Left of Small, bottom aligned with Small)
current_x_medium = current_x + w_small / 2 + fixed_spacing + w_medium / 2
calculated_positions["medium_frame"] = (current_x_medium, common_bottom_edge_y + h_medium / 2)
plotted_dims["medium_frame"] = frames_placed_dims["medium_frame"]

# Large Frame (Right of Medium, bottom aligned with Small)
# Note: The prompt asks for "rest align the bottom edge".
# Assuming "rest" means the remaining frames (medium and large).
# Let's place large to the right of medium.
current_x_large = current_x_medium + w_medium / 2 + fixed_spacing + w_large / 2
calculated_positions["large_frame"] = (current_x_large, common_bottom_edge_y + h_large / 2)
plotted_dims["large_frame"] = frames_placed_dims["large_frame"]


# --- Plotting ---
fig, ax = plt.subplots(figsize=(8, 12)) # Adjusted figsize for tall wall
ax.set_xlim(0, wall_w)
ax.set_ylim(0, wall_h)
ax.set_aspect('equal')
ax.set_title("Smallest Frame Centered, Others Aligned to its Bottom Edge")

# Draw wall
wall = patches.Rectangle((0, 0), wall_w, wall_h, edgecolor='gray', facecolor='whitesmoke')
ax.add_patch(wall)

# Draw frames
for label in frames_original_dims.keys(): # Iterate over original keys for consistency
    cx, cy = calculated_positions[label]
    plot_w, plot_h = plotted_dims[label] # Use the calculated plotted dimensions

    rect = patches.Rectangle((cx - plot_w/2, cy - plot_h/2), plot_w, plot_h, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)

    display_name = frame_display_names.get(label, label)
    original_w, original_h = frames_original_dims[label] # Show original dimensions in text
    ax.text(cx, cy, f"{display_name}\n({original_w:.1f}x{original_h:.1f})",
            ha='center', va='center', fontsize=7, fontweight='bold', color='black')

# --- Add Guide Lines ---
# Diagonal lines (red, dotted, faded)
ax.plot([0, wall_w], [0, wall_h], 'r:', alpha=0.3, linewidth=0.8) # Bottom-left to top-right
ax.plot([0, wall_w], [wall_h, 0], 'r:', alpha=0.3, linewidth=0.8) # Top-left to bottom-right

# Central vertical line (black, dotted, faded)
ax.axvline(x=wall_w / 2, color='k', linestyle=':', alpha=0.3, linewidth=0.8)

# Central horizontal line (black, dotted, faded) - this is the small frame's center alignment
ax.axhline(y=wall_h / 2, color='darkgray', linestyle='--', alpha=0.6, linewidth=1.0) # Highlight this line
ax.text(wall_w / 2, wall_h / 2 - 2, "Wall Midline (Small Frame's Centerline)", ha='center', va='top', fontsize=6, color='darkgray')

# Top horizontal line (black, dotted, faded) - reference for top measurements
ax.axhline(y=wall_h, color='k', linestyle=':', alpha=0.3, linewidth=0.8)

# Bottom horizontal line (black, dotted, faded) - reference for bottom measurements
ax.axhline(y=0, color='k', linestyle=':', alpha=0.3, linewidth=0.8)


# --- Add Vertical Guide Lines from Top/Bottom to Frames with Measurements ---
# Iterate through each frame
for label in frames_original_dims.keys():
    cx, cy = calculated_positions[label] # Center of the frame
    plot_w, plot_h = plotted_dims[label] # Actual plotted dimensions

    # --- Top Measurement ---
    frame_top_center_x = cx
    frame_top_center_y = cy + plot_h / 2
    measurement_from_top_cm = wall_h - frame_top_center_y

    # Draw dotted line from top of wall to frame top-center
    ax.annotate(text='', xy=(frame_top_center_x, frame_top_center_y),
                xytext=(frame_top_center_x, wall_h),
                arrowprops=dict(arrowstyle='->', color='blue', linestyle=':', alpha=0.6, linewidth=0.7))

    # Place measurement text for top
    text_y_position_top = frame_top_center_y + 1.5
    ax.text(frame_top_center_x, text_y_position_top, f"{measurement_from_top_cm:.1f} cm (T)",
            ha='center', va='bottom', fontsize=6, color='blue', fontweight='bold')

    # --- Bottom Measurement ---
    frame_bottom_center_x = cx
    frame_bottom_center_y = cy - plot_h / 2
    measurement_from_bottom_cm = frame_bottom_center_y # This is simply the y-coordinate of the bottom edge

    # Draw dotted line from bottom of wall to frame bottom-center
    ax.annotate(text='', xy=(frame_bottom_center_x, frame_bottom_center_y),
                xytext=(frame_bottom_center_x, 0), # Start from y=0 (bottom of wall)
                arrowprops=dict(arrowstyle='->', color='green', linestyle=':', alpha=0.6, linewidth=0.7))

    # Place measurement text for bottom
    text_y_position_bottom = frame_bottom_center_y - 1.5 # Offset slightly below the frame
    ax.text(frame_bottom_center_x, text_y_position_bottom, f"{measurement_from_bottom_cm:.1f} cm (B)",
            ha='center', va='top', fontsize=6, color='green', fontweight='bold')


# Remove axes, save and open
ax.axis('off')
plt.tight_layout()
image_path = "adjusted_layout_bed_sizes.png"
plt.savefig(image_path, dpi=150)
plt.close()
print(f"Layout saved to {image_path}")
print(f"Fixed Spacing Between Frames: {fixed_spacing:.1f} cm")
print(f"Calculated Left/Right Margin: {left_right_margin:.2f} cm")