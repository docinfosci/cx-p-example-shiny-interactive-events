import json
from io import StringIO

from shiny import App, ui, render, reactive

from canvasxpress.canvas import CanvasXpress

# Uncomment and set to a prior CX version to use the corresponding JS and CSS libraries.
# CanvasXpress.set_cdn_edition("49.8")

from canvasxpress.js.function import CXEvent
from canvasxpress.plot import graph, convert_to_reproducible_json

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
    The standard Shiny reactivity function.
    """
    @render.data_frame
    def house_statistic_matrix():
        """
        Called by Shiny to render the house_statistic_matrix data_frame UI element.
        """
        data = get_sample_dataframe()
        data = data.reset_index()
        return render.DataTable(
            data,
            selection_mode="row",
        )

    @render.text
    @reactive.event(input.point_selected)
    def selected_point_value():
        """
        Displays the selected chart point value.
        """
        return json.dumps(
            input.point_selected(),
            indent=4,
        )

    @render.text
    @reactive.event(house_statistic_matrix.cell_selection)
    def selected_row_value():
        """
        Displays the selected table row value.
        """
        selected_row_candidate = house_statistic_matrix.cell_selection()["rows"]
        if len(selected_row_candidate) == 1:
            selected_row = selected_row_candidate[0]
            return f"Index: {selected_row}\n{list(get_sample_dataframe().reset_index().iloc[selected_row])}"

    @reactive.effect
    def print_values_to_console():
        """
        Effects take place when any change event is registered.  This function prints available values to the console.
        """
        print(house_statistic_matrix.cell_selection()["rows"])
        print(input.point_selected())

    @render.ui
    @reactive.event(house_statistic_matrix.cell_selection)
    def chart_view():
        """
        On selection of a table row the chart is rendered and the point for the selected row is highlighted.
        A click event hook is also added that registeres, with Shiny, an event named "point_selected".
        Read the other function descriptions to see how this custom input event causes Shiny to react.

        ALAS, Shiny for Python's DataTable (etc.) do not yet support row pre-selection.  A custom components would
        need to be developed, which could be done -- probably by repacking a good JS option.
        """

        # Get a data object matching the matrix.
        xyz_data = get_sample_xyz()

        # Establish a standard chart config.
        configuration = {
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
        }

        # If a row is selected then identify the data coordinate (row x column) and add it to the config.
        selected_row_candidate = house_statistic_matrix.cell_selection()["rows"]
        if len(selected_row_candidate) > 0:
            selected_row = selected_row_candidate[0]
            configuration["selectedDataPoints"] = [
                [ xyz_data["y"]["vars"][selected_row], xyz_data["y"]["smps"][0] ],
            ]

        chart = CanvasXpress(
            render_to="example", # optional for a Shiny app
            data=xyz_data,
            config=configuration,
            events=[
                CXEvent(
                    id="click",
                    script= "Shiny.setInputValue('point_selected', o.y);"
                )
            ],
        )

        print(convert_to_reproducible_json(chart))

        # Render the graph.
        return graph(chart)

def get_ui():
    """
    Defines the UI to be presented by the Shiny application.
    """
    return ui.page_fluid(
        ui.row(
            ui.column(
                4,
                "The chart displays here when a row is selected.",
                ui.output_ui("chart_view")
            ),
            ui.column(
                4,
                "Select a row point to draw the chart with the value pre-selected.",
                ui.output_data_frame("house_statistic_matrix")
            ),
            ui.column(
                4,
                "Select a table row to see the values.",
                ui.output_text_verbatim("selected_row_value"),
                "Select a chart point to see the values.",
                ui.output_text_verbatim("selected_point_value")
            )
        ),
    )

app = App(get_ui(), server)
