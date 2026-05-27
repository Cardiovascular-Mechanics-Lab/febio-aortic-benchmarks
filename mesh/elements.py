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