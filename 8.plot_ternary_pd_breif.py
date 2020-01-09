from pymatgen import Composition
from pymatgen import MPRester, Composition
from pymatgen.analysis.phase_diagram import PDPlotter, PhaseDiagram, tet_coord, triangular_coord
import numpy as np
import plotly.graph_objects as go
import plotly
from scipy.spatial import ConvexHull


def plotly_lines(facet):
    # To make lines a loop.
    facet = np.vstack((facet, facet[0]))
    x, y = [facet[:,0], facet[:,1]]
    lines=dict(x=x, y=y, mode='lines', type='scatter', showlegend=False, line=dict(color= 'rgb(50,50,50)', width=5))
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


chemsys = 'Li-Lu-O'

with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
    entries = mpr.get_entries_in_chemsys(chemsys)

pd = PhaseDiagram(entries)

# different length but not at all
entries = pd.qhull_entries
qhull_data = pd.qhull_data
qhull_data = np.delete(qhull_data, -1, axis=0)

qhull_cord = qhull_data[:, 0:2]
qhull_cord = np.vstack([triangular_coord(each) for each in qhull_cord])
# qhull_x_values = 1.0 - qhull_data[:,0] - qhull_data[:,1]
# qhull_data = np.insert(qhull_data, 0, values=qhull_x_values, axis=1)
facet_vertices = pd.facets
facet_cord = [qhull_cord[each] for each in facet_vertices]

data = []

for facet in facet_cord:
    convex_lines = plotly_lines(facet)
    data.append(convex_lines)

nodes_array = np.vstack(facet_cord)

scatter_vertices = dict(
    mode = "markers",
    name = 'nodes',
    type = "scatter",
    x = nodes_array[:,0], y = nodes_array[:,1],
    # marker = dict(size=5, color="rgb(106, 90, 205)")
    marker = dict(size=15, color="rgb(67,67,67)")
)
data.append(scatter_vertices)

layout = dict(
    # title = '<b>Quaternary Phase Diagram</b>',
    # title_x = 0.5,
    xaxis = dict(visible=False),
    yaxis = dict(visible=False),
                # visible=False, showaxeslabels=False,
                #  zaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                #  camera= dict(eye = dict(x=2.0, y=1.0, z=0.5)),
    showlegend=False,
    template="plotly_white",
    width = 1000,
    height = 1000,
    # autosize = True
    # annotations = make_annotations(nodes_array, v_label),
)


fig = dict(data=data, layout=layout)
plotly.io.write_image(fig, 'binary.1.png', scale=8)
plotly.offline.plot(fig, filename='{fn}.html'.format(fn='binary.1'), show_link=False)