import pandas as pd 

data1 = pd.read_csv('tables/Li/Li_candidates_calc.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')
data2 = pd.read_csv('tables/Li/Li_candidates_exp.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')

data_merged = pd.merge(data1, data2, how='outer', on=['material_id', 'pretty_formula'])
data_merged.drop_duplicates(keep=False, inplace=True)
# data_merged.reset_index()

data1_contained = data_merged.append(data2)
data1_contained.drop_duplicates(keep=False, inplace=True)
# data1_contained.reset_index()

data2_contained = data_merged.append(data1)
data2_contained.drop_duplicates(keep=False, inplace=True)
# data2_contained.reset_index()

data1_contained.sort_index(axis=0).to_csv('tables/Li/set_difference.1.csv')
data2_contained.sort_index(axis=0).to_csv('tables/Li/set_difference.2.csv')
data_merged.sort_index(axis=0).to_csv('tables/Li/set_universal.0.csv')