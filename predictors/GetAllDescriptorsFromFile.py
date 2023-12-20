import subprocess
import os
import sys
import multiprocessing

work_dir = os.getcwd()
sh_dir = work_dir + '/predictors/shell-ML'

def get_descriptors_file(xyzPath, metal, metalGroup):
    MoveMHAtomFromXYZAllM(xyzPath, metal)
    processes = [
    multiprocessing.Process(target=GetID, args=(xyzPath,)),
    multiprocessing.Process(target=GetGroup, args=(xyzPath, metal)),
    multiprocessing.Process(target=GetMHDistFromXYZ34Lines, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllCoordinationNumber, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllAtomsElectroNegativity, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllAtomsElectronAffinity, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllNumberOfCoordinationAtoms, args=(xyzPath,)),
    multiprocessing.Process(target=GetLTrans, args=(xyzPath,)),
    ]

    [p.start() for p in processes]
    [p.join() for p in processes]

    GenExcelMHDist(xyzPath, metal, metalGroup)

def MoveMHAtomFromXYZAllM(xyzPath, metal):    
    # move metal to first line in xyz file
    subprocess.run([os.path.join(sh_dir, 'MoveMHAtomFromXYZAllM.sh'), xyzPath, metal])

def GetID(xyzPath):
    # Get ID from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetID.sh'), xyzPath])

'''
def GetMetal(xyzPath):
    # Get metals from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetMetal.sh'), xyzPath])

def GetBRHFreeEnergy(xyzPath):
    # Get free energy from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetBRHFreeEnergy.sh'), xyzPath])
'''

def GetGroup(xyzPath, metal):
    # Get Group from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetGroup.sh'), xyzPath, metal])

def GetMHDistFromXYZ34Lines(xyzPath):
    # Get M-H Distance from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetMHDistFromXYZ34Lines.sh'), xyzPath])

def GetAllCoordinationNumber(xyzPath):
    # Get Coordination Number from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetAllCoordinationNumber.sh'), xyzPath])

def GetAllAtomsElectroNegativity(xyzPath):
    # Get Atom ElectronNegativity from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetAllAtomsElectroNegativity.sh'), xyzPath])

def GetAllAtomsElectronAffinity(xyzPath):
    #Get Atom ElectronAffinity
    subprocess.run([os.path.join(sh_dir, 'GetAllAtomsElectronAffinity.sh'), xyzPath])

def GetAllNumberOfCoordinationAtoms(xyzPath):
    #Get Number of Coordination Atom from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetAllNumberOfCoordinationAtoms.sh'), xyzPath])

def GetLTrans(xyzPath):
    #Get H Trans Atom from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetLTrans.sh'), xyzPath])

'''
def GetGroupNum(xyzPath):
    #Get Group Number from xyz file
    subprocess.run([os.path.join(sh_dir, 'GetGroupNum.sh'), xyzPath])
'''

def GenExcelMHDist(xyzPath, metal, metalGroup):
    subprocess.run([os.path.join(sh_dir, 'GenExcelMHDist.sh'), xyzPath, metal, str(metalGroup)])

if __name__ == '__main__':
    xyzPath = sys.argv[1]
    metal = sys.argv[2]
    metalGroup = sys.argv[3]
    MoveMHAtomFromXYZAllM(xyzPath, metal)
    processes = [
    multiprocessing.Process(target=GetID, args=(xyzPath,)),
    multiprocessing.Process(target=GetGroup, args=(xyzPath, metal)),
    multiprocessing.Process(target=GetMHDistFromXYZ34Lines, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllCoordinationNumber, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllAtomsElectroNegativity, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllAtomsElectronAffinity, args=(xyzPath,)),
    multiprocessing.Process(target=GetAllNumberOfCoordinationAtoms, args=(xyzPath,)),
    multiprocessing.Process(target=GetLTrans, args=(xyzPath,)),
    ]

    [p.start() for p in processes]
    [p.join() for p in processes]

    GenExcelMHDist(xyzPath, metal, metalGroup)

