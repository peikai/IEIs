import os
import pickle

import numpy as np
import pandas
import plotly
import plotly.graph_objects as go
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.core import Composition
from pymatgen.ext.matproj import MPRester


def plotly_ternary_lines(dataframe):
    trace = go.Scatterternary({
        'mode': 'lines+markers',  # 'lines+markers+text',
        'a': dataframe.iloc[:, 0],
        'b': dataframe.iloc[:, 1],
        'c': dataframe.iloc[:, 2],
        'text': dataframe.iloc[:, 3],
        # 'line_width': 5,
        'marker': {
                'symbol': "circle-dot",
                'color': 'rgb(67,67,67)',
                'size': 8,
                'line': {'width': 12}
        },
        'showlegend': False
    })

    return trace


def tieline_phases(phaseDiagram, key_element):
    # find its coordinate in phase diagram
    comp = Composition(key_element)
    c = phaseDiagram.pd_coords(comp)
    # find facets that key element acted as a vertice
    # vertices of facets are stable phases
    facet_list = list()
    for f, s in zip(phaseDiagram.facets, phaseDiagram.simplexes):
        if s.in_simplex(c, PhaseDiagram.numerical_tol / 10):
            facet_list.append(f)
    return facet_list


def makeAxis(title, tickangle):
    return {
        'title': title,
        'titlefont': {'size': 20},
        'tickangle': tickangle,
        'tickfont': {'size': 15},
        'tickcolor': 'rgba(0,0,0,0)',
        'ticklen': 5,
        'showline': True,
        'showgrid': True,
        'showticklabels': False
    }


def REST_local(chemsys):
    if not os.path.exists('Temp/entries_{v}.pickle'.format(v=chemsys)):
        with MPRester(api_key='') as mpr:
            entries = mpr.get_entries_in_chemsys(chemsys)
        with open('Temp/entries_{v}.pickle'.format(v=chemsys), 'wb') as entries_local:
            pickle.dump(entries, entries_local)
    else:
        with open('Temp/entries_{v}.pickle'.format(v=chemsys), 'rb') as entries_temp:
            entries = pickle.load(entries_temp)
    return entries


def plot_ternary_pd(pd):
    # different length but it doesn't matter.
    entries = pd.qhull_entries
    entries_name = [entry.name for entry in entries]

    qhull_data = pd.qhull_data
    qhull_data = np.delete(qhull_data, -1, axis=0)

    qhull_x_values = 1.0 - qhull_data[:, 0] - qhull_data[:, 1]
    qhull_data = np.insert(qhull_data, 0, values=qhull_x_values, axis=1)

    qhull_cord = np.vstack([each for each in qhull_data[:, 0:3]])

    elements_list = [element.symbol for element in pd.elements]
    qhull_dataframe = pandas.DataFrame(qhull_cord, columns=elements_list)
    qhull_dataframe['name'] = entries_name

    fig = go.Figure()

    # add every facets to a single dataframe
    facet_list = pd.facets
    for facet in facet_list:
        # make a circle route
        facet = np.append(facet, facet[0])
        # draw each facet
        facet_dataframe = qhull_dataframe.iloc[facet, :]
        facet_trace = plotly_ternary_lines(facet_dataframe)
        fig.add_trace(facet_trace)

    fig.update_layout({
        'ternary': {
            'sum': 1,
            'aaxis': makeAxis(elements_list[0], 0),
            'baxis': makeAxis('<br>'+elements_list[1], 45),
            'caxis': makeAxis('<br>'+elements_list[2], -45)
        },
        'width': 1000,
        'height': 1000
        # ,
        # 'annotations': [{
        #   'showarrow': False,
        # 'text': 'Simple Ternary Plot with Markers',
        #   'x': 0.5,
        #   'y': 1.3,
        #   'font': { 'size': 15 }
        # }]
    })
    return fig


def main():
    chemsys = 'Be-O-Li'

    entries = REST_local(chemsys)
    pd = PhaseDiagram(entries)
    fig = plot_ternary_pd(pd)
    # plotly.io.write_image(fig, '{fn}.png'.format(fn=chemsys), scale=8)
    plotly.offline.plot(fig, filename='{fn}.html'.format(
        fn=chemsys), show_link=False, auto_open=False)


if __name__ == "__main__":
    main()
