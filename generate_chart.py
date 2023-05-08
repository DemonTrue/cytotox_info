import os
import cyt_chart as cyt
import shutil


def generate_charts(path_file, path_data, colormap):
    # colormap = 'linear' or 'percentile'
    formats = ['png', 'svg', 'pdf']
    path_formats = []
    filename = path_file.rsplit('\\', 1)[1].rsplit('.', 1)[0]

    reactions = cyt.read_data(path_data)

    cell_name = reactions[0][0]

    path_results = os.path.join('results', filename)

    for el in formats:
        path_formats.append(os.path.join(path_results, el))

    try:
        os.mkdir(path_results)
        for el in path_formats:
            try:
                os.mkdir(el)
            except OSError:
                pass
    except OSError:
        pass


    colors, cytotoxity_scale = cyt.choice_colormap(colormap, reactions)

    # plotting a color map
    cyt.cyt_colormap(cytotoxity_scale, colors, cell_name, colormap, path_formats, formats)

    # cycle through reactions from a file
    for count, reaction in enumerate(reactions):
        if count == 0: continue
        else:
            path_graph = []
            reaction_name = reaction[0][0]
            biofactor = cyt.calc_biofactor(reaction[2], reaction[3])  # biofactor calculation

            for el in path_formats:
                path_graph.append(os.path.join(el, reaction_name))
            # creating an array of colors for the substances in the considered reaction
            colors_data = cyt.fill_colors(reaction[4], colors, cytotoxity_scale)
            # plotting a diagram for a given reaction
            cyt.cyt_chart(path_graph, reaction_name, reaction[1], reaction[2], reaction[3], biofactor, colors_data, formats)

    path_png = os.path.join(path_results, 'png')
    path_static = os.path.join('static', 'figures', filename)

    if os.path.isdir(path_static):
        shutil.rmtree(path_static)

    shutil.copytree(path_png, path_static)

    return 0