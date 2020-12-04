import pandas as pd 

# Compare any couple of two sets
# to obtain the intersection set, difference set 
# and difference sets for individual counterpart, like A contains, B does not contain
# [usage-1] Archive result A and present result B
# [usage-2] Set A and subset B
# ...

# set1 = pd.read_csv('Archive-2020.11.21/tables/Merged/candidates_all_K.csv', usecols=['material_id', 'pretty_formula'])
# set2 = pd.read_csv('Tables/K/candidates.csv', usecols=['material_id', 'pretty_formula'])

set1 = pd.read_csv('Tables\set_intersection_LEI&KEI.csv', float_precision='round_trip')
set2 = pd.read_csv('Tables\set_intersection_LEI&NEI.csv', float_precision='round_trip')

# A U B - A ∩ B
set_difference = pd.merge(set1, set2, how='outer')
set_difference.drop_duplicates(keep=False, inplace=True)

# A ∩ B
set_intersection = pd.merge(set1, set2, how='inner')

# A - A ∩ B
set1_contains_only = set1.append(set_intersection)
set1_contains_only = set1_contains_only.drop_duplicates(keep=False)

# B - A ∩ B
set2_contains_only = set2.append(set_intersection)
set2_contains_only = set2_contains_only.drop_duplicates(keep=False)

set_difference.sort_index(axis=0).to_csv('set_difference.csv', index=False)
set1_contains_only.sort_index(axis=0).to_csv('set_difference.1.csv', index=False)
set2_contains_only.sort_index(axis=0).to_csv('set_difference.2.csv', index=False)
set_intersection.sort_index(axis=0).to_csv('set_intersection.csv', index=False)
