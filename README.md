# Searching for Ion and Electron Insulators

We would like to introduce three types of *ion and electron insulators*, i.e. *Li-ion & electron insulators* (LEIs), *Na-ion & electron insulators* (NEIs), and *K-ion & electron insulators*, and provide a set of codes here to screen candidate materials from computational material database, [Materials Project](https://materialsproject.org). The IEI materials are able to block the transport of multiple charge carriers (ions and electrons) and stay thermodynamically stable against specific alkali-metals. This kind of materials had been adopted in rechargeable solid-state Li/Na/K metal batteries in our work below.

> Pei, K., Kim, S.Y. & Li, J. Electrochemically stable lithium-ion and electron insulators (LEIs) for solid-state batteries. Nano Res. (2021). https://doi.org/10.1007/s12274-021-3627-1

## Structure and function of this repository

### 1.retrieve_chemical_systems.py

This program is used to search for all kinds of chemical systems that contain one specific element from online database, Materials Project. Once we get all possible chemical systems, corresponding phase diagrams can be built up to compare their thermodynamic stability.

### 2.extract_facets_and_tielined_phases.py

It is used to construct phase diagram for chemical systems, and extract the facets that contain the specific phase, like the Li_BCC. A function implemented in this program can confirm whether a certain phase locates in a phase region or not. This program will eventually produce a list of phases which are connected with the specified phase with a tie-line in the phase diagram, namely they will be able to stay thermodynamic stable at 0K.

### 3.screen_with_solubility_and_bandgap_criteria.py

It is used to further screen the phases subsequent to the program above, to exclude the phases that have dissolved atoms of the specified element in their lattice structure, and thereby make the candidates not only have thermodynamically stable contact with the specified alkali-metals, but also do not have solubility of them. In addition, this program will remove noble gases and pick up phases with the bandgap larger than 3 eV. Considering the calculation with PBE exchange-correlation functions usually underestimate the bandgap, it is large enough to find electronic insulators.

## How to cite
If this repository facilitates your research, a citation is expected.

[![DOI](https://zenodo.org/badge/228514002.svg)](https://zenodo.org/badge/latestdoi/228514002) 
