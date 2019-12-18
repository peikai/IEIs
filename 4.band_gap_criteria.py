import pandas as pd
from pymatgen import MPRester

entry_id_list = pd.read_csv('tables/Li_candidate_ids.csv')['entry_id'].to_list()
formula_list = pd.read_csv('tables/Li_candidate_names.csv')['pretty_formula'].to_list()

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    # entry id is an alias of task id
    candidates_large = mpr.query(criteria={'pretty_formula':{'$in': formula_list}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical'])
    candidates_small = mpr.query(criteria={'task_id':{'$in': entry_id_list}, 'band_gap':{'$gte':3.0}}, properties=['material_id', 'pretty_formula', 'band_gap', 'e_above_hull', 'theoretical'])

candidates_large_dataframe = pd.DataFrame(candidates_large)
candidates_small_dataframe = pd.DataFrame(candidates_small)

candidates_large_dataframe = candidates_large_dataframe.loc[(candidates_large_dataframe['e_above_hull']==0) | (candidates_large_dataframe['theoretical'] == True)]
candidates_large_dataframe = candidates_large_dataframe.loc[(candidates_large_dataframe['band_gap']>=3.0)]

candidates_large_dataframe.sort_values(by=['pretty_formula'], inplace=True)
candidates_small_dataframe.sort_values(by=['pretty_formula'], inplace=True)

candidates_large_dataframe.to_csv('Li_candidates_large_range.csv', index=False)
candidates_small_dataframe.to_csv('Li_candidates_small_range.csv', index=False)