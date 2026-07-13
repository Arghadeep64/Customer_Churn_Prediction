from dash.exceptions import PreventUpdate
from dash import Input, Output, State, html, no_update

from dashboard.layouts import layout
from dashboard.login import login_layout
from dashboard.register import register_layout
from models.predict import predict_customer

from database.queries import (
    delete_user,
    save_prediction,
    get_prediction_history,
    register_user,
    check_login,
    delete_selected_predictions,
    delete_all_predictions
)


current_user = None


def register_callbacks(app):

    @app.callback(
        Output(
            "settings_modal",
            "is_open"
        ),
        Input(
            "settings_btn",
            "n_clicks"
        ),
        State(
            "settings_modal",
            "is_open"
        ),
        prevent_initial_call=True
    )
    def toggle_settings(
        n,
        opened
    ):
        return not opened


    @app.callback(
        Output(
            "page_content",
            "children"
        ),
        Input(
            "url",
            "pathname"
        )
    )
    def display_page(pathname):

        if pathname == "/register":

            return register_layout

        elif pathname == "/dashboard":

            return layout

        return login_layout


    @app.callback(
        Output(
            "prediction_result",
            "children"
        ),
        Input(
            "predict_btn",
            "n_clicks"
        ),
        State(
            "gender",
            "value"
        ),
        State(
            "senior",
            "value"
        ),
        State(
            "partner",
            "value"
        ),
        State(
            "dependents",
            "value"
        ),
        State(
            "tenure",
            "value"
        ),
        State(
            "phone",
            "value"
        ),
        State(
            "multiple",
            "value"
        ),
        State(
            "internet",
            "value"
        ),
        State(
            "security",
            "value"
        ),
        State(
            "backup",
            "value"
        ),
        State(
            "device",
            "value"
        ),
        State(
            "support",
            "value"
        ),
        State(
            "tv",
            "value"
        ),
        State(
            "movies",
            "value"
        ),
        State(
            "contract",
            "value"
        ),
        State(
            "paper",
            "value"
        ),
        State(
            "payment",
            "value"
        ),
        State(
            "monthly",
            "value"
        )
    )
    def make_prediction(
        n_clicks,
        gender,
        senior,
        partner,
        dependents,
        tenure,
        phone,
        multiple,
        internet,
        security,
        backup,
        device,
        support,
        tv,
        movies,
        contract,
        paper,
        payment,
        monthly
    ):

        if n_clicks is None:

            return ""

        try:

            result, confidence = predict_customer(
                gender,
                senior,
                partner,
                dependents,
                tenure,
                phone,
                multiple,
                internet,
                security,
                backup,
                device,
                support,
                tv,
                movies,
                contract,
                paper,
                payment,
                monthly
            )


            save_prediction(
                current_user[1],       # Username
                current_user[0],       # User ID
                gender,
                senior,
                partner,
                dependents,
                tenure,
                phone,
                multiple,
                internet,
                security,
                backup,
                device,
                support,
                tv,
                movies,
                contract,
                paper,
                payment,
                monthly,
                result,
                confidence
            )


            color = "green"

            if "Churn" in result:

                color = "red"


            return html.Div([

                html.H3(
                    result,
                    style={
                        "color": color,
                        "textAlign": "center"
                    }
                ),

                html.H5(
                    f"Confidence : {confidence:.2f}%",
                    style={
                        "textAlign": "center"
                    }
                )

            ])


        except Exception as e:

            print()

            print(
                "========== CALLBACK ERROR =========="
            )

            print(e)

            print(
                "===================================="
            )

            print()


            return html.H4(
                f"Error : {e}",
                style={
                    "color": "red"
                }
            )


    @app.callback(
        Output(
            "history_table",
            "data"
        ),
        Output(
            "history_table",
            "columns"
        ),
        Input(
            "predict_btn",
            "n_clicks"
        )
    )
    def update_history(n_clicks):

        df = get_prediction_history()


        return (

            df.to_dict(
                "records"
            ),

            [

                {
                    "name": col,
                    "id": col
                }

                for col in df.columns

            ]

        )


    @app.callback(
        Output(
            "url",
            "pathname",
            allow_duplicate=True
        ),
        Input(
            "goto_register",
            "n_clicks"
        ),
        prevent_initial_call=True
    )
    def goto_register(n):

        if n is None:

            raise PreventUpdate


        return "/register"


    @app.callback(
        Output(
            "url",
            "pathname",
            allow_duplicate=True
        ),
        Input(
            "goto_login",
            "n_clicks"
        ),
        prevent_initial_call=True
    )
    def goto_login(n):

        if n is None:

            raise PreventUpdate


        return "/"


    @app.callback(
        Output(
            "register_message",
            "children"
        ),
        Input(
            "register_btn",
            "n_clicks"
        ),
        State(
            "register_username",
            "value"
        ),
        State(
            "register_email",
            "value"
        ),
        State(
            "register_password",
            "value"
        ),
        prevent_initial_call=True
    )
    def register(
        n,
        username,
        email,
        password
    ):

        if not username or not email or not password:

            return html.H5(
                "Fill all fields",
                style={
                    "color": "red"
                }
            )


        success = register_user(
            username,
            email,
            password
        )


        if success:

            return html.H5(
                "Registration Successful",
                style={
                    "color": "green"
                }
            )


        return html.H5(
            "User already exists",
            style={
                "color": "red"
            }
        )


    @app.callback(
        Output(
            "url",
            "pathname",
            allow_duplicate=True
        ),
        Output(
            "login_message",
            "children"
        ),
        Input(
            "login_btn",
            "n_clicks"
        ),
        State(
            "login_username",
            "value"
        ),
        State(
            "login_password",
            "value"
        ),
        prevent_initial_call=True
    )
    def login(
        n,
        username,
        password
    ):

        if n is None:

            raise PreventUpdate


        if not username or not password:

            return (

                no_update,

                html.H5(
                    "Please enter both username and password.",
                    style={
                        "color": "red",
                        "textAlign": "center",
                        "marginTop": "10px"
                    }
                )

            )


        user = check_login(
            username,
            password
        )


        if user:

            global current_user

            current_user = user


            return (

                "/dashboard",

                html.H5(
                    "Login Successful",
                    style={
                        "color": "green",
                        "textAlign": "center",
                        "marginTop": "10px"
                    }
                )

            )


        return (

            no_update,

            html.H5(
                "Invalid username or password.",
                style={
                    "color": "red",
                    "textAlign": "center",
                    "marginTop": "10px"
                }
            )

        )

    @app.callback(
        Output(
            "url",
            "pathname",
            allow_duplicate=True
        ),
        Input(
            "logout_btn",
            "n_clicks"
        ),
        prevent_initial_call=True
    )
    def logout(n):

        global current_user


        if n is None:

            raise PreventUpdate


        current_user = None


        return "/"


    @app.callback(
        Output(
            "url",
            "pathname",
            allow_duplicate=True
        ),
        Input(
            "delete_btn",
            "n_clicks"
        ),
        prevent_initial_call=True
    )
    def delete_account(n):

        global current_user


        if n is None:

            raise PreventUpdate


        delete_user(
            current_user[0]
        )


        current_user = None


        return "/"


    @app.callback(
        Output(
            "history_table",
            "data",
            allow_duplicate=True
        ),
        Input(
            "delete_selected",
            "n_clicks"
        ),
        Input(
            "delete_all",
            "n_clicks"
        ),
        State(
            "history_table",
            "selected_rows"
        ),
        State(
            "history_table",
            "data"
        ),
        prevent_initial_call=True
    )
    def delete_history(
        a,
        b,
        selected,
        data
    ):

        if a and selected:

            ids = [

                data[i]["id"]

                for i in selected

            ]


            delete_selected_predictions(
                ids
            )


        elif b:

            delete_all_predictions()


        df = get_prediction_history()


        return df.to_dict(
            "records"
        )


print("Callbacks loaded")