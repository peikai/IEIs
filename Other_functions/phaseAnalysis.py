import pandas as pd
from pymatgen.core import Composition, Element


def metals_only(phase):
    elements_list = Composition(phase).elements
    metal_boolean_list = [Element(e).is_metal for e in elements_list]
    return False not in metal_boolean_list

key_element = 'Li'
phase_list = pd.read_csv('Tables/{element}/tieline_distinct.csv'.formate(element=key_element), usecols=['pretty_formula'])
# marking those alloys comprise only with metals, thus we can analyze the tpye of the rest phases convinently
phase_list['metalsOnly'] = phase_list.pretty_formula.apply(metals_only)
phase_list = phase_list.loc[phase_list['metalsOnly'] == False]
phase_list.to_csv('phaseAnalysis.csv', index=False)
