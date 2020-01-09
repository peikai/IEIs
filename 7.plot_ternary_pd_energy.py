import numpy as np
import pandas
import plotly
import plotly.graph_objects as go
from pymatgen import Composition, MPRester
from pymatgen.analysis.phase_diagram import (PDPlotter, PhaseDiagram,
                                             tet_coord, triangular_coord, get_facets)
from scipy.spatial import ConvexHull, Delaunay


def merge_facet(convexhull):
    # index each equiation with a feature
    equitions = convexhull.equations
    id_list = [(each[0]*1 + each[1]*2 + each[2]*3 + each[3]*4) for each in convexhull.equations]
    dataframe = pandas.DataFrame(equitions)
    dataframe['id'] = id_list
    # find facets with the same hyperplane equation
    unique_id = np.unique(id_list)
    facet_list = []
    for id in unique_id:
        index_list = dataframe[dataframe.loc[:,'id'] == id].index
        facet_array = convexhull.simplices[index_list]
        facet_merged = np.unique(facet_array)
        facet_points = convexhull.points[facet_merged]
        facet_list.append(facet_points)
        
    return(facet_list)


def plotly_polyhedron(polyhedron):
    polyhedron= np.vstack(polyhedron)
    x, y, z = [polyhedron[:,0], polyhedron[:,1], polyhedron[:,2]]
    convex_polyhedon = dict(x=x, y=y, z=z, type= 'mesh3d', alphahull=0, opacity=0.1, color="rgb(106, 90, 205)")
    return(convex_polyhedon)

def plotly_lines(line_nodes):
    # To make lines a loop.
    line_nodes = np.vstack((line_nodes, line_nodes[0]))
    x, y, z = [line_nodes[:,0], line_nodes[:,1], line_nodes[:,2]]
    lines=dict(x=x, y=y, z=z, mode='lines', type='scatter3d', showlegend=False, line=dict(color= 'rgb(50,50,50)', width=3))
    return(lines)

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


# chemsys = 'Ca-N-Li-Al'
# chemsys = 'Li-Fe-O'
# chemsys = 'N-Li-Al'
chemsys = 'Li-Lu-O'

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)

# different length but not at all
entries = pd.qhull_entries
qhull_data = pd.qhull_data
qhull_data = np.delete(qhull_data, -1, axis=0)

facet_vertices = pd.facets

# qhull_cord = np.vstack([triangular_coord(each) for each in qhull_cord])
facet_cord = [qhull_data[each] for each in facet_vertices] # multi-level array, contains duplicates vertices

# do not need duplicated nodes using for construct convex hull
stable_nodes = np.unique(facet_vertices)
stable_cord = qhull_data[stable_nodes][:,0:2]
stable_energy = qhull_data[stable_nodes][:,2]

# nodes of projections of convex hull construction
nodes_bottom = np.insert(stable_cord, 2, values=0, axis=1)
# reshape array (3,) to (3,1)
nodes_top_z = stable_energy[:,np.newaxis]
nodes_top = np.insert(stable_cord, [2], values=nodes_top_z, axis=1)
# merge two parts of nodes
nodes_array = np.append(nodes_bottom, nodes_top, axis=0)

data = []

# plot scatters
scatter_vertices = dict(
    mode = "markers",
    name = 'nodes',
    type = "scatter3d",
    x = nodes_bottom[:,0], y = nodes_bottom[:,1], z = nodes_bottom[:,2],
    marker = dict(size=8, color="rgb(50,50,50)")
)
data.append(scatter_vertices)

scatter_vertices = dict(
    mode = "markers",
    name = 'nodes',
    type = "scatter3d",
    x = nodes_top[:,0], y = nodes_top[:,1], z = nodes_top[:,2],
    marker = dict(size=8, color="rgb(106, 90, 205)")
)
data.append(scatter_vertices)

# plot edges
for facet in facet_cord:
    # plot facets on the top
    convex_lines = plotly_lines(facet)
    data.append(convex_lines)
    # change z to zero, project facets to bottom
    facet[:,2] = 0
    # plot facets projections
    convex_lines = plotly_lines(facet)
    data.append(convex_lines)

# plot pillars
for pillar in zip(nodes_bottom[-3:], nodes_top[-3:]):
    convex_lines = plotly_lines(pillar)
    data.append(convex_lines)

# plot surfaces
polyhedron = plotly_polyhedron(nodes_array)
data.append(polyhedron)


# nodes_index = np.array(facet_vertices).flatten()
# nodes_index = np.unique(nodes_index)
# nodes_name = np.array([entries[each].name for each in nodes_index])
# nodes_array = np.vstack([qhull_cord[each] for each in nodes_index])


layout = dict(
    # title = '<b>Quaternary Phase Diagram</b>',
    title_x = 0.5,
    scene = dict(xaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                 yaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                # visible=False, showaxeslabels=False,
                 zaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                 camera= dict(eye = dict(x=2.0, y=1.0, z=0.5)),
                 ),
    showlegend=False,
    # width = 1000,
    # height = 1000,
    # autosize = True
    # annotations = make_annotations(nodes_array, v_label),
)

fig = dict(data=data, layout=layout)
plotly.io.write_image(fig, 'ternary_energy.png', scale=8)
plotly.offline.plot(fig, filename='{fn}.html'.format(fn='ternary_energy'), show_link=False)
