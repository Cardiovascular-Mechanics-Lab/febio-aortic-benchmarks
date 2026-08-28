"""
input_validation.py

Validation of user-defined model settings.
"""


def validate_geometry(geometry):
    for name, value in geometry.items():
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f'geometry["{name}"] must be greater than zero.'
            )


def validate_mesh(mesh, num_layers):
    for name, value in mesh.items():
        if not isinstance(value, int) or value < 2:
            raise ValueError(
                f'mesh["{name}"] must be an integer greater than or equal to 2.'
            )

    through_thickness_elements = mesh["nodes_z"] - 1

    if through_thickness_elements < num_layers:
        raise ValueError(
            "The mesh must contain at least one through-thickness "
            "element per layer. Increase mesh['nodes_z']."
        )


def validate_layers(layers):
    number = layers["number"]
    fractions = layers["fractions"]

    if number not in {1, 2, 3}:
        raise ValueError(
            'layers["number"] must be 1, 2, or 3.'
        )

    if len(fractions) != number:
        raise ValueError(
            "Provide one layer fraction for each selected layer."
        )

    if any(value <= 0 for value in fractions):
        raise ValueError(
            "All layer fractions must be greater than zero."
        )

    if abs(sum(fractions) - 1.0) > 1e-8:
        raise ValueError(
            "Layer fractions must sum to 1.0."
        )


def validate_loading(symmetry, loading):
    valid_symmetries = {"full", "half", "quarter"}
    valid_types = {"uniaxial", "biaxial"}
    valid_modes = {"symmetric_gauge", "grip_constrained"}

    if symmetry not in valid_symmetries:
        raise ValueError(
            f"Invalid symmetry: {symmetry}"
        )

    if loading["type"] not in valid_types:
        raise ValueError(
            f'Invalid loading type: {loading["type"]}'
        )

    if loading["mode"] not in valid_modes:
        raise ValueError(
            f'Invalid loading mode: {loading["mode"]}'
        )

    if loading["mode"] == "grip_constrained":
        if symmetry != "full" or loading["type"] != "uniaxial":
            raise ValueError(
                "grip_constrained is only supported for a full "
                "uniaxial model."
            )

    if loading["type"] == "uniaxial":
        if loading["displacement_x"] <= 0:
            raise ValueError(
                "Uniaxial loading requires a positive x displacement."
            )

    if loading["type"] == "biaxial":
        if loading["displacement_x"] <= 0:
            raise ValueError(
                "Biaxial loading requires a positive x displacement."
            )

        if loading["displacement_y"] <= 0:
            raise ValueError(
                "Biaxial loading requires a positive y displacement."
            )


def validate_analysis(analysis):
    if (
        not isinstance(analysis["time_steps"], int)
        or analysis["time_steps"] <= 0
    ):
        raise ValueError(
            "analysis['time_steps'] must be a positive integer."
        )

    if analysis["step_size"] <= 0:
        raise ValueError(
            "analysis['step_size'] must be greater than zero."
        )


def validate_output(output):
    if not output["model_name"].strip():
        raise ValueError(
            "output['model_name'] cannot be empty."
        )


def validate_material(material):
    valid_models = {"neo_hookean", "hgo", "fung"}

    if material["model"] not in valid_models:
        raise ValueError(
            f'Invalid material model: {material["model"]}'
        )

    if material["density"] <= 0:
        raise ValueError(
            "material['density'] must be greater than zero."
        )

    if material["model"] in {"hgo", "fung"}:
        valid_reference_directions = {"x", "y"}

        if material["reference_direction"] not in valid_reference_directions:
            raise ValueError(
                'material["reference_direction"] must be "x" or "y" '
                "for the HGO and Fung material models."
            )

def validate_inputs(
    *,
    geometry,
    mesh,
    material,
    layers,
    symmetry,
    loading,
    analysis,
    output,
):
    validate_geometry(geometry)
    validate_layers(layers)
    validate_mesh(mesh, layers["number"])
    validate_material(material)
    validate_loading(symmetry, loading)
    validate_analysis(analysis)
    validate_output(output)