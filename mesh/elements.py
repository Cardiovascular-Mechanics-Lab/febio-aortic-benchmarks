import numpy as np


def generate_elements(nx, ny, nz):
    
    
    """
    Generates Hex8 element connectivity for a structured mesh.

    Parameters:
    nx (int): Number of nodes in x direction
    ny (int): Number of nodes in y direction
    nz (int): Number of nodes in z direction

    Returns:
    elements (numpy array): Array containing [element_id, n1, n2, n3, n4, n5, n6, n7, n8]
    """

    #list for element data, elements in each direction are n -1, where n is number of nodes
    elements = []

    #initializing element ID counter
    element_id = 1

    # Generate elements in structured x-y-z order
    for k in range(nz - 1):
        for j in range(ny - 1):
            for i in range(nx - 1):
                # Convert structured (i,j,k) grid position into global node IDs for the Hex8 element corners
                n1 = i + j * nx + k * nx * ny + 1
                n2 = n1 + 1
                n3 = n1 + nx
                n4 = n3 + 1
                n5 = n1 + nx * ny
                n6 = n5 + 1
                n7 = n5 + nx
                n8 = n7 + 1
                # Node ordering follows FEBio Hex8 convention to ensure correct element orientation
                elements.append((element_id, n1, n2, n4, n3, n5, n6, n8, n7))
                element_id += 1
    #returns list of elements as an array
    return np.array(elements, dtype=int)

def split_elements_by_thickness(elements, nx, ny, nz, layers):
    """
    Assigns elements to tissue layers based on their position through the specimen thickness.

    The thickness is in z-direction.

    elements: array containing [element_id, n1, n2, n3, n4, n5, n6, n7, n8]
    nx, ny, nz: number of nodes in each direction
    layers: list of dictionaries, each with:
        "name"
        "fraction"
        "E"
        "v"

    Returns:
        layer_element_groups: list where each entry contains the elements
        assigned to the corresponding layer.
        Example for 3 layers:
        [
            intima elements,
            media elements,
            adventitia elements
        ]
    """

    #Number of elements per layer in thickness direction
    elements_per_thickness_layer = (nx - 1) * (ny - 1)

    #Elements through thickness direction
    total_thickness_elements = nz - 1

    # Convert user-defined layer fractions into number of element layers
    # rounds to nearest integer, and adjusts last layer to ensure total matches nz-1
    layer_counts = [
        round(layer["fraction"] * total_thickness_elements)
        for layer in layers
    ]

    # Making sure rounding does not lose/add layers
    difference = total_thickness_elements - sum(layer_counts)
    layer_counts[-1] += difference

    #Converts layer counts into cumulative boundaries
    # Example: number of elements per layer ([7, 2, 1]) becomes elements at boundaries ([7, 9, 10])
    layer_boundaries = []
    running_total = 0

    for count in layer_counts:
        running_total += count
        layer_boundaries.append(running_total)

    #element group per selected tissue layers
    layer_element_groups = [[] for _ in layers]

    #assigns elements to correct layer group based on their position in the thickness direction
    for element in elements:
        element_id = int(element[0])
        element_index = element_id - 1

        thickness_layer = element_index // elements_per_thickness_layer

        for layer_index, boundary in enumerate(layer_boundaries):
            if thickness_layer < boundary:
                layer_element_groups[layer_index].append(element)
                break

    return layer_element_groups