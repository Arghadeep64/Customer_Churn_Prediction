from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from dashboard.callbacks import register_callbacks


app = Dash(

    __name__,

    external_stylesheets=[dbc.themes.MORPH],

    suppress_callback_exceptions=True

)


app.layout = html.Div([

    dcc.Location(

        id="url"

    ),

    dcc.Store(

        id="session",

        storage_type="session"

    ),

    html.Div(

        id="page_content"

    )

])


register_callbacks(app)

server = app.server

if __name__ == "__main__":

    app.run(debug=True)