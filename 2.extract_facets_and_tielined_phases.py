import numpy as np
import pandas as pd
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Composition
from pymatgen.ext.matproj import MPRester
from retrying import retry
from tqdm import tqdm


def tieline_phases(phaseDiagram, key_element):
    # find its coordinate in phase diagram.
    comp = Composition(key_element)
    c = phaseDiagram.pd_coords(comp)
    # find facets that key element acted as a vertice.
    # vertices of facets are stable phases.
    facet_index_list = list()
    for f, s in zip(phaseDiagram.facets, phaseDiagram.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_index_list.append(f)
    # covert index list to entry list, for example, ['mp-135', 'mp-2049', 'mp-2283', 'mp-929'].
    facet_entries_list = list()
    qhull_entries = phaseDiagram.qhull_entries
    for facet in facet_index_list:
        facet_entries = [qhull_entries[index].entry_id for index in facet]
        facet_entries.sort()
        facet_entries_list.append(facet_entries)
    # find other phases in those facets.
    vertice_array = np.array(facet_index_list).flatten()
    tieline_entries_list = [{'material_id':qhull_entries[each].entry_id, 'pretty_formula':qhull_entries[each].name} for each in vertice_array]

    return(facet_entries_list, tieline_entries_list)


@retry(stop_max_attempt_number=20)
@timeout_decorator.timeout(300)
def get_phase_diagram_in_chemsys(chemsys):
    with MPRester(api_key='') as mpr:
        # using GGA and GGA+U mixed scheme as default, namely compatible_only=True
        entries = mpr.get_entries_in_chemsys(chemsys)
            
    phase_diagram = PhaseDiagram(entries)
    return phase_diagram

key_element = 'Li'

chemsys_list = pd.read_csv('Tables/{element}/chemsys_distinct.csv'.format(element=key_element)).chemsys.to_list()
# construct phase diagrams, search tielined phases, record targeted simplexes.
tieline_entries = list()
facet_entries = list()

for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
    phase_diagram = get_phase_diagram_in_chemsys(chemsys)
    facet_entries_list, tieline_entries_list = tieline_phases(phase_diagram, key_element=key_element)
    facet_entries.extend(facet_entries_list)
    tieline_entries.extend(tieline_entries_list)

# save simplexes to make statistics.
facet_dataframe = pd.DataFrame(facet_entries)
facet_dataframe.drop_duplicates().to_csv('Tables/{element}/facets_distinct.csv'.format(element=key_element), index=False)
# save phases have a tie-line with the key phase, like Li_BCC.
tieline_dataframe = pd.DataFrame(tieline_entries)
tieline_dataframe.drop_duplicates().to_csv('Tables/{element}/tieline_distinct.csv'.format(element=key_element), index=False)
