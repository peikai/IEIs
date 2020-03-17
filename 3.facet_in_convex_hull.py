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
    tieline_entries_dict = [{'material_id':phaseDiagram.qhull_entries[each].entry_id, 'pretty_formula':phaseDiagram.qhull_entries[each].name} for each in vertice_array]
    # # lithium: mp-135
    # tieline_phases.remove('mp-135')

    return(tieline_entries_dict)


chemsys_list = pd.read_csv('tables/Li/chemsys_all.csv').chemsys.to_list()
tieline_entries = list()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
        entries = mpr.get_entries_in_chemsys(chemsys)
        phaseDiagram = PhaseDiagram(entries)

        tieline_entries_dict = tieline_phases(phaseDiagram, key_element='Li')
        tieline_entries.extend(tieline_entries_dict)
        
tieline_dataframe = pd.DataFrame(tieline_entries)

tieline_dataframe.to_csv('Li_tieline.csv', index=False)

tieline_dataframe.drop_duplicates().to_csv('Li_tieline_distinct.csv', index=False)

tieline_dataframe.drop_duplicates('material_id').to_csv('Li_tieline_ids.csv', index=False)

tieline_dataframe.drop_duplicates('pretty_formula').to_csv('Li_tieline_names.csv', index=False)