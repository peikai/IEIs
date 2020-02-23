from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram
import pandas
from tqdm import tqdm

# vertex phases should be stable
pure_materials = pandas.read_csv('tables/pure_element_materials.csv').pretty_formula
# remove itself
pure_materials = pure_materials[~pure_materials.isin(['K'])]
# get all binary chemical systems
pure_elements = pure_materials.apply(lambda x: Composition(x).elements.pop())
chemsys_series = pure_elements.apply(lambda x: 'K-'+x.name)
chemsys_series.drop_duplicates(inplace=True)
# chemsys_series.to_csv('Li_chemsys_pure_elements.csv', index=False, header=['chemsys'])

# query all entries in each binary chemsys
# and find chemsys whose vertex phases directly tielined together
tielined_pure_elements = list()
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    for chemsys in tqdm(chemsys_series, total=len(chemsys_series)):
        entries = mpr.get_entries_in_chemsys(chemsys)
        pd = PhaseDiagram(entries)
        if len(pd.facets) == 1:
            elements = chemsys.split('-')
            elements.remove('K')
            tielined_pure_elements.extend(elements)

tielined_pure_elements = pandas.Series(tielined_pure_elements)
tielined_pure_elements.to_csv('K_tielined_pure_elements.csv', index=False, header=['elements'])