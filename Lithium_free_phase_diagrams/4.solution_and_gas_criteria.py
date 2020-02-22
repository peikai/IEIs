import pandas as pd
from pymatgen import Composition, Element

tieline_Lithiumfree_dataframe = pd.read_csv('tables\Sodiumfree\Na_tieline_Sodiumfree_distinct.csv')

# remove noble gas
boolean_gas = tieline_Lithiumfree_dataframe.pretty_formula.apply(lambda x : True not in [e.is_noble_gas for e in Composition(x).elements])
non_nobel_gas_dataframe = tieline_Lithiumfree_dataframe[boolean_gas]

non_nobel_gas_dataframe.to_csv('Na_tieline_Sodiumfree_non_gas.csv', index=False)