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


# def plotly_polyhedron(polyhedron):
#     polyhedron= np.vstack(polyhedron)
#     x, y, z = [polyhedron[:,0], polyhedron[:,1], polyhedron[:,2]]
#     convex_polyhedon = dict(x=x, y=y, z=z, type= 'mesh3d', alphahull=0, opacity=0.2, color="rgb(106, 90, 205)", lightposition=dict(z=1000))

#     return(convex_polyhedon)

def plotly_facet(facet_cord, color):
    x, y, z = facet_cord.T
    facet = dict(x = x, y = y, z = z, type='mesh3d', color=color, opacity=0.8) #lightposition=dict(x=4000, y=-300, z=400)
    return facet

def plotly_lines(line_nodes, dash, width):
    # To make lines a loop.
    line_nodes = np.vstack((line_nodes, line_nodes[0]))
    x, y, z = [line_nodes[:,0], line_nodes[:,1], line_nodes[:,2]]
    lines=dict(x=x, y=y, z=z, mode='lines', type='scatter3d', showlegend=False, line=dict(dash=dash, color='rgb(50,50,50)', width=width))
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

    # get original qhull data
    qhull_data = pd.qhull_data

    # simplices without irrelevant facets
    facet_vertices = pd.facets # multi-level array, contains duplicates vertices

    # an extra point exists in original pd.qhull_data, drop it
    qhull_data = np.delete(qhull_data, -1, axis=0)

    # convert vertex cordinations of each facet
    facet_cord_list = [qhull_data[each] for each in facet_vertices]

    # do not need duplicated nodes using for construct convex hull
    stable_nodes_index = np.unique(facet_vertices)
    # split cords and energies of stable entries from qhull data
    stable_cord_xy = qhull_data[stable_nodes_index][:,0:2]
    stable_energy = qhull_data[stable_nodes_index][:,2]

    # nodes of projected hull
    nodes_projected = np.insert(stable_cord_xy, 2, values=0, axis=1)
    # reshape array (3,) to (3,1)
    nodes_stable_z = stable_energy[:,np.newaxis]
    nodes_stable = np.insert(stable_cord_xy, [2], values=nodes_stable_z, axis=1)

    # unstable entries that under the hull
    qhull_data_dataframe = pandas.DataFrame(qhull_data)
    unstable_array = qhull_data_dataframe.append(pandas.DataFrame(nodes_stable)).drop_duplicates(keep=False).to_numpy()

    data = []

    # plot scatters
    scatter_vertices = dict(
        mode = "markers",
        name = 'nodes_projected',
        type = "scatter3d",
        x = nodes_projected[:,0], y = nodes_projected[:,1], z = nodes_projected[:,2],
        marker = dict(size=6, color="rgb(50,50,50)")
    )
    data.append(scatter_vertices)

    scatter_vertices = dict(
        mode = "markers",
        name = 'nodes_stable',
        type = "scatter3d",
        x = nodes_stable[:,0], y = nodes_stable[:,1], z = nodes_stable[:,2],
        # marker = dict(size=8, color="rgb(106, 90, 205)")
        # marker = dict(size=6, color="limegreen")
        marker = dict(size=6, color="rgb(67, 147, 195)")
        # marker = dict(size=8, color="rgb(47, 6, 150)")
        # marker = dict(size=8, color="rgb(214, 204, 35)")
        # marker = dict(size=8, color="rgb(97, 49, 150)")
    )
    data.append(scatter_vertices)

    # scatter_vertices = dict(
    #     mode = "markers",
    #     name = 'unstable_nodes',
    #     type = "scatter3d",
    #     x = unstable_array[:,0], y = unstable_array[:,1], z = unstable_array[:,2],
    #     marker = dict(size=8, color="rgb(169, 169, 169)")
    # )
    # data.append(scatter_vertices)

    # plot edges of facets
    for facet in facet_cord_list:
        # plot facets on the top
        convex_lines = plotly_lines(facet, dash='solid', width=4)
        data.append(convex_lines)
        # change z to zero, project facets to bottom
        facet_copy = facet.copy()
        facet_copy[:,2] = 0
        # plot facets projections
        convex_lines = plotly_lines(facet_copy, dash='solid', width=4)
        data.append(convex_lines)

    # plot surfaces for potential-energy envolope
    for facet_cord in facet_cord_list:
        # facet = plotly_facet(facet_cord, color='royalblue')
        # facet = plotly_facet(facet_cord, color='rgb(158,185,243)')
        # facet = plotly_facet(facet_cord, color='rgb(180, 80, 80)')
        # facet = plotly_facet(facet_cord, color='rgb(226, 104, 95)')
        # facet = plotly_facet(facet_cord, color='rgb(194, 48, 30)')
        # facet = plotly_facet(facet_cord, color='tomato')
        # facet = plotly_facet(facet_cord, color='orangered')
        facet = plotly_facet(facet_cord, color='rgb(146,197,222)')
        # facet = plotly_facet(facet_cord, color='rgb(106, 118, 252)')
        data.append(facet)

    # plot the convex hull
    # polyhedron = plotly_polyhedron(nodes_stable)
    # envolope = plotly_surface(nodes_stable)
    # data.append(envolope)

    # plot edges for convex hull
    # for facet in simplices_cord:
    #     convex_lines = plotly_lines(facet, dash='dash', width=2)
    #     data.append(convex_lines)

    layout = dict(
        title_x = 0.5,
        scene = dict(xaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    yaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    zaxis = dict(zeroline=False, showticklabels=False, showgrid=False, showline=False, title = {'text':''}, visible=False),
                    camera= dict(eye = dict(x=2.0, y=1.0, z=0.5)),
                    ),
        showlegend=False
    )

    fig = dict(data=data, layout=layout)
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
