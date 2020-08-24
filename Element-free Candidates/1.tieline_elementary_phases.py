import pandas as pd
from pymatgen import Composition, MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram
from tqdm import tqdm

key_element = 'Li'

# search for stable elementary phases
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.query(criteria={'nelements':1, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    
elementary_entries_dataframe = pd.DataFrame(entries)
elementary_entries_dataframe.to_csv('elementary_phases.csv', index=False)

elementary_entries = elementary_entries_dataframe['pretty_formula']
# remove itself
elementary_entries = elementary_entries[~elementary_entries.isin([key_element])]
# get all binary chemical systems
elements = elementary_entries.apply(lambda x: Composition(x).elements.pop())
chemsys_series = elements.apply(lambda x: key_element+'-'+x.name)
chemsys_series.drop_duplicates(inplace=True)

# find chemsys whose phase diagram contain only one facet
tielined_element_list = list()
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    for chemsys in tqdm(chemsys_series, total=len(chemsys_series)):
        entries = mpr.get_entries_in_chemsys(chemsys)
        phase_diagram = PhaseDiagram(entries)
        if len(phase_diagram.facets) == 1:
            elements = chemsys.split('-')
            elements.remove(key_element)
            tielined_element_list.extend(elements)

tielined_element_series = pd.Series(tielined_element_list)
tielined_element_series.to_csv('tielined_elementary_phases.csv', index=False, header=['elements'])
