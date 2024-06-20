""" This file helps visualising the graph using networkx and plotly
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure
from initializer import Graph

PREREQ_LINE_COLOUR = 'rgb(204, 255, 153)'
COREQ_LINE_COLOUR = 'rgb(255, 204, 102)'
EXCLUSION_LINE_COLOUR = 'rgb(210,210,210)'
OPTIONS_LINE_COLOUR = 'rgb(152, 177, 230)'
VERTEX_BORDER_COLOUR = 'rgb(20, 20, 20)'
COURSE_COLOUR = 'rgb(26, 255, 140)'
COPT_COLOUR = 'rgb(255, 153, 230)'


def visualize_graph(graph: Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 50000,
                    output_file: str = '') -> None:
    """
    Visualise Graph

        Green Markers: Courses
        Pink Markers: Course Collections such as CourseAnd/CourseOr

        Green Edge: Pre-Requisite
        Orange Edge: Co-Requisite
        Grey Edge: Exclusion

    """
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    c_opt_x_values = [pos[k][0] for k in graph_nx.nodes if graph_nx.nodes[k]['kind'] in ['CourseAnd', 'CourseOr']]
    c_opt_y_values = [pos[k][1] for k in graph_nx.nodes if graph_nx.nodes[k]['kind'] in ['CourseAnd', 'CourseOr']]

    c_x_values = [pos[k][0] for k in graph_nx.nodes if graph_nx.nodes[k]['kind'] == 'Course']
    c_y_values = [pos[k][1] for k in graph_nx.nodes if graph_nx.nodes[k]['kind'] == 'Course']

    labelsCourses = [node for node in graph_nx.nodes if graph_nx.nodes[node]['kind'] == 'Course']
    labelsOpt = [node for node in graph_nx.nodes if graph_nx.nodes[node]['kind'] != 'Course']

    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    coloursCourse = [COURSE_COLOUR for kind in kinds if kind == 'Course']
    coloursOpt = [COPT_COLOUR for kind in kinds if kind != 'Course']

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        if graph_nx.edges._adjdict[edge[0]][edge[1]]['kind'] == 'prereq':
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    line_width = 1.5

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=PREREQ_LINE_COLOUR, width=line_width),
                     hoverinfo='none',
                     )

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        if graph_nx.edges._adjdict[edge[0]][edge[1]]['kind'] == 'coreq':
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace4 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=COREQ_LINE_COLOUR, width=line_width),
                     hoverinfo='none',
                     )

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        if graph_nx.edges._adjdict[edge[0]][edge[1]]['kind'] == 'exclusion':
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace5 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=EXCLUSION_LINE_COLOUR, width=line_width),
                     hoverinfo='none',
                     )

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        if graph_nx.edges._adjdict[edge[0]][edge[1]]['kind'] == 'CourseOptions':
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace6 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=OPTIONS_LINE_COLOUR, width=line_width),
                     hoverinfo='none',
                     )

    trace7 = Scatter(x=c_x_values,
                     y=c_y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(
                         size=10,
                         color=coloursCourse,
                         line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                     ),
                     text=labelsCourses,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    trace8 = Scatter(x=c_opt_x_values,
                     y=c_opt_y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(
                         size=10,
                         color=coloursOpt,
                         line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                     ),
                     text=labelsOpt,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4, trace5, trace6, trace7, trace8]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)
