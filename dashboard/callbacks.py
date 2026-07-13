from dash.exceptions import PreventUpdate
from dash import Input, Output, State, html, no_update
import pandas as pd
import plotly.graph_objects as go

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
    delete_all_predictions,
    get_prediction_analytics_history
)


current_user = None


CHURN_LABEL = "Customer Will Churn"
STAY_LABEL = "Customer Will Stay"


def empty_analytics_figure(title, message):

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


def build_prediction_analytics_figures(dataframe):

    if dataframe is None or dataframe.empty:

        return (

            empty_analytics_figure(
                "Churn vs Non-Churn",
                "No prediction data available yet."
            ),

            empty_analytics_figure(
                "Churn Trend Over Time",
                "No prediction trend data available yet."
            ),

            empty_analytics_figure(
                "Confidence Distribution",
                "No confidence data available yet."
            )

        )


    predictions = dataframe.get("prediction", pd.Series(dtype="object"))
    churn_count = (predictions == CHURN_LABEL).sum()
    stay_count = (predictions == STAY_LABEL).sum()

    if churn_count + stay_count:

        distribution_figure = go.Figure(

            data=[

                go.Pie(

                    labels=["Churn", "Stay"],
                    values=[churn_count, stay_count],
                    hole=0.55,
                    textinfo="label+value+percent",
                    marker={"colors": ["#ef4444", "#6366f1"]}

                )

            ]

        )

        distribution_figure.update_layout(

            title={"text": "Churn vs Non-Churn", "x": 0.5},
            template="plotly_white",
            margin={"l": 20, "r": 20, "t": 55, "b": 20},
            legend={"orientation": "h", "y": -0.1}

        )

    else:

        distribution_figure = empty_analytics_figure(
            "Churn vs Non-Churn",
            "No prediction data available yet."
        )


    trend_data = dataframe.loc[

        predictions.isin([CHURN_LABEL, STAY_LABEL]),

        ["prediction", "prediction_time"]

    ].copy()

    trend_data["prediction_time"] = pd.to_datetime(

        trend_data["prediction_time"],
        errors="coerce"

    )

    trend_data = trend_data.dropna(subset=["prediction_time"])

    if trend_data.empty:

        trend_figure = empty_analytics_figure(
            "Churn Trend Over Time",
            "No prediction trend data available yet."
        )

    else:

        trend_data["date"] = trend_data["prediction_time"].dt.date
        trend_counts = trend_data.groupby(

            ["date", "prediction"]

        ).size().unstack(fill_value=0).sort_index()

        trend_figure = go.Figure()

        for label, name, color in [
            (CHURN_LABEL, "Churn", "#ef4444"),
            (STAY_LABEL, "Stay", "#6366f1")
        ]:

            trend_figure.add_trace(

                go.Scatter(

                    x=trend_counts.index,
                    y=(
                        trend_counts[label]
                        if label in trend_counts
                        else [0] * len(trend_counts)
                    ),
                    mode="lines+markers",
                    name=name,
                    line={"color": color}

                )

            )

        trend_figure.update_layout(

            title={"text": "Churn Trend Over Time", "x": 0.5},
            template="plotly_white",
            margin={"l": 40, "r": 20, "t": 55, "b": 40},
            xaxis_title="Date",
            yaxis_title="Predictions",
            legend={"orientation": "h", "y": -0.2}

        )


    confidence_values = dataframe.get("confidence", pd.Series(dtype="object"))

    confidence = pd.to_numeric(

        confidence_values.astype(str).str.strip().str.rstrip("%"),
        errors="coerce"

    )

    confidence = confidence.where(confidence.isna() | (confidence > 1), confidence * 100)
    confidence_data = pd.DataFrame({
        "confidence": confidence,
        "prediction": predictions
    })
    confidence_data = confidence_data.loc[
        confidence_data["confidence"].between(50, 100)
        & confidence_data["prediction"].isin([CHURN_LABEL, STAY_LABEL])
    ]

    if confidence_data.empty:

        confidence_figure = empty_analytics_figure(
            "Confidence Distribution",
            "No confidence data available yet."
        )

    else:

        bins = [50, 60, 70, 80, 90, 101]
        labels = ["50–60%", "60–70%", "70–80%", "80–90%", "90–100%"]
        confidence_data["range"] = pd.cut(

            confidence_data["confidence"],
            bins=bins,
            labels=labels,
            right=False,
            include_lowest=True

        )

        confidence_figure = go.Figure()

        for label, name, color in [
            (STAY_LABEL, "Stay", "#6366f1"),
            (CHURN_LABEL, "Churn", "#ef4444")
        ]:

            counts = (
                confidence_data.loc[
                    confidence_data["prediction"] == label,
                    "range"
                ]
                .value_counts()
                .reindex(labels, fill_value=0)
            )

            confidence_figure.add_trace(

                go.Bar(

                    x=labels,
                    y=counts.tolist(),
                    name=name,
                    marker_color=color

                )

            )

        confidence_figure.update_layout(

            title={"text": "Confidence Distribution", "x": 0.5},
            template="plotly_white",
            margin={"l": 40, "r": 20, "t": 55, "b": 40},
            xaxis={
                "title": "Confidence range",
                "type": "category",
                "categoryorder": "array",
                "categoryarray": labels
            },
            yaxis={
                "title": "Predictions",
                "rangemode": "tozero",
                "tickmode": "linear",
                "tick0": 0,
                "dtick": 1
            },
            barmode="group",
            legend={"orientation": "h", "y": -0.2}

        )


    return distribution_figure, trend_figure, confidence_figure


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
            "prediction_churn_distribution_chart",
            "figure"
        ),
        Output(
            "prediction_churn_trend_chart",
            "figure"
        ),
        Output(
            "prediction_confidence_distribution_chart",
            "figure"
        ),
        Input(
            "prediction_result",
            "children"
        ),
        Input(
            "history_table",
            "data"
        ),
        Input(
            "url",
            "pathname"
        )
    )
    def update_prediction_analytics(
        prediction_result,
        history_data,
        pathname
    ):

        dataframe = get_prediction_analytics_history()

        return build_prediction_analytics_figures(dataframe)


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
