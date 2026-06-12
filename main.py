"""
main.py

User-facing configuration file for generating FEBio input files.

This script defines the specimen geometry, mesh density, layer structure,
material properties, symmetry option, and loading configuration. It then
calls the mesh generation, layer assignment, boundary condition grouping,
and FEBio writer functions to create a .feb model file.
"""

from mesh.nodes import generate_nodes
from mesh.elements import generate_elements
from mesh.BC_groups import generate_BCgroups
from febio.writer import write_mesh_feb
from mesh.elements import split_elements_by_thickness

# USER INPUTS 

#Full specimen dimensions
length = 20  #mm
width = 10   #mm   
thickness = 1   #mm

#Mesh density 
#nx, ny, and nz are the number of nodes in each direction, 
# therefore the number of elements in each direction are nx-1, ny-1, and nz-1 respectively.

nx = 21  
ny = 7   
nz = 11  

#Layer parameters

# options: 1 (single homogeneous layer), 2 (intima-media and adventitia), 3 (intima, media, adventitia)
num_layers = 3

#User defined parameters for their chosen layer configuration (according to neo-Hookean material model only)
#Each layer has:
# - name: material name for FEBio file
# - fraction: fraction of total thickness occupied by the layer
# - E: Young's modulus
# - v: Poisson's ratio

if num_layers == 1:
    layers = [
        {
            "name": "Single Layer",
            "fraction": 1.0, 
            "E": 1,
            "v": 0.49
        }
    ]

elif num_layers == 2:
    layers = [
        #Intima-Media layer properties
        {
            "name": "Intima-Media",
            "fraction": 0.9,
            "E": 1,
            "v": 0.49
        },
        #Adventitia layer properties
        {
            "name": "Adventitia",
            "fraction": 0.1,
            "E": 1,
            "v": 0.4
        }
    ]

elif num_layers == 3:
    layers = [
        #Intima layer properties
        {
            "name": "Intima",
            "fraction": 0.2,
            "E": 0.5,
            "v": 0.49
        },

        #Media layer properties
        {
            "name": "Media",
            "fraction": 0.5,
            "E": 1,
            "v": 0.49
        },

        #Adventitia layer properties
        {
            "name": "Adventitia",
            "fraction": 0.3,
            "E": 1,
            "v": 0.4
        }
    ]
else: 
    raise ValueError("Invalid number of layers. Please choose 1, 2, or 3.")
  
#Check that user-defined layer fractions add to 1.0
total_fraction = sum(layer["fraction"] for layer in layers)

if abs(total_fraction - 1.0) > 1e-8:
    raise ValueError("Layer fractions must add to 1.0")

#Material model settings
# Currently the same for all layers and layer configurations for now

material_type = "neo-Hookean" #Same for all layers and layer configurations
density = 1


#Model Symmetry 

#Options: 
# "full": full specimen
# "half": x=0 symmetry plane
# "quarter": x=0 and y=0 symmetry planes
symmetry = "full"  

#Loading 

#Options: 
# "uniaxial": Loading in x-direction only
# "biaxial": Loading in both x and y directions
loading_type = "uniaxial"

#Options: 
# "symmetric_gauge": represents gauge region loading
# "grip_constrained": Simulates grip behvaiour, intented for full, unaxial model only
loading_mode = "symmetric_gauge" 

# Prescribed displacement magnitudes
# Represents half-specimen displacements, i.e. displacement per side.
#
# E.g. For a full symmetric model (uniaxial)
#   left face  = -prescribed_displacement_x
#   right face = +prescribed_displacement_x
#
# E.g. For half/quarter models (uniaxial):
#   symmetry plane = zero normal displacement
#   loaded face    = +prescribed_displacement_x
prescribed_displacement_x = 5 #mm, HALF model displacement in x (i.e. displacement per side of full specimen)
prescribed_displacement_y = 5  #mm, HALF model displacement in y (i.e. displacement per side of full specimen)

#Time steps
time_steps = 10 
step_size = 0.1

#Output file 
output_filename = f"models/sheet_{loading_type}_L{num_layers}_{symmetry}_{loading_mode}.feb"


nodes = generate_nodes(length, width, thickness, nx, ny, nz, symmetry)
elements = generate_elements(nx, ny, nz)
layer_element_groups = split_elements_by_thickness(elements, nx, ny, nz, layers)
BC_groups = generate_BCgroups(nodes, symmetry)

#Basic model summary for user reference
print("Nodes:", len(nodes))
print("Elements:", len(elements))
print("BC Groups:", len(BC_groups))

write_mesh_feb(output_filename, nodes, elements, BC_groups, material_type, density, layers, num_layers, prescribed_displacement_x, prescribed_displacement_y, time_steps, step_size, layer_element_groups, symmetry, loading_type, loading_mode)

print("FEBio file written: {}".format(output_filename))