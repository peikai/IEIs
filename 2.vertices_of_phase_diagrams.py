from pymatgen import Composition
import pandas as pd
import numpy as np


def drop_subset_chemsys(chemsys_series):
    chemsys_series = chemsys_series.apply(str.split, sep='-')
    # prepare set for subset function afterward
    chemsys_series = chemsys_series.apply(set)
    # prepare a list for iterations
    chemsys_list = chemsys_series.to_list()
    # prepare a dataframe to store other info
    chemsys_dataframe = pd.DataFrame(chemsys_series, columns=['pretty_formula', 'distinct'])
    # like, Li-Tl is not a subset of any chemsys, then store Li-Tl
    for index, row in chemsys_series.iteritems():
        boolean =  [row.issubset(chemsys) for chemsys in chemsys_list]
        # count including itself
        if not boolean.count(True) > 1:
            chemsys_dataframe.loc[index, 'distinct'] = True

    chemsys_distinct = chemsys_dataframe.loc[chemsys_dataframe['distinct'] == True] 
    chemsys_distinct = chemsys_distinct.pretty_formula.apply(lambda x : '-'.join(x))
    return chemsys_distinct
       

# entries_binary = pd.read_csv('tables/Li_binary.csv', usecols=['pretty_formula'])
# entries_ternary = pd.read_csv('tables/Li_ternary.csv', usecols=['pretty_formula'])
# entries_quaternary = pd.read_csv('tables/Li_quaternary.csv', usecols=['pretty_formula'])
# entries_others = pd.read_csv('tables/Li_others.csv', usecols=['pretty_formula'])
chemsys_all = pd.read_csv('tables/Li_all.csv', usecols=['pretty_formula'])

# element_binary = entries_binary.pretty_formula.apply(lambda x : [e.name for e in Composition(x).elements])
# element_ternary = entries_ternary.pretty_formula.apply(lambda x : [e.name for e in Composition(x).elements])
# element_quaternary = entries_quaternary.pretty_formula.apply(lambda x : [e.name for e in Composition(x).elements])
# element_others = entries_others.pretty_formula.apply(lambda x : [e.name for e in Composition(x).elements])

# chemsys_all = chemsys_all.pretty_formula.apply(lambda x : [e.name for e in Composition(x).elements])
chemsys_all= chemsys_all.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
chemsys_all.drop_duplicates(inplace=True)

chemsys_all = drop_subset_chemsys(chemsys_all)
chemsys_all.to_csv('chemsys_all.csv', index=False)


# element_binary = entries_binary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
# element_ternary = entries_ternary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
# element_quaternary = entries_quaternary.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
# element_others = entries_others.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
# element_all = element_all.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))


# element_binary.drop_duplicates(inplace=True)
# element_ternary.drop_duplicates(inplace=True)
# element_quaternary.drop_duplicates(inplace=True)
# element_others.drop_duplicates(inplace=True)
# element_all.drop_duplicates(inplace=True)

# element_binary.to_csv('Li_binary_elements.csv', index=False)
# element_ternary.to_csv('Li_ternary_elements.csv', index=False)
# element_quaternary.to_csv('Li_quaternary_elements.csv', index=False)
# element_others.to_csv('Li_others_elements.csv', index=False)
# element_all.to_csv('Li_all_elements.csv', index=False)

# element_binary
# element_ternary
# element_quaternary
# element_others