from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import (CompoundPhaseDiagram, PDEntry,
                                             PDPlotter, PhaseDiagram, get_facets)
import numpy as np


def tieline_phases(pd, key_element):
    # find its coordinate in phase diagram
    comp = Composition(key_element)
    c = pd.pd_coords(comp)
    # find facets that key element acted as a vertice
    facet_list = list()
    for f, s in zip(pd.facets, pd.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_list.append(f)

    # find other phases in those facets
    vertice_array = np.array(facet_list).flatten()
    tieline_phases = list(set(pd.qhull_entries[each].name for each in vertice_array))
    tieline_phases.remove('Li')

    return(tieline_phases)


with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    candidates = mpr.query(criteria={'pretty_formula':{'$in':formula_list}, 'band_gap': {'$lte': 2}}, properties=['material_id', 'pretty_formula'])
    entries = mpr.get_entries_in_chemsys('Li-Al-N')

    pd = PhaseDiagram(entries)
    formula_list = tieline_phases(pd, key_element='Li')
    

# find the vertice that appear three times, which will be Li
# main_vertice_id = np.argmax(np.bincount(vertice_array.flatten()))

# plotter = PDPlotter(pd)
# plotter.show()

# data = np.array([[e.composition.get_atomic_fraction(el) for el in pd.elements] + [e.energy_per_atom] for e in pd.stable_entries])
# print(len(data[:,1:]))

# print(len(pd.qhull_entries))
# print(len(pd.qhull_data))