import base64
import os
import tempfile
from shutil import copy2
from textwrap import dedent as s

import numpy as np 
import pandas as pd
import dash
from dash import dcc, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html
from dash.dependencies import Input, Output, State
from dash_bio.utils import pdb_parser as parser, mol3dviewer_styles_creator as sparser

import dash_bio
import CheckInputs
from layout_helper import run_standalone_app
from predictors.GetAllDescriptorsFromParams import get_alldescriptors
from predictors.model_prediction import make_predictions
import CheckInputs as ChInp

DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def header_colors():
    return {
        'bg_color': '#e7625f',
        'font_color': 'white'
    }


def layout():
    return html.Div(
        id='bde-body',
        className='app-body',
        children=[
            html.Div(
                id='bde-mode-tabs',
                className='control-tabs',
                children=[
                    dcc.Tabs(id='bde-tabs', value='what-is', children=[
                        dcc.Tab(
                            label='About',
                            value='what-is',
                            children=html.Div(className='control-tab', children=[
                                html.Br(),
                                html.H4(className='what-is', children='What is MLTMH?', style={'margin-top': '2rem', 'font-size': '2.5rem'}),
                                html.Br(),
                                html.P('MLTMH is a machine learning tool for predicting bond length, bond '
                                       'dissociation free energy and vibration frequency of M-H bond for transition metal hydrides.',
                                       style={'font-size': '1.3rem'}),
                                html.Br(),
                                html.P('You can run the prediction via one of the following tabs:\n',
                                       style={'font-size': '1.1rem'}),
                                html.P('1. Params: specify parameters of your molecule\n',
                                       style={'font-size': '1.1rem'}),
                                html.P('2. File: a well-defined structure is ready to upload',
                                       style={'font-size': '1.1rem'}),
                            ],
                            style={'margin-top': '1rem', 'margin-left': '1rem', 'margin-right':'1rem'}
                            )
                        ),

                        dcc.Tab(
                            label='Params',
                            value='define-parameters',
                            children=html.Div(className='control-tab', children=[
                                html.Div(
                                    title='select metal',
                                    className="app-controls-block",
                                    id='metal',
                                    children=[
                                        dbc.Label('Metal'),
                                        dbc.Input(
                                            id='metal-input',
                                            type='text',
                                            placeholder='Enter element symbol, e.g. Fe',
                                            size='md',
                                            #valid=True,
                                            required=True, maxlength=2,
                                            #loading_state={'is_loading': False}
                                        ),
                                    ],
                                    style={'margin-top': '1rem'}
                                ),

                                html.Div(
                                    title='select ligand atoms',
                                    className="app-controls-block",
                                    id='lig-atoms',
                                    children=[
                                        dbc.Label('Ligands'),
                                        
                                        html.Div(
                                            dbc.FormText('Specify the number of atoms directly linking to the metal.', color='secondary'),
                                            #style={'margin-bottom': '1rem'}
                                        ),
                                        
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup([
                                                            dbc.Input(id='#H', placeholder="1", type='number', min=1, step=1, pattern='[0-9]'),
                                                            dbc.InputGroupText(" H", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.1rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#B', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" B", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#C', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" C", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#N', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" N", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#O', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" O", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),
                                                    ],
                                                    #style={'margin-left': '2rem'},
                                                ),

                                                dbc.Col(
                                                    [
                                                        dbc.InputGroup([
                                                            dbc.Input(id='#F', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" F", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#Si', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" Si", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#P', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" P", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#S', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" S", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),

                                                        dbc.InputGroup([
                                                            dbc.Input(id='#Cl', placeholder="0", type='number', min=0, step=1),
                                                            dbc.InputGroupText(" X", style={'text-align': 'center'}),
                                                            ], 
                                                            className="mb-3",
                                                            #style={'margin-bottom': '0.2rem'}
                                                        ),
                                                    ],
                                                    #style={'margin-right':'10rem'},
                                                ),
                                            ],
                                            className="g-3",
                                            #style={'margin-top': '0.1rem'}                       
                                        ),    
                                    ],
                                    style={'margin-top': '1rem'},
                                ),

                                html.Div(
                                    title='select LTrans',
                                    className="app-controls-block",
                                    id='LTrans_atom',
                                    children=[
                                        dbc.Label('Trans atom'),
                                        
                                        html.Div(
                                            dbc.FormText('Select the atom at the trans position of H.', color='secondary'),
                                        ),

                                        dcc.Dropdown(
                                            id='LTrans',
                                            options=[
                                                {'label': 'None', 'value': 0},
                                                {'label': 'H', 'value': 1},
                                                {'label': 'B', 'value': 5},
                                                {'label': 'C', 'value': 6},
                                                {'label': 'N', 'value': 7},
                                                {'label': 'O', 'value': 8},
                                                {'label': 'F', 'value': 9},
                                                {'label': 'Si', 'value': 14},
                                                {'label': 'P', 'value': 15},
                                                {'label': 'S', 'value': 16},
                                                {'label': 'Cl', 'value': 17},
                                            ],
                                            value=0,
                                            style={'margin-top': '0.1rem'}
                                        ),
                                    ],
                                    style={'margin-top': '1rem'},
                                ),  

                                html.Div(
                                    title='select charge',
                                    className="app-controls-block",
                                    id='set_charge',
                                    children=[
                                        dbc.Label('Charge'),
                                        html.Div(
                                            dbc.FormText('Specify the net charge of the molecule.', color='secondary'),
                                            #style={'margin-bottom': '1rem'}
                                        ),

                                        dcc.Dropdown(
                                            id='charge',
                                            options=[
                                                {'label': '0', 'value': 0},
                                                {'label': '1', 'value': 1},
                                                {'label': '2', 'value': 2},
                                                {'label': '-1', 'value': -1},
                                                {'label': '-2', 'value': -2},
                                            ],
                                            value='0',
                                            style={'margin-top': '0.2rem'}
                                        ),
                                    ],
                                    style={'margin-top': '1rem'},
                                ),

                                html.Div(
                                    title='submit bottom',
                                    className='d-grid gap-2 col-6 mx-auto',
                                    id='submit_bottom1',
                                    children=[
                                        dbc.Button('Submit', id='submit1', outline=True, color='primary', className="me-1"),
                                    ],
                                    style={'margin-top': '1rem', 'margin-bottom': '2rem'},
                                ),

                                html.Div(id='check-params-info')

                                ],
                                style={'margin-left': '1rem', 'margin-right':'1rem'},
                            ),
                        ),

                        dcc.Tab(
                            label='File',
                            value='upload-file',
                            children=html.Div(className='control-tab', children=[
                                dbc.Alert(
                                    "Coming soon...",
                                    # "Ensure that at least one M-H in your molecule, otherwise M-H must be assigned to the molecule."
                                    color="warning",
                                    style={'margin-top': '1rem', 'margin-left': '2rem', 'margin-right': '2rem'}
                                ),

                                #html.Hr(),
                                html.Div(
                                    [   dbc.Label('1. Upload an XYZ file'),
                                        dcc.Upload(
                                            [
                                            'Drag and Drop or ',
                                            html.A('Click to Select a File')
                                            ], 
                                            id='upload-file',
                                            style={
                                                'width': '100%',
                                                'height': '50px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center'
                                            },
                                            accept='.xyz',
                                            disabled=True,
                                            disable_click=True
                                        ),
                                        html.Div(id='upload-file-info'),
                                    ],
                                    style={'margin-bottom': '1rem', 'margin-left': '2rem', 'margin-right': '2rem'}
                                ),

                                html.Div(
                                    [
                                        dbc.Label('2. Specify a charge to the uploaded molecule'),
                                        dbc.Input(id='file-charge', placeholder="0", type='number', step=1, disabled=True),
                                    ],
                                    style={'margin-top': '3rem', 'margin-left': '2rem', 'margin-right': '2rem'}
                                ),

                                html.Div(
                                    title='submit bottom',
                                    className='d-grid gap-2 col-6 mx-auto',
                                    id='submit_bottom2',
                                    children=[
                                        dbc.Button('Submit', id='submit2', outline=True, color='primary', className="me-1", disabled=True),
                                    ],
                                    style={'margin-top': '1rem', 'margin-bottom': '2rem'},
                                ),   

                            ])
                        )
                    ],
                        colors={
                            "border": "white",
                            "primary": "#119DFF",
                            "background": '#F5F5F5',
                        }
                    )                          
                ],    
                style={'width': '30%', 'display': 'inline-box', 'margin-left': '3rem'}
            ),

            html.Div(
                id='display-results',
                className='control-tabs',
                children=[
                    html.Div(
                        id='predicted-BDFE',
                        children=[
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(
                                    html.Img(
                                        className='msg_desc',
                                        src='data:image/png;base64,{}'.format(
                                            base64.b64encode(
                                                open(
                                                    './assets/molecule_icon.png', 'rb'
                                                ).read()
                                            ).decode()
                                        ),
                                        width='auto', height='auto', alt='',
                                        style={'margin': '0 auto', 'max-width': '100%', 'overflow': 'hidden'}
                                    ),
                                    width=6),
                                dbc.Col(width=6),
                            ])
                        ]
                    ),
                ],
                style={'margin': '0 auto', 'width': '60%', 'display': 'inline-box', 'float': 'right'}
            ),

            # Store all the params
            html.Div(
                [
                    dcc.Store(
                        id='metal_info',
                    ),

                    dcc.Store(
                        id='lig_info',
                    ),

                    dcc.Store(
                        id='LTrans_info',
                    ),

                    dcc.Store(
                        id='charge_info',
                    ),

                    dcc.Store(
                        id='check_params_stat'
                    )
                ],
            ),   
        ],
        style={'display': 'flex'}
    )


