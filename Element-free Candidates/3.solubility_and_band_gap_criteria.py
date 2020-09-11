import pandas as pd
from tqdm import tqdm
from retrying import retry
from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram

@retry(stop_max_attempt_number=10)
def recheck_e_above_hull(material_id, key_element):
    try:
        with MPRester(api_key='7F7ezXky4RsUOimpr') as mpr:
            entry = mpr.get_entry_by_material_id(material_id)
            pretty_formula = entry.name
            chemsys = Composition(pretty_formula).chemical_system + '-' + key_element
            entries = mpr.get_entries_in_chemsys(chemsys)
    except:
        print('MRPestError, retry!')
        
    phase_diagram = PhaseDiagram(entries)
    e_above_hull = phase_diagram.get_e_above_hull(entry)
    # to avoid kind of values -1.77635683940025E-15, and -0.000 after rounded
    if 0 > e_above_hull >= -phase_diagram.numerical_tol:
        e_above_hull = 0.0

    return(e_above_hull)


key_element='Li'

tieline_dataframe = pd.read_csv('tables/{element}-free/tieline_distinct.csv'.format(element=key_element))
# remove nobel gas
boolean_gas = tieline_dataframe.pretty_formula.apply(lambda x : True not in [e.is_noble_gas for e in Composition(x).elements])
tieline_dataframe = tieline_dataframe[boolean_gas]
tieline_dataframe.drop_duplicates(inplace=True)
tieline_dataframe.to_csv('tieline_distinct_without_gas.csv', index=False)
# band gap >= 3eV
material_id_list = tieline_dataframe['material_id'].to_list()
with MPRester(api_key='7F7ezXky4RsUOimpr') as mpr:
    # entry id is an alias of task id
    candidates = mpr.query(criteria={'task_id':{'$in': material_id_list}, 'band_gap':{'$gte':3.0}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical', 'icsd_ids'])
    # empty!! no one can meet the requirements.
    
candidates_dataframe = pd.DataFrame(candidates, columns=['material_id', 'pretty_formula', 'theoretical', 'band_gap', 'density', 'e_above_hull', 'icsd_ids'])

# progress_apply instead of apply to show process bar
# https://github.com/tqdm/tqdm
# Due to bug in Materials Project database, e_above_hull needs to be checked
# https://discuss.matsci.org/t/materials-project-database-release-log/1609

tqdm.pandas(desc="pandas_apply_process_1st")
candidates_dataframe['e_above_hull'] = candidates_dataframe.material_id.progress_apply(recheck_e_above_hull, key_element=key_element)
candidates_dataframe = candidates_dataframe.round({'band_gap':3,'density':3,'e_above_hull':3})
candidates_dataframe.sort_values(by=['theoretical', 'band_gap'], ascending=[True, False], inplace=True)
candidates_dataframe.to_csv('candidates.csv', float_format='%.3f', index=False)