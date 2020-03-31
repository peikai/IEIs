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

def merge_then_remove_subset(dataframe_1, dataframe_2, column):
    data_merged_dataframe = dataframe_1.append(dataframe_2, ignore_index=True)
    data_merged_series = data_merged_dataframe[column].drop_duplicates()
    data_distinct_series = drop_subset_chemsys(data_merged_series)
    return(data_distinct_series)

def extract_facets(facets_merged):
    facets_dict = dict()
    facets_merged.fillna('NaN', inplace=True)
    for row in facets_merged.itertuples():
        # remove index and NaN
        index, phases = row[0], row[1:]
        phases_set = set(phases)
        try:
            phases_set.remove('NaN')
        except:
            pass
        facets_dict[index] = phases_set
    facets_series = pd.Series(facets_dict)
    return facets_series

def drop_subset_facets(facets_merged):
    # make series for simplex phases, like {'mp-135', 'mp-131', 'mp-2286'}
    facets_series = extract_facets(facets_merged)
    # prepare a list to take iterations
    facets_list = facets_series.to_list()
    # prepare a dataframe to store other info
    facets_dataframe = facets_series.to_frame(name='facet')
    facets_dataframe['distinct'] = 'null'
    for index, row in facets_series.iteritems():
        boolean = [row.issubset(facet) for facet in facets_list]
        # count including itself
        if not boolean.count(True) > 1:
            facets_dataframe.loc[index, 'distinct'] = True

    facets_distinct_dataframe = facets_dataframe.loc[facets_dataframe['distinct'] == True]
    facets_distinct_series = facets_distinct_dataframe['facet']
    return facets_distinct_series

key_element = 'K'
# merge Lithium chemical systems
chemsys_1 = pd.read_csv('tables/{element}/chemsys_all.csv'.format(element=key_element), usecols=['chemsys'])
chemsys_2 = pd.read_csv('tables/{element}-free/chemsys.csv'.format(element=key_element), usecols=['chemsys'])
chemsys_distinct = merge_then_remove_subset(chemsys_1, chemsys_2, column='chemsys')
chemsys_distinct.to_csv('chemsys_all.csv', header=['chemsys'], index=False)
# merge thermodynamic stable phases
tieline_1 = pd.read_csv('tables/{element}/K_tieline_distinct.csv'.format(element=key_element))
tieline_2 = pd.read_csv('tables/{element}-free/tieline_distinct.csv'.format(element=key_element))
tieline_merged = tieline_1.append(tieline_2, ignore_index=True)
tieline_merged = tieline_merged.drop_duplicates()
tieline_merged.to_csv('tieline_distinct_all.csv', index=False)
# merge facets
facets_1 = pd.read_csv('tables/{element}/K_facets_distinct.csv'.format(element=key_element))
facets_2 = pd.read_csv('tables/{element}-free/facets_distinct.csv'.format(element=key_element))
facets_merged = facets_1.append(facets_2, ignore_index=True)
facets_merged = facets_merged.drop_duplicates()
facets_distinct = drop_subset_facets(facets_merged)
facets_distinct.to_csv('facets_distinct_all.csv', header=['facet'], index=False)