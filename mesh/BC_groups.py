import numpy as np


def generate_BCgroups(nodes, length, width, thickness, tolerance=1e-8):

    """
    Generates node groups for specimen faces and edges
    based on nodal coordinates.

    Parameters:
    nodes (numpy array):Array containing [node_id, x, y, z]
    length (float):Specimen length in x direction
    width (float):Specimen width in y direction
    thickness (float): Specimen thickness in z direction
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

    # Face node groups, used for loading and boundary conditions

    left_face = node_ids[np.isclose(x, 0.0, atol=tolerance)]

    right_face = node_ids[np.isclose(x, length, atol=tolerance)]

    front_face = node_ids[np.isclose(y, 0.0, atol=tolerance)]

    back_face = node_ids[np.isclose(y, width, atol=tolerance)]

    bottom_face = node_ids[np.isclose(z, 0.0, atol=tolerance)]

    top_face = node_ids[np.isclose(z, thickness, atol=tolerance)]

    #Edge node groups, used for constraining rigid body motions 

    front_left_edge = node_ids[np.isclose(x, 0.0, atol=tolerance) & np.isclose(y, 0.0, atol=tolerance)]

    bottom_left_edge = node_ids[np.isclose(x, 0.0, atol=tolerance) & np.isclose(z, 0.0, atol=tolerance)]

     # Store node groups in dictionary for FEBio NodeSet generation
    BC_groups = {

        "left_face": left_face,
        "right_face": right_face,

        "front_face": front_face,
        "back_face": back_face,

        "bottom_face": bottom_face,
        "top_face": top_face,

        "front_left_edge": front_left_edge,
        "bottom_left_edge": bottom_left_edge,
    }

    return BC_groups