from pymatgen import Composition
import pandas as pd


entries_binary = pd.read_csv('tables/Li_binary.csv', usecols=['pretty_formula'])
entries_ternary = pd.read_csv('tables/Li_ternary.csv', usecols=['pretty_formula'])
entries_quaternary = pd.read_csv('tables/Li_quaternary.csv', usecols=['pretty_formula'])
entries_others = pd.read_csv('tables/Li_others.csv', usecols=['pretty_formula'])

element_binary = entries_binary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
element_ternary = entries_ternary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
element_quaternary = entries_quaternary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
element_others = entries_others.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))

element_binary.drop_duplicates(inplace=True)
element_ternary.drop_duplicates(inplace=True)
element_quaternary.drop_duplicates(inplace=True)
element_others.drop_duplicates(inplace=True)

element_binary.to_csv('Li_binary_elements.csv', index=False)
element_ternary.to_csv('Li_ternary_elements.csv', index=False)
element_quaternary.to_csv('Li_quaternary_elements.csv', index=False)
element_others.to_csv('Li_others_elements.csv', index=False)

# element_binary
# element_ternary
# element_quaternary
# element_others