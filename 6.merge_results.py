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


# merge Lithium chemical systems
chemsys_1 = pd.read_csv('tables/Li/chemsys_all.csv', usecols=['chemsys'])
chemsys_2 = pd.read_csv('tables\Li-free\chemsys.csv', usecols=['chemsys'])
chemsys_distinct = merge_then_remove_subset(chemsys_1, chemsys_2, column='chemsys')
chemsys_distinct.to_csv('chemsys_all.csv', header=['chemsys'], index=False)

# merge thermodynamic stable phases
tieline_1 = pd.read_csv('tables/Li/Li_tieline_distinct.csv')
tieline_2 = pd.read_csv('tables/Li-free/tieline_distinct.csv')
tieline_merged = tieline_1.append(tieline_2, ignore_index=True)
tieline_merged = tieline_merged.drop_duplicates()
tieline_merged.to_csv('tieline_distinct_all.csv', index=False)
