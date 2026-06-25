from dash import html, dash_table
import dash_bootstrap_components as dbc


def history_table():

    return html.Div([

        dbc.Row([

            dbc.Col(

                dbc.Button(

                    "Delete Selected",

                    id="delete_selected",

                    color="danger",

                    className="w-100"

                ),

                width=3

            ),

            dbc.Col(

                dbc.Button(

                    "Delete All",

                    id="delete_all",

                    color="dark",

                    className="w-100"

                ),

                width=3

            )

        ],

        className="mb-3"

        ),


        dash_table.DataTable(

            id="history_table",

            data=[],

            columns=[],

            page_size=10,


            row_selectable="multi",

            selected_rows=[],


            style_table={

                "overflowX": "auto"

            },


            style_cell={

                "textAlign": "center",

                "padding": "10px"

            },


            style_header={

                "backgroundColor": "#0d6efd",

                "color": "white",

                "fontWeight": "bold"

            }

        )

    ])