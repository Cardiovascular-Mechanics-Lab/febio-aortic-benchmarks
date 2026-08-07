# FEBio Arterial Tissue Model Generator

This repository provides an open-source Python workflow for generating FEBio input files for layered arterial tissue specimens.

The current implementation creates structured rectangular tissue models that can be configured for different geometries, mesh densities, constitutive material models, anatomical layer structures, loading conditions, and symmetry representations.

The generated `.feb` files can be opened and solved using FEBio Studio.

---

# Current Features

- Structured Hex8 mesh generation for rectangular tissue specimens
- Full, half, and quarter symmetry models
- Uniaxial and biaxial loading
- Gauge-region and grip-constrained boundary-condition options
- One-, two-, and three-layer arterial tissue structures
- Automatic anatomical layer naming
    - 1 layer: Arterial Tissue
    - 2 layers: Intima-Media, Adventitia
    - 3 layers: Intima, Media, Adventitia
- Layer-specific material parameters
- Supported constitutive material models
    - Neo-Hookean
    - Holzapfel-Gasser-Ogden (HGO)
- Automatic validation of user inputs
- Automated generation of FEBio input files
- Automatic filename numbering to prevent overwriting existing models
- Printed model summary after successful model generation

---

# Project Structure

```text
.
├── main.py
├── validation.py
├── README.md
├── requirements.txt
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
└── generated_models/
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

Contains the constitutive material parameters for each supported material model.

Parameters are organized by:

- material model
- number of layers
- anatomical layer

The same constitutive model is applied to every layer, while parameter values may vary between layers.

---

## febio/material_processing.py

Internal module that:

- selects the active material parameter block
- validates material parameters
- assigns anatomical layer names
- assembles one material dictionary per layer

---

## validation.py

Validates:

- geometry
- mesh
- layer structure
- loading configuration
- analysis settings
- output settings

before the FEBio file is generated.

Specific error messages are generated to support the correction of invalid entries.

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
hgo_validation.feb
hgo_validation_2.feb
hgo_validation_3.feb
```

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

Users are responsible for maintaining a consistent unit system.

---

# Running the Code

### 1. Configure the model

Edit the model settings in

```text
main.py
```

If necessary, edit the constitutive material parameters in

```text
febio/material_library.py
```

---

### 2. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 3. Generate the FEBio input file

```bash
python main.py
```

If the model configuration is valid, a summary will be printed in the terminal and the generated `.feb` file will be saved in

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

- Young's modulus, **E**
- Poisson's ratio, **v**

Each anatomical layer may have different parameter values.

---

## Holzapfel-Gasser-Ogden (HGO)

Current material parameters:

- **c** – isotropic matrix parameter
- **k1** – fiber stiffness parameter
- **k2** – fiber nonlinearity parameter
- **kappa** – fiber dispersion parameter
- **gamma** – fiber-family angle
- **K** – bulk modulus

The local material reference direction follows the element **Node 1 → Node 2** direction, which is aligned with the specimen **x-direction**.

The fiber angle **γ** is measured relative to this local material direction.

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

Planned extensions include:

- Fung constitutive material model
- Additional arterial constitutive models
- Cylindrical tube geometry generated by mapping the rectangular mesh
- Axial stretch boundary conditions
- Additional benchmark and validation examples
- Optional automatic execution of the FEBio solver