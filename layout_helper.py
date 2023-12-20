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
    """Run demo app (tests/dashbio_demos/*/app.py) as standalone app."""
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.scripts.config.serve_locally = True
    # Handle callback to component with id "fullband-switch"
    app.config['suppress_callback_exceptions'] = True

    ## Get all information from filename
    app_name = os.getenv('DASH_APP_NAME', '')
    if app_name == '':
        app_name = os.path.basename(os.path.dirname(filename))
    app_name = app_name.replace('dash-', '')

    app_title = 'TMH Predicton Tool'

    # Assign layout
    app.layout = app_page_layout(
        page_layout=layout(),
        app_title=app_title,
        app_name=app_name,
        standalone=True,
        **header_colors()
    )

    # Register all callbacks
    callbacks(app)

    # return app object
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
                            #html.A(
                            #    id='dashbio-logo', children=[
                            #        #html.Img(
                            #        #    src='data:image/png;base64,{}'.format(
                            #        #        base64.b64encode(
                            #        #            open(
                            #        #                './assets/molecule_icon2.png', 'rb'
                            #        #            ).read()
                            #        #        ).decode()
                            #        #    ),
                            #        #    height='auto', alt='',
                            #        #    style={'max-width': '8%', 'overflow': 'hidden'}
                            #        #)],
                            #    href="/Portal" if standalone else "/dash-bio"
                            #),
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
                        } #'justify-content': 'flex-start'
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
