import numpy as np
import pandas as pd

element_list =    [x.strip() for x in ['h ', 'he',
                                       'li', 'be', 'b ', 'c ', 'n ', 'o ', 'f ', 'ne',
                                       'na', 'mg', 'al', 'si', 'p ', 's ', 'cl', 'ar',
                                       'k ', 'ca', 'sc', 'ti', 'v ', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr',
                                       'rb', 'sr', 'y ', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i ', 'xe',
                                       'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w ', 're', 'os', 'ir', 'pt', 'au',
                                       ]]
# Data from Angew. Chem. Int. Ed. Engl. 1996, 35, 150-163.
EN_list = np.array(                   [2.17, 0.00,
                                       0.91, 0.00, 1.88, 2.45, 2.93, 3.61, 4.14, 0.00,
                                       0.86, 1.21, 1.62, 2.12, 2.46, 2.64, 3.05, 0.00,
                                       0.73, 1.02, 1.40, 1.50, 1.60, 1.70, 1.60, 1.80, 1.90, 1.90, 1.40, 1.50, 1.77, 2.14, 2.25, 0.00, 0.00, 0.00,
                                       0.71, 0.96, 1.20, 1.30, 1.50, 2.20, 2.30, 2.30, 2.30, 2.20, 1.40, 1.40,  1.63, 2.12, 2.15, 0.00, 0.00, 0.00,
                                       0.80, 0.90, 1.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.30, 1.40, 2.30, 2.20, 2.20, 2.20, 2.30, 2.50,])
# Data from CRC Book 2014-2015.
EA_list = np.array(                   [17.39, 0.00,
                                       0.62, 0.00, 6.39,29.12, 0.01,33.69,78.38, 0.00,
                                       0.55, 0.00, 0.43,31.94, 17.2, 47.9,83.41, 0.00,
                                       0.00, 0.02, 4.34, 1.82,12.11,15.36, 0.00, 3.76,15.24,26.66,28.32, 0.00, 0.43, 1.23, 0.00, 0.00, 0.00, 0.00,
                                       0.49, 0.05, 7.08, 9.82,20.59,17.20,12.68,24.21,26.22,12.84,30.02, 0.00, 0.30, 1.11, 0.00, 0.00, 0.00, 0.00,
                                       0.47, 0.14, 0.47, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 7.43,18.79, 3.46,25.37,36.09,49.07,53.25,])

AW_M = {
    'Sc': 45.0, 'Ti': 47.9, 'V': 50.9, 'Cr':52.0, 'Mn': 54.9, 'Fe': 55.8, 'Co': 58.9, 'Ni': 58.7, 'Cu': 63.5, 'Zn': 65.4,
    'Y': 88.9, 'Zr': 91.2, 'Nb': 92.9, 'Mo': 96.0, 'Tc': 98.0, 'Ru': 101.1, 'Rh': 102.9, 'Pd': 106.4, 'Ag': 107.9, 'Cd': 112.4,
                'Hf':178.5, 'Ta': 180.9, 'W': 183.8, 'Re': 186.2, 'Os': 190.2, 'Ir': 192.2, 'Pt': 195.1, 'Au':197.0
}

dVE_M = {
    'Sc': 1, 'Ti': 2, 'V': 3, 'Cr':5, 'Mn': 5, 'Fe': 6, 'Co': 7, 'Ni': 8, 'Cu': 10, 'Zn': 10,
    'Y': 1, 'Zr': 2, 'Nb': 4, 'Mo': 5, 'Tc': 5, 'Ru': 7, 'Rh': 8, 'Pd': 10, 'Ag': 10, 'Cd': 10,
                'Hf': 2, 'Ta': 3, 'W': 4, 'Re': 5, 'Os': 6, 'Ir': 7, 'Pt': 9, 'Au':10
}
#                       H      B     C     N     O     F     Si    P     S    X
EN_lig_list = np.array([2.17, 1.88, 2.45, 2.93, 3.61, 4.14, 2.12, 2.46, 2.64, 3.05,])
EA_lig_list = np.array([17.39, 6.39, 29.12, 0.01, 33.69, 78.38, 31.94, 17.2, 47.9, 83.41])

def get_atomicNum(atom_list):
    atomicNum_list = []
    for atom in atom_list:
        atomicNum = element_list.index(atom) + 1
        atomicNum_list.append(atomicNum)
    return atomicNum_list

def get_EN(atomicNum_list):
    EN = []
    for atomicNum in atomicNum_list:
        element_EN = EN_list[atomicNum-1]
        EN.append(element_EN)
    return EN

