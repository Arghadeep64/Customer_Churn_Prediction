from dash import html
import dash_bootstrap_components as dbc


register_layout = dbc.Container([

    html.H1(

        "Customer Churn Prediction",

        className="text-center my-4"

    ),

    dbc.Card(

        dbc.CardBody([

            html.H3(

                "Register",

                className="text-center mb-4"

            ),

            dbc.Input(

                id="register_username",

                placeholder="Username",

                type="text",

                style={

                    "borderRadius": "12px"

                }

            ),

            html.Br(),

            dbc.Input(

                id="register_email",

                placeholder="Email",

                type="email",

                style={

                    "borderRadius": "12px"

                }

            ),

            html.Br(),

            dbc.Input(

                id="register_password",

                placeholder="Password",

                type="password",

                style={

                    "borderRadius": "12px"

                }

            ),

            html.Br(),

            dbc.Button(

                "Register",

                id="register_btn",

                color="success",

                className="w-100"

            ),

            html.Br(),

            html.Br(),

            dbc.Button(

                "Back To Login",

                id="goto_login",

                color="secondary",

                className="w-100"

            ),

            html.Br(),

            html.Br(),

            html.Div(

                id="register_message"

            )

        ]),

        style={

            "maxWidth": "450px",

            "margin": "auto",

            "marginTop": "50px",

            "padding": "20px",

            "borderRadius": "20px",

            "background": "rgba(255,255,255,0.85)",

            "backdropFilter": "blur(10px)",

            "boxShadow": "0 8px 32px rgba(0,0,0,0.15)"

        },

        className="fadein"

    )

], fluid=True)