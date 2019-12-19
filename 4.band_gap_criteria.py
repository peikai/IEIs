import pandas as pd
from pymatgen import MPRester

entry_id_list = pd.read_csv('tables/Na/Na_candidate_ids.csv')['entry_id'].to_list()
formula_list = pd.read_csv('tables/Na/Na_candidate_names.csv')['pretty_formula'].to_list()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    # entry id is an alias of task id
    candidates_all = mpr.query(criteria={'pretty_formula':{'$in': formula_list}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical'])
    candidates_calc = mpr.query(criteria={'task_id':{'$in': entry_id_list}, 'band_gap':{'$gte':3.0}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical'])

candidates_all_dataframe = pd.DataFrame(candidates_all)
candidates_calc_dataframe = pd.DataFrame(candidates_calc)

candidates_all_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['e_above_hull']==0) | (candidates_all_dataframe['theoretical'] == True)]
candidates_all_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['band_gap']>=3.0)]

candidates_exp_dataframe = candidates_all_dataframe.loc[(candidates_all_dataframe['theoretical'] == False)]

candidates_all_dataframe.sort_values(by=['pretty_formula'], inplace=True)
candidates_calc_dataframe.sort_values(by=['pretty_formula'], inplace=True)
candidates_exp_dataframe.sort_values(by=['pretty_formula'], inplace=True)

candidates_all_dataframe.to_csv('Na_candidates_all.csv', index=False)
candidates_calc_dataframe.to_csv('Na_candidates_calc.csv', index=False)
candidates_exp_dataframe.to_csv('Na_candidates_exp.csv', index=False)