import dash_core_components as dcc
import dash_html_components as html

html_layout = html.Div(
        [
            html.Div([
                html.Div([
                    html.A("JP Algo Trading Bot", className="navbar-brand"),
                    html.Div(id='live-update-nav')
                ], className="container-fluid", style={'justifyContent':'unset'})
            ], className="navbar navbar-expand-lg navbar-dark bg-dark"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(["Live Market Data"], className="card-header fw-bold "),
                        html.Div(id='live-update-market', className="card-text")
                    ], className="card text-center shadow m-4"),
                    html.Div([
                        html.Div(["Live Bot Terminal"], className="card-header text-center fw-bold "),
                        html.Div([
                            html.Div(id='live-update-terminal', className="card-text text-success")
                        ], className="card-body")
                    ], className="card text-white bg-dark shadow m-4")
                ], className="col"),
                html.Div([
                    html.Div([
                        html.Div(["Bot Status"], className="card-header text-center fw-bold"),
                        html.Div([
                            html.Div(id='live-update-status')
                        ], className="card-body")
                    ], className="card shadow m-4"),
                    html.Div([
                        html.Div(["Stocks Currently Analyzing"], className="card-header text-center fw-bold"),
                        html.Div(id='live-update-stocks', className="card-text")
                    ], className="card shadow m-4")
                ], className="col")
            ], className="row"),
            # dcc.Graph(id="live-graph", animate=True),
            dcc.Interval(
                id='interval-component',
                interval=1*5000, # in milliseconds
                n_intervals=0
            )
        ]
    )