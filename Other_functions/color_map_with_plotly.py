import plotly
import plotly.graph_objects as go
import random
import itertools

colors = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond',
'blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue',
'cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgray','darkgrey','darkgreen',
'darkkhaki','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen',
'darkslateblue','darkslategray','darkslategrey','darkturquoise','darkviolet','deeppink','deepskyblue',
'dimgray','dimgrey','dodgerblue','firebrick','floralwhite','forestgreen','fuchsia','gainsboro','ghostwhite',
'gold','goldenrod','gray','grey','green','greenyellow','honeydew','hotpink','indianred','indigo','ivory',
'khaki','lavender','lavenderblush','lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan',
'lightgoldenrodyellow','lightgray','lightgrey','lightgreen','lightpink','lightsalmon','lightseagreen',
'lightskyblue','lightslategray','lightslategrey','lightsteelblue','lightyellow','lime','limegreen',
'linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen',
'mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred','midnightblue','mintcream',
'mistyrose','moccasin','navajowhite','navy','oldlace','olive','olivedrab','orange','orangered','orchid',
'palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum',
'powderblue','purple','red','rosybrown','royalblue','rebeccapurple','saddlebrown','salmon','sandybrown',
'seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','slategrey','snow','springgreen',
'steelblue','tan','teal','thistle','tomato','turquoise','violet','wheat','white','whitesmoke','yellow','yellowgreen']

a = 10
b= round(len(colors)/a)
random_n_list = list(itertools.product(range(0, a), range(0, b)))

data = []
for i, color in enumerate(colors):
    scatter_vertices = dict(
        mode = "markers",
        name = color,
        type = "scatter",
        x = [random_n_list[i][0]], y = [random_n_list[i][1]],
        marker = dict(size=20, color=color)
    )
    data.append(scatter_vertices)

layout = dict(plot_bgcolor= "black")
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='{fn}.html'.format(fn='colormap'))
