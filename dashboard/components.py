from dash import html, dcc
import dash_bootstrap_components as dbc


prediction_form = dbc.Card(

    dbc.CardBody([

        html.H4(

            "Predict Customer Churn",

            className="text-center mb-4"

        ),


        dbc.Row([

        dbc.Col([

        dbc.Label("Gender"),

        dcc.Dropdown(

        id="gender",

        options=[

        {"label":"Female","value":"Female"},

        {"label":"Male","value":"Male"}

        ],

        value="Female",
        
        clearable=False,
        
        searchable=False

        )

        ],md=6),


        dbc.Col([

        dbc.Label("Senior Citizen"),

        dcc.Dropdown(

        id="senior",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6)

        ]),


        html.Br(),



        dbc.Row([


        dbc.Col([

        dbc.Label("Partner"),

        dcc.Dropdown(

        id="partner",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6),



        dbc.Col([

        dbc.Label("Dependents"),

        dcc.Dropdown(

        id="dependents",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6)


        ]),


        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Tenure"),

        dbc.Input(

        id="tenure",

        type="number",

        value=12,
        

        )

        ],md=6),



        dbc.Col([


        dbc.Label("Phone Service"),

        dcc.Dropdown(

        id="phone",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=1,
        clearable=False,

        searchable=False

        )

        ],md=6)

        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([

        dbc.Label("Multiple Lines"),

        dcc.Dropdown(

        id="multiple",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6),



        dbc.Col([


        dbc.Label("Internet Service"),

        dcc.Dropdown(

        id="internet",

        options=[

        {"label":"DSL","value":0},

        {"label":"Fiber optic","value":1},

        {"label":"No","value":2}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6)


        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Online Security"),

        dcc.Dropdown(

        id="security",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6),




        dbc.Col([


        dbc.Label("Online Backup"),

        dcc.Dropdown(

        id="backup",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,
        searchable=False

        )

        ],md=6)

        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Device Protection"),

        dcc.Dropdown(

        id="device",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,
        searchable=False

        )

        ],md=6),



        dbc.Col([


        dbc.Label("Tech Support"),

        dcc.Dropdown(

        id="support",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,
        searchable=False

        )

        ],md=6)

        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Streaming TV"),

        dcc.Dropdown(

        id="tv",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,
        clearable=False,
        searchable=False

        )

        ],md=6),



        dbc.Col([


        dbc.Label("Streaming Movies"),

        dcc.Dropdown(

        id="movies",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=0,  
        clearable=False,

        searchable=False  

        )

        ],md=6)


        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Contract"),

        dcc.Dropdown(

        id="contract",

        options=[

        {"label":"Month-to-month","value":0},

        {"label":"One year","value":1},

        {"label":"Two year","value":2}

        ],

        value=0,
        clearable=False,

        searchable=False

        )

        ],md=6),




        dbc.Col([


        dbc.Label("Paperless Billing"),

        dcc.Dropdown(

        id="paper",

        options=[

        {"label":"No","value":0},

        {"label":"Yes","value":1}

        ],

        value=1,
        clearable=False,
        searchable=False

        )

        ],md=6)

        ]),



        html.Br(),




        dbc.Row([


        dbc.Col([


        dbc.Label("Payment Method"),

        dcc.Dropdown(

        id="payment",

        options=[

        {"label":"Bank Transfer","value":0},

        {"label":"Credit Card","value":1},

        {"label":"Electronic Check","value":2},

        {"label":"Mailed Check","value":3}

        ],

        value=2,
        clearable=False,
        searchable=False

        )

        ],md=6),




        dbc.Col([


        dbc.Label("Monthly Charges"),

        dbc.Input(

        id="monthly",

        type="number",

        value=70

        )

        ],md=6)

        ]),



        html.Br(),



        dbc.Button(

        "Predict",

        id="predict_btn",

        color="primary",

        className="w-50 mx-auto d-block"

        ),



        html.Br(),



        dbc.Card(

        dbc.CardBody(

        html.Div(

        id="prediction_result"

        )

        ),

        className="mt-4"

        )

            ])

        )