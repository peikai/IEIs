import os
import pickle
from itertools import combinations

import numpy as np
import plotly
from plotly.express.colors import qualitative as palette
from pymatgen.analysis.phase_diagram import PhaseDiagram, tet_coord
from pymatgen.core import Composition
from pymatgen.ext.matproj import MPRester
from scipy.spatial import ConvexHull


def plotly_polyhedron(polyhedron, color):
    polyhedron = np.vstack(polyhedron)
    x, y, z = [polyhedron[:, 0], polyhedron[:, 1], polyhedron[:, 2]]
    convex_polyhedon = dict(x=x, y=y, z=z, type='mesh3d',
                            alphahull=1, opacity=0.2, color=color)
    return(convex_polyhedon)


def plotly_lines(seg, dash):
    # To make lines a loop.
    # facet = np.vstack((facet, facet[0]))
    x, y, z = [seg[:, 0], seg[:, 1], seg[:, 2]]
    seg = dict(x=x, y=y, z=z, mode='lines', type='scatter3d',
               showlegend=False, line=dict(color='rgb(50,50,50)', dash=dash, width=3))
    return(seg)


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
    return(facet_list)


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


def plot_quaternary_pd(pd):
    # different length but not at all
    qhull_data = pd.qhull_data
    qhull_data = np.delete(qhull_data, -1, axis=0)

    qhull_cord = np.vstack([tet_coord(qhull_data[i, 0:3])
                            for i in range(qhull_data.shape[0])])
    facet_vertices = pd.facets
    qhull_stable = [qhull_cord[each] for each in facet_vertices]

    data = []

    # plot dash segment lines between nodes
    line_list = []
    for qhull in qhull_stable:
        polyhedron = qhull[:, 0:3]
        hull = ConvexHull(polyhedron)
        for simplex in hull.simplices:
            facet = polyhedron[simplex]
            lines = list(combinations(facet, 2))
            lines = [np.array(l) for l in lines]
            for line in lines:
                duplicate_boolean = [
                    (line.round(3) == l.round(3)).all() for l in line_list]
                if not True in duplicate_boolean:
                    line_list.append(line)

    for line in line_list:
        convex_lines = plotly_lines(line, 'dash')
        data.append(convex_lines)

    #######################################################
    # If need to draw certain faces in solid lines, like the faces on the front,
    # ddd coordinations of the facet here.
    # note to comment them out at the first run.
    #######################################################
    facet_front = [[[0.5, 0.8660254, 0.],
                    [0.83333333, 0.28867513, 0.],
                    [0., 0., 0]],
                   [[0.83333333, 0.28867513, 0.],
                    [1., 0., 0],
                    [0., 0., 0]]]

    for facet in facet_front:
        lines_front = list(combinations(facet, 2))
        lines_front = [np.array(l) for l in lines_front]
        for line in lines_front:
            convex_lines = plotly_lines(line, 'solid')
            data.append(convex_lines)
    #######################################################

    facet_element = tieline_phases(pd, 'Li')
    qhull_element = np.array([qhull_cord[each] for each in facet_element])
    for index, qhull in enumerate(qhull_element):
        polyhedron = qhull[:, 0:3]
        color = palette.Plotly[index % 10]
        convex_polyhedon = plotly_polyhedron(polyhedron, color=color)
        data.append(convex_polyhedon)

    # add node points
    nodes_index = np.array(facet_vertices).flatten()
    nodes_index = np.unique(nodes_index)
    # nodes_name = np.array([entries[each].name for each in nodes_index])
    nodes_array = np.vstack([qhull_cord[each] for each in nodes_index])

    scatter_vertices = dict(
        mode="markers",
        name='nodes',
        type="scatter3d",
        x=nodes_array[:, 0], y=nodes_array[:, 1], z=nodes_array[:, 2],
        # marker = dict(size=5, color="rgb(106, 90, 205)")
        marker=dict(size=6, color="rgb(50,50,50)")
    )
    data.append(scatter_vertices)

    layout = dict(
        # title = '<b>Quaternary Phase Diagram</b>',
        title_x=0.5,
        scene=dict(xaxis=dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title={'text': ''}, visible=False),
                   yaxis=dict(zeroline=False, showticklabels=False, showgrid=False,
                              showline=False, title={'text': ''}, visible=False),
                   # visible=False, showaxeslabels=False,
                   zaxis=dict(zeroline=False, showticklabels=False, showgrid=False,
                              showline=False, title={'text': ''}, visible=False),
                   camera=dict(eye=dict(x=2.0, y=1.0, z=0.5)),
                   ),
        showlegend=False,
        # width = 1000,
        # height = 1000,
        autosize=True
        # annotations = make_annotations(nodes_array, v_label),
    )

    fig = dict(data=data, layout=layout)
    return fig


def main():
    chemsys = 'Ca-Cl-K-Li'
    entries = REST_local(chemsys)
    pd = PhaseDiagram(entries)
    fig = plot_quaternary_pd(pd)
    plotly.offline.plot(fig, filename='{fn}.html'.format(
        fn=chemsys), show_link=False, auto_open=False)


if __name__ == "__main__":
    main()
