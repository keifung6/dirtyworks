import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

# ================= Configuration Parameters =================
base_dir = r"D:\photos4yy"
frame_range = range(31, 39)
rect_numbers = [1, 2, 3]
output_dir = r"D:\photos4yy\output"

# ============== Visualization Parameters ================
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 18,
    "font.weight": "bold"  # Global font bold
})

# ================= Core Logic =================
os.makedirs(output_dir, exist_ok=True)

for rect_num in rect_numbers:
    image_paths = [
        os.path.join(base_dir, f"frame{fn}", f"rect_{rect_num}.png")
        for fn in frame_range
    ]
    
    # Create canvas and main plot
    fig = plt.figure(figsize=(24, 12))
    main_axes = [plt.subplot(2, 4, i+1) for i in range(8)]
    
    # Set uniform subplot spacing
    plt.subplots_adjust(
        wspace=0.1,
        hspace=0.1,
        left=0.05,
        right=0.95,
        bottom=0.05,
        top=0.95
    )
    
    # Load all subplots
    for ax, img_path in zip(main_axes, image_paths):
        try:
            img = Image.open(img_path)
            ax.imshow(img, aspect='auto', origin='upper')
        except Exception as e:
            print(f"Loading failed: {img_path} | Error: {str(e)}")
            img = np.zeros((300, 300, 3))
        
        ax.axis('off')
        ax.set_xlim(0, 300)
        ax.set_ylim(300, 0)  # Maintain image coordinate system
    
    # ==== Precisely aligned coordinate system ====
    ax_main = main_axes[0]  # Target subplot
    
    # Get absolute coordinate position of subplot 1
    pos = ax_main.get_position()
    
    # Create perfectly aligned axes
    ax_coord = fig.add_axes([
        pos.x0,         # Left boundary alignment
        pos.y0,         # Bottom boundary alignment
        pos.width,      # Same width
        pos.height      # Same height
    ])
    
    # ==== Key modification: Hide all axis lines ====
    for spine in ax_coord.spines.values():
        spine.set_visible(False)
    
    # ==== Axis configuration ====
    ax_coord.set_xlim(0, 300)
    ax_coord.set_ylim(0, 300)
    ax_coord.set_xticks([0, 100, 200, 300])
    ax_coord.set_yticks([100, 200, 300])
    
    # Configure tick parameters (hide tick lines, show only labels)
    ax_coord.tick_params(
        axis='both',
        which='both',
        length=0,            # Completely hide tick lines
        width=0,
        labelsize=28,
        pad=5,               # Adjust distance between labels and boundaries
        labelrotation=0,
        labelcolor='black'
    )
    
    # ==== Key modification: Rotate Y-axis labels 90 degrees ====
    for label in ax_coord.get_yticklabels():
        label.set_rotation(270)  # Rotate 90 degrees counterclockwise
        label.set_verticalalignment('center')  # Vertical center alignment
        label.set_horizontalalignment('center')  # Horizontal center alignment
    
    # ==== Fine-tuning label positions ====
    # X-axis labels displayed at the bottom
    ax_coord.xaxis.set_ticks_position('bottom')
    ax_coord.xaxis.set_label_position('bottom')
    
    # Y-axis labels displayed on the left
    ax_coord.yaxis.set_ticks_position('left')
    ax_coord.yaxis.set_label_position('left')
    
    # Force labels to stick to boundaries
    ax_coord.tick_params(axis='x', pad=5)  # Move X-axis labels up by 5 points
    ax_coord.tick_params(axis='y', pad=25)  # Move Y-axis labels right by 25 points
    
    # ==== Key modification: Bold font ====
    for label in ax_coord.get_xticklabels() + ax_coord.get_yticklabels():
        label.set_fontname('Times New Roman')
        label.set_weight('bold')  # Bold font
    
    # Hide axis layer
    ax_coord.set_frame_on(False)
    ax_coord.patch.set_alpha(0)
    
    # Save results
    output_path = os.path.join(output_dir, f"rect{rect_num}_rotated_labels.jpg")
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.1,
        facecolor='white'
    )
    plt.close()

print("Processing complete! Output directory:", output_dir)