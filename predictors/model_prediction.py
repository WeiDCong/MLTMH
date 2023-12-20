import pandas as pd
import numpy as np
import joblib

# 'CoordNum', 'EN-M', 'EN-B', 'EN-C', 'EN-N', 'EN-O', 'EN-F', 'EN-Si', 'EN-P', 'EN-S', 'EN-Cl', 'EA-M', 'H', 'B', 'C', 'N', 'P', 'S', 'Charge', 'LTrans', 'GrpNum'

def make_predictions(input, mode, charge, numOfMH):
    model_BDFE = joblib.load('./models/BDFE_XGB_25.pkl')
    model_MH = joblib.load('./models/MH_XGB_16.pkl')
    model_VMH = joblib.load('./models/VMH_XGB_19.pkl')
    findData = pd.read_csv("./predictors/data6153ForFind.csv")
    x_findSimilar = np.array(findData[['Metal', 'CoordNum', 'H', 'B', 'C', 'N', 'O', 'F', 'Si', 'P', 'S', 'Cl']]).reshape(-1,12)
    y_findSimilar = np.array(findData[['ID', 'BDE', 'M-H', 'VMH']]).reshape(-1, 4)

    if mode == 'params':
        x_inputPred_BDFE, x_inputPred_MH, x_inputPred_VMH = np.array(input[0][0]), np.array(input[1]), np.array(input[2])
        x_forFind = np.array(input[0][1])
        x_forFind = x_forFind.astype('O')
        x_forFind[1:] = x_forFind[1:].astype('i')
        #print(x_forFind)
    elif mode == 'file':
        df = pd.read_excel(input)
        if numOfMH != 0:
            df['H'] = numOfMH
        df['Charge'] = charge
        x_inputPred = np.array(df[['CoordNum', 'EN-M', 'EN-B', 'EN-C', 'EN-N', 'EN-O', 'EN-F', 'EN-Si', 'EN-P', 'EN-S', 'EN-Cl', 'EA-M', 'H', 'B', 'C', 'N', 'P', 'S', 'Charge', 'LTrans', 'GrpNum']])
        x_forFind = np.array(df[['Metal', 'CoordNum', 'H', 'B', 'C', 'N', 'O', 'F', 'Si', 'P', 'S', 'Cl']]).flatten()
        #print(x_forFind)
    
    x_forFind[2:] = np.where(x_forFind[2:]>0, 1, 0)
    x_forFind[0] = x_forFind[0].capitalize()
    x_BDFE, x_MH, x_VMH = x_inputPred_BDFE.reshape(-1, 25), x_inputPred_MH.reshape(-1, 16), x_inputPred_VMH.reshape(-1, 19),
    print(x_forFind)
    print(x_BDFE)
    y_pred_BDFE, y_pred_MH, y_pred_VMH = model_BDFE.predict(x_BDFE), model_MH.predict(x_MH), model_VMH.predict(x_VMH)
    y_pred_BDFE, y_pred_MH, y_pred_VMH = ('%.1f' % y_pred_BDFE), ('%.3f' % y_pred_MH), ('%.0f' % y_pred_VMH), 

    similarResultIdx = np.where((x_findSimilar == x_forFind).all(axis=1)) #To find the idx of element whose components all equal to the specified array
    #print(similarResultIdx)
    #similarResultDescrip = x_findSimilar[similarResultIdx]
    similarResult = y_findSimilar[similarResultIdx]
    allsimilarResults = get_similarResults(similarResult)
    print(similarResult)

    return [y_pred_BDFE, y_pred_MH, y_pred_VMH], allsimilarResults

def get_similarResults(similarResults):
    formulaID = np.loadtxt('./predictors/cifFormula.log', dtype=str, delimiter=":", usecols=[0])
    formulaSum = np.loadtxt('./predictors/cifFormula.log', dtype=str, delimiter=":", usecols=[1])
    Formula_list = np.array([])
    ID_list = similarResults[:,0]
    BDFE_list, MH_list, VMH_list = similarResults[:,1], similarResults[:,2], similarResults[:,3]
    for ID in ID_list:
        try:
            index = np.where(formulaID == ID)
            Sum = formulaSum[index]
            Formula_list = np.append(Formula_list, Sum)
        except Exception as e:
            pass 
    ID_list = [ x.split('.')[0] for x in ID_list]
    ID_list = np.array(ID_list).reshape(-1,1)
    Formula_list = Formula_list.reshape(-1,1)
    BDFE_list, MH_list, VMH_list = [ ('%.1f' % x) for x in BDFE_list], [ ('%.3f' % x) for x in MH_list], [ ('%.0f' % x) for x in VMH_list]
    BDFE_list, MH_list, VMH_list = np.array(BDFE_list).reshape(-1,1), np.array(MH_list).reshape(-1,1), np.array(VMH_list).reshape(-1,1)
    allsimilarResults = np.concatenate((ID_list, Formula_list, BDFE_list, MH_list, VMH_list), axis=1)
    
    return allsimilarResults