def callbacks(_app):

    @_app.callback(
        Output('metal_info', 'data'),
        Input('metal-input', 'value'),
        prevent_initial_callbacks=True
    )
    def store_metal(metal):
        return metal
    
    @_app.callback(
        Output('lig_info', 'data'), 
        Input('#H', 'value'),
        Input('#B', 'value'),  
        Input('#C', 'value'),  
        Input('#N', 'value'),  
        Input('#O', 'value'),  
        Input('#F', 'value'),  
        Input('#Si', 'value'), 
        Input('#P', 'value'),   
        Input('#S', 'value'),
        Input('#Cl', 'value'),      
    )
    def store_ligands(H, B, C, N, O, F, Si, P, S, Cl):
        lig_list = []
        if H is None:
            lig_list.append(1)
        else:
            lig_list.append(H)
        for i in [B, C, N, O, F, Si, P, S, Cl]:
            if i is None:
                lig_list.append(0)
            else:
                lig_list.append(i)
        return lig_list 
    
    @_app.callback(
        Output('LTrans_info', 'data'),
        Input('LTrans', 'value'),
    )
    def store_ltrans(ltrans):
        if ltrans is None:
            ltrans = 0
        return ltrans
    
    @_app.callback(
        Output('charge_info', 'data'),
        Input('charge', 'value'),
    )
    def store_ltrans(charge):
        if charge is None:
            charge = 0
        return charge
        
    @_app.callback(
        [Output('check-params-info', 'children'),
        Output('check_params_stat', 'data'),],
        Input('metal_info', 'data'),
        Input('lig_info', 'data'),
        Input('LTrans_info', 'data'),
        Input('submit1', 'n_clicks'),
        prevent_initial_callbacks=True
    )
    def check_params(metal, ligands, ltrans, clicks):
        stat = 0
        child = None
        if metal is not None:
            chk_metal_stat = ChInp.check_metal(metal)
            chk_lig_stat = ChInp.check_ligand_number(ligands)
            chk_ltrans_stat = ChInp.check_LTrans(ligands, ltrans)
            child = [chk_metal_stat, chk_lig_stat, chk_ltrans_stat]
            None_num = [ x for x in child if x is None]
            if len(None_num) == 3:
                stat = 1
                print(f'all is ok, stat: {stat}, clicks: {clicks}')
            #return [child, stat]
        else:
            if clicks:
                child = html.Div(
                    dbc.Alert("Please complete all params!", color="warning"),
                    style={'font-size': '0.8rem', }
                )
                #return [child, stat]
        
        return [child, stat]
    
    @_app.callback(
        Output('predicted-BDFE', 'children'),
        State('metal_info', 'data'),
        State('lig_info', 'data'),
        State('LTrans_info', 'data'),
        State('charge_info', 'data'),
        Input('submit1', 'n_clicks'),
        #Input('check-params-info', 'children'),
        State('check_params_stat', 'data'),
        State('predicted-BDFE', 'children'),
        prevent_initial_callbacks=True
    )
    def show_prediction(metal, lig, ltrans, charge, n_clicks, chk_stat, img):
        print(f'predict, stat: {chk_stat}, clicks: {n_clicks}, metal:{metal}')
        if chk_stat == 1 and n_clicks:
            print('predicting')
            alldescriptors = get_alldescriptors(metal, lig, ltrans, charge)
            preditions, allsimilarResults = make_predictions(alldescriptors, 'params', charge, lig[0])
            BDFE_card = dbc.Card(
                            [
                                dbc.CardHeader('BDFE', style={'text-align': 'center', 'font-size': '1.5rem'}),
                                dbc.CardBody([
                                    dcc.Markdown(
                                        f'''# **{preditions[0]}**''',
                                        style={'text-align': 'center', 'font-size': '6rem'}
                                    )
                                ]),
                                dbc.CardFooter('kcal/mol', style={'text-align': 'center', 'font-size': '1.2rem'})
                            ],
                            #style={"width": "20rem"},
                        )
            MH_card = dbc.Card(
                            [
                                dbc.CardHeader('Bond length', style={'text-align': 'center', 'font-size': '1.5rem'}),
                                dbc.CardBody([
                                    dcc.Markdown(
                                        f'''# **{preditions[1]}**''',
                                        style={'text-align': 'center', 'font-size': '6rem'}
                                    )
                                ]),
                                dbc.CardFooter(u'\u00C5', style={'text-align': 'center', 'font-size': '1.2rem'})
                            ],
                            #style={"width": "20rem"},
                        )
            VMH_card = dbc.Card(
                            [
                                dbc.CardHeader('Vibration', style={'text-align': 'center', 'font-size': '1.5rem'}),
                                dbc.CardBody([
                                    dcc.Markdown(
                                        f'''# **{preditions[2]}**''',
                                        style={'text-align': 'center', 'font-size': '6rem'}
                                    )
                                ]),
                                dbc.CardFooter('cm-1', style={'text-align': 'center', 'font-size': '1.2rem'})
                            ],
                            #style={"width": "20rem"},
                        )
            child_1 = html.Div(
                [
                    dbc.Alert('✅ Prediction done!', color="success"),
                    dbc.Row(
                        [
                            dbc.Col(BDFE_card, width='auto', style={'margin': '0 auto', 'float': 'right'}),
                            dbc.Col(MH_card, width='auto', style={'margin': '0 auto', 'float': 'right'}),
                            dbc.Col(VMH_card, width='auto', style={'margin': '0 auto', 'float': 'right'}),
                        ]
                    ),

                    #dbc.Label('Predicted BDFE in kcal/mol', style={'text-align': 'center', 'font-size': '1.5rem', 'margin-top': '1rem',}),
                    #dcc.Markdown(
                    #    f'''# **{preditions}**''',
                    #    style={'text-align': 'center', 'font-size': '8rem', 'margin-top': '1rem',}
                    #),
                    html.Br(),
                    html.Hr(),
                ],
                style={'text-align': 'center'}
            )

            if len(allsimilarResults) != 0:
                child_2 = html.Div(
                    [
                        html.P(children=[
                                dcc.Markdown(
                                f'''For reference, listed below are molecules with the same __metal__, __coordination number__ and __ligand elements__.''',
                                style={'text-align': 'center'}
                                ),
                            ],
                            style={'text-align': 'center', 'background': 'mintcream', 'border': '0.6px solid', 'border-radius': '8px', 'margin-top': '1rem',}
                        ),

                        show_similar_results(allsimilarResults)
                    ]
                )
                
                return [child_1, child_2]
            else:
                return child_1
        else:
            return dash.no_update

    def show_similar_results(allsimilarResults):
        allsimilarResultsDf = pd.DataFrame(allsimilarResults)
        allsimilarResultsDf.columns = ['CCDC Refcode', 'Formula', 'BDFE', 'Bond length', 'Vibration']

        linked_allsimilarResultDf = add_links2ccdc(allsimilarResultsDf)
 
        child = dbc.Container([
                    dbc.Label('* Click the Refcode for more information.'),
                    dcc.Markdown(id='link-to-ccdc'),
                    dash_table.DataTable(
                        id='similar-result-table',
                        data=linked_allsimilarResultDf.to_dict('records'),
                        columns=[{'id': c, 'name': c, 'presentation': 'markdown',} for c in linked_allsimilarResultDf.columns],
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'text-align': 'left'
                            } for c in linked_allsimilarResultDf.columns
                        ],
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 242, 255)',
                            }
                        ],
                        style_data={
                            'text-align': 'center',
                        },
                        style_header={
                            #'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold',
                            'text-align': 'center',
                            'font-size': '1.2rem'
                        },
                        page_size=10,

                    )
                ])
        
        return child


    def add_links2ccdc(allsimilarResultsDf):

        def f(df):
            ccdcSearch_1 = 'https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid='
            ccdcSearch_2 = '&DatabaseToSearch=Published'
            return f"[{df['CCDC Refcode']}]({ccdcSearch_1}+{df['CCDC Refcode']}+{ccdcSearch_2})"
        
        allsimilarResultsDf['CCDC Refcode'] = allsimilarResultsDf.apply(f, axis=1)

        return allsimilarResultsDf

    @_app.callback(
        Output('upload-file-info', 'children'),
        Input('upload-file', 'filename'),
        prevent_initial_callbacks=True
    )
    def update_upload_state(filename):
        if filename is not None:
            children=[
                dbc.Alert(f'{filename} uploaded successfully!', color='light')
            ]
            return children
        

    


app = run_standalone_app(layout, callbacks, header_colors, __file__)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
                






                                



