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

tieline_phases_dataframe = pd.read_csv('tables/Lithiumfree/Li_tieline_Lithiumfree_non_solubility_and_gas.csv')
entry_id_list = tieline_phases_dataframe['entry_id'].to_list()

with MPRester(api_key='7F7ezXky4RsUOimpr') as mpr:
    # entry id is an alias of task id
    candidates_calc = mpr.query(criteria={'task_id':{'$in': entry_id_list}, 'band_gap':{'$gte':3.0}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical', 'icsd_ids'])
    # empty!! no one can meet the requirements.
    
candidates_calc_dataframe = pd.DataFrame(candidates_calc, columns=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical', 'icsd_ids'])

# progress_apply instead of apply to show process bar
# https://github.com/tqdm/tqdm
# Due to bug in Materials Project database, e_above_hull needs to be checked
# https://discuss.matsci.org/t/materials-project-database-release-log/1609
tqdm.pandas(desc="pandas_apply_process_1st")
candidates_calc_dataframe['e_above_hull'] = candidates_calc_dataframe.material_id.progress_apply(recheck_e_above_hull, key_element=key_element)
candidates_calc_dataframe = candidates_calc_dataframe.round({'band_gap':3,'e_above_hull':3})
candidates_calc_dataframe.sort_values(by=['theoretical', 'band_gap'], ascending=[True, False], inplace=True)
candidates_calc_dataframe.to_csv('Li_candidates_Lithiumfree_calc.csv', float_format='%.3f', index=False)