from pymatgen import MPRester, Composition, Element
from pymatgen.analysis.phase_diagram import PhaseDiagram
import numpy as np
import pandas as pd
from tqdm import tqdm
from retrying import retry
import eventlet

def drop_subset_chemsys(chemsys_series):
    # split chemsys str to find element-wise subset relations
    chemsys_series = chemsys_series.apply(str.split, sep='-')
    # prepare set for subset function afterward
    chemsys_series = chemsys_series.apply(set)
    # prepare a list for iterations
    chemsys_list = chemsys_series.to_list()
    # prepare a dataframe to store other info
    chemsys_dataframe = chemsys_series.to_frame(name='elements')
    ## chemsys_dataframe = pd.DataFrame(chemsys_series, columns=['pretty_formula'])
    chemsys_dataframe['distinct'] = 'null'
    # like, A-B is not a subset of any chemsys, then store A-B
    for index, row in chemsys_series.iteritems():
        boolean =  [row.issubset(chemsys) for chemsys in chemsys_list]
        # count including itself
        if not boolean.count(True) > 1:
            chemsys_dataframe.loc[index, 'distinct'] = True

    chemsys_distinct_dataframe = chemsys_dataframe.loc[chemsys_dataframe['distinct'] == True]
    chemsys_distinct_dataframe.loc[:, 'chemsys'] = chemsys_distinct_dataframe.elements.apply(lambda x : '-'.join(x))
    chemsys_distinct_series = chemsys_distinct_dataframe['chemsys']
    chemsys_distinct_series = chemsys_distinct_series.apply(lambda x: '-'.join(sorted(x.split('-'))))
    return chemsys_distinct_series


def tieline_phases(phaseDiagram, key_element):
    # find its coordinate in phase diagram
    comp = Composition(key_element)
    c = phaseDiagram.pd_coords(comp)
    # find facets that key element acted as a vertice
    # vertices of facets are stable phases
    facet_index_list = list()
    for f, s in zip(phaseDiagram.facets, phaseDiagram.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_index_list.append(f)
    # covert index list to entry list, for example, ['mp-135', 'mp-2049', 'mp-2283', 'mp-929']
    facet_entries_list = list()
    qhull_entries = phaseDiagram.qhull_entries
    for facet in facet_index_list:
        facet_entries = [qhull_entries[index].entry_id for index in facet]
        facet_entries.sort()
        facet_entries_list.append(facet_entries)
    # find other phases in those facets
    vertice_array = np.array(facet_index_list).flatten()
    tieline_entries_list = [{'material_id':qhull_entries[each].entry_id, 'pretty_formula':qhull_entries[each].name} for each in vertice_array]

    return(facet_entries_list, tieline_entries_list)


@retry(stop_max_attempt_number=20)
def get_phase_diagram_in_chemsys(chemsys):
    eventlet.monkey_patch() 
    with eventlet.Timeout(120, True):
        try:
            with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
                entries = mpr.get_entries_in_chemsys(chemsys)
                phase_diagram = PhaseDiagram(entries)
        except:
            print('MRPestError, retry!')
    return phase_diagram

key_element = 'Li'
# find entries in Lithium-compounds-free Lithium phases diagrams
elements_in_periodic_table = pd.read_csv('tables\element_list.csv')
## elements consist of tielined pure elements
tielined_elements = pd.read_csv('tables/{element}-free/tielined_elementary_phases.csv'.format(element=key_element))
## other elments
merged = elements_in_periodic_table.append(tielined_elements)
other_elements = merged.drop_duplicates(keep=False)
other_elements.reset_index(inplace=True, drop=True)
## perform the query
tielined_elements_list = tielined_elements.elements.to_list()
other_elements_list = other_elements.elements.to_list()
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.query(criteria={'elements':{'$in': tielined_elements_list, '$nin':other_elements_list}, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])

entries = pd.DataFrame(entries)
entries.to_csv('entries.csv', index=False)

# find chemical systems of entries (tielined pure elements have been included), then remove subsets
## join element in chemsys str, then drop duplicated chemsys
chemsys_all = entries.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
chemsys_all.drop_duplicates(inplace=True)

## combine with Li into chemical systems, and sort elements of each chemical system in alphabetical order
## warning: once add Li as a vertex, Lithium compounds may occur in phase diagrams
chemsys_all = chemsys_all.apply(lambda x: key_element+'-'+x)
chemsys_distinct = drop_subset_chemsys(chemsys_all)
chemsys_distinct.to_csv('chemsys.csv', header=['chemsys'], index=False)

# construct phase diagrams and search tielined phases 
chemsys_list = chemsys_distinct.to_list()
tieline_entries = list()
facet_entries = list()

for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
    phase_diagram = get_phase_diagram_in_chemsys(chemsys)
    facet_entries_list, tieline_entries_list = tieline_phases(phase_diagram, key_element=key_element)
    facet_entries.extend(facet_entries_list)
    tieline_entries.extend(tieline_entries_list)

# save simplexes to make statistics
facet_dataframe = pd.DataFrame(facet_entries)
facet_dataframe.drop_duplicates().to_csv('facets_distinct.csv', index=False)
# save phases have a tie-line with Lithium
tieline_dataframe = pd.DataFrame(tieline_entries)
# some Lithium compounds are also mixed in, kick them out; we only need Li-free compounds
boolean_element = tieline_dataframe.pretty_formula.apply(lambda x : Element(key_element) not in Composition(x).elements)
tieline_dataframe = tieline_dataframe[boolean_element]
# number of tielined entries may not be the same with queried entries, see Ba-Na-Li system
tieline_dataframe.drop_duplicates().to_csv('tieline_distinct.csv', index=False)