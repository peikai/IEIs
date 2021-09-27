import os
import pickle
from itertools import combinations

import numpy as np
import plotly
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.ext.matproj import MPRester


def plotly_lines(line_nodes, dash, width):
    x, y, z = [line_nodes[:, 0], line_nodes[:, 1], line_nodes[:, 2]]
    lines = dict(x=x, y=y, z=z, mode='lines', type='scatter3d', showlegend=False,
                 line=dict(dash=dash, color='rgb(50,50,50)', width=width))
    return lines


def plotly_hulls(x, y, z, i, j, k, color):
    hull = dict(x=x, y=y, z=z, i=i, j=j, k=k, type='mesh3d', opacity=1, color=color,
                lighting=dict(ambient=0.8, diffuse=1, specular=1),
                lightposition=dict(x=100000, y=100000, z=-100000))
    return hull


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


def plot_envelope(pd):
    # get original qhull data
    qhull_data = pd.qhull_data
    # an extra point exists in original pd.qhull_data, drop it
    qhull_data = np.delete(qhull_data, -1, axis=0)

    # simplices without irrelevant facets
    facet_vertices = pd.facets  # multi-level array, contains duplicates vertices
    # convert vertex cordinations of each facet
    facet_cord_list = [qhull_data[each] for each in facet_vertices]
    # do not need duplicated nodes using for construct convex hull
    stable_nodes_index = np.unique(facet_vertices)
    # split cords and energies of stable entries from qhull data
    stable_cord_xy = qhull_data[stable_nodes_index][:, 0:2]
    stable_energy = qhull_data[stable_nodes_index][:, 2]
    # nodes of projected hull
    nodes_projected = np.insert(stable_cord_xy, 2, values=0, axis=1)
    # reshape array (3,) to (3,1)
    nodes_stable_z = stable_energy[:, np.newaxis]
    nodes_stable = np.insert(
        stable_cord_xy, [2], values=nodes_stable_z, axis=1)

    # plot section
    data = []

    # plot scatters of stable nodes
    scatter_vertices = dict(
        mode="markers",
        name='nodes_stable',
        type="scatter3d",
        x=nodes_stable[:, 0], y=nodes_stable[:, 1], z=nodes_stable[:, 2],
        marker=dict(size=6, color="rgb(44,113,147)")
    )
    data.append(scatter_vertices)

    # plot scatters of projected nodes
    scatter_vertices = dict(
        mode="markers",
        name='nodes_projected',
        type="scatter3d",
        x=nodes_projected[:, 0], y=nodes_projected[:,
                                                   1], z=nodes_projected[:, 2],
        marker=dict(size=6, color="rgb(50,50,50)")
    )
    data.append(scatter_vertices)

    # merge edges and remove duplicates
    edge_list = []
    for facet in facet_cord_list:
        edge_list.extend(list(combinations(facet, 2)))
    edge_array = np.array(edge_list)
    edge_array = np.unique(edge_array, axis=0)
    # plot edges of facets
    for edge in edge_array:
        # plot edges on the top
        convex_lines = plotly_lines(edge, dash='solid', width=4)
        data.append(convex_lines)
        # change z to zero, project facets to bottom
        edge_copy = edge.copy()
        edge_copy[:, 2] = 0
        # plot facets projections
        convex_lines = plotly_lines(edge_copy, dash='solid', width=4)
        data.append(convex_lines)

    # plot potential-energy envelope, see https://plotly.com/python/3d-mesh/
    x, y, z = qhull_data.T
    i, j, k = np.array(facet_vertices).T
    hull = plotly_hulls(x, y, z, i, j, k, color='rgb(146,197,222)')
    data.append(hull)

    layout = dict(
        title_x=0.5,
        scene=dict(xaxis=dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title={'text': ''}, visible=False),
                   yaxis=dict(zeroline=False, showticklabels=False, showgrid=False,
                              showline=False, title={'text': ''}, visible=False),
                   zaxis=dict(zeroline=False, showticklabels=False, showgrid=False,
                              showline=False, title={'text': ''}, visible=False),
                   camera=dict(up=dict(x=0, y=0, z=-1),
                               eye=dict(x=1, y=1, z=-1))
                   ),
        showlegend=False
    )

    fig = dict(data=data, layout=layout)
    return fig


def main():
    # [option] plot in batch
    # pretty_formula_list = pandas.read_csv('tables/Li/candidates.csv').pretty_formula.to_list()
    # chemsys_list = [Composition(each).chemical_system+'-Li' for each in pretty_formula_list if len(Composition(each).elements)==2]
    # for i, chemsys in enumerate(chemsys_list):
    #     plot_envelope(chemsys)
    #     print('{I}/{L}'.format(I=i+1, L=len(chemsys_list)))

    # [option] plot a given chemical system
    chemsys = 'Be-O-Li'
    entries = REST_local(chemsys)
    pd = PhaseDiagram(entries)
    fig = plot_envelope(pd)
    plotly.offline.plot(fig, filename='{fn}.html'.format(
        fn=chemsys), show_link=False, auto_open=False)


if __name__ == "__main__":
    main()
