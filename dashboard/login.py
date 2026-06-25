from dash import html
import dash_bootstrap_components as dbc


login_layout = dbc.Container([

    html.H1(

        "Customer Churn Prediction",

        className="text-center my-4"

    ),


    dbc.Card(

        dbc.CardBody([


            html.H3(

                "Login",

                className="text-center mb-4"

            ),


            dbc.Input(

                id="login_username",

                placeholder="Username",

                type="text",

                style={

                    "borderRadius": "12px"

                }

            ),

            html.Br(),


            dbc.Input(

                id="login_password",

                placeholder="Password",

                type="password",

                style={

                    "borderRadius": "12px"

                }

            ),

            html.Br(),


            dbc.Button(

                "Login",

                id="login_btn",

                color="primary",

                className="w-100"

            ),

            html.Br(),

            html.Br(),


            dbc.Button(

                "Register",

                id="goto_register",

                color="secondary",

                className="w-100"

            ),

            html.Br(),

            html.Br(),


            html.Div(

                id="login_message"

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