def write_neo_hookean(file, layer, material_id, density):

    file.write(
        f'    <material id="{material_id}" '
        f'name="{layer["name"]}" '
        f'type="neo-Hookean">\n'
    )

    file.write(f'      <density>{density}</density>\n')
    file.write(f'      <E>{layer["E"]}</E>\n')
    file.write(f'      <v>{layer["v"]}</v>\n')

    file.write('    </material>\n\n')

def write_HGO(file, layer, material_id, density,reference_direction):

    pressure_model = "default"
    mat_axis_type = "local"

    material_axes = {
        "x": "1,2,4",
        "y": "2,3,1",
    }

    mat_axis = material_axes[reference_direction]

    # Local material-axis convention for the structured Hex8 mesh:
    #
    #     x -> e1 aligned with specimen x-axis -> local nodes 1,2,4
    #     y -> e1 aligned with specimen y-axis -> local nodes 2,3,1
    #
    # The HGO fiber-family angle gamma is measured relative to e1 
    # according to FEBio guidelines.
    
    file.write(
        f'    <material id="{material_id}" '
        f'name="{layer["name"]}" '
        f'type="Holzapfel-Gasser-Ogden">\n'
    )

    file.write(f'      <density>{density}</density>\n')
    file.write(f'      <k>{layer["K"]}</k>\n')
    file.write(
        f'      <pressure_model>{pressure_model}</pressure_model>\n'
    )
    file.write(f'      <c>{layer["c"]}</c>\n')
    file.write(f'      <k1>{layer["k1"]}</k1>\n')
    file.write(f'      <k2>{layer["k2"]}</k2>\n')
    file.write(f'      <kappa>{layer["kappa"]}</kappa>\n')
    file.write(f'      <gamma>{layer["gamma"]}</gamma>\n')

    file.write(f'      <mat_axis type="{mat_axis_type}">\n')
    file.write(f'        <local>{mat_axis}</local>\n')
    file.write('      </mat_axis>\n')

    file.write('    </material>\n\n')

def write_Fung(file, layer, material_id, density, reference_direction):

    pressure_model = "default"
    mat_axis_type = "local"

    material_axes = {
        "x": "1,2,4",
        "y": "2,3,1",
    }

    mat_axis = material_axes[reference_direction]

    # Local material-axis convention for the structured Hex8 mesh:
    #
    #     x -> e1 aligned with specimen x-axis -> local nodes 1,2,4
    #     y -> e1 aligned with specimen y-axis -> local nodes 2,3,1
    #
    # The Fung engineering constants E1, E2, E3, G12, G23, G31,
    # v12, v23, and v31 are interpreted relative to these local axes.

    file.write(
        f'    <material id="{material_id}" '
        f'name="{layer["name"]}" '
        f'type="Fung orthotropic">\n'
    )

    file.write(f'      <density>{density}</density>\n')
    file.write(f'      <k>{layer["K"]}</k>\n')
    file.write(
        f'      <pressure_model>{pressure_model}</pressure_model>\n'
    )

    file.write(f'      <E1>{layer["E1"]}</E1>\n')
    file.write(f'      <E2>{layer["E2"]}</E2>\n')
    file.write(f'      <E3>{layer["E3"]}</E3>\n')

    file.write(f'      <G12>{layer["G12"]}</G12>\n')
    file.write(f'      <G23>{layer["G23"]}</G23>\n')
    file.write(f'      <G31>{layer["G31"]}</G31>\n')

    file.write(f'      <v12>{layer["v12"]}</v12>\n')
    file.write(f'      <v23>{layer["v23"]}</v23>\n')
    file.write(f'      <v31>{layer["v31"]}</v31>\n')

    file.write(f'      <c>{layer["c"]}</c>\n')

    file.write(f'      <mat_axis type="{mat_axis_type}">\n')
    file.write(f'        <local>{mat_axis}</local>\n')
    file.write('      </mat_axis>\n')

    file.write('    </material>\n\n')