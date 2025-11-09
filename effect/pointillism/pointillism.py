# effect/quantum_pointillism/quantum_pointillism.py
import numpy as np
import importlib.util
import os

# --- Import QuantumBrush utilities ---
# This is how QuantumBrush modules are typically loaded dynamically
utils_spec = importlib.util.spec_from_file_location("utils", os.path.join(os.path.dirname(os.path.dirname(__file__)), "effect", "utils.py"))
utils = importlib.util.module_from_spec(utils_spec)
utils_spec.loader.exec_module(utils)

# Optional: Import our helper functions if you create them in separate files later
# sampling_spec = importlib.util.spec_from_file_location("utils_sampling", os.path.join(os.path.dirname(__file__), "utils_sampling.py"))
# utils_sampling = importlib.util.module_from_spec(sampling_spec)
# sampling_spec.loader.exec_module(utils_sampling)

def run(params):
    """
    Main run function for the Quantum Pointillism brush.
    Currently implements classical Poisson disk sampling for pointillism.
    The quantum Ising model logic will replace the color generation part later.
    """
    print("Quantum Pointillism brush started.")

    # --- 1. Extract Parameters and Inputs ---
    image = params["stroke_input"]["image_rgba"].copy().astype(np.float64) # Work with float for calculations
    path = params["stroke_input"]["path"] # Shape: (N, 2) where each row is [y, x]
    user_inputs = params["user_input"]

    dot_count = user_inputs["Dot Count"]
    target_color_hex = user_inputs["Target Color"] # e.g., "#FF5733"
    coupling_strength = user_inputs["Coupling Strength"]
    evolution_time = user_inputs["Evolution Time"]
    dot_size = user_inputs["Dot Size"]

    # Convert hex color to RGB array [0-255]
    # QuantumBrush's apply_effect.py usually handles this conversion for 'color' type,
    # so target_color should already be a numpy array like [R, G, B] (e.g., [255, 87, 51])
    target_color_rgb = target_color_hex # Already converted by apply_effect.py
    print(f"Target Color RGB: {target_color_rgb}")

    height, width = image.shape[:2]
    radius = 30  # Define a region around the stroke path for dot placement

    # --- 2. Get Stroke Region and Sample Dot Positions ---
    print("Sampling dot positions using Poisson disk...")
    region = utils.points_within_radius(path, radius, border=(height, width))
    if len(region) == 0:
        print("Warning: No region found under stroke. Returning original image.")
        return image.astype(np.uint8)

    # --- Classical Poisson Disk Sampling (Stub) ---
    # Replace this section with quantum logic later
    dot_positions = poisson_disk_sample_stub(region, dot_count, min_dist=2*dot_size)

    if len(dot_positions) == 0:
        print("Warning: No dots sampled. Returning original image.")
        return image.astype(np.uint8)

    print(f"Sampled {len(dot_positions)} dot positions.")

    # --- 3. Generate Colors (Currently Classical, Placeholder for Quantum) ---
    # For now, use the target color or a simple variation based on position/initial color.
    # This is where the quantum circuit will eventually determine the color for each dot.
    colors = []
    for y, x in dot_positions:
        # Get original color at this pixel
        original_color = image[y, x, :3] # RGB part

        # --- STUB: Classical Color Logic ---
        # Example: Blend original color with target color based on some rule
        # This should be replaced by quantum state evolution and measurement
        alpha_blend = 0.5
        new_color = (1 - alpha_blend) * original_color + alpha_blend * target_color_rgb
        colors.append(np.clip(new_color, 0, 255))

        # --- FUTURE: Quantum Color Logic ---
        # 1. Encode original_color (or a property of it) into a quantum state |psi_i>
        # 2. Build Ising Hamiltonian H based on dot_positions and coupling_strength
        # 3. Evolve state: |psi_i(t)> = exp(-iHt) |psi_i>
        # 4. Measure state to get new color properties (e.g., expectation values <X>, <Y>, <Z>)
        # 5. Decode measurement back to RGB
        # colors.append(decoded_quantum_color)

    colors = np.array(colors).astype(np.uint8) # Convert back to uint8 for image

    # --- 4. Draw Dots ---
    print("Drawing dots...")
    for i, (y, x) in enumerate(dot_positions):
        color = colors[i]
        draw_circle(image, (y, x), dot_size, color)

    print("Quantum Pointillism brush finished.")
    return image.astype(np.uint8) # Ensure output is uint8


# --- Helper Functions ---

def poisson_disk_sample_stub(points, n_samples, min_dist=5.0, seed=None):
    """
    STUB: Classical Poisson disk sampling using a simple random approach.
    This should be replaced with a more robust algorithm like Bridson's algorithm
    or the one provided earlier if you put it in a separate file.
    For now, it just randomly selects points ensuring a minimum distance.
    """
    if seed is not None:
        np.random.seed(seed)

    if len(points) <= n_samples:
        return points

    indices = np.random.choice(len(points), size=min(n_samples * 3, len(points)), replace=False)
    candidates = points[indices]

    selected = []
    for pt in candidates:
        if not selected:
            selected.append(pt)
        else:
            # Calculate distances to all currently selected points
            dists = np.linalg.norm(selected - pt, axis=1)
            if np.all(dists >= min_dist):
                selected.append(pt)
                if len(selected) >= n_samples:
                    break

    return np.array(selected)


def draw_circle(image, center, radius, color):
    """
    Draws a filled circle on the image.
    """
    y, x = center
    height, width = image.shape[:2]

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dy*dy + dx*dx <= radius*radius:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    image[ny, nx, :3] = color # Set RGB
                    image[ny, nx, 3] = 255 # Set Alpha to fully opaque


# --- Optional: For standalone testing (uncomment if needed) ---
# if __name__ == "__main__":
#     # Example of how you might test the run function independently
#     # This is just a conceptual example, as the full params dict is complex to mock.
#     # You would typically test by running the full QuantumBrush app.
#     test_params = {
#         "stroke_input": {
#             "image_rgba": np.random.randint(0, 255, (100, 100, 4), dtype=np.uint8),
#             "path": np.array([[50, 50], [55, 55], [60, 60]]) # Example path
#         },
#         "user_input": {
#             "Dot Count": 20,
#             "Coupling Strength": 0.5,
#             "Evolution Time": 1.0,
#             "Target Color": np.array([255, 0, 0]), # Red
#             "Dot Size": 2
#         }
#     }
#     result_image = run(test_params)
#     print("Standalone test run completed. Shape:", result_image.shape)
