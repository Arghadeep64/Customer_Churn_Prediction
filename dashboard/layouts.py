from dashboard.components import prediction_form
from dashboard.history import history_table

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib


df = pd.read_csv("dataset/customer_churn.csv")


model = joblib.load("models/churn_model.pkl")


importance_df = pd.DataFrame({

    "Feature":

    df.drop(

        ["customerID", "Churn"],

        axis=1

    ).columns,

    "Importance":

    model.feature_importances_

})


importance_df = importance_df.sort_values(

    by="Importance",

    ascending=True

)


importance_fig = px.bar(

    importance_df,

    x="Importance",

    y="Feature",

    orientation="h",

    title="Feature Importance"

)


importance_fig.update_layout(

   title_x=0.5,

    height=450

)


churn_fig = px.bar(

    df['Churn'].value_counts().reset_index(),

    x='Churn',

    y='count',

    title='Customer Churn Distribution'

)


contract_fig = px.histogram(

    df,

    x='Contract',

    title='Contract Distribution'

)


def analytics_placeholder(title, message):

    figure = go.Figure()

    figure.add_annotation(

        text=message,
        showarrow=False,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        font={"size": 16, "color": "#64748b"}

    )

    figure.update_layout(

        title={"text": title, "x": 0.5},
        template="plotly_white",
        margin={"l": 30, "r": 30, "t": 55, "b": 30},
        xaxis={"visible": False},
        yaxis={"visible": False}

    )

    return figure


churn_distribution_placeholder = analytics_placeholder(

    "Churn vs Non-Churn",
    "Loading prediction analytics..."

)


churn_trend_placeholder = analytics_placeholder(

    "Churn Trend Over Time",
    "Loading prediction analytics..."

)


confidence_distribution_placeholder = analytics_placeholder(

    "Confidence Distribution",
    "Loading prediction analytics..."

)


layout = dbc.Container([


   dbc.Row([

    dbc.Col(

        html.H1(

            "Customer Churn Prediction Dashboard",

            className="my-4"

        ),

        width=10

    ),

    dbc.Col(

        dbc.Button(

            "⚙ Settings",

            id="settings_btn",

            color="secondary",

            className="mt-2 w-100"

        ),

        width=2

    )
]),


    dbc.Row([


        dbc.Col(

            dbc.Card(

                dbc.CardBody([

                    html.H3("7043"),

                    html.P("Total Customers")

                ])

            )

        ),


        dbc.Col(

            dbc.Card(

                dbc.CardBody([

                    html.H3("1869"),

                    html.P("Churned Customers")

                ])

            )

        ),


        dbc.Col(

            dbc.Card(

                dbc.CardBody([

                    html.H3("73.46%"),

                    html.P("Retention Rate")

                ])

            )

        ),


        dbc.Col(

            dbc.Card(

                dbc.CardBody([

                    html.H3("80.70%"),

                    html.P("Model Accuracy")

                ])

            )

        )

    ]),


    html.Br(),


    dbc.Row([


        dbc.Col(

            dcc.Graph(

                figure=churn_fig

            )

        ),


        dbc.Col(

            dcc.Graph(

                figure=contract_fig

            )

        )

    ]),


    html.Br(),


    dcc.Graph(

        figure=importance_fig

    ),


    html.Br(),


    prediction_form,


    html.Br(),


    html.H3(

        "Prediction History",

        className="text-center"

    ),

    


    html.Br(),
    dbc.Modal(

    [

        dbc.ModalHeader(

            dbc.ModalTitle(

                "Settings"

            )

        ),

        dbc.ModalBody([


            dbc.Button(

                "Logout",

                id="logout_btn",

                color="danger",

                className="w-100"

            ),

            html.Br(),

            html.Br(),


            dbc.Button(

                "Delete Account",

                id="delete_btn",

                color="dark",

                className="w-100"

            )

        ])

    ],

    id="settings_modal",

    is_open=False

),

    history_table(),


    html.Br(),


    html.H3(

        "Prediction Analytics (Based on Prediction History)",

        className="text-center"

    ),


    dbc.Row([

        dbc.Col(

            dbc.Card(

                dbc.CardBody(

                    dcc.Graph(

                        id="prediction_churn_distribution_chart",

                        figure=churn_distribution_placeholder,

                        style={"height": "360px", "width": "100%"},

                        config={"responsive": True}

                    )

                )

            ),

            md=6

        ),


        dbc.Col(

            dbc.Card(

                dbc.CardBody(

                    dcc.Graph(

                        id="prediction_churn_trend_chart",

                        figure=churn_trend_placeholder,

                        style={"height": "360px", "width": "100%"},

                        config={"responsive": True}

                    )

                )

            ),

            md=6

        )

    ]),


    html.Br(),


    dbc.Row([

        dbc.Col(

            dbc.Card(

                dbc.CardBody(

                    dcc.Graph(

                        id="prediction_confidence_distribution_chart",

                        figure=confidence_distribution_placeholder,

                        style={"height": "360px", "width": "100%"},

                        config={"responsive": True}

                    )

                )

            )

        )

    ])


], fluid=True)
