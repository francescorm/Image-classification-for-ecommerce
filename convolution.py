#!bin/python

from PIL import Image, ImageEnhance, ImageFilter
import cv2
import os
import numpy as np

from skimage.exposure import rescale_intensity



tempDir='temp/convolved/'
tempDirConvolved='temp/convolved/temp'

#Kernel OUTLINE
outline = np.array((
	[-1, -1, 1],
	[-1, 8, -1],
	[-1, -1, -1]), dtype="int")


#FUNZIONE CHE ESEGUE MATERIALMENTE LA CONVOLUZIONE 

def convolve(image, kernel):
	# grab the spatial dimensions of the image, along with
	# the spatial dimensions of the kernel
	(iH, iW) = image.shape[:2]
	(kH, kW) = kernel.shape[:2]
 
	# allocate memory for the output image, taking care to
	# "pad" the borders of the input image so the spatial
	# size (i.e., width and height) are not reduced
	pad = (kW - 1) // 2
	image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
		cv2.BORDER_REPLICATE)
	output = np.zeros((iH, iW), dtype="float32")
    # loop over the input image, "sliding" the kernel across
	# each (x, y)-coordinate from left-to-right and top to
	# bottom
	for y in np.arange(pad, iH + pad):
		for x in np.arange(pad, iW + pad):
			# extract the ROI of the image by extracting the
			# *center* region of the current (x, y)-coordinates
			# dimensions
			roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
 
			# perform the actual convolution by taking the
			# element-wise multiplicate between the ROI and
			# the kernel, then summing the matrix
			k = (roi * kernel).sum()
 
			# store the convolved value in the output (x,y)-
			# coordinate of the output image
			output[y - pad, x - pad] = k
            
            	# rescale the output image to be in the range [0, 255]
	output = rescale_intensity(output, in_range=(0, 255))
	output = (output * 255).astype("uint8")
 
	# return the output image
	return output



#FUNZIONE CHE A PARTIRE DALLE IMMAGINI CREA LE LORO CONVOLUZIONI
#E LE METTE NELLA CARTELLA TEMP E RESTITUISCE IL SUO PERCORSO

def convolveImage(immagineStop):
	# load the input image and convert it to grayscal
    image = cv2.imread(immagineStop)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    subdir = tempDir
    filename = "{}.png".format(os.getpid())
    src = os.path.join(subdir,filename)
    convoleOutput = convolve(gray, outline)
    opencvOutput = cv2.filter2D(gray, -1, outline)
    #cv2.imwrite(filename, opencvOutput)
    cv2.imwrite(src,opencvOutput)
    im = Image.open(src) # the second one
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    convolvedImageFile = os.path.join(tempDir,filename)
    im.save(convolvedImageFile)
    return convolvedImageFile