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

def write_HGO(file, layer, material_id, density):

    pressure_model = "Abaqus (GOH)"
    mat_axis_type = "local"
    mat_axis = "1,2,4"

    """ mat_axis currently defined for loading along the circumferential direction (x-axis) of the specimen.
    Future iterations could include different definitions of mat_axis for different loading directions, or user-defined mat_axis values."""

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