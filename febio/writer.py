from febio.material_writers import write_neo_hookean, write_HGO, write_Fung
def write_mesh_feb(
    filename,
    base_filename,
    nodes,
    elements,
    BC_groups,
    material_model,
    density,
    reference_direction,
    layers,
    num_layers,
    prescribed_displacement_x,
    prescribed_displacement_y,
    time_steps,
    step_size,
    layer_element_groups,
    symmetry,
    loading_type,
    loading_mode,
):
    """
    Writes a FEBio .feb input file for a layered rectangular specimen based on user input from main.py..

    Parameters:
        filename: output .feb file name
        base_filename: base file name for the model (used for standard naming of output files)
        nodes: array containing [node_id, x, y, z]
        elements: array containing [element_id, n1, ..., n8]
        BC_groups: dictionary of node sets used for boundary conditions
        material_model: FEBio material model name
        density: material density used for all layers
        reference_direction: HGO local material reference direction,"x" or "y"
        layers: list of layer dictionaries containing name, fraction, E, and v
        num_layers: number of material layers
        prescribed_displacement_x: prescribed displacement in x direction
        prescribed_displacement_y: prescribed displacement in y direction
        time_steps: number of FEBio time steps
        step_size: time increment size
        layer_element_groups: list of element groups, one per layer
        symmetry: full, half, or quarter model
        loading_type: uniaxial or biaxial
        loading_mode: symmetric_gauge or grip_constrained
    """
    with open(filename, "w") as file:

        file.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')

        file.write('<febio_spec version="4.0">\n\n')

        # MODULE
        file.write('  <Module type="solid">\n')
        file.write('    <units>mm-N-s</units>\n')
        file.write('  </Module>\n\n')

        # Static solid mechanics analysis settings
               # -----------------------------------------------------------------
        # CONTROL SECTION
        #
        # Static analysis settings and nonlinear solution controls.
        #
        # The automatic time-stepper settings below were found to provide
        # robust convergence during HGO verification against Gasser et al. (2006)
        # -----------------------------------------------------------------------

        file.write('  <Control>\n')

        file.write('    <analysis type="static"/>\n')

        file.write(
            f'    <time_steps>{time_steps}</time_steps>\n'
        )
        file.write(
            f'    <step_size>{step_size}</step_size>\n'
        )

        # Automatic time stepping
        file.write('    <time_stepper type="default">\n')
        file.write('      <max_retries>25</max_retries>\n')
        file.write('      <opt_iter>11</opt_iter>\n')
        file.write('      <dtmin>0</dtmin>\n')
        file.write('      <dtmax>0.1</dtmax>\n')
        file.write('      <aggressiveness>-2</aggressiveness>\n')
        file.write('      <cutback>0.5</cutback>\n')
        file.write('      <dtforce>0</dtforce>\n')
        file.write('    </time_stepper>\n')

        # Nonlinear solid solver
        file.write('    <solver type="solid">\n')
        file.write('      <max_refs>25</max_refs>\n')
        file.write(
            '      <diverge_reform>1</diverge_reform>\n'
        )
        file.write(
            '      <reform_each_time_step>1'
            '</reform_each_time_step>\n'
        )

        file.write('      <qn_method type="BFGS">\n')
        file.write('        <max_ups>10</max_ups>\n')
        file.write('        <max_buffer_size>0</max_buffer_size>\n')
        file.write('        <cycle_buffer>1</cycle_buffer>\n')
        file.write('        <cmax>100000</cmax>\n')
        file.write('      </qn_method>\n')

        file.write('    </solver>\n')

        file.write('  </Control>\n\n')

        # MATERIAL SECTION

        if len(layers) != num_layers:
            raise ValueError(
                f"num_layers={num_layers} but layers contains {len(layers)} entries"
            )

        file.write('  <Material>\n')

        for i, layer in enumerate(layers, start=1):

            if material_model == "neo_hookean":
                write_neo_hookean(file, layer, i, density)

            elif material_model == "hgo":
                write_HGO(
                    file,
                    layer,
                    i,
                    density,
                    reference_direction,
                )

            elif material_model == "fung":
                write_Fung(
                    file,
                    layer,
                    i,
                    density,
                    reference_direction,
                )

            else:
                raise ValueError(f"Unknown material type: {material_model}")

        file.write('  </Material>\n\n')
        
        # MESH SECTION
        file.write('  <Mesh>\n\n')

        # Write FEBio node coordinates from generated node array
        # Nodes
        file.write('    <Nodes name="Object1">\n')

        for node in nodes:

            node_id = int(node[0])

            x = node[1]
            y = node[2]
            z = node[3]

            file.write(
                f'      <node id="{node_id}">{x}, {y}, {z}</node>\n')

        file.write('    </Nodes>\n\n')


        # Write Hex8 element connectivity from generated element array
        # Elements

        for layer, layer_elements in zip(layers, layer_element_groups):

            file.write(f'    <Elements type="hex8" name="{layer["name"]}">\n')

            for element in layer_elements:

                element_id = int(element[0])

                node_ids = element[1:]

                node_string = ", ".join(str(int(n)) for n in node_ids)

                file.write(f'      <elem id="{element_id}">{node_string}</elem>\n')

            file.write('    </Elements>\n\n')

    
        # Node Sets/BC groups
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

        for layer in layers:
            file.write(
                f'    <SolidDomain name="{layer["name"]}" mat="{layer["name"]}"/>\n'
            )

        file.write('  </MeshDomains>\n\n')

        # BOUNDARY CONDITIONS
        file.write('  <Boundary>\n')


        if loading_type == "uniaxial":
            # Symmetry-based boundary conditions
            if symmetry == "full" and loading_mode == "symmetric_gauge":
                #Assigns prescribed displacement to both edges normal to x-axis (in posiytive & negative directions)
                file.write('    <bc name="pull_left_x" node_set="left_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{-prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

            elif symmetry == "full" and loading_mode == "grip_constrained":
                
                #Fix left face, simulating a grip that constrains motion in x, y, z
                file.write('    <bc name="constrain_left_x" node_set="left_face" type="zero displacement">\n')
                file.write('      <x_dof>1</x_dof>\n')
                file.write('      <y_dof>1</y_dof>\n')
                file.write('      <z_dof>1</z_dof>\n')
                file.write('    </bc>\n\n')

                #Fix right face in y and z, prescribed dispalcement in x
                file.write('    <bc name="fix_right_grip_yz" node_set="right_face" type="zero displacement">\n')
                file.write('      <x_dof>0</x_dof>\n')
                file.write(f'     <y_dof>1</y_dof>\n')
                file.write(f'     <z_dof>1</z_dof>\n')
                file.write('    </bc>\n\n')
                
                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')
                
            elif symmetry == "half" and loading_mode == "symmetric_gauge":

                #Assigns zero displacement to symmetry plane in x, where the model is cut for half model
                file.write('    <bc name="symmetry_x" node_set="symmetry_x" type="zero displacement">\n')
                file.write('      <x_dof>1</x_dof>\n')
                file.write('      <y_dof>0</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')
            
            elif symmetry == "quarter" and loading_mode == "symmetric_gauge":

                #Assigns zero displacement for symmetry planes in x and in y, prescribed displacement for right face
                file.write('    <bc name="symmetry_x" node_set="symmetry_x" type="zero displacement">\n')
                file.write('      <x_dof>1</x_dof>\n')
                file.write('      <y_dof>0</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="symmetry_y" node_set="symmetry_y" type="zero displacement">\n')
                file.write('      <x_dof>0</x_dof>\n')
                file.write('      <y_dof>1</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')   

            else:
                raise ValueError("symmetry must be 'full', 'half', or 'quarter'")
             
             
            # Y anchor for full and half models only
            # Quarter models already contain a y-symmetry plane, so the y-anchorwas not added for it.
       
            if loading_mode == "symmetric_gauge":

                if symmetry in ["full", "half"]:
                    file.write('    <bc name="fix_y_anchor" node_set="y_anchor" type="zero displacement">\n')
                    file.write('      <x_dof>0</x_dof>\n')
                    file.write('      <y_dof>1</y_dof>\n')
                    file.write('      <z_dof>0</z_dof>\n')
                    file.write('    </bc>\n\n')

                # Z anchor for all models to prevent rigid body motion
                file.write('    <bc name="fix_z_anchor" node_set="z_anchor" type="zero displacement">\n')
                file.write('      <x_dof>0</x_dof>\n')
                file.write('      <y_dof>0</y_dof>\n')
                file.write('      <z_dof>1</z_dof>\n')
                file.write('    </bc>\n\n')
       
       
        elif loading_type == "biaxial":

            #Supporting biaxial only in symmetric gauge model until I receive confirmation on the interpretation of grip constarined model
            if loading_mode != "symmetric_gauge":
                raise ValueError("biaxial loading only supports loading_mode='symmetric_gauge'")

            if symmetry == "full":

                # Pull in x direction
                file.write('    <bc name="pull_left_x" node_set="left_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{-prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                # Pull in y direction
                file.write('    <bc name="pull_front_y" node_set="front_face" type="prescribed displacement">\n')
                file.write('      <dof>y</dof>\n')
                file.write(f'      <value lc="1">{-prescribed_displacement_y}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_back_y" node_set="back_face" type="prescribed displacement">\n')
                file.write('      <dof>y</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_y}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')


            elif symmetry == "half":

                # x symmetry
                file.write('    <bc name="symmetry_x" node_set="symmetry_x" type="zero displacement">\n')
                file.write('      <x_dof>1</x_dof>\n')
                file.write('      <y_dof>0</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                # Pull in x direction
                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                # Pull in y direction
                file.write('    <bc name="pull_front_y" node_set="front_face" type="prescribed displacement">\n')
                file.write('      <dof>y</dof>\n')
                file.write(f'      <value lc="1">{-prescribed_displacement_y}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_back_y" node_set="back_face" type="prescribed displacement">\n')
                file.write('      <dof>y</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_y}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')


            elif symmetry == "quarter":

                # x symmetry
                file.write('    <bc name="symmetry_x" node_set="symmetry_x" type="zero displacement">\n')
                file.write('      <x_dof>1</x_dof>\n')
                file.write('      <y_dof>0</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                # y symmetry
                file.write('    <bc name="symmetry_y" node_set="symmetry_y" type="zero displacement">\n')
                file.write('      <x_dof>0</x_dof>\n')
                file.write('      <y_dof>1</y_dof>\n')
                file.write('      <z_dof>0</z_dof>\n')
                file.write('    </bc>\n\n')

                # Pull in positive x and y directions
                file.write('    <bc name="pull_right_x" node_set="right_face" type="prescribed displacement">\n')
                file.write('      <dof>x</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_x}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')

                file.write('    <bc name="pull_back_y" node_set="back_face" type="prescribed displacement">\n')
                file.write('      <dof>y</dof>\n')
                file.write(f'      <value lc="1">{prescribed_displacement_y}</value>\n')
                file.write('      <relative>0</relative>\n')
                file.write('    </bc>\n\n')
            else:
                raise ValueError("symmetry must be 'full', 'half', or 'quarter'")
            
            file.write('    <bc name="fix_z_anchor" node_set="z_anchor" type="zero displacement">\n')
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
        file.write('      <var type="reaction forces"/>\n')
        file.write('    </plotfile>\n')
        file.write('    <logfile>\n')
        file.write(f'      <node_data data="Rx" file="{base_filename}_Rx_data.txt" node_set="right_face"/>\n')
        file.write('    </logfile>\n')
        file.write('  </Output>\n\n')


        file.write('</febio_spec>\n')

