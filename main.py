"""
main.py

User-facing script for generating an FEBio input file for a layered
arterial tissue specimen.

Workflow:
    1. Define the model settings in this file.
    2. Edit layer-specific constitutive parameters in
       febio/material_library.py, if required.
    3. Save the changes and run this file.
    4. Open the generated .feb file in FEBio Studio.

Unit convention:
    Length: mm
    Force: N
    Stress: MPa

Coordinate convention:
    x: specimen length and primary loading direction
    y: specimen width and secondary loading direction
    z: specimen thickness

All geometry dimensions describe the full specimen. Half- and
quarter-symmetry geometries are calculated internally.
"""

from pathlib import Path
import re

from febio.material_processing import get_material_layers
from febio.writer import write_mesh_feb
from mesh.boundary_sets import generate_boundary_sets
from mesh.elements import (
    generate_elements,
    split_elements_by_thickness,
)
from mesh.nodes import generate_nodes
from validation import validate_inputs


# -------------------------------------------------------------------------
# FULL SPECIMEN GEOMETRY
# -------------------------------------------------------------------------

geometry = {
    "length": 10.0,
    "width": 3.0,
    "thickness": 0.5,
}


# -------------------------------------------------------------------------
# MESH
#
# Values represent the number of nodes in each direction.
#
# Number of elements:
#     x direction = nodes_x - 1
#     y direction = nodes_y - 1
#     z direction = nodes_z - 1
# -------------------------------------------------------------------------

mesh = {
    "nodes_x": 41,
    "nodes_y": 21,
    "nodes_z": 5,
}


# -------------------------------------------------------------------------
# MATERIAL MODEL
#
# The selected constitutive model is applied to every layer, but the
# material parameters may vary between layers.
#
# Currently supported:
#     "neo_hookean"
#     "hgo"
#
# Edit layer-specific parameters in febio/material_library.py.
# -------------------------------------------------------------------------

material = {
    "model": "hgo",
    "density": 1.0,        # units tonne/mm^3
}


# -------------------------------------------------------------------------
# LAYER CONFIGURATION
#
# Supported anatomical structures:
#
#     1 layer:
#         Arterial Tissue
#
#     2 layers:
#         Intima-Media
#         Adventitia
#
#     3 layers:
#         Intima
#         Media
#         Adventitia
#
# Fractions are listed in the same order as the anatomical names above.
# Fractions must be positive decimals that sum to 1.0.
# -------------------------------------------------------------------------

layers = {
    "number": 1,
    "fractions": [1.0],
}


# -------------------------------------------------------------------------
# LOADING AND SYMMETRY
#
# symmetry options:
#     "full"
#     "half"
#     "quarter"
#
# loading type options:
#     "uniaxial"
#     "biaxial"
#
# loading mode options:
#     "symmetric_gauge"
#     "grip_constrained"
#
# Valid combinations:
#
#     uniaxial + symmetric_gauge:
#         full, half, or quarter
#
#     uniaxial + grip_constrained:
#         full only
#
#     biaxial + symmetric_gauge:
#         full, half, or quarter
#
#     biaxial + grip_constrained:
#         not supported
#
# Prescribed displacements represent displacement per side of the
# corresponding full specimen. Unused displacement values may remain
# defined.
# -------------------------------------------------------------------------

symmetry = "full"

loading = {
    "type": "uniaxial",
    "mode": "grip_constrained",
    "displacement_x": 0.15,
    "displacement_y": 0.15,
}


# -------------------------------------------------------------------------
# ANALYSIS CONTROL
#
# Final analysis time = time_steps * step_size
# -------------------------------------------------------------------------

analysis = {
    "time_steps": 20,
    "step_size": 0.05,
}


# -------------------------------------------------------------------------
# OUTPUT
#
# Enter the model name without the .feb extension.
# Generated files are saved in generated_models/.
#
# If the filename already exists, a number is appended automatically.
# Example:
#     hgo_full_symmetric.feb
#     hgo_full_symmetric_2.feb
# -------------------------------------------------------------------------

output = {
    "model_name": "hgo_validation",
}


######################## END OF USER-INPUT SECTION ########################

# -------------------------------------------------------------------------
# MODEL ASSEMBLY
# -------------------------------------------------------------------------

def normalize_material_model(model_name: str) -> str:
    """Convert material-model labels to a consistent internal form."""

    return (
        model_name
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def create_unique_output_path(
    model_name: str,
    output_directory: str = "generated_models",
) -> tuple[str, Path]:
    """
    Create a unique FEBio output path.

    The output directory is intentionally not included in the main
    user-input section, but may be changed here if required.
    """

    sanitized_name = model_name.strip()

    if sanitized_name.lower().endswith(".feb"):
        sanitized_name = sanitized_name[:-4]

    sanitized_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        sanitized_name,
    ).strip("_")

    if not sanitized_name:
        raise ValueError(
            'output["model_name"] does not contain any valid '
            "filename characters."
        )

    directory = Path(output_directory)
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    candidate = directory / f"{sanitized_name}.feb"
    counter = 2

    while candidate.exists():
        candidate = directory / f"{sanitized_name}_{counter}.feb"
        counter += 1

    return candidate.name, candidate


