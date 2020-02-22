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
    convex_polyhedon = dict(x=x, y=y, z=z, type= 'mesh3d', alphahull=0, opacity=0.2, color="rgb(106, 90, 205)")
    return(convex_polyhedon)

def plotly_lines(line_nodes, dash, width):
    # To make lines a loop.
    line_nodes = np.vstack((line_nodes, line_nodes[0]))
    x, y, z = [line_nodes[:,0], line_nodes[:,1], line_nodes[:,2]]
    lines=dict(x=x, y=y, z=z, mode='lines', type='scatter3d', showlegend=False, line=dict(dash=dash, color= 'rgb(50,50,50)', width=width))
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


def plot_convex_hull(chemsys):
    with MPRester(api_key='25wZTKoyHkvhXFfO') as mpr:
        entries = mpr.get_entries_in_chemsys(chemsys)

    pd = PhaseDiagram(entries)

    # get original qhull data, simplices
    entries = pd.qhull_entries
    qhull_data = pd.qhull_data
    qhull_simplices = get_facets(qhull_data)
    simplices_cord = [qhull_data[each] for each in qhull_simplices]

    # simplices without irrelevant facets
    facet_vertices = pd.facets

    # an extra point exists in original pd.qhull_data
    qhull_data = np.delete(qhull_data, -1, axis=0)

    # multi-level array, contains duplicates vertices
    facet_cord = [qhull_data[each] for each in facet_vertices]

    # do not need duplicated nodes using for construct convex hull
    stable_nodes = np.unique(facet_vertices)
    stable_cord = qhull_data[stable_nodes][:,0:2]
    stable_energy = qhull_data[stable_nodes][:,2]

    # nodes of projections of convex hull construction
    nodes_bottom = np.insert(stable_cord, 2, values=0, axis=1)
    # reshape array (3,) to (3,1)
    nodes_top_z = stable_energy[:,np.newaxis]
    nodes_top = np.insert(stable_cord, [2], values=nodes_top_z, axis=1)

    # merge nodes_top with nodes_bottom
    # nodes_hull = np.append(nodes_bottom, nodes_top, axis=0)
    # or use nodes of convex hull
    nodes_hull = pd.qhull_data
    extra_node = nodes_hull[-1]
    # reshape (3,) to (1,3)
    extra_node = extra_node[np.newaxis,:]

    # unstable entries
    qhull_data_dataframe = pandas.DataFrame(qhull_data)
    qhull_data_dataframe = qhull_data_dataframe[qhull_data_dataframe.loc[:,2] < 1e-11]
    unstable_array = qhull_data_dataframe.append(pandas.DataFrame(nodes_top)).drop_duplicates(keep=False).to_numpy()

    data = []

    # plot scatters
    scatter_vertices = dict(
        mode = "markers",
        name = 'nodes_bottom',
        type = "scatter3d",
        x = nodes_bottom[:,0], y = nodes_bottom[:,1], z = nodes_bottom[:,2],
        marker = dict(size=8, color="rgb(50,50,50)")
    )
    data.append(scatter_vertices)

    scatter_vertices = dict(
        mode = "markers",
        name = 'nodes_top',
        type = "scatter3d",
        x = nodes_top[:,0], y = nodes_top[:,1], z = nodes_top[:,2],
        marker = dict(size=8, color="rgb(106, 90, 205)")
    )
    data.append(scatter_vertices)

    scatter_vertices = dict(
        mode = "markers",
        name = 'unstable_nodes',
        type = "scatter3d",
        x = unstable_array[:,0], y = unstable_array[:,1], z = unstable_array[:,2],
        marker = dict(size=8, color="rgb(169, 169, 169)")
    )
    data.append(scatter_vertices)

    scatter_vertices = dict(
        mode = "markers",
        name = 'extra_node',
        type = "scatter3d",
        x = extra_node[:,0], y = extra_node[:,1], z = extra_node[:,2],
        marker = dict(symbol='circle-open', size=8, color="rgb(0, 0, 0)")
    )
    data.append(scatter_vertices)

    # plot edges of facets
    for facet in facet_cord:
        # plot facets on the top
        convex_lines = plotly_lines(facet, dash='solid', width=5)
        data.append(convex_lines)
        # change z to zero, project facets to bottom
        facet[:,2] = 0
        # plot facets projections
        convex_lines = plotly_lines(facet, dash='solid', width=5)
        data.append(convex_lines)

    # plot edges for convex hull
    for facet in simplices_cord:
        convex_lines = plotly_lines(facet, dash='dash', width=2)
        data.append(convex_lines)

    # plot pillars
    # for pillar in zip(nodes_bottom[-3:], nodes_top[-3:]):
    #     convex_lines = plotly_lines(pillar, dash='longdash')
    #     data.append(convex_lines)

    # plot surfaces
    polyhedron = plotly_polyhedron(nodes_hull)
    data.append(polyhedron)

    layout = dict(
        # title = '<b>Ternary Phase Diagram</b>',
        title_x = 0.5,
        scene = dict(xaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    yaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    # visible=False, showaxeslabels=False,
                    zaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    camera= dict(eye = dict(x=2.0, y=1.0, z=0.5)),
                    ),
        showlegend=False
    )

    fig = dict(data=data, layout=layout)
    plotly.io.write_image(fig, '{fn}.png'.format(fn=chemsys), scale=8)
    plotly.offline.plot(fig, filename='{fn}.html'.format(fn=chemsys), show_link=False, auto_open=False)

def main():
    # plot in batch
    # pretty_formula_list = pandas.read_csv('tables/Li/Li_candidates_calc.csv').pretty_formula.to_list()
    # chemsys_list = [Composition(each).chemical_system+'-Li' for each in pretty_formula_list if len(Composition(each).elements)==2]
    # for i, chemsys in enumerate(chemsys_list):
    #     plot_convex_hull(chemsys)
    #     print('{I}/{L}'.format(I=i+1, L=len(chemsys_list)))
    
    # plot a given chemical system
    chemsys = 'O-Lu-Li'
    plot_convex_hull(chemsys)

if __name__ == "__main__":
    main()

