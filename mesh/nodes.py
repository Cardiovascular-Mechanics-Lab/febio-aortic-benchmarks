import numpy as np


# defining function that generates nodes
def generate_nodes(length, width, thickness, nx, ny, nz,symmetry):
    
    """
    Generates structured node coordinates for a rectangular 3D FEBio mesh based on user-defined geometry and mesh density. 
    
    Parameters:
    length (float): Length of the specimen in x direction
    width (float): Width of the specimen in y direction
    thickness (float): Thickness of the specimen in z direction
    nx (int): Number of nodes in x direction
    ny (int): Number of nodes in y direction
    nz (int): Number of nodes in z direction
    symmetry (str): Type of symmetry for the model, selected by user
    
    Returns:
    nodes (numpy array): Array where each row contains [node_id, x, y, z]

    """

# Assess user-selected symmetry, defines coordinate limits accordingly
#Full models are centred at origin, half and quarter models are cut along the symmetry planes in x and y 


    if symmetry == "full":
        #Centred at origin
        x_min, x_max = -length/2, length/2
        y_min, y_max = -width/2, width/2
        z_min, z_max = -thickness/2, thickness/2

    elif symmetry == "half":
        #cuts specimen along x=0 symmetry plane
        x_min, x_max = 0, length/2
        y_min, y_max = -width/2, width/2
        z_min, z_max = -thickness/2, thickness/2

    elif symmetry == "quarter":
        #Cuts specimen along x=0 and y=0 symmetry planes
        x_min, x_max = 0, length/2
        y_min, y_max = 0, width/2
        z_min, z_max = -thickness/2, thickness/2

    else:
        raise ValueError(
            "symmetry must be 'full', 'half', or 'quarter'"
    )


# Generate evenly spaced coordinates in each direction
# Arguments: (start, stop, number_of_points)
    x_vals = np.linspace(x_min, x_max, nx)
    y_vals = np.linspace(y_min, y_max, ny) 
    z_vals = np.linspace(z_min, z_max, nz) 

    #list for node data
    nodes = []

    node_id = 1


    # Node numbering progresses:
    # x direction first,
    # then y direction,
    # then z direction.

    for k, z in enumerate(z_vals):
        for j, y in enumerate(y_vals):
            for i, x in enumerate(x_vals):
                nodes.append((node_id, x, y, z))
                node_id += 1
    #returns list of nodes as an array
    
    return np.array(nodes)
