import base64
import os

from dash import Dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def run_standalone_app(
        layout,
        callbacks,
        header_colors,
        filename
):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.scripts.config.serve_locally = True
    app.config['suppress_callback_exceptions'] = True

    app_name = os.getenv('DASH_APP_NAME', '')
    if app_name == '':
        app_name = os.path.basename(os.path.dirname(filename))
    app_name = app_name.replace('dash-', '')

    app_title = 'TMH Predicton Tool'

    app.layout = app_page_layout(
        page_layout=layout(),
        app_title=app_title,
        app_name=app_name,
        standalone=True,
        **header_colors()
    )

    callbacks(app)

    return app


def app_page_layout(page_layout,
                    app_title="TMH Predicton Tool",
                    app_name="",
                    light_logo=True,
                    standalone=False,
                    bg_color="#506784",
                    font_color="#F3F6FA"):
    return html.Div(
        id='main_page',
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                id='app-page-header',
                children=[
                    html.Div(
                        children=[
                            html.H3(
                                app_title,
                                style={'text-align': 'center', 'font-size': '2.0rem', 'margin-top': '0 auto', 'margin-bottom': '0 auto',}
                            ),
                        ],
                        style={
                            'margin-left':'1rem', 
                            'display': 'flex',
                            'align-items': 'center',
                            #'justify-content': 'flex-around'
                        } 
                    )
                ],
                style={
                    'background': bg_color,
                    'color': font_color,
                }
            ),

            html.Br(),
            #html.Br(),
            html.Div(
                id='app-page-content',
                children=page_layout
            )
        ],
    )
