# FEBio Arterial Tissue Model Generator

This repository provides an open-source Python workflow for generating FEBio input files for layered arterial tissue specimens.

The current implementation creates structured rectangular tissue models that can be configured for different geometries, mesh densities, constitutive material models, anatomical layer structures, loading conditions, and symmetry representations.

The generated `.feb` files can be opened in FEBio Studio and solved using the FEBio solver.

---

# Current Features

- Structured Hex8 mesh generation for rectangular tissue specimens
- Full, half, and quarter symmetry models
- Uniaxial and biaxial loading
- Symmetric-gauge and grip-constrained loading modes
- One-, two-, and three-layer arterial tissue structures
- Automatic anatomical layer naming
    - 1 layer: Arterial Tissue
    - 2 layers: Intima-Media, Adventitia
    - 3 layers: Intima, Media, Adventitia
- Layer-specific material parameters
- Supported constitutive material models
    - Neo-Hookean
    - Holzapfel-Gasser-Ogden (HGO)
    - Fung orthotropic
- User-defined local material reference direction for HGO and Fung orthotropic material models
- Automatic validation of user inputs and material parameters
- Automated generation of FEBio input files
- Automatic filename numbering to prevent overwriting existing models
- Printed model summary after successful model generation

---

# Project Structure

```text
.
├── main.py
├── input_validation.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── febio/
│   ├── material_library.py
│   ├── material_processing.py
│   ├── material_writers.py
│   └── writer.py
│
├── mesh/
│   ├── nodes.py
│   ├── elements.py
│   └── boundary_sets.py
│
├── documents/
│   ├── MATERIAL_MODEL_VERIFICATION.md
│   ├── FUNG_PARAMETER_CONVERSION.xlsx
│   └── figures/
│
└── generated_models/
    ├── example_fung_3layer_biaxial_quarter.feb
    └── example_neo_hookean_2layer_uniaxial_half.feb
```

## main.py

Primary user-facing file.

Users define:

- specimen geometry
- mesh density
- constitutive material model
- number of anatomical layers
- layer thickness fractions
- symmetry
- loading type
- loading mode
- prescribed displacements
- analysis settings
- output model name

Run this file to generate the FEBio input file.

---

## febio/material_library.py

Secondary user-facing file.

Contains the constitutive material parameters for each supported material model. Parameter values are defined for the anatomical layers supported by the one-, two-, and three-layer configurations.

The number of active layers and their thickness fractions are selected in `main.py`. The same constitutive model is applied to every layer, while parameter values may vary between layers.

---

## febio/material_processing.py

Internal module that:

- selects the active material parameter block
- validates material parameters
- assigns anatomical layer names
- assembles one material dictionary per layer

---

## febio/material_writers.py

Internal module containing the FEBio material-definition writers for each supported constitutive material model.

Currently supports:

- Neo-Hookean
- Holzapfel-Gasser-Ogden (HGO)
- Fung orthotropic

---

## input_validation.py


Validates user-defined model settings before model generation, including:

- geometry
- mesh
- material-model selection
- layer structure
- loading configuration
- analysis settings
- output settings

Invalid configurations generate descriptive error messages before the FEBio input file is written.

---

## mesh/

Contains the structured mesh generation routines.

- `nodes.py` – Generates node coordinates
- `elements.py` – Generates Hex8 element connectivity and assigns elements to layers
- `boundary_sets.py` – Generates node sets for loading, symmetry, and rigid-body constraints

---

## febio/writer.py

Combines the mesh, material, loading, and analysis information into a complete FEBio `.feb` input file.

---

## generated_models/

Default output directory for generated FEBio input files.

If a file with the requested model name already exists, a number is appended automatically.

Example:

```text
hgo_verfication.feb
hgo_verification_2.feb
hgo_verification_3.feb
```

---

## `documents/`

Contains supporting documentation for the model generator.

- [`MATERIAL_MODEL_VERIFICATION.md`](documents/MATERIAL_MODEL_VERIFICATION.md) – Documents the verification of the implemented constitutive material models against published results.
- [`FUNG_PARAMETER_CONVERSION.xlsx`](documents/FUNG_PARAMETER_CONVERSION.xlsx) – Documents the conversion of the Fung material parameters reported by Bhat & Yamada (2022) to the engineering constants required by the FEBio Fung orthotropic material model.
- `figures/` – Contains figures used in the supporting documentation.

---

# Coordinate and Unit Conventions

Current coordinate system:

- **x** – specimen length and primary loading direction
- **y** – specimen width and secondary loading direction
- **z** – specimen thickness

All geometry entered in `main.py` corresponds to the **full specimen**.

Half- and quarter-symmetry geometries are calculated automatically.

Unit convention:

- Length: mm
- Force: N
- Stress: MPa
- Density: tonne/mm³

Users are responsible for maintaining a consistent unit system.

---

# Installation and Requirements

This project requires Python to generate the FEBio input files and FEBio/FEBio Studio to open and solve the generated models.

