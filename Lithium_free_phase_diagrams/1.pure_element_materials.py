from pymatgen import MPRester
import pandas as pd


with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries_pure = mpr.query(criteria={'nelements':1, 'e_above_hull':{'$eq':0}}, properties=['material_id', 'pretty_formula'])
    
dataframe = pd.DataFrame(entries_pure)
dataframe.to_csv('pure_element_materials.csv', index=False)

