#!bin/python


from PIL import Image
import argparse
import cv2
import os
from convolution import convolveImage



scontornate ='temp/scontornate/'
bordered ='temp/bordered/'


def riconoscimentoContorni(filenameImage):
    # construct the argument parse and parse the arguments
    # #rawImage = cv2.imread('1.jpg')
    #####
    #Convoluzione dell'immagine
    ####
    convolvedImage = convolveImage(filenameImage)
    image =  cv2.imread(convolvedImage)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #--- performing Otsu threshold ---
    ret,thresh1 = cv2.threshold(gray, 0,255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
    #cv2.imshow('thresh1', thresh1) 
    #cv2.waitKey(0)
    #--- choosing the right kernel
    # --- kernel size of 3 rows (to join dots above letters 'i' and 'j')
    # #--- and 10 columns to join neighboring letters in words and neighboring words
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (150, 3))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    #cv2.imshow('dilation', dilation)
    #cv2.waitKey(0)
    #---Finding contours ---
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = image.copy()
    #print (contours[0])
    #QUI BISOGNA PRENDERE l'array piu grande.
    #per il contorno identificato dalla matricola sono circa 2300 pixel per il rettangolo piu grande.
    #il piu piccolo scende a 300
    #print(len(contours[0]))
    arrayConParola=contours[0]
    for (subarray) in contours:
        if (len(subarray) > len(arrayConParola)):
            arrayConParola=subarray
    #print (len(arrayConParola))
    x, y, w, h = cv2.boundingRect(arrayConParola)
    cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.imshow('final', im2)
    #cv2.waitKey(0)
    crop_img = image[y:y+h, x:x+w]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    filename = "{}.png".format(os.getpid())
    immagineScontornata = os.path.join(scontornate,filename)
    cv2.imwrite(immagineScontornata, crop_img)
    #return immagineScontornata
    immagineBordered=addBordersToImage(immagineScontornata)
    return immagineBordered



def addBordersToImage(filename):
    temp = cv2.imread(filename)
    color = [255, 255, 255] # 'cause purple!    
    # border widths; I set them all to 150
    top, bottom, left, right = [100]*4
    borderType = cv2.BORDER_CONSTANT
    img_with_border = cv2.copyMakeBorder(temp, top, bottom, left, right, borderType, value=color)
    filenamebordi = "bordi.jpg".format(os.getpid())
    immagineScontornata = os.path.join(bordered,filenamebordi)
    cv2.imwrite(immagineScontornata, img_with_border)
    return immagineScontornata

