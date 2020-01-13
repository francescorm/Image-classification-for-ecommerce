# import the necessary packages
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
import numpy as np
import random

from skimage.exposure import rescale_intensity



# construct the Sobel x-axis kernel
'''
custom = np.array((
	[2, -0.1, 0],
	[0, 3, -1],
	[0, -1, 0]), dtype="int")
'''
outline = np.array((
	[-1, -1, 1],
	[-1, 8, -1],
	[-1, -1, -1]), dtype="int")

# construct a sharpening filter
sharpen = np.array((
	[0, -1, 0],
	[-1, 5, -1],
	[0, -1, 0]), dtype="int")

    # construct the Laplacian kernel used to detect edge-like
# regions of an image
laplacian = np.array((
	[0, 1, 0],
	[1, -4, 1],
	[0, 1, 0]), dtype="int")
 
# construct the Sobel x-axis kernel
sobelX = np.array((
	[-1, 0, 1],
	[-2, 0, 2],
	[-1, 0, 1]), dtype="int")
 
# construct the Sobel y-axis kernel
sobelY = np.array((
	[-1, -2, -1],
	[0, 0, 0],
	[1, 2, 1]), dtype="int")



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





def convolveImage(immagineStop):
	# load the input image and convert it to grayscal
	image = cv2.imread(immagineStop)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	subdir = "/home/francesco/Scrivania/immaginiNewTest/Python/elaborazione/src/Esperimento2/"
	#randomName = str(random.randint(1,999))
	#filename2 = randomName+".png"
	filename = "{}.png".format(os.getpid())
	src = os.path.join(subdir,filename)
	convoleOutput = convolve(gray, outline)
	opencvOutput = cv2.filter2D(gray, -1, outline)
	cv2.imwrite(filename, opencvOutput)
	cv2.imwrite(src,opencvOutput)
	im = Image.open(filename) # the second one
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1')
	im.save(filename)
	return filename
    




def grepText(immagine):
	im = Image.open(immagine)
	im.convert('1', dither=Image.NONE)
	im = im.filter(ImageFilter.MedianFilter())
	#enhancer = ImageEnhance.Contrast(im)
	#im = enhancer.enhance(2)
	im = im.convert('1')
	text = pytesseract.image_to_string(im)
	return text



def grepMatricola(immagineStop):
	# construct the argument parse and parse the arguments
	'''
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
	args = vars(ap.parse_args())
	'''
	# load the example image and convert it to grayscale
	#image = cv2.imread(args["image"])
	image = cv2.imread(immagineStop)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 	# check to see if we should apply thresholding to preprocess the
	# image
	#if args["preprocess"] == "thresh":
	#	gray = cv2.threshold(gray, 0, 255,
	#		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 	# make a check to see if median blurring should be done to remove
	# noise
	#el
	#if args["preprocess"] == "blur":
	#gray = cv2.medianBlur(gray, 3)
 
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, opencvOutput)
    #cv2.waitKey(0)
	im = Image.open(filename)
	im.convert('1', dither=Image.NONE)
	text = pytesseract.image_to_string(im)
	os.remove(filename)
	#print(text)
	return text
	#print ("prova")
	# show the output images
	#cv2.imshow("Image", image)
	#cv2.imshow("Output", gray)
	#cv2.waitKey(0)


