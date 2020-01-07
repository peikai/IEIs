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

chemsys = 'Li-O-Lu'


with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)
# plotter = PDPlotter(pd, show_unstable=True)
# plotter.show()

# different length but not at all
entries = pd.qhull_entries
qhull_data = pd.qhull_data
qhull_data = np.delete(qhull_data, -1, axis=0)


data = []

qhull = ConvexHull(qhull_data)
polyhedron_vertices = qhull.points[qhull.vertices]

convex_polyhedon = plotly_polyhedron(polyhedron_vertices, color=1)
data.append(convex_polyhedon)

scatter_vertices = dict(
    mode = "markers",
    name = 'nodes',
    type = "scatter3d",
    x = polyhedron_vertices[:,0], y = polyhedron_vertices[:,1], z = polyhedron_vertices[:,2],
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
plotly.io.write_image(fig, 'ternary.png', scale=8)
plotly.offline.plot(fig, filename='{fn}.html'.format(fn='ternary'), show_link=False)