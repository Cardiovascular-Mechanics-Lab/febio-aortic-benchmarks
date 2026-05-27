import numpy as np


# defining function that generates nodes
def generate_nodes(length, width, thickness, nx, ny, nz):
    
    """
    Generates structured node coordinates for a rectangular 3D FEBio mesh based on user-defined geometry and mesh density. 
    
    Parameters:
    length (float): Length of the specimen in x direction
    width (float): Width of the specimen in y direction
    thickness (float): Thickness of the specimen in z direction
    nx (int): Number of nodes in x direction
    ny (int): Number of nodes in y direction
    nz (int): Number of nodes in z direction
    
    Returns:
    nodes (numpy array): Array where each row contains [node_id, x, y, z]

    """

# Generate evenly spaced coordinates in each direction
# Arguments: (start, stop, number_of_points)
    x_vals = np.linspace(0, length, nx)
    y_vals = np.linspace(0, width, ny) 
    z_vals = np.linspace(0, thickness, nz) 

    #list for node data
    nodes = []

    node_id = 1

    # Generate nodes, node numbering progresses first in x, then y, then z
    for k, z in enumerate(z_vals):
        for j, y in enumerate(y_vals):
            for i, x in enumerate(x_vals):
                nodes.append((node_id, x, y, z))
                node_id += 1
    #returns list of nodes as an array
    return np.array(nodes)

# Python convention for running this block only when the file is run directly (i.e. if this file is imported as a module, this block will not execute)
if __name__ == "__main__":

    length = 20
    width = 10 
    thickness = 1 

    nx = 21
    ny = 6 
    nz = 2

    nodes = generate_nodes(length, width, thickness, nx, ny, nz)

    print("Number of nodes:", len(nodes))
    print ("First 5 nodes:")
    print(nodes[:5])

    print("Last 5 nodes:")
    print(nodes[-5:])
