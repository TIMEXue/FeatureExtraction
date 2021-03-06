import argparse
import glob 
import os
import re
import cv2 
import argparse
import numpy
import extraction


def loadsClasses(diretorio):
    for i in glob.glob( diretorio + '/*'):      
        if re.search('\\.jpg\\b', i, re.IGNORECASE) or re.search('\\.png\\b', i, re.IGNORECASE) or re.search('\\.jpeg\\b', i, re.IGNORECASE):
            imagePath = i
            arqOrder.write(i)
            arqOrder.write('\n')
            classe = imagePath.split("/")
            listClass.append(classe[len(classe)-2])
        loadsClasses(i + '/')

def header(atribute):
    atribute += 1
    arq.write('%\n%\n@RELATION ')
    arq.write(method)
    arq.write('\n')
    for i in range(1,atribute):
        arq.write('@ATTRIBUTE ')
        arq.write(str(i))
        arq.write(' REAL\n')
    arq.write('@ATTRIBUTE class {')
    cont = 1
    for c in nameClasses:
            arq.write(c)
            if (cont != len(nameClasses)):
                arq.write(',') 
            cont += 1    
    arq.write('}\n\n@DATA\n')

def finish():
    arq.write('%\n')
    arq.write('%\n')
    arq.write('%')
    arq.close()

def extract(diretorio):
    for i in glob.glob( diretorio + '/*'):     
        if re.search('\\.jpg\\b', i, re.IGNORECASE) or re.search('\\.png\\b', i, re.IGNORECASE) or re.search('\\.jpeg\\b', i, re.IGNORECASE):
            imagePath = i
            print('------------------> ', imagePath)
            classe = imagePath.split("/")
            features = []
            if(method == 'fomc'):
                features = extractor.extractionFeaturesColor(imagePath)
            else:
                features = extractor.extractionFeatures(imagePath)
            for k in range(len(features)):
                arq.write(str(features[k]))
                arq.write(', ')
            arq.write(classe[len(classe)-2])
            arq.write('\n')
        extract(i + '/')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
    help="path to input images dataset ")
ap.add_argument("-m", "--method", required=True,
    help="enter the desired method ")
ap.add_argument("-n", "--deepName", required=False,
    help="enter the name desired method to deep learning ")
args = vars(ap.parse_args())

directoryImagesIn = args["dataset"]
method = args["method"]
listClass = []
arqOrder = open('OrderOfImages.txt', 'w')
loadsClasses(directoryImagesIn)
nameClasses = set(listClass)
arqOrder.close()
deepName = args["deepName"] 
systemT = ''
if ( os.name == 'nt'): 
    systemT = 'windows'
else:
    systemT = 'Linux '

print('\n#################### ', method, ' ####################\n' )
if (method == 'lbp'):
    from extraction.lbp import LBP
    extractor = LBP()
    arq = open('lbp.arff', 'w')
    header(352)
    extract(directoryImagesIn)
    finish()
elif (method == 'fom'):
    from extraction.fom import FOM
    extractor = FOM()
    arq = open('fom.arff', 'w')
    header(8)
    extract(directoryImagesIn)
    finish()
elif (method == 'fomc'):
    from extraction.fom import FOM
    extractor = FOM()
    arq = open('fomc.arff', 'w')
    header(24)
    extract(directoryImagesIn)
    finish()
elif (method == 'surf'):
    from extraction.surf import Surf
    extractor = Surf()
    arq = open('surf.arff', 'w')
    header(70)
    extract(directoryImagesIn)
    finish()
elif (method == 'zernike'):
    from extraction.zernike import Zernike
    extractor = Zernike()
    arq = open('zernike.arff', 'w')
    header(72)
    extract(directoryImagesIn)
    finish()
elif (method == 'haralick'):
    from extraction.haralick import Haralick
    extractor = Haralick()
    arq = open('haralick.arff', 'w')
    header(13)
    extract(directoryImagesIn)
    finish()
elif (method == 'gch'):
    from extraction.gch import GCH
    extractor = GCH()
    arq = open('GCH.arff', 'w')
    header(30)
    extract(directoryImagesIn)
    finish()
elif (method == 'deep'):
    print('******************** ', deepName, '\n' )
    from extraction.deep import Deep
    method = method + '_'+ deepName
    extractor = Deep(deepName)
    arq = open('deep_'+deepName+'.arff', 'w')
    if (deepName == 'VGG16' or deepName == 'VGG19'):
        header(512) 
    elif (deepName == 'Xception' or deepName == 'ResNet50' or deepName == 'ResNet50V2'or deepName == 'ResNet101' or deepName == 'ResNet152' or deepName == 'ResNet101V2' or deepName == 'ResNet152V2' or deepName == 'InceptionV3'):
        header(2048)
    elif (deepName == 'InceptionResNetV2'):
        header(1536)
    elif (deepName == 'MobileNet' or deepName == 'DenseNet121'):
        header(1024)
    elif (deepName == 'MobileNetV2'):
        header(1280)
    elif (deepName == 'DenseNet169'):
        header(1664)
    elif (deepName == 'DenseNet201'):
        header(1920)
    elif (deepName == 'NASNetMobile'):
        header(1056)
    elif (deepName == 'NASNetLarge'):
        header(4032)
    else:
        print('\n########### Error - Inconsistent Information! (deepName) ###########\n')
    extract(directoryImagesIn)
    finish()
else:
    print('\n########### Error - Inconsistent Information! (method) ###########\n')