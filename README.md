## Synopsis

This script is used to speed up image classification operations for ecommerce. Starting from a folder containing raw images, it is possible to create folders renamed with the correct serial number and which contain all the photos taken referred to that serial. In this way you can automate all operations for post production because all images are correctly classified.


## Code Example

All images can be loaded in folder 'todo', the run a main.py and then you can find all your images correctly classified in 'done' folder.
Based on your images you should set threshold for recognizing "stop images" because the software works analyzing istogram of all images.

Once it finds which are "stop images", it runs some convolution to isolate serial from the images. Than it runs tesseract to grep text from image


## Installation

Please note that you should resize input images to max 300kb because convolution is really heavy. You can decide to create a script to resize before the run or you can use other software like lightroom or gimp or whatever you want.



## Tests

You can try software with test images inside 'todo' folder. 
Please, note the it's just a script ;) if you need changes just ask!


## License

Creative Commons

