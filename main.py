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


# Merge adjacent voxels for simplification
def merge_voxels(voxel_shapes):
    merged_shapes = []

    # Sort by from and to coordinates for consistent merging
    voxel_shapes.sort()

    for voxel in voxel_shapes:
        # Check if there is a mergeable voxel already
        merged = False
        for i in range(len(merged_shapes)):
            existing = merged_shapes[i]
            # Simple check for merge condition (you can enhance this)
            if voxel[0][1:] == existing[0][1:] and voxel[1][1:] == existing[1][1:]:
                # Merge in x-direction if they are adjacent
                if voxel[0][0] == existing[1][0] or voxel[1][0] == existing[0][0]:
                    merged_shapes[i] = (
                        [min(voxel[0][0], existing[0][0])] + voxel[0][1:],
                        [max(voxel[1][0], existing[1][0])] + voxel[1][1:]
                    )
                    merged = True
                    break

        if not merged:
            merged_shapes.append(voxel)

    return merged_shapes


# Generate the Java code for VoxelShapes
def generate_voxel_shape_code(merged_shapes):
    # Create individual box statements for each voxel shape
    shape_definitions = [
        f"box({from_coord[0]}, {from_coord[1]}, {from_coord[2]}, {to_coord[0]}, {to_coord[1]}, {to_coord[2]})"
        for from_coord, to_coord in merged_shapes
    ]

    # Join the boxes with Shapes.or to create a complete VoxelShape
    shape_code = "Shapes.or(\n    " + ",\n    ".join(shape_definitions) + "\n);"

    # Add Java code to wrap it in a variable definition
    java_code = f"VoxelShape SHAPE = {shape_code}"

    return java_code


# Main function to parse, merge, and generate the code
def main():
    voxel_shapes = parse_voxel_shape('model.json')
    merged_voxel_shapes = merge_voxels(voxel_shapes)
    java_code = generate_voxel_shape_code(merged_voxel_shapes)

    print("// Generated Minecraft VoxelShape Code")
    print(java_code)


if __name__ == "__main__":
    main()