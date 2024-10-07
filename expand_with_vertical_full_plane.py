import json


# Parse the voxel shape JSON file
def parse_voxel_shape(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    voxel_shapes = []

    # Check if 'elements' exists in the JSON
    if 'elements' in data:
        elements = data['elements']
        for element in elements:
            from_coord = element['from']
            to_coord = element['to']
            voxel_shapes.append((from_coord, to_coord))

    return voxel_shapes


# Calculate the outer bounding box for all voxel shapes, and expand vertical plane to one block
def calculate_outer_bounding_box(voxel_shapes):
    # Initialize min and max coordinates with extreme values
    min_coord = [float('inf')] * 3
    max_coord = [float('-inf')] * 3

    for from_coord, to_coord in voxel_shapes:
        # Update min coordinates
        min_coord = [min(min_coord[i], from_coord[i]) for i in range(3)]
        # Update max coordinates
        max_coord = [max(max_coord[i], to_coord[i]) for i in range(3)]

    # Expand y dimension to 16 units (1 block height)
    min_coord[1] = 0  # Set y-min to 0
    max_coord[1] = 16  # Set y-max to 16

    # Ensure either x or z dimension is fully expanded to 16 units
    x_width = max_coord[0] - min_coord[0]
    z_width = max_coord[2] - min_coord[2]

    # Expand the dimension with larger width (x or z) to 16 units
    if x_width >= z_width:
        min_coord[0] = 0
        max_coord[0] = 16
    else:
        min_coord[2] = 0
        max_coord[2] = 16

    return min_coord, max_coord


# Generate the Java code for the outer bounding box
def generate_bounding_box_code(min_coord, max_coord):
    # Create a single box statement for the bounding box
    shape_definition = f"box({min_coord[0]}, {min_coord[1]}, {min_coord[2]}, {max_coord[0]}, {max_coord[1]}, {max_coord[2]})"

    # Wrap the statement in a VoxelShape definition
    java_code = f"VoxelShape SHAPE = Shapes.or(\n    {shape_definition}\n);"

    return java_code


# Main function to parse and generate the bounding box code
def main():
    # Path to the JSON file containing voxel shapes
    json_file = 'model.json'

    voxel_shapes = parse_voxel_shape(json_file)
    min_coord, max_coord = calculate_outer_bounding_box(voxel_shapes)
    java_code = generate_bounding_box_code(min_coord, max_coord)

    print("// Generated Minecraft VoxelShape Code for Bounding Box")
    print(java_code)


if __name__ == "__main__":
    main()
