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
        "E": [None, None],
        "v": [None, None],
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
        "kappa": [0.266],
        "gamma": [49.98],
        "K": [65.0],
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

# =============================================================================
# FUNG ORTHOTROPIC PARAMETERS
#
# E1:  elastic modulus in local material direction 1, MPa
# E2:  elastic modulus in local material direction 2, MPa
# E3:  elastic modulus in local material direction 3, MPa
# G12: shear modulus in the local 1-2 plane, MPa
# G23: shear modulus in the local 2-3 plane, MPa
# G31: shear modulus in the local 3-1 plane, MPa
# v12: Poisson's ratio associated with local directions 1 and 2
# v23: Poisson's ratio associated with local directions 2 and 3
# v31: Poisson's ratio associated with local directions 3 and 1
# c:   Fung exponential scaling coefficient, MPa
# K:   bulk modulus, MPa
#
# The material directions are defined by the local material axes assigned
# in the FEBio model. Their orientation relative to the specimen is
# controlled using reference_direction in main.py.
#
# The default 1-layer values correspond to specimen CNd1_65, Table 2e,
# from Bhat & Yamada (2022), used in the Fung material-model verification.
# =============================================================================

FUNG_PARAMETERS = {
    1: {
        "E1": [0.00711],
        "E2": [0.17431],
        "E3": [0.17431],
        "G12": [0.005],
        "G23": [0.06857],
        "G31": [0.005],
        "v12": [0.0],
        "v23": [0.271],
        "v31": [0.0],
        "c": [0.00658],
        "K": [10.0],
    },

    2: {
        # Layer order: [Intima-Media, Adventitia]
        "E1": [None, None],
        "E2": [None, None],
        "E3": [None, None],
        "G12": [None, None],
        "G23": [None, None],
        "G31": [None, None],
        "v12": [None, None],
        "v23": [None, None],
        "v31": [None, None],
        "c": [None, None],
        "K": [None, None],
    },

    3: {
        # Layer order: [Intima, Media, Adventitia]
        "E1": [None, None, None],
        "E2": [None, None, None],
        "E3": [None, None, None],
        "G12": [None, None, None],
        "G23": [None, None, None],
        "G31": [None, None, None],
        "v12": [None, None, None],
        "v23": [None, None, None],
        "v31": [None, None, None],
        "c": [None, None, None],
        "K": [None, None, None],
    },

}