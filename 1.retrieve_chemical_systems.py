from pymatgen.ext.matproj import MPRester
import pandas as pd


def drop_subset_chemsys(chemsys_series):
    # split chemsys str to find element-wise subset relations
    chemsys_series = chemsys_series.apply(str.split, sep='-')
    # prepare set for subset function afterward
    chemsys_series = chemsys_series.apply(set)
    # prepare a list for iterations
    chemsys_list = chemsys_series.to_list()
    # prepare a dataframe to store other info
    chemsys_dataframe = chemsys_series.to_frame(name='elements')
    ## chemsys_dataframe = pd.DataFrame(chemsys_series, columns=['pretty_formula'])
    chemsys_dataframe['distinct'] = 'null'
    # like, A-B is not a subset of any chemsys, then store A-B
    for index, row in chemsys_series.iteritems():
        boolean =  [row.issubset(chemsys) for chemsys in chemsys_list]
        # count including itself
        if not boolean.count(True) > 1:
            chemsys_dataframe.loc[index, 'distinct'] = True

    chemsys_distinct_dataframe = chemsys_dataframe.loc[chemsys_dataframe['distinct'] == True]
    chemsys_distinct_dataframe.loc[:, 'chemsys'] = chemsys_distinct_dataframe.elements.apply(lambda x : '-'.join(x))
    chemsys_distinct_series = chemsys_distinct_dataframe['chemsys']
    chemsys_distinct_series = chemsys_distinct_series.apply(lambda x: '-'.join(sorted(x.split('-'))))
    return chemsys_distinct_series

key_element = 'Li'

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    chemsys = mpr.query(criteria={'elements':{'$in':[key_element]}}, properties=['chemsys'])
chemsys_dataframe = pd.DataFrame(chemsys).drop_duplicates()

chemsys_distinct = drop_subset_chemsys(chemsys_dataframe['chemsys'])
chemsys_distinct.to_csv('Tables/{element}/chemsys_distinct.csv'.format(element=key_element), header=['chemsys'], index=False)