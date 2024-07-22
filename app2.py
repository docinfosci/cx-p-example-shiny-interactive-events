import json
from io import StringIO

from shiny import App, ui, render, reactive

from canvasxpress.canvas import CanvasXpress

# Uncomment and set to a prior CX version to use the corresponding JS and CSS libraries.
# CanvasXpress.set_cdn_edition("49.8")

from canvasxpress.plot import graph

import pandas

def get_sample_dataframe():
    """
    Creates a Pandas DataFrame and returns it for use in the UI rendering.
    """
    data = pandas.read_csv(
        StringIO(
            """
    Alcohol	Tobacco
North	6.47	4.03
Yorkshire	6.13	3.76
Northeast	6.19	3.77
East Midlands	4.89	3.34
West Midlands	5.63	3.47
East Anglia	4.52	2.92
Southeast	5.89	3.2
Southwest	4.79	2.71
Wales	3.53	3.53
Scotland	6.08	4.51
Northern Ireland	4.02	4.56
            """.strip()
        ),
        sep="\t",
        index_col=0,
    )
    return data


def get_sample_xyz():
    """
    Creates an XYZ data object for CanvasXpress that aligns with the sample DataFrame.
    """
    matrix = get_sample_dataframe()
    data = {
        "y": {
            "smps": list(matrix.columns),
            "vars": list(matrix.index),
            "data": matrix.values.tolist(),
        }
    }
    return data


def server(input, output, session):
    """
    An empty server function.  There is no reactivity in this app.
    """
    pass

def get_ui():
    """
    Defines the UI to be presented by the Shiny application.
    """

    # Get a data object matching the matrix.
    xyz_data = get_sample_xyz()

    # Establish a standard chart config.
    chart = CanvasXpress(
        render_to="example",  # optional for a Shiny app
        data=xyz_data,
        config={
            "citation": "Moore, David S., and George P. McCabe (1989). Introduction to the Practice of Statistics, p. 179.",
            "dataTableTransposed": False,
            "graphType": "Scatter2D",
            "title": "Average weekly household spending, in British pounds, on tobacco products&nl;and alcoholic beverages for each of the 11 regions of Great Britain.",
            "xAxis": ["Alcohol"],
            "xAxisTitle": "Alcohol",
            "yAxis": ["Tobacco"],
            "yAxisTitle": "Tobacco",
            "theme": "Stata",
            "toolbarType": "fixed",
        },
    )

    return ui.page_fluid(
        # Graph the chart in place.  No reactivity needed.
        graph(chart),
    )

app = App(get_ui(), server)
