"""
writer.py

Converts procedurally generated mesh, material, boundary-condition, and loading data into
a valid FEBio input (.feb) file.
"""

def write_mesh_feb(filename, nodes, elements, BC_groups):

    """
    Writes a FEBio .feb input file for a simple uniaxial plate model.

    Parameters:
        filename: output .feb file name
        nodes: array containing [node_id, x, y, z]
        elements: array containing [element_id, n1, ..., n8]
        BC_groups: dictionary of node sets used for boundary conditions
    """
    with open(filename, "w") as file:

        file.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')

        file.write('<febio_spec version="4.0">\n\n')

        # MODULE
        file.write('  <Module type="solid"/>\n\n')

        # Static solid mechanics analysis settings
        # CONTROL SECTION
        file.write('  <Control>\n')

        file.write('    <analysis type="static"/>\n')

        file.write('    <time_steps>10</time_steps>\n')
        file.write('    <step_size>0.1</step_size>\n')

        file.write('    <solver>\n')
        file.write('      <max_refs>25</max_refs>\n')
        file.write('      <diverge_reform>1</diverge_reform>\n')
        file.write('      <reform_each_time_step>1</reform_each_time_step>\n')
        file.write('    </solver>\n')

        file.write('  </Control>\n\n')

        # Neo-Hookean material currently hardcoded for initial testing
        # TODO: make material type and parameters user-defined from main.py
        # MATERIAL SECTION
        file.write('  <Material>\n')
        file.write('    <material id="1" name="Material1" type="neo-Hookean">\n')
        file.write('      <density>1</density>\n')
        file.write('      <E>0.5</E>\n')
        file.write('      <v>0.49</v>\n')
        file.write('    </material>\n')
        file.write('  </Material>\n\n')

        # MESH SECTION
        file.write('  <Mesh>\n\n')

        # Write FEBio node coordinates from generated node array
        # NODES
        file.write('    <Nodes name="Object1">\n')

        for node in nodes:

            node_id = int(node[0])

            x = node[1]
            y = node[2]
            z = node[3]

            file.write(
                f'      <node id="{node_id}">{x}, {y}, {z}</node>\n'
            )

        file.write('    </Nodes>\n\n')


        # Write Hex8 element connectivity from generated element array
        # ELEMENTS
        file.write('    <Elements type="hex8" name="Part1">\n')

        for element in elements:

            element_id = int(element[0])

            node_ids = element[1:]

            node_string = ", ".join(
                str(int(n)) for n in node_ids
            )

            file.write(
                f'      <elem id="{element_id}">{node_string}</elem>\n'
            )

        file.write('    </Elements>\n\n')
    
        # NODE SETS / BC GROUPS
        for group_name, node_ids in BC_groups.items():

            file.write(f'    <NodeSet name="{group_name}">\n')

            node_string = ", ".join(
                str(int(node_id)) for node_id in node_ids
            )

            file.write(f'      {node_string}\n')
            file.write('    </NodeSet>\n\n')

        file.write('  </Mesh>\n\n')

        # Assign material to the solid element domain
        # MESH DOMAIN
        file.write('  <MeshDomains>\n')
        file.write('    <SolidDomain name="Part1" mat="Material1"/>\n')
        file.write('  </MeshDomains>\n\n')

        # BOUNDARY CONDITIONS
        file.write('  <Boundary>\n')

        #Fix x-displacement on left face (anchors specimen)
        file.write('    <bc name="fix_left_x" node_set="left_face" type="zero displacement">\n')
        file.write('      <x_dof>1</x_dof>\n')
        file.write('      <y_dof>0</y_dof>\n')
        file.write('      <z_dof>0</z_dof>\n')
        file.write('    </bc>\n\n')
        
        #Apply prescribed x-displacement on right face (uniaxial, 1/2 model)
        file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
        file.write('      <dof>x</dof>\n')
        file.write('      <value lc="1">2</value>\n')
        file.write('      <relative>0</relative>\n')
        file.write('    </bc>\n\n')
        
        #Anchor one line in y direction to prevent rigid body motion
        file.write('    <bc name="fix_front_left_y" node_set="front_left_edge" type="zero displacement">\n')
        file.write('      <x_dof>0</x_dof>\n')
        file.write('      <y_dof>1</y_dof>\n')
        file.write('      <z_dof>0</z_dof>\n')
        file.write('    </bc>\n\n')

        #Anchor one line in z direction to prevent rigid body motion
        file.write('    <bc name="fix_bottom_left_z" node_set="bottom_left_edge" type="zero displacement">\n')
        file.write('      <x_dof>0</x_dof>\n')
        file.write('      <y_dof>0</y_dof>\n')
        file.write('      <z_dof>1</z_dof>\n')
        file.write('    </bc>\n\n')

        file.write('  </Boundary>\n\n')

        # Load curve ramps prescribed displacement from 0 to full value over the step
        # LOAD DATA
        file.write('  <LoadData>\n')
        file.write('    <load_controller id="1" name="LC1" type="loadcurve">\n')
        file.write('      <interpolate>LINEAR</interpolate>\n')
        file.write('      <extend>CONSTANT</extend>\n')
        file.write('      <points>\n')
        file.write('        <pt>0,0</pt>\n')
        file.write('        <pt>1,1</pt>\n')
        file.write('      </points>\n')
        file.write('    </load_controller>\n')
        file.write('  </LoadData>\n\n')

        # Request variables to save in the FEBio plot file for post-processing
        # OUTPUT 
        file.write('  <Output>\n')
        file.write('    <plotfile type="febio">\n')
        file.write('      <var type="displacement"/>\n')
        file.write('      <var type="stress"/>\n')
        file.write('      <var type="Lagrange strain"/>\n')
        file.write('      <var type="relative volume"/>\n')
        file.write('    </plotfile>\n')
        file.write('  </Output>\n\n')

        file.write('</febio_spec>\n')