def print_model_summary(
    *,
    material_layers,
    nodes,
    elements,
    layer_element_groups,
    boundary_sets,
    output_path,
) -> None:
    """Print a summary of the generated model."""

    final_time = (
        analysis["time_steps"]
        * analysis["step_size"]
    )

    print("\nFEBio model summary")
    print("===================")

    print(f'Model name:       {output["model_name"]}')
    print(f"Output path:      {output_path}")

    print("\nGeometry")
    print("--------")
    print(f'Length:           {geometry["length"]}')
    print(f'Width:            {geometry["width"]}')
    print(f'Thickness:        {geometry["thickness"]}')
    print(f"Symmetry:         {symmetry}")

    print("\nMesh")
    print("----")
    print(f'Nodes in x:       {mesh["nodes_x"]}')
    print(f'Nodes in y:       {mesh["nodes_y"]}')
    print(f'Nodes in z:       {mesh["nodes_z"]}')
    print(f"Total nodes:      {len(nodes)}")
    print(f"Total elements:   {len(elements)}")

    print("\nMaterial")
    print("--------")
    print(f'Model:            {material["model"]}')
    print(f'Density:          {material["density"]}')
    print(f'Layers:           {layers["number"]}')

    for layer, element_group in zip(
        material_layers,
        layer_element_groups,
    ):
        print(
            f'  {layer["name"]}: '
            f'fraction={layer["fraction"]}, '
            f'elements={len(element_group)}'
        )

    print("\nLoading")
    print("-------")
    print(f'Type:             {loading["type"]}')
    print(f'Mode:             {loading["mode"]}')
    print(
        f'Displacement x:   {loading["displacement_x"]}'
    )
    print(
        f'Displacement y:   {loading["displacement_y"]}'
    )

    print("\nAnalysis")
    print("--------")
    print(f'Time steps:       {analysis["time_steps"]}')
    print(f'Step size:        {analysis["step_size"]}')
    print(f"Final time:       {final_time}")
    print(f"Boundary sets:    {len(boundary_sets)}")


def generate_model() -> Path:
    """Validate, assemble, and write the configured FEBio model."""

    validate_inputs(
    geometry=geometry,
    mesh=mesh,
    material=material,
    layers=layers,
    symmetry=symmetry,
    loading=loading,
    analysis=analysis,
    output=output,
)

    normalized_material_model = normalize_material_model(
        material["model"]
    )

    material_layers = get_material_layers(
        material_model=normalized_material_model,
        num_layers=layers["number"],
        layer_fractions=layers["fractions"],
    )

    base_filename, output_path = create_unique_output_path(
        output["model_name"]
    )

    nodes = generate_nodes(
        geometry["length"],
        geometry["width"],
        geometry["thickness"],
        mesh["nodes_x"],
        mesh["nodes_y"],
        mesh["nodes_z"],
        symmetry,
    )

    elements = generate_elements(
        mesh["nodes_x"],
        mesh["nodes_y"],
        mesh["nodes_z"],
    )

    layer_element_groups = split_elements_by_thickness(
        elements,
        mesh["nodes_x"],
        mesh["nodes_y"],
        mesh["nodes_z"],
        material_layers,
    )

    boundary_sets = generate_boundary_sets(
        nodes,
        symmetry,
    )

    print_model_summary(
        material_layers=material_layers,
        nodes=nodes,
        elements=elements,
        layer_element_groups=layer_element_groups,
        boundary_sets=boundary_sets,
        output_path=output_path,
    )

    write_mesh_feb(
        str(output_path),
        base_filename,
        nodes,
        elements,
        boundary_sets,
        normalized_material_model,
        material["density"],
        material_layers,
        layers["number"],
        loading["displacement_x"],
        loading["displacement_y"],
        analysis["time_steps"],
        analysis["step_size"],
        layer_element_groups,
        symmetry,
        loading["type"],
        loading["mode"],
    )

    return output_path


def main() -> None:
    """Run the arterial tissue model generator."""

    try:
        output_path = generate_model()

    except ValueError as error:
        print("\nConfiguration error")
        print("===================")
        print(error)
        raise SystemExit(1) from error

    print(
        "\nFEBio input file created successfully:"
        f"\n{output_path}"
    )


if __name__ == "__main__":
    main()