from mesh.nodes import generate_nodes
from mesh.elements import generate_elements
from mesh.BC_groups import generate_BCgroups
from febio.writer import write_mesh_feb

# USER INPUTS 

length = 20 
width = 10
thickness = 1

nx = 21
ny = 6
nz = 2

# USER INPUTS TO BE ADDED (currently hardcoded in writer.py file or non-existent):
# element type (hex8, hex20, etc.)
# material types for different layers
# Loading type (uniaxial, biaxial)
# model symmetry (full, half, quarter)
# boundary conditions (displacement, force)? (mentioned that displacement is easiest with the testing apparatus but could be useful)

nodes = generate_nodes(length, width, thickness, nx, ny, nz)
elements = generate_elements(nx, ny, nz)
BC_groups = generate_BCgroups(nodes, length, width, thickness)
output_filename = "jobs/sheet_mesh.feb"

print("Nodes:", len(nodes))
print("Elements:", len(elements))
print("BC Groups:", len(BC_groups))

write_mesh_feb(output_filename, nodes, elements, BC_groups)
print("FEBio file written: {}".format(output_filename))