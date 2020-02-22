import pandas as pd
from pymatgen import Composition, Element

# Merge binary tieline phases
tieline_dataframe = pd.read_csv('tables/Li/Li_tieline.csv')
tieline_Lithiumfree_dataframe = pd.read_csv('tables\Lithiumfree\Li_tieline_Lithiumfree_distinct.csv')
tieline_dataframe = tieline_dataframe.append(tieline_Lithiumfree_dataframe, ignore_index=True)
tieline_distinct_dataframe = tieline_dataframe.drop_duplicates()
tieline_distinct_dataframe.to_csv('Li_tieline_distinct.csv', index=False)

# remove noble gas
boolean_gas = tieline_distinct_dataframe.pretty_formula.apply(lambda x : True not in [e.is_noble_gas for e in Composition(x).elements])
no_nobel_gas_dataframe = tieline_distinct_dataframe[boolean_gas]

# screen phases without element Li
key_element = 'Li'
boolean_element = no_nobel_gas_dataframe.pretty_formula.apply(lambda x : Element(key_element) not in Composition(x).elements)
non_solution_phases_dataframe = no_nobel_gas_dataframe[boolean_element]
non_solution_phases_dataframe.reset_index(drop=True).to_csv('Li_tieline_non_solubility_and_gas.csv', index=False)