"""
material_library.py

User-editable constitutive parameters for the supported material models.

The material model selected in main.py is applied to every anatomical
layer. Material parameter values may vary between layers.

Parameter-list order:

    1 layer:
        [Arterial Tissue]

    2 layers:
        [Intima-Media, Adventitia]

    3 layers:
        [Intima, Media, Adventitia]

Only the block corresponding to the selected material model and number
of layers is used. Placeholder values in unused blocks have no effect.

Unit convention:
    Stress parameters: MPa
    Angles: degrees
"""


# =============================================================================
# NEO-HOOKEAN PARAMETERS
#
# E: Young's modulus, MPa
# v: Poisson's ratio
# =============================================================================

NEO_HOOKEAN_PARAMETERS = {
    1: {
        "E": [1.0],
        "v": [0.49],
    },

    2: {
        # Layer order: [Intima-Media, Adventitia]
        "E": [1.0, 1.0],
        "v": [0.49, 0.40],
    },

    3: {
        # Layer order: [Intima, Media, Adventitia]
        "E": [None, None, None],
        "v": [None, None, None],
    },
}


# =============================================================================
# HOLZAPFEL-GASSER-OGDEN PARAMETERS
#
# c:     isotropic matrix parameter, MPa
# k1:    fiber stiffness parameter, MPa
# k2:    fiber nonlinearity parameter, dimensionless
# kappa: fiber dispersion parameter, dimensionless
# gamma: fiber-family angle, degrees
# K:     bulk modulus, MPa
#
# gamma is measured relative to the local material reference direction.
# For the current structured Hex8 mesh, this direction follows element
# Node 1 -> Node 2 and is aligned with the specimen x-axis.
# =============================================================================

HGO_PARAMETERS = {
    1: {
        "c": [0.00764],
        "k1": [0.9966],
        "k2": [524.6],
        "kappa": [0.226],
        "gamma": [49.98],
        "K": [35.0],
    },

    2: {
        # Layer order: [Intima-Media, Adventitia]
        "c": [None, None],
        "k1": [None, None],
        "k2": [None, None],
        "kappa": [None, None],
        "gamma": [None, None],
        "K": [None, None],
    },

    3: {
        # Layer order: [Intima, Media, Adventitia]
        "c": [None, None, None],
        "k1": [None, None, None],
        "k2": [None, None, None],
        "kappa": [None, None, None],
        "gamma": [None, None, None],
        "K": [None, None, None],
    },
}


# future constitutive models added here.
#
# for example:
#
# FUNG_PARAMETERS = {
#     1: {...},
#     2: {...},
#     3: {...},
# }