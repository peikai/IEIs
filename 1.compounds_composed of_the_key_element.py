from pymatgen import MPRester
import pandas as pd


with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries_binary = mpr.query(criteria={'elements':{'$all': ['Li']}, 'nelements':2}, properties=['material_id', 'pretty_formula'])
    entries_ternary = mpr.query(criteria={'elements':{'$all': ['Li']}, 'nelements':3}, properties=['material_id', 'pretty_formula'])
    entries_quaternary = mpr.query(criteria={'elements':{'$all': ['Li']}, 'nelements':4}, properties=['material_id', 'pretty_formula'])
    entries_others = mpr.query(criteria={'elements':{'$all': ['Li']}, 'nelements':{'$gte':5}}, properties=['material_id', 'pretty_formula'])

binary_dataframe = pd.DataFrame(entries_binary)
ternary_dataframe = pd.DataFrame(entries_ternary)
quaternary_dataframe = pd.DataFrame(entries_quaternary)
others_dataframe = pd.DataFrame(entries_others)

binary_dataframe.to_csv('Li_binary.csv', index=False)
ternary_dataframe.to_csv('Li_ternary.csv', index=False)
quaternary_dataframe.to_csv('Li_quaternary.csv', index=False)
others_dataframe.to_csv('Li_others.csv', index=False)



