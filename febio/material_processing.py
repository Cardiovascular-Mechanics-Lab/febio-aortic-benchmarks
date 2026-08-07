"""
material_processing.py

Internal selection, validation, and assembly of material-layer data.
"""

from numbers import Real

from febio.material_library import (
    HGO_PARAMETERS,
    NEO_HOOKEAN_PARAMETERS,
)


LAYER_NAMES = {
    1: ["Arterial Tissue"],
    2: ["Intima-Media", "Adventitia"],
    3: ["Intima", "Media", "Adventitia"],
}


REQUIRED_PARAMETERS = {
    "neo_hookean": ("E", "v"),
    "hgo": ("c", "k1", "k2", "kappa", "gamma", "K"),
}


MATERIAL_PARAMETER_LIBRARY = {
    "neo_hookean": NEO_HOOKEAN_PARAMETERS,
    "hgo": HGO_PARAMETERS,
}


def validate_parameter_block(
    *,
    material_model: str,
    num_layers: int,
    parameter_block: dict,
) -> None:
    """Validate the structure of the selected parameter block."""

    required_parameters = REQUIRED_PARAMETERS[material_model]

    missing_parameters = [
        parameter
        for parameter in required_parameters
        if parameter not in parameter_block
    ]

    if missing_parameters:
        raise ValueError(
            f"{material_model} parameters for {num_layers} layer(s) "
            f"are missing: {missing_parameters}.\n"
            "Edit febio/material_library.py."
        )

    for parameter in required_parameters:
        values = parameter_block[parameter]

        if not isinstance(values, list):
            raise ValueError(
                f'{material_model.upper()} parameter "{parameter}" '
                "must be provided as a list in "
                "febio/material_library.py."
            )

        if len(values) != num_layers:
            raise ValueError(
                f'{material_model.upper()} parameter "{parameter}" '
                f"contains {len(values)} values, but {num_layers} "
                "layers were selected.\n"
                "Provide one value per anatomical layer in "
                "febio/material_library.py."
            )

        if any(value is None for value in values):
            raise ValueError(
                f'{material_model.upper()} parameter "{parameter}" '
                f"contains undefined values for the selected "
                f"{num_layers}-layer model.\n"
                "Replace the None values in "
                "febio/material_library.py."
            )

        if any(
            not isinstance(value, Real) or isinstance(value, bool)
            for value in values
        ):
            raise ValueError(
                f'{material_model.upper()} parameter "{parameter}" '
                "must contain only numerical values."
            )


def validate_material_parameter_values(
    *,
    material_model: str,
    parameter_block: dict,
) -> None:
    """Validate allowable ranges for the selected parameters."""

    if material_model == "neo_hookean":
        if any(value <= 0 for value in parameter_block["E"]):
            raise ValueError(
                "Every Neo-Hookean E value must be greater than zero."
            )

        if any(
            value <= -1.0 or value >= 0.5
            for value in parameter_block["v"]
        ):
            raise ValueError(
                "Every Neo-Hookean Poisson ratio must satisfy "
                "-1 < v < 0.5."
            )

    elif material_model == "hgo":
        for parameter in ("c", "k1", "k2", "K"):
            if any(
                value <= 0
                for value in parameter_block[parameter]
            ):
                raise ValueError(
                    f'Every HGO "{parameter}" value must be '
                    "greater than zero."
                )

        if any(
            value < 0 or value > (1.0 / 3.0)
            for value in parameter_block["kappa"]
        ):
            raise ValueError(
                "Every HGO kappa value must lie between 0 and 1/3."
            )


def assemble_layers(
    *,
    material_model: str,
    num_layers: int,
    layer_fractions: list[float],
    parameter_block: dict,
) -> list[dict]:
    """Create one complete material dictionary per anatomical layer."""

    layer_names = LAYER_NAMES[num_layers]
    required_parameters = REQUIRED_PARAMETERS[material_model]

    assembled_layers = []

    for layer_index, layer_name in enumerate(layer_names):
        layer = {
            "name": layer_name,
            "fraction": layer_fractions[layer_index],
        }

        for parameter in required_parameters:
            layer[parameter] = parameter_block[parameter][layer_index]

        assembled_layers.append(layer)

    return assembled_layers


def get_material_layers(
    *,
    material_model: str,
    num_layers: int,
    layer_fractions: list[float],
) -> list[dict]:
    """Select, validate, and assemble the active material layers."""

    if material_model not in MATERIAL_PARAMETER_LIBRARY:
        raise ValueError(
            f'Unknown material model: "{material_model}".\n'
            f"Supported models: "
            f"{sorted(MATERIAL_PARAMETER_LIBRARY)}"
        )

    if num_layers not in LAYER_NAMES:
        raise ValueError(
            "The number of layers must be 1, 2, or 3."
        )

    if len(layer_fractions) != num_layers:
        raise ValueError(
            f"{num_layers} layers were selected, but "
            f"{len(layer_fractions)} fractions were provided."
        )

    parameter_library = MATERIAL_PARAMETER_LIBRARY[material_model]
    parameter_block = parameter_library[num_layers]

    validate_parameter_block(
        material_model=material_model,
        num_layers=num_layers,
        parameter_block=parameter_block,
    )

    validate_material_parameter_values(
        material_model=material_model,
        parameter_block=parameter_block,
    )

    return assemble_layers(
        material_model=material_model,
        num_layers=num_layers,
        layer_fractions=layer_fractions,
        parameter_block=parameter_block,
    )