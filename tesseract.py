#!bin/python


import pytesseract
from PIL import Image


#Copiato trained data arial
#Su 
#/usr/share/tesseract-ocr/4.00/tessdata/Arial


def returnTextFromImage(imageName):
    im = Image.open(imageName)
    im.convert('1', dither=Image.NONE)
    text = pytesseract.image_to_string(im,lang='Arial')
    return text