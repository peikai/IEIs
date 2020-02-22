from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram
import numpy as np
import pandas as pd
from tqdm import tqdm


def drop_subset_chemsys(chemsys_series):
    # split chemsys str to find element-wise subset relations
    chemsys_series = chemsys_series.apply(str.split, sep='-')
    # prepare set for subset function afterward
    chemsys_series = chemsys_series.apply(set)
    # prepare a list for iterations
    chemsys_list = chemsys_series.to_list()
    # prepare a dataframe to store other info
    chemsys_dataframe = pd.DataFrame(chemsys_series, columns=['pretty_formula'])
    chemsys_dataframe['distinct'] = 'null'
    # like, A-B is not a subset of any chemsys, then store A-B
    for index, row in chemsys_series.iteritems():
        boolean =  [row.issubset(chemsys) for chemsys in chemsys_list]
        # count including itself
        if not boolean.count(True) > 1:
            chemsys_dataframe.loc[index, 'distinct'] = True

    chemsys_distinct_dataframe = chemsys_dataframe.loc[chemsys_dataframe['distinct'] == True]
    chemsys_distinct_dataframe.loc[:, 'chemsys'] = chemsys_distinct_dataframe.pretty_formula.apply(lambda x : '-'.join(x))
    chemsys_distinct_series = chemsys_distinct_dataframe['chemsys']
    return chemsys_distinct_series


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
    tieline_entries_dict = [{'entry_id':phaseDiagram.qhull_entries[each].entry_id, 'pretty_formula':phaseDiagram.qhull_entries[each].name} for each in vertice_array]
    # # lithium: mp-135
    # tieline_phases.remove('mp-135')

    return(tieline_entries_dict)

# find entries in Lithium-compounds-free Lithium phases diagrams
elements_in_periodic_table = pd.read_csv('tables\element_list.csv')
## elements consist of tielined pure elements
tielined_elements = pd.read_csv('tables\Lithiumfree\Li_tielined_pure_elements.csv')
## other elments
merged = elements_in_periodic_table.append(tielined_elements)
other_elements = merged.drop_duplicates(keep=False)
other_elements.reset_index(inplace=True, drop=True)
## build a large chemsys containing all tielined pure elements, deprecated
## chemsys = '-'.join(elements)

tielined_elements_list = tielined_elements.elements.to_list()
other_elements_list = other_elements.elements.to_list()
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.query(criteria={'elements':{'$in': tielined_elements_list, '$nin':other_elements_list}, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])

entries = pd.DataFrame(entries)
entries.to_csv('entries_Lithiumfree.csv', index=False)

# find chemical systems of entries (tielined pure elements have been included), then remove subsets
## join element in chemsys str, then drop duplicated chemsys
chemsys_all = entries.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
chemsys_all.drop_duplicates(inplace=True)

## combine with Li into chemical systems, and sort elements of each chemical system in alphabetical order
chemsys_all = chemsys_all.apply(lambda x: 'Li-'+x)
chemsys_all = chemsys_all.apply(lambda x: '-'.join(sorted(x.split('-'))))
chemsys_distinct = drop_subset_chemsys(chemsys_all)
chemsys_distinct.to_csv('chemsys_Lithiumfree.csv', header=['chemsys'], index=False)

# construct phase diagrams and search tielined phases 
chemsys_list = chemsys_distinct.to_list()
tieline_entries = list()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    for chemsys in tqdm(chemsys_list, total=len(chemsys_list)):
        entries = mpr.get_entries_in_chemsys(chemsys)
        phaseDiagram = PhaseDiagram(entries)
        tieline_entries_dict = tieline_phases(phaseDiagram, key_element='Li')
        tieline_entries.extend(tieline_entries_dict)
        
tieline_dataframe = pd.DataFrame(tieline_entries)
## to compare results
# tieline_dataframe.to_csv('Li_tieline_Lithiumfree.csv', index=False)
tieline_dataframe.drop_duplicates().to_csv('Li_tieline_Lithiumfree_distinct.csv', index=False)
tieline_dataframe.drop_duplicates('entry_id').to_csv('Li_tieline_Lithiumfree_ids.csv', index=False)
tieline_dataframe.drop_duplicates('pretty_formula').to_csv('Li_tieline_Lithiumfree_names.csv', index=False)
