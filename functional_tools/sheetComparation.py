import pandas as pd 


# [option-1] Archive result A and present result B
# set1 = pd.read_csv('Archive-2020.11.21/tables/Merged/candidates_all_K.csv', usecols=['material_id', 'pretty_formula'])
# set2 = pd.read_csv('Tables/K/candidates.csv', usecols=['material_id', 'pretty_formula'])

# [option-2] Set A and subset B
set1 = pd.read_csv('Tables/Na/candidates.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')
set2 = pd.read_csv('Tables/Li/candidates.csv', usecols=['material_id', 'pretty_formula'], index_col='material_id')

# A U B - A ∩ B
set_difference = pd.merge(set1, set2, how='outer', on=['material_id', 'pretty_formula'])
set_difference.drop_duplicates(keep=False, inplace=True)
# set_merged.reset_index()

# A ∩ B
set_intersection = pd.merge(set1, set2, how='inner', on=['material_id', 'pretty_formula'])

# A - A ∩ B
set1_contains_only = set1.append(set_intersection)
set1_contains_only = set1_contains_only.drop_duplicates(keep=False)

# B - A ∩ B
set2_contains_only = set2.append(set_intersection)
set2_contains_only = set2_contains_only.drop_duplicates(keep=False)

set_difference.sort_index(axis=0).to_csv('set_difference.csv')
set1_contains_only.sort_index(axis=0).to_csv('set_difference.1.csv')
set2_contains_only.sort_index(axis=0).to_csv('set_difference.2.csv')
set_intersection.sort_index(axis=0).to_csv('set_intersection.csv')