def get_EA(atomicNum_list):
    EA = []
    for atomicNum in atomicNum_list:
        element_EA = EA_list[atomicNum-1]
        EA.append(element_EA)
    return EA

def get_metalNum_Group_Period(metalInput):
    metalAtomicNum = get_atomicNum([metalInput.lower()])[0]
    if metalAtomicNum <= 36:
       metalGroup = metalAtomicNum - 18
       metalPeriod = 4
    elif metalAtomicNum <= 54:
       metalGroup = metalAtomicNum - 36
       metalPeriod = 5
    elif metalAtomicNum >= 72:
        metalGroup = metalAtomicNum - 68
        metalPeriod = 6
    return metalAtomicNum, metalGroup, metalPeriod

def get_metalCR(metalInput):
    Ele = np.array(["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au"])
    CovalRadius = np.array([1.70, 1.60, 1.53, 1.39, 1.50, 1.42, 1.38, 1.24, 1.32, 1.22, 1.90, 1.75, 1.64, 1.54, 1.47, 1.46, 1.42, 1.39, 1.45, 1.44, 1.75, 1.70, 1.62, 1.51, 1.44, 1.41, 1.36, 1.36])
    idx = np.where(Ele == metalInput)
    CR = CovalRadius[idx[0][0]]
    return CR

def get_AW_M(metalInput):
    AW = AW_M[metalInput]
    return AW

def get_dVE_M(metalInput):
    dVE = dVE_M[metalInput]
    return dVE

def get_alldescriptors(metalInput, lig_list, ltrans, charge):
    """
    BDFE_XGB_25: 'PN-M','CR-M','GN-M','LTrans','CN','EA-M','X','Q','P','N','H','O','EA-Si','S','EA-S','EN-S','B','EN-C','EN-B','EA-B','F','EN-F','EA-F','EA-H','EN-H'
    MH_XGB_16: 'GN-M', 'PN-M', 'EN-M', 'dVE-M', 'LTrans', 'CN', 'P', 'Q', 'H', 'N', 'X', 'EA-Si', 'B', 'S', 'VE-C', 'F'
    VMH_XGB_19: 'EA-M','GN-M','VE-M','LTrans','EN-M','CN','dVE-M','P','Q','H','N','X','O','EA-Si','S','B','VE-C','F','AW-M'
    """
    AN_M, GN_M, PN_M = get_metalNum_Group_Period(metalInput)
    CR_M = get_metalCR(metalInput)
    AN_M = get_atomicNum([metalInput.lower()])
    EN_M = get_EN(AN_M)
    EA_M = get_EA(AN_M)
    AW_M = get_AW_M(metalInput)
    dVE_M = get_dVE_M(metalInput)

    #EN_ele = [5, 6, 7, 8, 9, 14, 15, 16, 17]
    #EN_lig = get_EN(EN_ele)
    #for m, n in zip(lig_list[1:], range(len(lig_list[1:]))):
    #    if m == 0:
    #        EN_lig[n] = 0
    #EA_ele = AN_M
    #EA_all = get_EA(EA_ele)
    VE_C = 4
    EA_Si, EA_S, EA_B, EA_F, EA_H = 31.94, 47.9, 6.39, 78.38, 17.39
    EN_S, EN_C, EN_B, EN_F, EN_H = 2.64, 2.45, 1.8, 4.14, 2.17
    H, B, N, O, F, P, S, X = lig_list[0], lig_list[1], lig_list[3], lig_list[4], lig_list[5], lig_list[7], lig_list[8], lig_list[9],

    num_ele = lig_list[0:4] + lig_list[-3:-1]
    CN = sum(lig_list)

    alldescriptors_BDFE = [[PN_M, CR_M, GN_M, ltrans, CN,] + EA_M + [X, int(charge), P, N, H, O, EA_Si, S, EA_S, EN_S, B, EN_C, EN_B, EA_B, F, EN_F, EA_F, EA_H, EN_H], [metalInput, CN,] + lig_list]
    alldescriptors_MH = [GN_M, PN_M,] + EN_M + [dVE_M, ltrans, CN, P, int(charge), H, N, X, EA_Si, B, S, VE_C, F]
    alldescriptors_VMH = EA_M + [GN_M, GN_M, ltrans,] + EN_M + [CN, dVE_M, P, int(charge), H, N, X, O, EA_Si, S, B, VE_C, F, AW_M]
    print(alldescriptors_BDFE)

    return [alldescriptors_BDFE, alldescriptors_MH, alldescriptors_VMH]







