from pymatgen import MPRester
import pandas as pd


with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries_binary = mpr.query(criteria={'elements':{'$all': ['Na']}, 'nelements':2, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    entries_ternary = mpr.query(criteria={'elements':{'$all': ['Na']}, 'nelements':3, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    entries_quaternary = mpr.query(criteria={'elements':{'$all': ['Na']}, 'nelements':4, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    entries_others = mpr.query(criteria={'elements':{'$all': ['Na']}, 'nelements':{'$gte':5}, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    entries_all = mpr.query(criteria={'elements':{'$all': ['Na']}, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    

binary_dataframe = pd.DataFrame(entries_binary)
ternary_dataframe = pd.DataFrame(entries_ternary)
quaternary_dataframe = pd.DataFrame(entries_quaternary)
others_dataframe = pd.DataFrame(entries_others)
all_dataframe = pd.DataFrame(entries_all)

binary_dataframe.to_csv('Na_binary.csv', index=False)
ternary_dataframe.to_csv('Na_ternary.csv', index=False)
quaternary_dataframe.to_csv('Na_quaternary.csv', index=False)
others_dataframe.to_csv('Na_others.csv', index=False)
all_dataframe.to_csv('Na_all.csv', index=False)

