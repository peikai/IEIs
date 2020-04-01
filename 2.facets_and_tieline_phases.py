from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram
import numpy as np
import pandas as pd
from tqdm import tqdm


def tieline_phases(phaseDiagram, key_element):
    # find coordinates of the key element in phase diagram
    comp = Composition(key_element)
    c = phaseDiagram.pd_coords(comp)
    # find facets that key element acted as a vertice
    facet_index_list = list()
    for f, s in zip(phaseDiagram.facets, phaseDiagram.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_index_list.append(f)
    # find phases in facets
    vertice_array = np.array(facet_index_list).flatten()
    qhull_entries = phaseDiagram.qhull_entries
    tieline_entries_dict = [{'material_id':qhull_entries[each].entry_id, 'pretty_formula':qhull_entries[each].name} for each in vertice_array]
    # covert index list to entry list and record retrieved simplexes
    facet_entries_list = list()
    for facet in facet_index_list:
        facet_entries = [qhull_entries[index].entry_id for index in facet]
        facet_entries.sort()
        facet_entries_list.append(facet_entries)

    return(facet_entries_list, tieline_entries_dict)


key_element = 'Li'
chemsys_list = pd.read_csv('tables/{element}/chemsys.csv'.format(element=key_element)).chemsys.to_list()
# record phases that have a tie-line with the key element as well as the simplex they belong to
tieline_entries = list()
facet_entries = list()
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
        entries = mpr.get_entries_in_chemsys(chemsys)
        phaseDiagram = PhaseDiagram(entries)
        facet_entries_list, tieline_entries_dict = tieline_phases(phaseDiagram, key_element=key_element)
        facet_entries.extend(facet_entries_list)
        tieline_entries.extend(tieline_entries_dict)
        
tieline_dataframe = pd.DataFrame(tieline_entries).drop_duplicates()
facet_dataframe = pd.DataFrame(facet_entries).drop_duplicates()
tieline_dataframe.to_csv('tieline_distinct.csv', index=False)
facet_dataframe.to_csv('facets_distinct.csv', index=False)