import numpy as np


def generate_boundary_sets(nodes, symmetry, tolerance=1e-8):

    """
    Generates node groups for specimen faces and edges
    based on nodal coordinates.

    Parameters:
    nodes (numpy array):Array containing [node_id, x, y, z]
    symmetry (str): Type of symmetry for the model ("full", "half", "quarter")
    tolerance (float): Numerical tolerance used when comparing coordinates

    Returns:
    BC_groups (dict):Dictionary containing node sets for faces and edges
        used in FEBio boundary conditions
    """
    
    # Extract node IDs and coordinate arrays 
    node_ids = nodes[:, 0].astype(int)

    x = nodes[:, 1]
    y = nodes[:, 2]
    z = nodes[:, 3]

    #Stores minimum and maximum coordinates in each direction (geometric limits)
    x_min = np.min(x)
    x_max = np.max(x)

    y_min = np.min(y)
    y_max = np.max(y)

    z_min = np.min(z)
    z_max = np.max(z)

    # Face node groups, used for loading and boundary conditions

    left_face = node_ids[np.isclose(x, x_min, atol=tolerance)]

    right_face = node_ids[np.isclose(x, x_max, atol=tolerance)]

    front_face = node_ids[np.isclose(y, y_min, atol=tolerance)]

    back_face = node_ids[np.isclose(y, y_max, atol=tolerance)]

    bottom_face = node_ids[np.isclose(z, z_min, atol=tolerance)]

    top_face = node_ids[np.isclose(z, z_max, atol=tolerance)]

#Rigid Body Motion Prevention 
    #Prevents translation while allowing deformation

    #Identifying single node for anchor point to prevent rigid body motion in z 
    z_anchor_point = node_ids[
        np.isclose(x, x_min, atol=tolerance) &
        np.isclose(y, y_min, atol=tolerance) &
        np.isclose(z, z_min, atol=tolerance)]
    
    #Identifying y-coordinate closest to the centre of the specimen
    y_mid = y[np.argmin(np.abs(y - 0.0))]  

    #Identifies a line of nodes to prevent rigid body motion in y while allowing deformation
    # Used instead of fixing an entire face which restricted contraction during uniaxial loading
    y_anchor_line = node_ids[
        np.isclose(x, x_min, atol=tolerance) &
        np.isclose(y, y_mid, atol=tolerance)]

     # Store node groups in dictionary for FEBio NodeSet generation
    BC_groups = {

        "left_face": left_face,
        "right_face": right_face,

        "front_face": front_face,
        "back_face": back_face,

        "bottom_face": bottom_face,
        "top_face": top_face,

    }

    BC_groups["y_anchor"] = y_anchor_line
    BC_groups["z_anchor"] = z_anchor_point

    #Symmetry planes, identifying and storing node groups for boundary conditions for the different symmetry cases 
    if symmetry in ["half", "quarter"]:
        BC_groups["symmetry_x"] = left_face # x = 0 plane for these symmetry options 

    if symmetry == "quarter":
        BC_groups["symmetry_y"] = front_face # y = 0 plane


    return BC_groups