
import numpy as np
import pandas as pd
from tqdm import tqdm
from pymatgen import Composition, Element, MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

key_element = 'Na'
target_phase = 'BeO'

chemsys = key_element + '-' + Composition(target_phase).chemical_system
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)

for facet in pd.facets:
    chempots = pd._get_facet_chempots(facet)
    namelist = [pd.qhull_entries[i].name for i in facet]
    complist = [pd.qhull_entries[i].composition for i in facet]
    energylist = [pd.qhull_entries[i].energy_per_atom for i in facet]
    m = [[c.get_atomic_fraction(e) for e in pd.elements] for c in
            complist]

    chempots = np.linalg.solve(m, energylist)
    chempots = dict(zip(pd.elements, chempots))
    mu = chempots[Element(key_element)]
    print('-'.join(namelist))
    print(np.round(mu,3))

# print(pd.get_chempot_range_map([Element(key_element)]))
chempotlist = np.round(pd.get_transition_chempots(Element(key_element)), 3)
print(chempotlist)