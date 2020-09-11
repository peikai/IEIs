
import numpy as np
import pandas as pd
from tqdm import tqdm
from retrying import retry
from pymatgen import Composition, Element, MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, GrandPotentialPhaseDiagram

@retry(stop_max_attempt_number=10)
def FullChemicalPotentialWindow(target_phase, key_element):
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
        # prepare for binary systems, of which two endnodes tielined directly, like Li-Zr
        average_chempots.append(transition_chempots[0])
    average_chempots = np.round(average_chempots,3)

    boolean_list = []
    for chempot in average_chempots:
        # GrandPotentialPhaseDiagram works good even for binary systems to find stable phases
        pd_open = GrandPotentialPhaseDiagram(entries, {Element(key_element):chempot})
        stable_phases = [entry.name for entry in pd_open.stable_entries]
        boolean_list.append(target_phase in stable_phases)
    return(False not in boolean_list)


key_element = 'Li'
candidates_dataframe = pd.read_csv('tables/merged/tieline_without_solubility_and_gas_all_{element}.csv'.format(element=key_element))

tqdm.pandas(desc="pandas_apply_process")
candidates_dataframe.loc[:, 'FullWindow'] = candidates_dataframe.pretty_formula.progress_apply(FullChemicalPotentialWindow, key_element=key_element)
candidates_dataframe.to_csv('fullwindow_all_{element}.csv'.format(element=key_element), float_format='%.3f', index=False)
