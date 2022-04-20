# Searching for Ion and Electron Insulators

We would like to introduce three types of *ion and electron insulators*, i.e. *Li-ion & electron insulators* (LEIs), *Na-ion & electron insulators* (NEIs), and *K-ion & electron insulators* (KEIs), and provide a set of codes here to screen candidate materials from computational material database, [Materials Project](https://materialsproject.org). The IEI materials are able to block the transport of multiple charge carriers (ions and electrons) and stay thermodynamically stable against specific alkali-metals. This kind of materials had been adopted in rechargeable solid-state Li/Na/K metal batteries in our work below.

> Pei, K., Kim, S.Y. & Li, J. Electrochemically stable lithium-ion and electron insulators (LEIs) for solid-state batteries. Nano Res. (2021). https://doi.org/10.1007/s12274-021-3627-1

## Structure and function of this repository

### 1.retrieve_chemical_systems.py

This program is used to search for all kinds of chemical systems that contain one specific element from online material database, Materials Project. Once we get all possible chemical systems, corresponding phase diagrams can be constructed to compare the thermodynamic stability among phases of interest.

### 2.extract_facets_and_tielined_phases.py

It will construct phase diagrams for specified chemical systems, and extract the facets that contain the specific phase, for example to return all facets where the Li_BCC is located in. This program will eventually produce a list of phases, and each of them has a tie-line connect with the specified phase like Li_BCC in phase diagrams, namely they will be able to remain thermodynamic stable at 0K.

### 3.screen_with_solubility_and_bandgap_criteria.py

This program is used to exclude those phases that have dissolved specified atoms in their lattice structure, and thereby make the rest candidates not only being thermodynamically stable against the specified metals, but also do not have solubility of them. This property will ensure the candidates have electrochemical stability at the entire range of the chemical potential.

In addition, this program will remove noble gases and pick up phases with bandgap larger than 3 eV. Considering the calculations with PBE exchange-correlation functions usually [underestimate the bandgap by about 40%](https://wiki.materialsproject.org/Calculations_Manual#Accuracy_of_Band_Structures), we presumed that it is large enough to find electronic insulators.

### 4.verify_full_stability_window.py (in Other_functions directory)

For the phases in list above, this program can check the stability window in terms of the specified chemical potential, like the Li potential. Every phase with the stability on the entire chemical potential window will be tagged with "FullWindow" is "True".

### 5.plot_envelope.py

This program is used to plot a potential-energy envelope with the lowest formation energy for all phases in a ternary chemical system, like the Li-Be-O2 system. Any phases that are located on this envelope are the most stable phases - they have the lowest DFT-calculated formation energies at their composition. Among them, those phases in a simplex (facet of the envelope) have the most advantage in terms of thermodynamic potential, and will stay stable together, rather than others will decompose spontaneously in a thermodynamic system.

### 6.plot_quaternary_pd.py

A quaternary phase diagram can be plotted by this program, like the Li-K-Ca-Cl2 phase diagram. This program can also highlight the phase regions where a specific phase is located.

### 7.plot_ternary_pd_with_background.py

This program can help to construct a ternary phase diagram.

### Others

Colormap of plolty, dataframe to html convertor, etc

## How to cite
If this repository facilitates your research, a citation is expected to link source codes and broadcast its usefulness to peers.

> Kai Pei. (2021). peikai/IEIs: Release 2.1 (v2.1). Zenodo. https://doi.org/10.5281/zenodo.6472078

[![DOI](https://zenodo.org/badge/228514002.svg)](https://zenodo.org/badge/latestdoi/228514002) 