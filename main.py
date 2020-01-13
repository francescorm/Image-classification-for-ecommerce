#!bin/python

from convolution import convolveImage
from contorni import riconoscimentoContorni
from tesseract import returnTextFromImage   
import os
from foldermanager import createDir, copiaFoto
import cv2
import numpy as np

cartellaFoto ='todo/'

cartellaTemp='temp/'


folderClassified='done/'
#cartellaClassificateSenzaBollino='done/senzaBollino/'
#cartellaClassificateConBollino='done/conBollino/'

limitPixelOverExposed=2000
def istogram(immagine):
    img = cv2.imread(immagine) #reads image data
    color = ('b')
    histr = cv2.calcHist([img],[0],None,[256],[0,256])
    overexposed=histr[200:255]
    total = np.sum(overexposed)
    return total



def avviaRecuperoTesto(filename):
    convolvedImage= convolveImage(filename)
    immagineDaRiconoscere= riconoscimentoContorni(convolvedImage)
    print (immagineDaRiconoscere)
    matricola = returnTextFromImage(immagineDaRiconoscere)
    return matricola

def classifica():
    for subdir, dirs, files in os.walk(cartellaFoto):
        if files:
            files.sort()
            tempFolder=''
            for file in files:
                print (file)
                src = os.path.join(subdir,file)
                pixelOverexposed = istogram(src)
                print (pixelOverexposed)
                if (pixelOverexposed<=limitPixelOverExposed):
                    print ("immagine stop")
                    print ("cropping")
                    src = os.path.join(subdir,file)
                    matricola= avviaRecuperoTesto(src)
                    print (matricola)
                    tempFolder=matricola
                    createDir(matricola,folderClassified)
                else:
                    print ("")
                    copiaFoto(tempFolder,src,folderClassified)


def main():
    classifica()
   


if __name__ == "__main__":
    main()
