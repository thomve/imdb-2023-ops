import requests
import dash
from datetime import datetime
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("Input Form", className="card-title"),
                                    html.Div(
                                        [
                                            dcc.Checklist(id="isAdult", options=["IsAdult"], value=[], className="form-control mb-2"),
                                            dcc.Input(id="runtimeMinutes", value=90, type="number", placeholder="runtime minutes", className="form-control mb-2"),
                                            dcc.Input(id="averageRating", value=5, type="number", placeholder="Avg rating", className="form-control mb-2"),
                                            dcc.Input(id="numVotes", value=1000, type="number", placeholder="Num votes", className="form-control mb-2"),
                                            dcc.Input(id="budget", value=100000, type="number", placeholder="budget", className="form-control mb-2"),
                                            dcc.Slider(id="release_year", min=1980, max=datetime.now().year + 1, value=2000, step=1, className="form-control mb-2", marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                                            dcc.Slider(id="release_month", min=1, max=12, step=1, value=6, className="form-control mb-2", marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                                            dcc.Slider(id="release_day", min=1, max=31, step=1, value=15, className="form-control mb-2", marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                                            dcc.Checklist(id="Adventure", options=["Adventure"], value=[], className="form-control mb-2"),
                                            dcc.Checklist(id="Animation", options=["Animation"], value=[], className="form-control mb-2"),
                                            dcc.Checklist(id="Drama", options=["Drama"], value=[], className="form-control mb-2"),
                                            dcc.Checklist(id="Action", options=["Action"], value=[], className="form-control mb-2"),
                                            dcc.Checklist(id="Crime", options=["Crime"], value=[], className="form-control mb-2"),
                                            html.Button("Predict", id="submit-button", n_clicks=0, className="btn btn-primary"),
                                        ]
                                    ),
                                ]
                            ),
                            className="mb-4",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("Net profit", className="card-title"),
                                    html.Div(id="prediction-output"),
                                ]
                            ),
                            className="mb-4",
                        ),
                    ],
                    md=5,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("SHAP force Plot", className="card-title"),
                                    dcc.Graph(id="shap-force-plot"),
                                ]
                            ),
                            className="mb-4",
                        ),
                    ],
                    md=7,
                ),
            ]
        ),
    ],
    fluid=True,
)


def contains_only_value(lst, value):
    if len(lst) == 1 and lst[0] == value:
        return 1
    else:
        return 0


# Define callback to handle prediction
@app.callback(
    [Output("prediction-output", "children"), Output("shap-force-plot", "figure")],
    [Input("submit-button", "n_clicks")],
    [
        State("isAdult", "value"),
        State("runtimeMinutes", "value"),
        State("averageRating", "value"),
        State("numVotes", "value"),
        State("budget", "value"),
        State("release_year", "value"),
        State("release_month", "value"),
        State("release_day", "value"),
        State("Adventure", "value"),
        State("Animation", "value"),
        State("Drama", "value"),
        State("Action", "value"),
        State("Crime", "value")
    ],
)
def predict(n_clicks, 
            isAdult, 
            runtimeMinutes, 
            averageRating, 
            numVotes,
            budget,
            release_year,
            release_month,
            release_day,
            Adventure,
            Animation,
            Drama,
            Action,
            Crime):
    if n_clicks > 0:
        input_data = {
            "isAdult": contains_only_value(isAdult, "isAdult"),
            "runtimeMinutes": runtimeMinutes,
            "averageRating": averageRating,
            "numVotes": numVotes,
            "budget": budget,
            "release_year": release_year,
            "release_month": release_month,
            "release_day": release_day,
            "Adventure": contains_only_value(Adventure, "Adventure"),
            "Animation": contains_only_value(Animation, "Animation"),
            "Drama": contains_only_value(Drama, "Drama"),
            "Action": contains_only_value(Action, "Action"),
            "Crime": contains_only_value(Crime, "Crime")
        }
        # Make request to FastAPI predict endpoint
        predict_response = requests.post("http://localhost:8000/predict", json=input_data)

        if predict_response.status_code == 200:
            prediction = predict_response.json()["prediction"]

        fig = {}
        return prediction, fig
    
    else:
        return "", {}


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
