import pandas as pd 

data1 = pd.read_csv('entries.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')
data2 = pd.read_csv('tieline_distinct.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')

# A U B - A ∩ B
data_merged = pd.merge(data1, data2, how='outer', on=['material_id', 'pretty_formula'])
data_merged.drop_duplicates(keep=False, inplace=True)
# data_merged.reset_index()

# A - A ∩ B
data1_intersect_data2 = pd.merge(data1, data2, how='inner', on=['material_id', 'pretty_formula'])
data1_contained = data1.append(data1_intersect_data2)
data1_contained = data1_contained.drop_duplicates(keep=False)

# B - A ∩ B
data2_contained = data2.append(data1_intersect_data2)
data2_contained = data2_contained.drop_duplicates(keep=False)

data_merged.sort_index(axis=0).to_csv('set_universal.0.csv')
data1_contained.sort_index(axis=0).to_csv('set_difference.1.csv')
data2_contained.sort_index(axis=0).to_csv('set_difference.2.csv')
