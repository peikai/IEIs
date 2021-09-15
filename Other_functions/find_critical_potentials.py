
import numpy as np
import pandas as pd
from pymatgen import Composition, Element, MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram


key_element = 'Li'
target_phase = 'BeO'

chemsys = key_element + '-' + Composition(target_phase).chemical_system
with MPRester(api_key='') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)

for facet in pd.facets:
    # read-made, chempots = pd._get_facet_chempots(facet)
    # implement again
    namelist = [pd.qhull_entries[i].name for i in facet]
    complist = [pd.qhull_entries[i].composition for i in facet]
    energylist = [pd.qhull_entries[i].energy_per_atom for i in facet]
    m = [[c.get_atomic_fraction(e) for e in pd.elements] for c in
            complist]
    # solve a linear matrix equation, sum(μ*n) = E
    chempots = np.linalg.solve(m, energylist)
    chempots = dict(zip(pd.elements, chempots))
    mu = chempots[Element(key_element)]
    # print chemical potential of key element in each equilibrium
    print('-'.join(namelist)+': '+str(np.round(mu,3)))

# print transition points of phase equilibria in terms of chemical potential
chempotlist = np.round(pd.get_transition_chempots(Element(key_element)), 3)
print(chempotlist)
