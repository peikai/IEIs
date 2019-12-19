from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import (CompoundPhaseDiagram, PDEntry,
                                             PDPlotter, PhaseDiagram, get_facets)
import numpy as np
import pandas as pd
from tqdm import tqdm


def tieline_phases(phaseDiagram, key_element):
    # find its coordinate in phase diagram
    comp = Composition(key_element)
    c = phaseDiagram.pd_coords(comp)
    # find facets that key element acted as a vertice
    # vertices of facets are stable phases
    facet_list = list()
    for f, s in zip(phaseDiagram.facets, phaseDiagram.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_list.append(f)

    # find other phases in those facets
    vertice_array = np.array(facet_list).flatten()
    tieline_phase_ids = list(set(phaseDiagram.qhull_entries[each].entry_id for each in vertice_array))
    tieline_phase_name = list(set(phaseDiagram.qhull_entries[each].name for each in vertice_array))
    # # lithium: mp-135
    # tieline_phases.remove('mp-135')

    return(tieline_phase_ids, tieline_phase_name)


chemsys_list = pd.read_csv('tables/K/chemsys_all.csv').chemsys.to_list()
candidate_id_set = set()
candidate_name_set = set()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    # candidates = mpr.query(criteria={'pretty_formula':{'$in':formula_list}, 'band_gap': {'$lte': 2}}, properties=['material_id', 'pretty_formula'])
    for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
        entries = mpr.get_entries_in_chemsys(chemsys, compatible_only=False)
        # entries = mpr.get_entries({'chemsys':{'$in':chemsys_list}})

        phaseDiagram = PhaseDiagram(entries)
        id_list, formula_list = tieline_phases(phaseDiagram, key_element='K')
        candidate_id_set.update(id_list)
        candidate_name_set.update(formula_list)

candidate_id_dataframe = pd.DataFrame(candidate_id_set, columns=['entry_id'])
candidate_name_dataframe = pd.DataFrame(candidate_name_set, columns=['pretty_formula'])
candidate_id_dataframe.to_csv('K_candidate_ids.csv', index=False)
candidate_name_dataframe.to_csv('K_candidate_names.csv', index=False)