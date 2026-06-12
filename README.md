# FEBio Aortic Tissue Benchmark

## Current features:
- Structured Hex8 mesh generation of a simple sheet
- Full, half, and quarter specimen symmetry models 
- Uniaxial & Biaxial loading models 
- Boundary conditions that support gauge region modeling and grip-constrained modeling (for full specimen model only)
- 1-, 2-, 3-layer tissue models
    - Layer-specific Neo-Hookean material properties 
- Automated FEBio input file generation

## Project structure 

main.py
- user configuration file 

mesh/
- nodes.py
- elements.py
- BC_groups.py 

febio/
- writer.py 

models/
- generated .feb files 

## Running the Code

1. Configure geometry, materials, symmetry and loading in 'main.py'
2. Run: 
    ''' bash 
    python main.py
    '''
3. Open the generated '.feb' file in FEBio Studio (file saved in 'models/')
4. Run the simulation using FEBio 

## Future work:

- Current material model: Neo-Hookean, future work will implement HGO models as well (and others?)

