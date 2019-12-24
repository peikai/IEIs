from pymatgen import Composition
from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PDPlotter, PhaseDiagram, tet_coord
import numpy as np
import plotly.graph_objects as go
import plotly
from scipy.spatial import ConvexHull

def plotly_polyhedron(polyhedron, color):
    polyhedron= np.vstack(polyhedron)
    x, y, z = [polyhedron[:,0], polyhedron[:,1], polyhedron[:,2]]
    convex_polyhedon = dict(x=x, y=y, z=z, type= 'mesh3d', alphahull=1, opacity=0.2, color=color)
    return(convex_polyhedon)

def plotly_lines(facet):
    # To make lines a loop.
    facet = np.vstack((facet, facet[0]))
    x, y, z = [facet[:,0], facet[:,1], facet[:,2]]
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
chemsys = 'Li-Hf-W-Se'
# chemsys = 'N-Li-Al'

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)
# plotter = PDPlotter(pd, show_unstable=True)
# plotter.show()

# different length but not at all
entries = pd.qhull_entries
qhull_data = pd.qhull_data
qhull_data = np.delete(qhull_data, -1, axis=0)

qhull_cord = np.vstack([tet_coord(qhull_data[i, 0:3]) for i in range(qhull_data.shape[0])])

# qhull_x_values = 1.0 - qhull_data[:,0] - qhull_data[:,1]
# qhull_data = np.insert(qhull_data, 0, values=qhull_x_values, axis=1)
facet_vertices = pd.facets
qhull_stable = [qhull_cord[each] for each in facet_vertices]

# facets_hull = np.array([[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0]])
# qhull_stable = np.insert(qhull_stable, 0, values=facets_hull, axis=0)

data = []

for qhull in qhull_stable:
    polyhedron = qhull[:,0:3]
    hull = ConvexHull(polyhedron)
    for simplex in hull.simplices:
        facet = polyhedron[simplex]
        convex_lines = plotly_lines(facet)
        data.append(convex_lines)

facet_element = tieline_phases(pd, 'Li')
qhull_element = np.array([qhull_cord[each] for each in facet_element])

# Different style with atoms color.
colors = np.arange(len(qhull_element))
for qhull, color in zip(qhull_element, colors):
    polyhedron = qhull[:,0:3]
    convex_polyhedon = plotly_polyhedron(polyhedron, color=color)
    data.append(convex_polyhedon)

# add node points
nodes_index = np.array(facet_vertices).flatten()
nodes_index = np.unique(nodes_index)
nodes_name = np.array([entries[each].name for each in nodes_index])
nodes_array = np.vstack([qhull_cord[each] for each in nodes_index])

scatter_vertices = dict(
    mode = "markers",
    name = 'nodes',
    type = "scatter3d",
    x = nodes_array[:,0], y = nodes_array[:,1], z = nodes_array[:,2],
    # marker = dict(size=5, color="rgb(106, 90, 205)")
    marker = dict(size=8, color="rgb(106, 90, 205)")
)
data.append(scatter_vertices)

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
    width = 1000,
    height = 1000,
    # autosize = True
    # annotations = make_annotations(nodes_array, v_label),
)

# fig = go.Figure(data=[go.Mesh3d(z=polyhedron_data[:,2], x=polyhedron_data[:,0], y=polyhedron_data[:,1],opacity=0.8)])
# fig = go.Figure(data=[go.Surface(color=polyhedron_data[:,2], x=polyhedron_data[:,0], y=polyhedron_data[:,1],opacity=0.2)])

fig = dict(data=data, layout=layout)
plotly.io.write_image(fig, 'quaternary.png', scale=8)
plotly.offline.plot(fig, filename='{fn}.html'.format(fn='quaternary'), show_link=False)