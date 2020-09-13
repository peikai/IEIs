import pandas as pd
import numpy as np
from pymatgen import Element, MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

''' test why H contained in results
# with MPRester(api_key='7F7ezXky4RsUOimpr') as mpr:
#     candidates = mpr.query(criteria={'task_id':{'$in': ['mp-10172', 'mp-10173']}}, 
#                                     properties=['material_id', 'pretty_formula', 'band_gap', 'density', 'e_above_hull', 'theoretical', 'icsd_ids'])

# print(candidates)

key_element = 'Li'
tieline_dataframe = pd.read_csv('tables/{element}/tieline_distinct.csv'.format(element=key_element))

# remove noble gas
boolean_gas = tieline_dataframe.pretty_formula.apply(lambda x : True not in [e.is_noble_gas for e in Composition(x).elements])
no_nobel_gas_dataframe = tieline_dataframe[boolean_gas]

# screen phases without the key element
boolean_element = no_nobel_gas_dataframe.pretty_formula.apply(lambda x : Element(key_element) not in Composition(x).elements)
vanishing_solubility_phases_dataframe = no_nobel_gas_dataframe[boolean_element]
'''

'''
# test Li-free chemsys are all composed of metals, result: metal and noble gas
# Lifree_chemsys = pd.read_csv('tables\Li-free\chemsys.csv')
# Lifree_chemsys = pd.read_csv('tables/Na-free/chemsys.csv')
Lifree_chemsys = pd.read_csv('tables/K-free/chemsys.csv')
element_list = [chemsys.split('-') for chemsys in Lifree_chemsys.values[:,0]]
element_flatten_list = []
for each in element_list:
    element_flatten_list.extend(each)
element_flatten_set = set(element_flatten_list)
print(element_flatten_set)

element_list = list(element_flatten_set)
metal_element_boolen_list = [Element(e).is_metal for e in element_list]
print(metal_element_boolen_list)
for a, b in zip(element_list, metal_element_boolen_list):
    if a and b == False:
        print(a)
'''

# find out how many Li-containing crystals and inorganic crystal structures 
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    # candidates = mpr.query(criteria={'elements':{'$all': ['Li']}}, properties=['material_id', 'pretty_formula'])
    candidates = mpr.query(criteria={'e_above_hull':{'$gte':0}}, properties=['material_id', 'pretty_formula'])

'''
# check two elements grand potential phase diagram works well

key_element = 'Li'
target_phase = 'Zr'

chemsys = key_element + '-' + Composition(target_phase).chemical_system
with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)
    pd_closed = PhaseDiagram(entries)

transition_chempots = pd_closed.get_transition_chempots(Element(key_element))
# The exact mu value used to construct the plot for each range is 
# the average of the endpoints of the range, with the exception of the last range, 
# which is plotted at the value of the last endpoint minus 0.1.
# https://matsci.org/t/question-on-phase-diagram-app-chemical-potential/511
average_chempots = []
if len(transition_chempots) > 1:
    for i in range(len(transition_chempots)-1):
        ave = (transition_chempots[i] + transition_chempots[i+1])/2
        average_chempots.append(ave)
    average_chempots.append(transition_chempots[-1]-0.1)
elif len(transition_chempots) == 1:
    # for binary system, of which two phase nodes tielined directly, no intervening phases
    average_chempots.append(transition_chempots[0])
average_chempots = np.round(average_chempots,3)

boolean_list = []
for chempot in average_chempots:
    # GrandPotentialPhaseDiagram works good even for binary system, like Li-Zr to find stable phases
    pd_open = GrandPotentialPhaseDiagram(entries, {Element(key_element):chempot})
    stable_phases = [entry.name for entry in pd_open.stable_entries]
    boolean_list.append(target_phase in stable_phases)
print(False not in boolean_list)
'''