The workflow was developed and tested using **FEBio Studio 3.2.0** and the corresponding FEBio solver. Compatibility with other FEBio versions has not been verified.

[FEBio and FEBio Studio](https://febio.org/) are not included with this repository and must be installed separately.

Python dependencies are listed in `requirements.txt`.

To create a local Python virtual environment, navigate to the repository directory in a terminal and run:

```powershell
python -m venv .venv
```

Activate the virtual environment (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

> **User prerequisites:** This workflow assumes that users have basic familiarity with Python, including editing Python scripts, working with a Python environment, and running scripts from a terminal or integrated development environment (IDE). Basic familiarity with FEBio and FEBio Studio is also recommended for reviewing and running the generated models.

> **Note:** This project and its Python environment were developed and tested using Visual Studio Code (VS Code). VS Code is not required to run the project; however, the setup and execution process may differ when using other IDEs or development environments.

---

# Running the Code

### 1. Activate the virtual environment

If the virtual environment is not already active, activate it before running the model generator.

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 2. Configure the model

Edit the model settings in:

```text
main.py
```

Model geometry, mesh, layer structure, loading conditions, symmetry, and analysis settings are configured directly in `main.py`.

If necessary, edit the constitutive material parameters in:

```text
febio/material_library.py
```

---

### 3. Generate the FEBio input file

Run:

```bash
python main.py
```

If the model configuration is valid, a summary will be printed in the terminal and the generated `.feb` file will be saved in:

```text
generated_models/
```

---

### 4. Open the model in FEBio Studio

Open the generated `.feb` file as a model in FEBio Studio and run the simulation using the FEBio solver.

---

# Material Models

## Neo-Hookean

Current material parameters:

- Young's modulus, **$E$**
- Poisson's ratio, **$\nu$**

Each anatomical layer may have different parameter values.

---

## Holzapfel-Gasser-Ogden (HGO)

Material parameters:

- **$c$** – isotropic matrix parameter
- **$k_1$** – fiber stiffness parameter
- **$k_2$** – fiber nonlinearity parameter
- **$\kappa$** – fiber dispersion parameter
- **$\gamma$** – fiber-family angle
- **$K$** – bulk modulus (written as `k` in the FEBio material definition)

The local material reference direction is selected in `main.py` using `reference_direction`.

- `"x"` – local material direction e1 follows the specimen x-direction
- `"y"` – local material direction e1 follows the specimen y-direction

The fiber-family angle $\gamma$ is measured relative to e1.

Each anatomical layer may have a different set of HGO material parameters.

---

## Fung Orthotropic

Material parameters:

- **$E_1, E_2, E_3$** – elastic moduli along the local material directions
- **$\nu_{12}, \nu_{23}, \nu_{31}$** – Poisson's ratios
- **$G_{12}, G_{23}, G_{31}$** – shear moduli
- **$c$** – exponential scaling coefficient
- **$K$** – bulk modulus (written as `k` in the FEBio material definition)

The local material axes are controlled by the `reference_direction` setting in `main.py`.

- `"x"` – local material direction e1 follows the specimen x-direction
- `"y"` – local material direction e1 follows the specimen y-direction

The Fung engineering constants are interpreted relative to the resulting local material coordinate system.

Each anatomical layer may have a different set of Fung material parameters.

---

# Material Model Verification

The HGO and Fung material-model implementations were verified against previously published results.

Verification cases, model configurations, parameter conversions, comparison figures, sensitivity analyses, and known limitations are documented in the [Material Model Verification](documents/MATERIAL_MODEL_VERIFICATION.md) document.

## HGO

The Holzapfel-Gasser-Ogden implementation was evaluated using the material parameters and force-displacement results reported by Gasser et al. (2006).

The verification includes circumferential and axial specimens with and without fiber dispersion.

## Fung Orthotropic

The Fung orthotropic implementation was evaluated using material parameters and stress-strain results reported by Bhat & Yamada (2022).

The verification includes isotropic and transversely isotropic material configurations. The conversion of the published Fung coefficients to the engineering constants required by FEBio is documented in [`FUNG_PARAMETER_CONVERSION.xlsx`](documents/FUNG_PARAMETER_CONVERSION.xlsx).

---

# Loading Options

## Loading Types

- `uniaxial`
- `biaxial`

## Loading Modes

- `symmetric_gauge`
- `grip_constrained`

Currently supported combinations:

| Loading Type | Loading Mode | Supported Symmetry |
|--------------|--------------|--------------------|
| Uniaxial | `symmetric_gauge` | Full, Half, Quarter |
| Uniaxial | `grip_constrained` | Full |
| Biaxial | `symmetric_gauge` | Full, Half, Quarter |
| Biaxial | `grip_constrained` | Not currently supported |

Invalid loading combinations are rejected before the FEBio file is generated.

---

# Future Work

Potential extensions include:

- Additional arterial constitutive material models
- Cylindrical tube geometry generated by mapping the rectangular mesh
- Additional benchmark and verification examples
- Optional automatic execution of the FEBio solver