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

from itertools import product


def _allocate_thickness_rows(layer_fractions, total_rows):
    """
    Convert layer fractions into positive integer element-row counts.

    The returned counts:
        - sum to total_rows;
        - assign at least one row to every layer;
        - minimize the squared difference between the requested and
          represented layer fractions.
    """

    num_layers = len(layer_fractions)

    if total_rows < num_layers:
        raise ValueError(
            "The mesh does not contain enough through-thickness element "
            "rows to assign at least one row to every layer. "
            "Increase nodes_z."
        )

    best_counts = None
    best_error = float("inf")

    # Each count must be at least 1. The final count is calculated
    # from the remaining rows so that the total always matches.
    for leading_counts in product(
        range(1, total_rows + 1),
        repeat=num_layers - 1,
    ):
        final_count = total_rows - sum(leading_counts)

        if final_count < 1:
            continue

        counts = list(leading_counts) + [final_count]

        error = sum(
            ((count / total_rows) - fraction) ** 2
            for count, fraction in zip(counts, layer_fractions)
        )

        if error < best_error:
            best_error = error
            best_counts = counts

    if best_counts is None:
        raise ValueError(
            "A valid through-thickness layer allocation could not be found."
        )

    return best_counts


def split_elements_by_thickness(elements, nx, ny, nz, layers):
    """
    Assign elements to anatomical layers according to their position
    through the specimen thickness.

    The thickness direction is z.

    Parameters
    ----------
    elements:
        Array containing
        [element_id, n1, n2, n3, n4, n5, n6, n7, n8].

    nx, ny, nz:
        Numbers of nodes in the x, y, and z directions.

    layers:
        List of assembled layer dictionaries. Each layer must contain:
            - "name"
            - "fraction"

        Material parameters may also be present but are not used by
        this function.

    Returns
    -------
    list
        One element group per anatomical layer, in the same order as
        the input layer list.
    """

    elements_per_thickness_row = (nx - 1) * (ny - 1)
    total_thickness_rows = nz - 1

    layer_fractions = [
        layer["fraction"]
        for layer in layers
    ]

    layer_counts = _allocate_thickness_rows(
        layer_fractions,
        total_thickness_rows,
    )

    # Convert row counts into cumulative boundaries.
    #
    # Example:
    #     counts = [3, 1]
    #     boundaries = [3, 4]
    layer_boundaries = []
    running_total = 0

    for count in layer_counts:
        running_total += count
        layer_boundaries.append(running_total)

    layer_element_groups = [
        []
        for _ in layers
    ]

    for element in elements:
        element_id = int(element[0])
        element_index = element_id - 1

        thickness_row = (
            element_index
            // elements_per_thickness_row
        )

        for layer_index, boundary in enumerate(layer_boundaries):
            if thickness_row < boundary:
                layer_element_groups[layer_index].append(element)
                break

    return layer_element_groups