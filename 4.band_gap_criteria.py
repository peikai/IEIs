import pandas as pd
from tqdm import tqdm
from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram


def recheck_e_above_hull(material_id, key_element):
    entry = mpr.get_entry_by_material_id(material_id)
    pretty_formula = entry.name
    chemsys = Composition(pretty_formula).chemical_system + '-' + key_element
    entries = mpr.get_entries_in_chemsys(chemsys)
    
    phase_diagram = PhaseDiagram(entries)
    e_above_hull = phase_diagram.get_e_above_hull(entry)
    # to avoid kind of values -1.77635683940025E-15, and -0.000 after rounded
    if 0 > e_above_hull >= -phase_diagram.numerical_tol:
        e_above_hull = 0.0

    return(e_above_hull)


tqdm.pandas(desc="pandas_apply_process:")

entry_id_list = pd.read_csv('tables/K/K_tieline_ids.csv')['entry_id'].to_list()
formula_list = pd.read_csv('tables/K/K_tieline_names.csv')['pretty_formula'].to_list()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    # entry id is an alias of task id
    candidates_all = mpr.query(criteria={'pretty_formula':{'$in': formula_list}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical', 'icsd_ids'])
    candidates_calc = mpr.query(criteria={'task_id':{'$in': entry_id_list}, 'band_gap':{'$gte':3.0}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical', 'icsd_ids'])

candidates_all_dataframe = pd.DataFrame(candidates_all)
candidates_calc_dataframe = pd.DataFrame(candidates_calc)

# Due to bug in Materials Project database, e_above_hull needs to be checked
# https://discuss.matsci.org/t/materials-project-database-release-log/1609
# progress_apply instead of apply to show process bar
# https://github.com/tqdm/tqdm

candidates_all_dataframe['e_above_hull'] = candidates_all_dataframe.material_id.progress_apply(recheck_e_above_hull, key_element='K')
candidates_calc_dataframe['e_above_hull'] = candidates_calc_dataframe.material_id.progress_apply(recheck_e_above_hull, key_element='K')

candidates_all_dataframe = candidates_all_dataframe.round({'band_gap':3,'e_above_hull':3})
candidates_calc_dataframe = candidates_calc_dataframe.round({'band_gap':3,'e_above_hull':3})

candidates_all_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['e_above_hull']==0) | (candidates_all_dataframe['theoretical'] == False)]
candidates_all_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['band_gap']>=3.0)]

candidates_exp_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['theoretical'] == False)]

candidates_all_dataframe.sort_values(by=['pretty_formula'], inplace=True)
candidates_calc_dataframe.sort_values(by=['pretty_formula'], inplace=True)
candidates_exp_dataframe.sort_values(by=['pretty_formula'], inplace=True)

# candidates_all_dataframe.reset_index(inplace=True)
# candidates_calc_dataframe.reset_index(inplace=True)
# candidates_exp_dataframe.reset_index(inplace=True)

candidates_all_dataframe.to_csv('K_candidates_all.csv', float_format='%.3f', index=False)
candidates_calc_dataframe.to_csv('K_candidates_calc.csv', float_format='%.3f', index=False)
candidates_exp_dataframe.to_csv('K_candidates_exp.csv', float_format='%.3f', index=False)