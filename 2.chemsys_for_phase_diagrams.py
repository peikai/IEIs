from pymatgen import Composition
import pandas as pd
import numpy as np


def drop_subset_chemsys(chemsys_series):
    # split chemsys str to find element-wise subset relations
    chemsys_series = chemsys_series.apply(str.split, sep='-')
    # prepare set for subset function afterward
    chemsys_series = chemsys_series.apply(set)
    # prepare a list for iterations
    chemsys_list = chemsys_series.to_list()
    # prepare a dataframe to store other info
    chemsys_dataframe = pd.DataFrame(chemsys_series, columns=['pretty_formula'])
    chemsys_dataframe['distinct'] = 'null'
    # like, A-B is not a subset of any chemsys, then store A-B
    for index, row in chemsys_series.iteritems():
        boolean =  [row.issubset(chemsys) for chemsys in chemsys_list]
        # count including itself
        if not boolean.count(True) > 1:
            chemsys_dataframe.loc[index, 'distinct'] = True

    chemsys_distinct_dataframe = chemsys_dataframe.loc[chemsys_dataframe['distinct'] == True] 
    chemsys_distinct_dataframe.loc[:, 'chemsys'] = chemsys_distinct_dataframe.pretty_formula.apply(lambda x : '-'.join(x))
    chemsys_distinct_series = chemsys_distinct_dataframe['chemsys']
    return chemsys_distinct_series
       

chemsys_all = pd.read_csv('tables/K/K_all.csv', usecols=['pretty_formula'])

# join element in chemsys str, then drop duplicated chemsys
chemsys_all= chemsys_all.pretty_formula.apply(lambda x : '-'.join([e.name for e in Composition(x).elements]))
chemsys_all.drop_duplicates(inplace=True)

chemsys_all = drop_subset_chemsys(chemsys_all)
chemsys_all.to_csv('chemsys_all.csv', header=['chemsys'], index=False)
