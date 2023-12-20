import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html

metals = np.array([x.strip() for x in ['sc', 'ti', 'v ', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 
                                       'y ', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 
                                             'hf', 'ta', 'w ', 're', 'os', 'ir', 'pt', 'au', 
                                       ]])

lig_ele_list = np.array([x.strip() for x in ['h ', 
                                             'b ', 'c ', 'n ', 'o ', 'f ',
                                             'si', 'p ', 's ', 'cl',
                                            ]])

lig_atomicNum_list = np.array([1, 
                               5, 6, 7, 8, 9,
                               14, 15, 16, 17,
                            ])

def check_metal(metal):
    print(f'metal: {len(metal)}')
    if metal.lower() in metals:
        return
    elif metal is None or len(metal) == 0:
        return
    else:
        return html.Div(
            dbc.Alert("Invalid metal symbol!", color="danger"),
            style={'font-size': '0.8rem', }
        )

def check_ligand_number(num):
    for i in num:
        if type(i) is float:
            return html.Div(
                dbc.Alert("Invalid number of ligand atom!", color="danger"),
                style={'font-size': '0.8rem', }
            )
        else:
            continue
    return
    
def check_LTrans(lig_list, ltrans):
    if ltrans == 0:
        return
    else:
        print(lig_list)
        idx = np.where(lig_atomicNum_list == ltrans)[0][0]
        if lig_list[idx] != 0:
            return
        else:
            return html.Div(
            dbc.Alert("Trans atom should be one of the ligand atoms specified above!", color="danger"),
            style={'font-size': '0.8rem', }
        )

